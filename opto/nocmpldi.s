.globl main
main:
        lis     4,0x1fff
        ori     4,4,0x1fff
        sldi    4,4,7
        mtctr   4
        .p2align 7,,127
.Loop:
# 2 nops plus (3 compares): 0.614s with li/cmpld; 0.416s w/ cmpldi
# The one with 3 compares li/cmpld requires an extra i-fetch

        li      0,0
        cmpld   6,3,0
        li      0,0
        cmpld   6,3,0
        li      0,0
        cmpld   6,3,0

	nop
	nop     # .614s

        bdnz    .Loop
        nop
        blr
