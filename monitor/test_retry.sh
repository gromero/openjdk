#!/bin/bash
cd ~/hg/jdk11/jdk/JTwork/scratch/0 && \
for count in `seq 1 10`; do /home/gromero/hg/jdk11/jdk/./build/linux-ppc64le-normal-server-release/jdk/bin/java -cp /home/gromero/hg/jdk11/jdk/JTwork/classes/0/compiler/rtm/locking/TestRTMRetryCount.d:/home/gromero/hg/jdk11/jdk/test/hotspot/jtreg/compiler/rtm/locking:/home/gromero/hg/jdk11/jdk/JTwork/classes/0/test/lib:/home/gromero/hg/jdk11/jdk/test/lib:/home/gromero/hg/jdk11/jdk/JTwork/classes/0:/home/gromero/hg/jdk11/jdk/test/hotspot/jtreg:/home/gromero/jtreg/lib/javatest.jar:/home/gromero/jtreg/lib/jtreg.jar -Xcomp -server -XX:-TieredCompilation -XX:+UseRTMLocking -XX:+UnlockDiagnosticVMOptions -XX:+UnlockExperimentalVMOptions -Xbootclasspath/a:. -XX:+WhiteBoxAPI --add-exports java.base/jdk.internal.misc=ALL-UNNAMED -XX:CompileCommand=compileonly,compiler.testlibrary.rtm.BusyLock::test -XX:-UseRTMXendForLockBusy -XX:RTMTotalCountIncrRate=1 -XX:RTMRetryCount=${count} -XX:RTMTotalCountIncrRate=1 -XX:+PrintPreciseRTMLockingStatistics compiler.testlibrary.rtm.BusyLock true 5000; done | awk -F: '/# rtm lock aborts  :/ {print $2}'

#   3
#   5
#   7
#   9
#  11
#  13
#  15
#  17
#  19
#  21
