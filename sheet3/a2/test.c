#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Program %s takes one argument\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    char *fname, *wrconst, rdbuf[PATH_MAX];
    int fd;

    fname = argv[1];

    wrconst = "test";

    // Open file for writing:

    fd = open(fname, O_WRONLY);

    if (write(fd, wrconst, strlen(wrconst))) {
        printf("Successfully written to %s file\n", fname);
    }
    else {
        printf("Unable to write to %s file\n", fname);
    }

    close(fd);

    // Open file for reading:

    fd = open(fname, O_RDONLY);

    if (read(fd, rdbuf, strlen(wrconst))) {
        printf("Successfully read from %s file\n", fname);
    }
    else {
        printf("Unable to read from %s file\n", fname);
    }

    close(fd);

    return 0;
}