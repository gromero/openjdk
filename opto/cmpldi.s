.globl main
main:
        lis     0,0x1fff
        mtctr   0
        .p2align 7,,127
.Loop:
# 2 nops plus (3 compares): 0.614s with li/cmpld; 0.416s w/ cmpldi
# The one with 3 compares li/cmpld requires an extra i-fetch

        cmpldi  6,3,0
        cmpldi  6,3,0
        cmpldi  6,3,0

	nop
	nop     # .614s

        bdnz    .Loop
        nop
        blr
