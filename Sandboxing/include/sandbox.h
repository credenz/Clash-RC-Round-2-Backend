#include <fcntl.h>
#include <seccomp.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stddef.h>


void rules( )
{
    int rc = -1;
    scmp_filter_ctx ctx=seccomp_init(SCMP_ACT_KILL);
    if (ctx == NULL)
         goto out;

    rc = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(close), 0);
    if (rc < 0)
         goto out;

    rc = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    if (rc < 0)
         goto out;

    rc = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    if (rc < 0)
         goto out;

    rc = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 3,
                    SCMP_A0(SCMP_CMP_EQ, fd),
                    SCMP_A1(SCMP_CMP_EQ, (scmp_datum_t)buf);
    if (rc < 0)
         goto out;

    rc = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 1,
                    SCMP_CMP(0, SCMP_CMP_EQ, fd));
    if (rc < 0)
         goto out;

    rc = seccomp_rule_add_array(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 1,
                          arg_cmp);
    if (rc < 0)
         goto out;

    rc = seccomp_load(ctx);
    if (rc < 0)
         goto out;

    /* ... */

out:
    seccomp_release(ctx);
}