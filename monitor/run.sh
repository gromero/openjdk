#!/bin/bash -x

/home/gromero/openjdks/jdk11/bin/javac  -cp /home/gromero/hg/jdk11/jdk/build/linux-ppc64le-normal-server-release/support/test/lib/wb.jar m.java
/home/gromero/openjdks/jdk11/bin/java -Xbootclasspath/a:/home/gromero/hg/jdk11/jdk/build/linux-ppc64le-normal-server-release/support/test/lib/wb.jar -XX:+UnlockDiagnosticVMOptions -XX:+WhiteBoxAPI  m $1

