#!/bin/bash -x

sed -i 's/\.long 0x7c00051d/tbegin\./' $1
sed -i 's/\.long 0x7c00071d/tabort\. r0/' $1
sed -i 's/\.long 0x7c00055d/tend\./' $1
