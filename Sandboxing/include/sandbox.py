from seccomp import *
import sys


def install_filter():
    f = SyscallFilter(defaction=KILL)
    f.add_rule(ALLOW, "read")
    f.add_rule(ALLOW, "write")
    f.add_rule(ALLOW, "fstat")
    f.add_rule(ALLOW, 'ioctl')
    f.add_rule(ALLOW, 'sigaltstack')
    f.add_rule(ALLOW, "rt_sigaction")
    f.add_rule(ALLOW, "exit_group")
    f.add_rule(ALLOW, "read")
    f.add_rule(ALLOW, "stat")

    f.load()


install_filter()
