#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dlfcn.h>

// Definition of PATH_MAX:
#include <linux/limits.h>

#define PATH_TO_LIBC "/lib/x86_64-linux-gnu/libc.so.6"
#define PATH_TO_WHITELIST "whitelist.txt"

typedef ssize_t (*_read_t)(int, void *, size_t);
typedef ssize_t (*_write_t)(int, const void *, size_t);

void *libc_handle = NULL;

/**
 * @brief Get the absolute path of a file given its descriptor
 * 
 * @param fd File descriptor
 * @param buf Buffer to write the path to
 */
void get_filepath(int fd, char *buf) {
    char fdpath[PATH_MAX] = "";
    sprintf(fdpath, "/proc/self/fd/%i", fd);

    if (readlink(fdpath, buf, PATH_MAX) == -1) {
        fprintf(stderr, "Unable to open file descriptor %s\n", fdpath);
        exit(EXIT_FAILURE);
    }
}

/**
 * @brief Check if file is whitelisted
 * 
 * @param fd File descriptor
 * @return int 0 stands for false and 1 stands for true
 */
int whitelisted(int fd) {
    // Get absolute path of file being checked:
    char filepath[PATH_MAX];
    get_filepath(fd, filepath);

    // Each line from the whitelist is an absolute path to a file:
    char line[PATH_MAX];

    // Open whitelist:
    FILE *wl_file = fopen(PATH_TO_WHITELIST, "r");

    if (!wl_file) {
        fprintf(stderr, "Unable to open whitelist file %s\n", PATH_TO_WHITELIST);
        exit(EXIT_FAILURE);
    }

    // Read whitelist line by line, stripping the newline off and comparing it to the path being checked, exitting when
    // the whitelist is all read-out or when the paths being compared are equal:
    int status = -1;
    while (fgets(line, PATH_MAX, wl_file) && (status = strcmp(filepath, strtok(line, "\n"))));

    if (fclose(wl_file)) {
        fprintf(stderr, "Unable to close whitelist file %s\n", PATH_TO_WHITELIST);
        exit(EXIT_FAILURE);
    }

    if (status) {
        // Loop exitted because fgets reached EOF,
        // therefore the file was not found in the whitelist
        return 0;
    }
    else {
        // Loop exitted because strcmp returned that the strings are equal,
        // therefore the file was found in the whitelist
        return 1;
    }
}

/**
 * @brief Load original symbol dynamically
 * 
 * @param sym Symbol name
 * @return void* Pointer to original symbol
 */
void *load_sym(const char *sym) {
    if (!libc_handle) {
        // Open libc dinamically:
        libc_handle = dlopen(PATH_TO_LIBC, RTLD_LAZY);

        // If dlopen call failed:
        if (!libc_handle) {
            fprintf(stderr, "Unable to open dynamic library %s\n", PATH_TO_LIBC);
            exit(EXIT_FAILURE);
        }
    }

    // Get pointer to symbol from libc:
    void *orig_sym = dlsym(libc_handle, sym);

    if (!sym) {
        fprintf(stderr, "Unable to find symbol %s\n", sym);
        exit(EXIT_FAILURE);
    }

    return orig_sym;
}

ssize_t read(int fd, void *buf, size_t count) {
    if (whitelisted(fd)) {
        return ((_read_t) load_sym("read"))(fd, buf, count);
    }
    else {
        return (ssize_t) NULL;
    }
}

ssize_t write(int fd, const void *buf, size_t count) {
    if (whitelisted(fd)) {
        return ((_write_t) load_sym("write"))(fd, buf, count);
    }
    else {
        return (ssize_t) NULL;
    }
}