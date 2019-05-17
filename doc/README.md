== How to run selected Jtreg tests that depend on native libs:
```
make test JTREG="OPTIONS=-nativepath:/home/gromero/hg/jdk/jdk/build/linux-ppc64le-server-release/support/test/hotspot/jtreg/native/lib" TEST=./test/hotspot/jtreg/compiler/rtm
```

== That don't rely on native libs:
```
JT_JAVA=/usr/lib/jvm/java-1.8.0-openjdk-ppc64el  /home/gromero/jtreg/bin/jtreg -v1 -conc:1  -jdk:./buildd/linux-ppc64le-server-release/jdk/ ./test/hotspot/jtreg/compiler/rtm
```
