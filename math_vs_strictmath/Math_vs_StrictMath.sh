#!/bin/bash

if [ ! -z $1 ]
then
  JAVA_PATH=$1

if [ ! -f ${JAVA_PATH}/java ]
then
  echo "No Java runtime executable found! Exiting..."
  exit 1
fi

if [ ! -f ${JAVA_PATH}/javac ]
then
  echo "No Java compiler found! Exiting..."
  exit 1
fi

fi

####################
# One arg functions.
for FUNCTION in sin cos tan asin acos atan exp log log10 sqrt cbrt sinh cosh tanh expm1 log1p
do
  MClassname=Math_${FUNCTION}
  SMClassname=StrictMath_${FUNCTION}
  outputFile=`uname -m`.txt

 #echo Target: ${FUNCTION}
  sed "s|FUNC|${FUNCTION}|" Math_FUNC.java       > ${MClassname}.java
  sed "s|FUNC|${FUNCTION}|" StrictMath_FUNC.java > ${SMClassname}.java

  ${JAVA_PATH}/javac ${MClassname}.java
  ${JAVA_PATH}/javac ${SMClassname}.java

  MATH_REALTIME=$({ time ${JAVA_PATH}/java ${MClassname} ; } |& fgrep real | cut -f2)
  STRICT_MATH_REALTIME=$({ time ${JAVA_PATH}/java ${SMClassname} ; } |& fgrep real | cut -f2)
  STAT_OUTPUT="${FUNCTION} ${MATH_REALTIME} ${STRICT_MATH_REALTIME}"
  echo ${STAT_OUTPUT}

  # x86_64.txt or ppc64le.txt
  echo ${STAT_OUTPUT} >> ${outputFile}
done

#####################
# Two args functions.
for FUNCTION in IEEEremainder atan2 pow hypot
do
  MClassname=Math_${FUNCTION}
  SMClassname=StrictMath_${FUNCTION}
  outputFile=`uname -m`.txt

  sed "s|FUNC|${FUNCTION}|" Math_FUNC_2args.java       > ${MClassname}.java
  sed "s|FUNC|${FUNCTION}|" StrictMath_FUNC_2args.java > ${SMClassname}.java

  ${JAVA_PATH}/javac ${MClassname}.java
  ${JAVA_PATH}/javac ${SMClassname}.java

  MATH_REALTIME=$({ time ${JAVA_PATH}/java ${MClassname} ; } |& fgrep real | cut -f2)
  STRICT_MATH_REALTIME=$({ time ${JAVA_PATH}/java ${SMClassname} ; } |& fgrep real | cut -f2)
  STAT_OUTPUT="${FUNCTION} ${MATH_REALTIME} ${STRICT_MATH_REALTIME}"
  echo ${STAT_OUTPUT}

  # x86_64.txt or ppc64le.txt
  echo ${STAT_OUTPUT} >> ${outputFile}
done
