#!/bin/bash

# TODO:
#	repo, tag as arguments
#	build .tar.xz filename using variables


repo=jdk9
subrepos="corba hotspot jdk jaxws jaxp langtools nashorn"

if [ ! -z "$1" ]
then
  tag=$1
else
  tag=`hg id -t --cwd ${repo}`
fi

echo "Extracting archives from Mercurial repo (tag: ${tag})..."
hg archive -t tar ${repo}.tar --cwd ${repo}
echo "> ${repo}..."
for subrepo in ${subrepos}
do
  echo ">> ${subrepo}..."
  hg archive -t tar ${subrepo}.tar --cwd ${repo}/${subrepo}
done

mkdir tarball
pushd tarball

echo "Populating tree..."

cp ../${repo}/${repo}.tar .
tar xf ${repo}.tar
rm ${repo}.tar
# mv ${repo} jdk9
pushd jdk9

for subrepo in ${subrepos} 
do
# mkdir ${subrepo}
# pushd ${subrepo}
  cp ../../${repo}/${subrepo}/${subrepo}.tar .
  tar xf ${subrepo}.tar
  rm ${subrepo}.tar
# popd
done


if [ -e jdk ]
then # remove elliptic-curve ciphers, not supported on RHEL 7.2.
  echo "Removing ECC..."
  rm -vr jdk/src/jdk.crypto.ec/share/native/libsunec/impl
fi

popd

echo "Generating tarball..."
tar cJf "jdk9-${tag}.tar.xz" jdk9
mv "jdk9-${tag}.tar.xz" ../

popd

rm -fr tarball
