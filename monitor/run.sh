#!/bin/bash -x

# DO BEFORE USE:
# make build-test-lib

#/home/gromero/openjdks/jdk11/bin/javac    -cp /home/gromero/hg/jdk/jdk/build/linux-x86_64-normal-server-release/support/test/lib/wb.jar --add-exports java.base/jdk.internal.misc=ALL-UNNAMED m.java
/home/gromero/openjdks/jdk11/bin/java -Xbootclasspath/a:/home/gromero/hg/jdk/jdk/build/linux-x86_64-normal-server-release/support/test/lib/wb.jar --add-exports java.base/jdk.internal.misc=ALL-UNNAMED -XX:+UnlockDiagnosticVMOptions -XX:+WhiteBoxAPI  m $1


## FOR RETRY COUNT ABORT
/home/gromero/openjdks/jdk11/bin/java -Xbootclasspath/a:/home/gromero/hg/jdk/jdk/build/linux-x86_64-normal-server-release/support/test/lib/wb.jar -XX:+UnlockExperimentalVMOptions -XX:+UnlockDiagnosticVMOptions -XX:+WhiteBoxAPI -XX:+UseRTMLocking -XX:+PrintPreciseRTMLockingStatistics -XX:-TieredCompilation -Xcomp -XX:-UseRTMXendForLockBusy -XX:RTMTotalCountIncrRate=1 -XX:RTMRetryCount=3 -XX:RTMTotalCountIncrRate=1 --add-exports java.base/jdk.internal.misc=ALL-UNNAMED -XX:CompileOnly=x.syncAndTest m 1

# gromero@moog:~/git/openjdk/monitor$ /home/gromero/openjdks/jdk9/bin/java -Xbootclasspath/a:/home/gromero/hg/jdk/jdk/build/linux-x86_64-normal-server-release/support/test/lib/wb.jar -XX:+UnlockExperimentalVMOptions -XX:+UnlockDiagnosticVMOptions -XX:+WhiteBoxAPI -XX:+UseRTMLocking -XX:+PrintPreciseRTMLockingStatistics -XX:-TieredCompilation -Xcomp -XX:CompileOnly=x.transactionalRegion -XX:+UseRTMXendForLockBusy m 1

# /home/gromero/openjdks/jdk9/bin/java -Xbootclasspath/a:/home/gromero/hg/jdk/jdk/build/linux-x86_64-normal-server-release/support/test/lib/wb.jar -XX:+UnlockExperimentalVMOptions -XX:+UnlockDiagnosticVMOptions -XX:+WhiteBoxAPI -XX:+UseRTMLocking -XX:+PrintPreciseRTMLockingStatistics -XX:-TieredCompilation -Xcomp -XX:CompileOnly=x.transactionalRegion -XX:+UseRTMXendForLockBusy m 1

# /home/gromero/openjdks/jdk11/bin/java -Xbootclasspath/a:/home/gromero/hg/jdk/jdk/build/linux-x86_64-normal-server-release/support/test/lib/wb.jar -XX:+UnlockExperimentalVMOptions -XX:+UnlockDiagnosticVMOptions -XX:+WhiteBoxAPI -XX:+UseRTMLocking -XX:+PrintPreciseRTMLockingStatistics -XX:-TieredCompilation -Xcomp -XX:CompileOnly=x.transactionalRegion -XX:-UseRTMXendForLockBusy  --add-exports java.base/jdk.internal.misc=ALL-UNNAMED -XX:CompileOnly=compileonly,jdk.internal.misc.Unsafe::pageSize m 1
