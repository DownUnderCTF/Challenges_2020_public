/*
 * Credits for this sandbox file goes to 0xddaa from HITCON
 */

#include <sys/user.h>
#include <stddef.h>
#include <errno.h>
#include <sys/syscall.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
#include <sys/prctl.h>
#include "bpf-helper.h"

void sandbox()
{
    struct bpf_labels lab = {
        .count = 0,
    };
    struct sock_filter filter[] = {
        LOAD_ARCHITECTURE,
        JNE32(AUDIT_ARCH_X86_64, KILL),
        LOAD_SYSCALL_NR,
        SYSCALL(__NR_rt_sigreturn, ALLOW),
        SYSCALL(__NR_exit_group, ALLOW),
        SYSCALL(__NR_exit, ALLOW),
        SYSCALL(__NR_open, ALLOW),
        SYSCALL(__NR_read, ALLOW),
        SYSCALL(__NR_write, ALLOW),
        SYSCALL(__NR_brk, ALLOW),
        SYSCALL(__NR_mmap, ALLOW),
        SYSCALL(__NR_mprotect, ALLOW),
        SYSCALL(__NR_close, ALLOW),
        KILL,
    };
    bpf_resolve_jumps(&lab, filter, sizeof(filter) / sizeof(*filter));

    struct sock_fprog prog = {
        .filter = filter,
        .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
    };
    prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
    prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
}

