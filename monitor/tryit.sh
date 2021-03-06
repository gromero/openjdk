ARCH=`uname -m`
SOURCE=m.java
PROGRAM=${SOURCE%.java}
JDK_SOURCE=/home/gromero/hg/jdk/jdk
DEBUGLEVEL=build/linux-ppc64le-server-release
BUILD=$JDK_SOURCE/$DEBUGLEVEL
JAVA_HOME=$BUILD/jdk

JAVA=$JAVA_HOME/bin/java
JAVAC=$JAVA_HOME/bin/javac

ppc64_abort_ratio() {
set -x

LD_LIBRARY_PATH=/home/gromero/hg/jdk/jdk/src/utils/hsdis/build/linux-ppc64le

# javac
$JAVAC \
   -cp $BUILD/support/test/lib/wb.jar \
   --add-exports java.base/jdk.internal.misc=ALL-UNNAMED \
   $SOURCE

# java
# LD_LIBRARY_PATH=/home/gromero/hg/jdk11/jdk/src/utils/hsdis/build/linux-ppc64le \
$JAVA \
   -Xbootclasspath/a:$BUILD/support/test/lib/wb.jar \
   -XX:+UnlockExperimentalVMOptions \
   -XX:+UnlockDiagnosticVMOptions \
   -XX:+WhiteBoxAPI \
   -XX:-TieredCompilation \
   -Xcomp \
   --add-exports \
   java.base/jdk.internal.misc=ALL-UNNAMED \
   $@ \
   $PROGRAM

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
   -XX:RTMLockingThreshold=100000 \
   -XX:RTMAbortThreshold=0 \
   --add-exports \
   java.base/jdk.internal.misc=ALL-UNNAMED \
   -XX:CompileOnly=x.transactionalRegion \
    m 1

# RTMAbortRatio + UseRTMDeopt -> deoptimize if abort ratio >= RTMAbortRatio.
# RTMAbortThreshold -> number of abort necessary to calculate  abort ratio. 0 means on every abort.
# RTMLockingThreshold -> if the abort ratio remains low after RTMLockingThreshold, deopt and recompile with RTM locks and wo/ abort ratio calculation.

set +x
}

if [[ "$ARCH" = "ppc64le" ]]
then
  echo "Running on PPC64 LE..."
  ppc64_abort_ratio $@
else
  echo "Running on x86_64..."
  x64_abort_ratio
fi
