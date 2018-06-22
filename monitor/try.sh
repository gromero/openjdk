ARCH=`uname -m`

ppc64_abort_ratio() {
set -x

# javac
/home/gromero/openjdks/jdk11/bin/javac \
   -cp /home/gromero/hg/jdk11/jdk/build/linux-ppc64le-normal-server-release/support/test/lib/wb.jar \
   --add-exports java.base/jdk.internal.misc=ALL-UNNAMED \
   m.java

# java
/home/gromero/openjdks/jdk11/bin/java \
   -Xbootclasspath/a:/home/gromero/hg/jdk11/jdk/build/linux-ppc64le-normal-server-release/support/test/lib/wb.jar \
   -XX:+UnlockExperimentalVMOptions \
   -XX:+UnlockDiagnosticVMOptions \
   -XX:+WhiteBoxAPI \
   -XX:+UseRTMLocking \
   -XX:+PrintPreciseRTMLockingStatistics \
   -XX:-TieredCompilation \
   -Xcomp \
   -XX:-UseRTMXendForLockBusy \
   -XX:RTMTotalCountIncrRate=1 \
   -XX:+UseRTMDeopt \
   -XX:RTMAbortRatio=10 \
   --add-exports \
   java.base/jdk.internal.misc=ALL-UNNAMED \
   -XX:CompileOnly=x.transactionalRegion \
   m 1

set +x
}

x64_abort_ratio() {
set -x

# javac
/home/gromero/openjdks/jdk11/bin/javac \
   -cp /home/gromero/hg/jdk/jdk/build/linux-x86_64-normal-server-release/support/test/lib/wb.jar \
   --add-exports java.base/jdk.internal.misc=ALL-UNNAMED \
   m.java

# java
/home/gromero/openjdks/jdk11/bin/java \
   -Xbootclasspath/a:/home/gromero/hg/jdk/jdk/build/linux-x86_64-normal-server-release/support/test/lib/wb.jar \
   -XX:+UnlockExperimentalVMOptions \
   -XX:+UnlockDiagnosticVMOptions \
   -XX:+WhiteBoxAPI \
   -XX:+UseRTMLocking \
   -XX:+PrintPreciseRTMLockingStatistics \
   -XX:-TieredCompilation \
   -Xcomp \
   -XX:-UseRTMXendForLockBusy \
   -XX:RTMTotalCountIncrRate=1 \
   -XX:+UseRTMDeopt \
   -XX:RTMAbortRatio=10 \
   --add-exports \
   java.base/jdk.internal.misc=ALL-UNNAMED \
   -XX:CompileOnly=x.transactionalRegion \
    m 1

set +x
}

if [[ "$ARCH" = "ppc64le" ]]
then
  echo "Running on PPC64 LE..."
  ppc64_abort_ratio
else
  echo "Running on x86_64..."
  x64_abort_ratio
fi
