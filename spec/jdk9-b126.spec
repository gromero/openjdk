# FIXME

# When this is added to Fedora-proper, it must be synced with
# java-1.8.0-openjdk. Otherwise, many 'newer' features in java-1.8.0-openjdk
# will be missing from this RPM.

# Copr on build on i686, x86_64, and ppc64le
# For other builds use:
# - arm-koji build --scratch f24 blah.src.rpm
# - ppc-koji build --scratch f24 blah.src.rpm
# - s390-koji build --scratch f24 blah.src.rpm


# note, parametrised macros are order-senisitve (unlike not-parametrized) even with normal macros
# also necessary when passing it as parameter other macros. If not macro, then it is considered as switch
%global debug_suffix_unquoted -debug
# quoted one for shell operations
%global debug_suffix "%{debug_suffix_unquoted}"
%global normal_suffix ""

#if you wont only debug build, but providing java, build only normal build, but  set normalbuild_parameter
%global debugbuild_parameter  slowdebug
%global normalbuild_parameter release
%global debug_warning This package have full debug on. Install only in need, and remove asap.
%global debug_on with full debug on
%global for_debug for packages with debug on

# by default we build normal build always.
%global include_normal_build 1
%if %{include_normal_build}
%global build_loop1 %{normal_suffix}
%else
%global build_loop1 %{nil}
%endif

# by default we build debug build during main build only on intel arches
%ifarch %{ix86} x86_64
%global include_debug_build 1
%else
%global include_debug_build 0
%endif

%if %{include_debug_build}
%global build_loop2 %{debug_suffix}
%else
%global build_loop2 %{nil}
%endif

# if you disable both builds, then build fails
%global build_loop  %{build_loop1} %{build_loop2}
# note, that order  normal_suffix debug_suffix, in case of both enabled,
# is expected in one single case at the end of build


%global aarch64         aarch64 arm64 armv8
# sometimes we need to distinguish big and little endian PPC64
%global ppc64le         ppc64le
%global ppc64be         ppc64 ppc64p7
%global multilib_arches %{power64} sparc64 x86_64
%global jit_arches      %{ix86} x86_64 sparcv9 sparc64 %{aarch64} %{power64}

# With diabled nss is NSS deactivated, so in NSS_LIBDIR can be wrong path
# the initialisation must be here. LAter the pkg-connfig have bugy behaviour
#looks liekopenjdk RPM specific bug
# Always set this so the nss.cfg file is not broken
%global NSS_LIBDIR %(pkg-config --variable=libdir nss)

# fix for https://bugzilla.redhat.com/show_bug.cgi?id=1111349
%global _privatelibs libmawt[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%ifarch x86_64
%global archinstall amd64
%endif
%ifarch ppc
%global archinstall ppc
%endif
%ifarch ppc64le
%global archinstall ppc64le
%endif
%ifarch ppc64be


%global archinstall ppc64
%endif
%ifarch %{ix86}
%global archinstall i386
%endif
%ifarch ia64
%global archinstall ia64
%endif
%ifarch s390
%global archinstall s390
%endif
%ifarch s390x
%global archinstall s390x
%endif
%ifarch %{arm}
%global archinstall arm
%endif
%ifarch %{aarch64}
%global archinstall aarch64
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%global archinstall sparc
%endif
# 64 bit sparc
%ifarch sparc64
%global archinstall sparcv9
%endif
%ifnarch %{jit_arches}
%global archinstall %{_arch}
%endif



%ifarch %{jit_arches}
%global with_systemtap 1
%else
%global with_systemtap 0
%endif

# Convert an absolute path to a relative path.  Each symbolic link is
# specified relative to the directory in which it is installed so that
# it will resolve properly within chrooted installations.
%global script 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'
%global abs2rel %{__perl} -e %{script}

# New Version-String scheme-style defines
%global majorver 9
%global securityver 0

# Standard JPackage naming and versioning defines.
%global origin          openjdk
#%%global updatever       0
%global minorver           0
%global buildver        126
# priority must be 7 digits in total
%global priority        000000%{minorver}
%global javaver         1.9.0
%global newjavaver      %{majorver}.%{minorver}.%{securityver}


# parametrized macros are order-sensitive
%global fullversion     %{name}-%{version}-%{release}
#images stub
%global jdkimage       jdk
# output dir stub
%global buildoutputdir() %{expand:jdk9/build%1}
#we can copy the javadoc to not arched dir, or made it not noarch
%global uniquejavadocdir()    %{expand:%{fullversion}%1}
#main id and dir of this jdk
%global uniquesuffix()        %{expand:%{fullversion}.%{_arch}%1}

# Standard JPackage directories and symbolic links.
%global sdkdir()        %{expand:%{uniquesuffix %%1}}
%global jrelnk()        %{expand:jre-%{javaver}-%{origin}-%{version}-%{release}.%{_arch}%1}

%global sdkbindir()     %{expand:%{_jvmdir}/%{sdkdir %%1}/bin}
%global jrebindir()     %{expand:%{_jvmdir}/%{sdkdir %%1}/bin}
%global jvmjardir()     %{expand:%{_jvmjardir}/%{uniquesuffix %%1}}

%if %{with_systemtap}
# Where to install systemtap tapset (links)
# We would like these to be in a package specific subdir,
# but currently systemtap doesn't support that, so we have to
# use the root tapset dir for now. To distinquish between 64
# and 32 bit architectures we place the tapsets under the arch
# specific dir (note that systemtap will only pickup the tapset
# for the primary arch for now). Systemtap uses the machine name
# aka build_cpu as architecture specific directory name.
%global tapsetroot /usr/share/systemtap
%global tapsetdir %{tapsetroot}/tapset/%{_build_cpu}
%endif

# not-duplicated scriplets for normal/debug packages
%global update_desktop_icons /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%global post_script() %{expand:
update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
exit 0
}


%global post_headless() %{expand:
# FIXME: identical binaries are copied, not linked. This needs to be
# fixed upstream.
%ifarch %{jit_arches}
%ifnarch %{ppc64le}
#see https://bugzilla.redhat.com/show_bug.cgi?id=513605
%{jrebindir %%1}/java -Xshare:dump >/dev/null 2>/dev/null
%endif
%endif

ext=.gz
alternatives \\
  --install %{_bindir}/java java %{jrebindir %%1}/java %{priority} \\
  --slave %{_jvmdir}/jre jre %{_jvmdir}/%{sdkdir %%1} \\
  --slave %{_jvmjardir}/jre jre_exports %{_jvmjardir}/%{jrelnk %%1} \\
  --slave %{_bindir}/jjs jjs %{jrebindir %%1}/jjs \\
  --slave %{_bindir}/keytool keytool %{jrebindir %%1}/keytool \\
  --slave %{_bindir}/orbd orbd %{jrebindir %%1}/orbd \\
  --slave %{_bindir}/pack200 pack200 %{jrebindir %%1}/pack200 \\
  --slave %{_bindir}/rmid rmid %{jrebindir %%1}/rmid \\
  --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir %%1}/rmiregistry \\
  --slave %{_bindir}/servertool servertool %{jrebindir %%1}/servertool \\
  --slave %{_bindir}/tnameserv tnameserv %{jrebindir %%1}/tnameserv \\
  --slave %{_bindir}/unpack200 unpack200 %{jrebindir %%1}/unpack200 \\
  --slave %{_mandir}/man1/java.1$ext java.1$ext \\
  %{_mandir}/man1/java-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jjs.1$ext jjs.1$ext \\
  %{_mandir}/man1/jjs-%{uniquesuffix %%1}.1$ext \\
  --slave %{_bindir}/policytool policytool %{jrebindir %%1}/policytool \\
  --slave %{_mandir}/man1/keytool.1$ext keytool.1$ext \\
  %{_mandir}/man1/keytool-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/orbd.1$ext orbd.1$ext \\
  %{_mandir}/man1/orbd-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/pack200.1$ext pack200.1$ext \\
  %{_mandir}/man1/pack200-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/rmid.1$ext rmid.1$ext \\
  %{_mandir}/man1/rmid-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/rmiregistry.1$ext rmiregistry.1$ext \\
  %{_mandir}/man1/rmiregistry-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/servertool.1$ext servertool.1$ext \\
  %{_mandir}/man1/servertool-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/tnameserv.1$ext tnameserv.1$ext \\
  %{_mandir}/man1/tnameserv-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/unpack200.1$ext unpack200.1$ext \\
  %{_mandir}/man1/unpack200-%{uniquesuffix %%1}.1$ext
#TODO add alternatives for appletviewer, idlj, jrunscript and jstatd?

for X in %{origin} %{javaver} ; do
  alternatives \\
    --install %{_jvmdir}/jre-"$X" \\
    jre_"$X" %{_jvmdir}/%{sdkdir %%1} %{priority} \\
    --slave %{_jvmjardir}/jre-"$X" \\
    jre_"$X"_exports %{_jvmdir}/%{sdkdir %%1}
done

update-alternatives --install %{_jvmdir}/jre-%{javaver}-%{origin} jre_%{javaver}_%{origin} %{_jvmdir}/%{jrelnk %%1} %{priority} \\
--slave %{_jvmjardir}/jre-%{javaver}       jre_%{javaver}_%{origin}_exports      %{jvmjardir %%1}

update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
exit 0
}

%global postun_script() %{expand:
update-desktop-database %{_datadir}/applications &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{update_desktop_icons}
fi
exit 0
}


%global postun_headless() %{expand:
  alternatives --remove java %{jrebindir %%1}/java
  alternatives --remove jre_%{origin} %{_jvmdir}/%{sdkdir %%1}
  alternatives --remove jre_%{javaver} %{_jvmdir}/%{sdkdir %%1}
  alternatives --remove jre_%{javaver}_%{origin} %{_jvmdir}/%{jrelnk %%1}
}

%global posttrans_script() %{expand:
%{update_desktop_icons}
}

%global post_devel() %{expand:
ext=.gz
alternatives \\
  --install %{_bindir}/javac javac %{sdkbindir %%1}/javac %{priority} \\
  --slave %{_jvmdir}/java java_sdk %{_jvmdir}/%{sdkdir %%1} \\
  --slave %{_jvmjardir}/java java_sdk_exports %{_jvmjardir}/%{sdkdir %%1} \\
  --slave %{_bindir}/appletviewer appletviewer %{sdkbindir %%1}/appletviewer \\
  --slave %{_bindir}/idlj idlj %{sdkbindir %%1}/idlj \\
  --slave %{_bindir}/jar jar %{sdkbindir %%1}/jar \\
  --slave %{_bindir}/jarsigner jarsigner %{sdkbindir %%1}/jarsigner \\
  --slave %{_bindir}/javadoc javadoc %{sdkbindir %%1}/javadoc \\
  --slave %{_bindir}/javah javah %{sdkbindir %%1}/javah \\
  --slave %{_bindir}/javap javap %{sdkbindir %%1}/javap \\
  --slave %{_bindir}/jcmd jcmd %{sdkbindir %%1}/jcmd \\
  --slave %{_bindir}/jconsole jconsole %{sdkbindir %%1}/jconsole \\
  --slave %{_bindir}/jdb jdb %{sdkbindir %%1}/jdb \\
  --slave %{_bindir}/jdeps jdeps %{sdkbindir %%1}/jdeps \\
  --slave %{_bindir}/jimage jimage %{sdkbindir %%1}/jimage \\
  --slave %{_bindir}/jinfo jinfo %{sdkbindir %%1}/jinfo \\
  --slave %{_bindir}/jmap jmap %{sdkbindir %%1}/jmap \\
  --slave %{_bindir}/jps jps %{sdkbindir %%1}/jps \\
  --slave %{_bindir}/jrunscript jrunscript %{sdkbindir %%1}/jrunscript \\
  --slave %{_bindir}/jsadebugd jsadebugd %{sdkbindir %%1}/jsadebugd \\
  --slave %{_bindir}/jshell jshell %{sdkbindir %%1}/jshell \\
  --slave %{_bindir}/jstack jstack %{sdkbindir %%1}/jstack \\
  --slave %{_bindir}/jstat jstat %{sdkbindir %%1}/jstat \\
  --slave %{_bindir}/jstatd jstatd %{sdkbindir %%1}/jstatd \\
  --slave %{_bindir}/rmic rmic %{sdkbindir %%1}/rmic \\
  --slave %{_bindir}/schemagen schemagen %{sdkbindir %%1}/schemagen \\
  --slave %{_bindir}/serialver serialver %{sdkbindir %%1}/serialver \\
  --slave %{_bindir}/wsgen wsgen %{sdkbindir %%1}/wsgen \\
  --slave %{_bindir}/wsimport wsimport %{sdkbindir %%1}/wsimport \\
  --slave %{_bindir}/xjc xjc %{sdkbindir %%1}/xjc \\
  --slave %{_mandir}/man1/appletviewer.1$ext appletviewer.1$ext \\
  %{_mandir}/man1/appletviewer-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/idlj.1$ext idlj.1$ext \\
  %{_mandir}/man1/idlj-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jar.1$ext jar.1$ext \\
  %{_mandir}/man1/jar-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jarsigner.1$ext jarsigner.1$ext \\
  %{_mandir}/man1/jarsigner-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/javac.1$ext javac.1$ext \\
  %{_mandir}/man1/javac-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/javadoc.1$ext javadoc.1$ext \\
  %{_mandir}/man1/javadoc-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/javah.1$ext javah.1$ext \\
  %{_mandir}/man1/javah-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/javap.1$ext javap.1$ext \\
  %{_mandir}/man1/javap-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jcmd.1$ext jcmd.1$ext \\
  %{_mandir}/man1/jcmd-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jconsole.1$ext jconsole.1$ext \\
  %{_mandir}/man1/jconsole-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jdb.1$ext jdb.1$ext \\
  %{_mandir}/man1/jdb-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jdeps.1$ext jdeps.1$ext \\
  %{_mandir}/man1/jdeps-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jimage.1$ext jimage.1$ext \\
  %{_mandir}/man1/jimage-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jinfo.1$ext jinfo.1$ext \\
  %{_mandir}/man1/jinfo-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jmap.1$ext jmap.1$ext \\
  %{_mandir}/man1/jmap-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jps.1$ext jps.1$ext \\
  %{_mandir}/man1/jps-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jrunscript.1$ext jrunscript.1$ext \\
  %{_mandir}/man1/jrunscript-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jsadebugd.1$ext jsadebugd.1$ext \\
  %{_mandir}/man1/jsadebugd-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jstack.1$ext jstack.1$ext \\
  %{_mandir}/man1/jstack-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jstat.1$ext jstat.1$ext \\
  %{_mandir}/man1/jstat-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jstatd.1$ext jstatd.1$ext \\
  %{_mandir}/man1/jstatd-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/policytool.1$ext policytool.1$ext \\
  %{_mandir}/man1/policytool-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/rmic.1$ext rmic.1$ext \\
  %{_mandir}/man1/rmic-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/schemagen.1$ext schemagen.1$ext \\
  %{_mandir}/man1/schemagen-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/serialver.1$ext serialver.1$ext \\
  %{_mandir}/man1/serialver-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/wsgen.1$ext wsgen.1$ext \\
  %{_mandir}/man1/wsgen-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/wsimport.1$ext wsimport.1$ext \\
  %{_mandir}/man1/wsimport-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/xjc.1$ext xjc.1$ext \\
  %{_mandir}/man1/xjc-%{uniquesuffix %%1}.1$ext

for X in %{origin} %{javaver} ; do
  alternatives \\
    --install %{_jvmdir}/java-"$X" \\
    java_sdk_"$X" %{_jvmdir}/%{sdkdir %%1} %{priority} \\
    --slave %{_jvmjardir}/java-"$X" \\
    java_sdk_"$X"_exports %{_jvmjardir}/%{sdkdir %%1}
done

update-alternatives --install %{_jvmdir}/java-%{javaver}-%{origin} java_sdk_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir %%1} %{priority} \\
--slave %{_jvmjardir}/java-%{javaver}-%{origin}       java_sdk_%{javaver}_%{origin}_exports      %{_jvmjardir}/%{sdkdir %%1}

update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

exit 0
}

%global postun_devel() %{expand:
  alternatives --remove javac %{sdkbindir %%1}/javac
  alternatives --remove java_sdk_%{origin} %{_jvmdir}/%{sdkdir %%1}
  alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdkdir %%1}
  alternatives --remove java_sdk_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir %%1}

update-desktop-database %{_datadir}/applications &> /dev/null || :

if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{update_desktop_icons}
fi
exit 0
}

%global posttrans_devel() %{expand:
%{update_desktop_icons}
}

%global post_javadoc() %{expand:
alternatives \\
  --install %{_javadocdir}/java javadocdir %{_javadocdir}/%{uniquejavadocdir %%1}/api \\
  %{priority}
exit 0
}

%global postun_javadoc() %{expand:
  alternatives --remove javadocdir %{_javadocdir}/%{uniquejavadocdir %%1}/api
exit 0
}

%global files_jre() %{expand:
%{_datadir}/icons/hicolor/*x*/apps/java-%{javaver}.png
%{_datadir}/applications/*policytool%1.desktop
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libjsoundalsa.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libsplashscreen.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libawt_xawt.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libjawt.so
%{_jvmdir}/%{sdkdir %%1}/bin/policytool
}


%global files_jre_headless() %{expand:
%defattr(-,root,root,-)
%dir %{_jvmdir}/%{sdkdir %%1}
%license %{_jvmdir}/%{sdkdir %%1}/ASSEMBLY_EXCEPTION
%license %{_jvmdir}/%{sdkdir %%1}/LICENSE
%license %{_jvmdir}/%{sdkdir %%1}/THIRD_PARTY_README
%{_jvmdir}/%{sdkdir %%1}/release
%{_jvmdir}/%{sdkdir %%1}/jrt-fs.jar
%{_jvmdir}/%{jrelnk %%1}
%{_jvmjardir}/%{jrelnk %%1}
%{_jvmprivdir}/%{sdkdir %%1}
%{jvmjardir %%1}
%dir %{_jvmdir}/%{sdkdir %%1}/bin
%{_jvmdir}/%{sdkdir %%1}/bin/appletviewer
%{_jvmdir}/%{sdkdir %%1}/bin/idlj
%{_jvmdir}/%{sdkdir %%1}/bin/java
%{_jvmdir}/%{sdkdir %%1}/bin/jjs
%{_jvmdir}/%{sdkdir %%1}/bin/jrunscript
%{_jvmdir}/%{sdkdir %%1}/bin/jstatd
%{_jvmdir}/%{sdkdir %%1}/bin/keytool
%{_jvmdir}/%{sdkdir %%1}/bin/orbd
%{_jvmdir}/%{sdkdir %%1}/bin/pack200
%{_jvmdir}/%{sdkdir %%1}/bin/rmid
%{_jvmdir}/%{sdkdir %%1}/bin/rmiregistry
%{_jvmdir}/%{sdkdir %%1}/bin/servertool
%{_jvmdir}/%{sdkdir %%1}/bin/tnameserv
%{_jvmdir}/%{sdkdir %%1}/bin/unpack200
%{_jvmdir}/%{sdkdir %%1}/jmods
%dir %{_jvmdir}/%{sdkdir %%1}/lib
%{_jvmdir}/%{sdkdir %%1}/lib/classlist
%{_jvmdir}/%{sdkdir %%1}/lib/jexec
%{_jvmdir}/%{sdkdir %%1}/lib/modules
%{_jvmdir}/%{sdkdir %%1}/lib/psfont.properties.ja
%{_jvmdir}/%{sdkdir %%1}/lib/psfontj2d.properties
%{_jvmdir}/%{sdkdir %%1}/lib/tzdb.dat
%dir %{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/jli
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/jli/libjli.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/jvm.cfg
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libattach.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libawt.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libawt_headless.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libdt_socket.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libfontmanager.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libinstrument.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libj2gss.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libj2pcsc.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libj2pkcs11.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libjaas_unix.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libjava.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libjavajpeg.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libjdwp.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libjimage.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libjsig.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libjsound.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/liblcms.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libmanagement.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libmanagement_ext.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libmlib_image.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libnet.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libnio.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libprefs.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/librmi.so
%ifnarch %{arm}
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libsaproc.so
%endif
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libsctp.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libunpack.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libverify.so
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libzip.so
%{_jvmdir}/%{sdkdir %%1}/lib/security/cacerts
%dir %{_jvmdir}/%{sdkdir %%1}/lib/security
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/lib/security/US_export_policy.jar
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/lib/security/local_policy.jar
#FIXME is the blacklisted certs really supposed to be config(noreplace)?
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/lib/security/blacklisted.certs
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/security/java.policy
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/security/java.security
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/logging.properties
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/security/nss.cfg
#TODO which of these should be noreplace? all of them?
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/management/jmxremote.access
%config %{_jvmdir}/%{sdkdir %%1}/conf/management/jmxremote.password.template
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/management/management.properties
%config %{_jvmdir}/%{sdkdir %%1}/conf/management/snmp.acl.template
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/net.properties
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/sound.properties
%config %{_jvmdir}/%{sdkdir %%1}/lib/accessibility.properties
%{_mandir}/man1/appletviewer-%{uniquesuffix %%1}.1*
%{_mandir}/man1/idlj-%{uniquesuffix %%1}.1*
%{_mandir}/man1/java-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jjs-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jrunscript-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jstatd-%{uniquesuffix %%1}.1*
%{_mandir}/man1/keytool-%{uniquesuffix %%1}.1*
%{_mandir}/man1/orbd-%{uniquesuffix %%1}.1*
%{_mandir}/man1/pack200-%{uniquesuffix %%1}.1*
%{_mandir}/man1/rmid-%{uniquesuffix %%1}.1*
%{_mandir}/man1/rmiregistry-%{uniquesuffix %%1}.1*
%{_mandir}/man1/servertool-%{uniquesuffix %%1}.1*
%{_mandir}/man1/tnameserv-%{uniquesuffix %%1}.1*
%{_mandir}/man1/unpack200-%{uniquesuffix %%1}.1*
%{_jvmdir}/%{sdkdir %%1}/lib/audio/
%ifarch %{jit_arches}
%attr(664, root, root) %ghost %{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/server/classes.jsa
%attr(664, root, root) %ghost %{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/client/classes.jsa
%endif
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/server/
%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/client/
}

%global files_devel() %{expand:
%defattr(-,root,root,-)
%license %{_jvmdir}/%{sdkdir %%1}/ASSEMBLY_EXCEPTION
%license %{_jvmdir}/%{sdkdir %%1}/LICENSE
%license %{_jvmdir}/%{sdkdir %%1}/THIRD_PARTY_README
%dir %{_jvmdir}/%{sdkdir %%1}/bin
%{_jvmdir}/%{sdkdir %%1}/bin/appletviewer
%{_jvmdir}/%{sdkdir %%1}/bin/idlj
%{_jvmdir}/%{sdkdir %%1}/bin/jar
%{_jvmdir}/%{sdkdir %%1}/bin/jarsigner
%{_jvmdir}/%{sdkdir %%1}/bin/javac
%{_jvmdir}/%{sdkdir %%1}/bin/javadoc
%{_jvmdir}/%{sdkdir %%1}/bin/javah
%{_jvmdir}/%{sdkdir %%1}/bin/javap
%{_jvmdir}/%{sdkdir %%1}/bin/jconsole
%{_jvmdir}/%{sdkdir %%1}/bin/jcmd
%{_jvmdir}/%{sdkdir %%1}/bin/jdb
%{_jvmdir}/%{sdkdir %%1}/bin/jdeps
%{_jvmdir}/%{sdkdir %%1}/bin/jimage
%{_jvmdir}/%{sdkdir %%1}/bin/jhsdb
%{_jvmdir}/%{sdkdir %%1}/bin/jinfo
%{_jvmdir}/%{sdkdir %%1}/bin/jlink
%{_jvmdir}/%{sdkdir %%1}/bin/jmap
%{_jvmdir}/%{sdkdir %%1}/bin/jmod
%{_jvmdir}/%{sdkdir %%1}/bin/jps
%{_jvmdir}/%{sdkdir %%1}/bin/jrunscript
%{_jvmdir}/%{sdkdir %%1}/bin/jsadebugd
%{_jvmdir}/%{sdkdir %%1}/bin/jshell
%{_jvmdir}/%{sdkdir %%1}/bin/jstack
%{_jvmdir}/%{sdkdir %%1}/bin/jstat
%{_jvmdir}/%{sdkdir %%1}/bin/jstatd
%{_jvmdir}/%{sdkdir %%1}/bin/policytool
%{_jvmdir}/%{sdkdir %%1}/bin/rmic
%{_jvmdir}/%{sdkdir %%1}/bin/schemagen
%{_jvmdir}/%{sdkdir %%1}/bin/serialver
%{_jvmdir}/%{sdkdir %%1}/bin/wsgen
%{_jvmdir}/%{sdkdir %%1}/bin/wsimport
%{_jvmdir}/%{sdkdir %%1}/bin/xjc
%{_jvmdir}/%{sdkdir %%1}/include
#%{_jvmdir}/%{sdkdir %%1}/lib
%{_jvmdir}/%{sdkdir %%1}/lib/ct.sym
%if %{with_systemtap}
%{_jvmdir}/%{sdkdir %%1}/tapset
%endif
%{_jvmjardir}/%{sdkdir %%1}
%{_datadir}/applications/*jconsole%1.desktop
%{_mandir}/man1/appletviewer-%{uniquesuffix %%1}.1*
%{_mandir}/man1/idlj-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jar-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jarsigner-%{uniquesuffix %%1}.1*
%{_mandir}/man1/javac-%{uniquesuffix %%1}.1*
%{_mandir}/man1/javadoc-%{uniquesuffix %%1}.1*
%{_mandir}/man1/javah-%{uniquesuffix %%1}.1*
%{_mandir}/man1/javap-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jconsole-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jcmd-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jdb-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jdeps-%{uniquesuffix %%1}.1*
#FIXME enable when aviablable
#%{_mandir}/man1/jimage-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jinfo-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jmap-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jps-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jrunscript-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jsadebugd-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jstack-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jstat-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jstatd-%{uniquesuffix %%1}.1*
%{_mandir}/man1/policytool-%{uniquesuffix %%1}.1*
%{_mandir}/man1/rmic-%{uniquesuffix %%1}.1*
%{_mandir}/man1/schemagen-%{uniquesuffix %%1}.1*
%{_mandir}/man1/serialver-%{uniquesuffix %%1}.1*
%{_mandir}/man1/wsgen-%{uniquesuffix %%1}.1*
%{_mandir}/man1/wsimport-%{uniquesuffix %%1}.1*
%{_mandir}/man1/xjc-%{uniquesuffix %%1}.1*
%if %{with_systemtap}
%{tapsetroot}
%endif
}

%global files_demo() %{expand:
%defattr(-,root,root,-)
%license %{_jvmdir}/%{sdkdir %%1}/ASSEMBLY_EXCEPTION
%license %{_jvmdir}/%{sdkdir %%1}/LICENSE
%license %{_jvmdir}/%{sdkdir %%1}/THIRD_PARTY_README
#%{_jvmdir}/%{sdkdir %%1}/demo
}

%global files_src() %{expand:
%defattr(-,root,root,-)
%doc README.src
%{_jvmdir}/%{sdkdir %%1}/src.zip
}

%global files_javadoc() %{expand:
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{uniquejavadocdir %%1}
%license %{buildoutputdir %%1}/images/%{jdkimage}/ASSEMBLY_EXCEPTION
%license %{buildoutputdir %%1}/images/%{jdkimage}/LICENSE
%license %{buildoutputdir %%1}/images/%{jdkimage}/THIRD_PARTY_README
}

%global files_accessibility() %{expand:
#%{_jvmdir}/%{sdkdir %%1}/lib/%{archinstall}/libatk-wrapper.so
#%{_jvmdir}/%{sdkdir %%1}/lib/ext/java-atk-wrapper.jar
#%{_jvmdir}/%{sdkdir %%1}/lib/accessibility.properties
}

# not-duplicated requires/provides/obsolate for normal/debug packages
%global java_rpo() %{expand:
Requires: fontconfig
Requires: xorg-x11-fonts-Type1

# Requires rest of java
Requires: %{name}-headless%1 = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%1 = %{epoch}:%{version}-%{release}

Provides: java-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}

# Standard JPackage base provides.
#Provides: jre-%{javaver}-%{origin}%1 = %{epoch}:%{version}-%{release}
#Provides: jre-%{origin}%1 = %{epoch}:%{version}-%{release}
#Provides: jre-%{javaver}%1 = %{epoch}:%{version}-%{release}
#Provides: java-%{javaver}%1 = %{epoch}:%{version}-%{release}
#Provides: jre = %{javaver}%1
#Provides: java-%{origin}%1 = %{epoch}:%{version}-%{release}
#Provides: java%1 = %{epoch}:%{javaver}
# Standard JPackage extensions provides.
#Provides: java-fonts%1 = %{epoch}:%{version}

}

%global java_headless_rpo() %{expand:
# Require /etc/pki/java/cacerts.
Requires: ca-certificates
# Require jpackage-utils for ownership of /usr/lib/jvm/
Requires: jpackage-utils
# Require zoneinfo data provided by tzdata-java subpackage.
Requires: tzdata-java >= 2014f-1
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

Provides: java-%{javaver}-%{origin}-headless = %{epoch}:%{version}-%{release}

# Standard JPackage base provides.
#Provides: jre-%{javaver}-%{origin}-headless%1 = %{epoch}:%{version}-%{release}
#Provides: jre-%{origin}-headless%1 = %{epoch}:%{version}-%{release}
#Provides: jre-%{javaver}-headless%1 = %{epoch}:%{version}-%{release}
#Provides: java-%{javaver}-headless%1 = %{epoch}:%{version}-%{release}
#Provides: jre-headless%1 = %{epoch}:%{javaver}
#Provides: java-%{origin}-headless%1 = %{epoch}:%{version}-%{release}
#Provides: java-headless%1 = %{epoch}:%{javaver}
# Standard JPackage extensions provides.
#Provides: jndi%1 = %{epoch}:%{version}
#Provides: jndi-ldap%1 = %{epoch}:%{version}
#Provides: jndi-cos%1 = %{epoch}:%{version}
#Provides: jndi-rmi%1 = %{epoch}:%{version}
#Provides: jndi-dns%1 = %{epoch}:%{version}
#Provides: jaas%1 = %{epoch}:%{version}
#Provides: jsse%1 = %{epoch}:%{version}
#Provides: jce%1 = %{epoch}:%{version}
#Provides: jdbc-stdext%1 = 4.1
#Provides: java-sasl%1 = %{epoch}:%{version}

}

%global java_devel_rpo() %{expand:
# Require base package.
Requires:         %{name}%1 = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%1 = %{epoch}:%{version}-%{release}
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

Provides: java-%{javaver}-%{origin}-devel = %{epoch}:%{version}-%{release}

# Standard JPackage devel provides.
#Provides: java-sdk-%{javaver}-%{origin}%1 = %{epoch}:%{version}
#Provides: java-sdk-%{javaver}%1 = %{epoch}:%{version}
#Provides: java-sdk-%{origin}%1 = %{epoch}:%{version}
#Provides: java-sdk%1 = %{epoch}:%{javaver}
#Provides: java-%{javaver}-devel%1 = %{epoch}:%{version}
#Provides: java-devel-%{origin}%1 = %{epoch}:%{version}
#Provides: java-devel%1 = %{epoch}:%{javaver}

}


%global java_demo_rpo() %{expand:
Requires: %{name}%1 = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%1 = %{epoch}:%{version}-%{release}

Provides: java-%{javaver}-%{origin}-demo = %{epoch}:%{version}-%{release}

}

%global java_javadoc_rpo() %{expand:
OrderWithRequires: %{name}-headless%1 = %{epoch}:%{version}-%{release}
# Post requires alternatives to install javadoc alternative.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall javadoc alternative.
Requires(postun): %{_sbindir}/alternatives

Provides: java-%{javaver}-%{origin}-javadoc = %{epoch}:%{version}-%{release}

# Standard JPackage javadoc provides.
#Provides: java-javadoc%1 = %{epoch}:%{version}-%{release}
#Provides: java-%{javaver}-javadoc%1 = %{epoch}:%{version}-%{release}

}

%global java_src_rpo() %{expand:
Requires: %{name}-headless%1 = %{epoch}:%{version}-%{release}

Provides: java-%{javaver}-%{origin}-headless = %{epoch}:%{version}-%{release}

}

%global java_accessibility_rpo() %{expand:
Requires: java-atk-wrapper
Requires: %{name}%1 = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%1 = %{epoch}:%{version}-%{release}

Provides: java-%{javaver}-%{origin}-accessiblity = %{epoch}:%{version}-%{release}
}

# Prevent brp-java-repack-jars from being run.
%global __jar_repack 0

Name:    java-%{majorver}-%{origin}
Version: %{newjavaver}.%{buildver}
Release: 1%{?dist}
# java-1.5.0-ibm from jpackage.org set Epoch to 1 for unknown reasons,
# and this change was brought into RHEL-4.  java-1.5.0-ibm packages
# also included the epoch in their virtual provides.  This created a
# situation where in-the-wild java-1.5.0-ibm packages provided "java =
# 1:1.5.0".  In RPM terms, "1.6.0 < 1:1.5.0" since 1.6.0 is
# interpreted as 0:1.6.0.  So the "java >= 1.6.0" requirement would be
# satisfied by the 1:1.5.0 packages.  Thus we need to set the epoch in
# JDK package >= 1.6.0 to 1, and packages referring to JDK virtual
# provides >= 1.6.0 must specify the epoch, "java >= 1:1.6.0".
Epoch:   1
Summary: OpenJDK Runtime Environment
Group:   Development/Languages

License:  ASL 1.1 and ASL 2.0 and GPL+ and GPLv2 and GPLv2 with exceptions and LGPL+ and LGPLv2 and MPLv1.0 and MPLv1.1 and Public Domain and W3C
URL:      http://openjdk.java.net/

# Source from upstrem OpenJDK9 project. To regenerate, use
# ./generate_source_tarball.sh jdk9 jdk9 jdk9-%%{buildver}
Source0:  jdk9-jdk-%{majorver}+%{buildver}.tar.xz

# Custom README for -src subpackage
Source2:  README.src

# Use 'generate_tarballs.sh' to generate the following tarballs
# They are based on code contained in the IcedTea7 project.

# Systemtap tapsets. Zipped up to keep it small.
Source8: systemtap-tapset.tar.gz

# Desktop files. Adapated from IcedTea.
Source9: jconsole.desktop.in
Source10: policytool.desktop.in

# nss configuration file
Source11: nss.cfg

# Removed libraries that we link instead
Source12: remove-intree-libraries.sh

# Ensure we aren't using the limited crypto policy
Source13: TestCryptoLevel.java

Source20: repackReproduciblePolycies.sh

# RPM/distribution specific patches

# Ignore AWTError when assistive technologies are loaded 
Patch1:   accessible-toolkit.patch

# Restrict access to java-atk-wrapper classes
Patch3: java-atk-wrapper-security.patch
# RHBZ 808293
Patch4: PStack-808293.patch
# Allow multiple initialization of PKCS11 libraries
Patch5: multiple-pkcs11-library-init.patch
Patch12: removeSunEcProvider-RH1154143.patch
Patch13: libjpeg-turbo-1.4-compat.patch

#
# OpenJDK specific patches
#

# JVM heap size changes for s390 (thanks to aph)
Patch100: java-1.9.0-openjdk-s390-java-opts.patch
Patch101: sorted-diff.patch
# Type fixing for s390
Patch102: java-1.9.0-openjdk-size_t.patch
Patch103: dont-define-stdlib.patch

Patch300: jstack-pr1845.patch

Patch400: ppc_stack_overflow_fix.patch 

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: alsa-lib-devel
BuildRequires: binutils
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: fontconfig
BuildRequires: freetype-devel
BuildRequires: giflib-devel
BuildRequires: gcc-c++
BuildRequires: gtk2-devel
BuildRequires: lcms2-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libxslt
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXinerama-devel
BuildRequires: libXt-devel
BuildRequires: libXtst-devel
# Requirements for setting up the nss.cfg
BuildRequires: nss-devel
BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
#BuildRequires: redhat-lsb
BuildRequires: zip
BuildRequires: java-1.8.0-openjdk-devel
# Zero-assembler build requirement.
%ifnarch %{jit_arches}
BuildRequires: libffi-devel
%endif

# cacerts build requirement.
BuildRequires: openssl

%if %{with_systemtap}
BuildRequires: systemtap-sdt-devel
%endif


# this is built always, also during debug-only build
# when it is built in debug-only, then this package is just placeholder
%{java_rpo %{nil}}

%description
The OpenJDK runtime environment.

%if %{include_debug_build}
%package debug
Summary: OpenJDK Runtime Environment %{debug_on}
Group:   Development/Languages

%{java_rpo %{debug_suffix_unquoted}}
%description debug
The OpenJDK runtime environment.
%{debug_warning}
%endif

%if %{include_normal_build}
%package headless
Summary: OpenJDK Runtime Environment
Group:   Development/Languages

%{java_headless_rpo %{nil}}

%description headless
The OpenJDK runtime environment without audio and video support.
%endif

%if %{include_debug_build}
%package headless-debug
Summary: OpenJDK Runtime Environment %{debug_on}
Group:   Development/Languages

%{java_headless_rpo %{debug_suffix_unquoted}}

%description headless-debug
The OpenJDK runtime environment without audio and video support.
%{debug_warning}
%endif

%if %{include_normal_build}
%package devel
Summary: OpenJDK Development Environment
Group:   Development/Tools

%{java_devel_rpo %{nil}}

%description devel
The OpenJDK development tools.
%endif

%if %{include_debug_build}
%package devel-debug
Summary: OpenJDK Development Environment %{debug_on}
Group:   Development/Tools

%{java_devel_rpo %{debug_suffix_unquoted}}

%description devel-debug
The OpenJDK development tools.
%{debug_warning}
%endif

%if %{include_normal_build}
%package demo
Summary: OpenJDK Demos
Group:   Development/Languages

%{java_demo_rpo %{nil}}

%description demo
The OpenJDK demos.
%endif

%if %{include_debug_build}
%package demo-debug
Summary: OpenJDK Demos %{debug_on}
Group:   Development/Languages

%{java_demo_rpo %{debug_suffix_unquoted}}

%description demo-debug
The OpenJDK demos.
%{debug_warning}
%endif

%if %{include_normal_build}
%package src
Summary: OpenJDK Source Bundle
Group:   Development/Languages

%{java_src_rpo %{nil}}

%description src
The OpenJDK source bundle.
%endif

%if %{include_debug_build}
%package src-debug
Summary: OpenJDK Source Bundle %{for_debug}
Group:   Development/Languages

%{java_src_rpo %{debug_suffix_unquoted}}

%description src-debug
The OpenJDK source bundle %{for_debug}.
%endif

%if %{include_normal_build}
%package javadoc
Summary: OpenJDK API Documentation
Group:   Documentation
Requires: jpackage-utils
BuildArch: noarch

%{java_javadoc_rpo %{nil}}

%description javadoc
The OpenJDK API documentation.
%endif

%if %{include_debug_build}
%package javadoc-debug
Summary: OpenJDK API Documentation %{for_debug}
Group:   Documentation
Requires: jpackage-utils
BuildArch: noarch

%{java_javadoc_rpo %{debug_suffix_unquoted}}

%description javadoc-debug
The OpenJDK API documentation %{for_debug}.
%endif

%if %{include_normal_build}
%package accessibility
Summary: OpenJDK accessibility connector

%{java_accessibility_rpo %{nil}}

%description accessibility
Enables accessibility support in OpenJDK by using java-atk-wrapper. This allows
compatible at-spi2 based accessibility programs to work for AWT and Swing-based
programs.

Please note, the java-atk-wrapper is still in beta, and OpenJDK itself is still
being tuned to be working with accessibility features. There are known issues
with accessibility on, so please do not install this package unless you really
need to.
%endif

%if %{include_debug_build}
%package accessibility-debug
Summary: OpenJDK accessibility connector %{for_debug}

%{java_accessibility_rpo %{debug_suffix_unquoted}}

%description accessibility-debug
See normal java-%{version}-openjdk-accessibility description.
%endif

%prep
if [ %{include_normal_build} -eq 0 -o  %{include_normal_build} -eq 1 ] ; then
  echo "include_normal_build is %{include_normal_build}"
else
  echo "include_normal_build is %{include_normal_build}, thats invalid. Use 1 for yes or 0 for no"
  exit 11
fi
if [ %{include_debug_build} -eq 0 -o  %{include_debug_build} -eq 1 ] ; then
  echo "include_debug_build is %{include_debug_build}"
else
  echo "include_debug_build is %{include_debug_build}, thats invalid. Use 1 for yes or 0 for no"
  exit 12
fi
if [ %{include_debug_build} -eq 0 -a  %{include_normal_build} -eq 0 ] ; then
  echo "you have disabled both include_debug_build and include_debug_build. no go."
  exit 13
fi
%setup -q -c -n %{uniquesuffix ""} -T -a 0
# https://bugzilla.redhat.com/show_bug.cgi?id=1189084
prioritylength=`expr length %{priority}`
if [ $prioritylength -ne 7 ] ; then
 echo "priority must be 7 digits in total, violated"
 exit 14
fi
cp %{SOURCE2} .

# OpenJDK patches

# Remove libraries that are linked
sh %{SOURCE12}

%patch1
%patch3
%patch4
%patch5
%patch12
%patch13

# s390 build fixes
%ifarch s390
%patch100
%patch102
%endif

%patch101
%patch103

# Zero PPC fixes.
#  TODO: propose them upstream
%patch400

# Extract systemtap tapsets
%if %{with_systemtap}

tar xzf %{SOURCE8}

%patch300

%if %{include_debug_build}
cp -r tapset tapset%{debug_suffix}
%endif


for suffix in %{build_loop} ; do
  for file in "tapset"$suffix/*.in; do
    OUTPUT_FILE=`echo $file | sed -e s:%{javaver}\.stp\.in$:%{version}-%{release}.%{_arch}.stp:g`
    sed -e s:@ABS_SERVER_LIBJVM_SO@:%{_jvmdir}/%{sdkdir $suffix}/lib/%{archinstall}/server/libjvm.so:g $file > $file.1
# TODO find out which architectures other than i686 have a client vm
%ifarch %{ix86}
    sed -e s:@ABS_CLIENT_LIBJVM_SO@:%{_jvmdir}/%{sdkdir $suffix}/lib/%{archinstall}/client/libjvm.so:g $file.1 > $OUTPUT_FILE
%else
    sed -e '/@ABS_CLIENT_LIBJVM_SO@/d' $file.1 > $OUTPUT_FILE
%endif
    sed -i -e s:@ABS_JAVA_HOME_DIR@:%{_jvmdir}/%{sdkdir $suffix}:g $OUTPUT_FILE
    sed -i -e s:@INSTALL_ARCH_DIR@:%{archinstall}:g $OUTPUT_FILE
  done
done
# systemtap tapsets ends
%endif 

# Prepare desktop files
for suffix in %{build_loop} ; do
for file in %{SOURCE9} %{SOURCE10} ; do
    FILE=`basename $file | sed -e s:\.in$::g`
    EXT="${FILE##*.}"
    NAME="${FILE%.*}"
    OUTPUT_FILE=$NAME$suffix.$EXT
    sed -e s:#JAVA_HOME#:%{sdkbindir $suffix}:g $file > $OUTPUT_FILE
    sed -i -e  s:#JRE_HOME#:%{jrebindir $suffix}:g $OUTPUT_FILE
    sed -i -e  s:#ARCH#:%{version}-%{release}.%{_arch}$suffix:g $OUTPUT_FILE
done
done

%build
# How many cpu's do we have?
export NUM_PROC=`/usr/bin/getconf _NPROCESSORS_ONLN 2> /dev/null || :`
export NUM_PROC=${NUM_PROC:-1}

%ifarch s390x sparc64 alpha %{power64} %{aarch64}
export ARCH_DATA_MODEL=64
%endif
%ifarch alpha
export CFLAGS="$CFLAGS -mieee"
%endif

EXTRA_CFLAGS="-fstack-protector-strong"
#see https://bugzilla.redhat.com/show_bug.cgi?id=1120792
EXTRA_CFLAGS="$EXTRA_CFLAGS -Wno-error"
EXTRA_CPP_FLAGS="-Wno-error"
# PPC/PPC64 needs -fno-tree-vectorize since -O3 would
# otherwise generate wrong code producing segfaults.
%ifarch %{power64} ppc
EXTRA_CFLAGS="$EXTRA_CFLAGS -fno-tree-vectorize"
# fix rpmlint warnings
EXTRA_CFLAGS="$EXTRA_CFLAGS -fno-strict-aliasing"
%endif

%if 0%{?fedora} > 23
EXTRA_CFLAGS="$EXTRA_CFLAGS -Wno-error -std=gnu++98  -fno-delete-null-pointer-checks -fno-lifetime-dse -fpermissive"
EXTRA_CPP_FLAGS="$EXTRA_CPP_FLAGS -Wno-error -std=gnu++98 -fno-delete-null-pointer-checks -fno-lifetime-dse"
%endif

(cd jdk9/common/autoconf
 bash ./autogen.sh
)

for suffix in %{build_loop} ; do
if [ "$suffix" = "%{debug_suffix}" ] ; then
debugbuild=%{debugbuild_parameter}
else
debugbuild=%{normalbuild_parameter}
fi

mkdir -p %{buildoutputdir $suffix}
pushd %{buildoutputdir $suffix}

bash ../configure \
%ifnarch %{jit_arches}
    --with-jvm-variants=zero \
%endif
%ifarch %{ppc64le}
    --with-jobs=1 \
%endif
    --with-version-build=%{buildver} \
    --with-version-pre="ea" \
    --with-version-opt="" \
    --with-boot-jdk=/usr/lib/jvm/java-1.8.0-openjdk/ \
    --with-debug-level=$debugbuild \
    --with-native-debug-symbols=internal \
    --enable-unlimited-crypto \
    --with-zlib=system \
    --with-libjpeg=system \
    --with-giflib=system \
    --with-libpng=system \
    --with-lcms=system \
    --with-stdc++lib=dynamic \
    --with-extra-cxxflags="$EXTRA_CPP_FLAGS" \
    --with-extra-cflags="$EXTRA_CFLAGS" \
    --with-num-cores="$NUM_PROC" \
    --disable-javac-server \
    --disable-warnings-as-errors

make \
    JAVAC_FLAGS=-g \
    LOG=trace \
    DEBUG_BINARIES=true \
    JAVAC_FLAGS=-g \
    STRIP_POLICY=no_strip \
    POST_STRIP_CMD="" \
    WARNINGS_ARE_ERRORS="-Wno-error" \
    CFLAGS_WARNINGS_ARE_ERRORS="-Wno-error" \
    all

# the build (erroneously) removes read permissions from some jars
# this is a regression in OpenJDK 7 (our compiler):
# http://icedtea.classpath.org/bugzilla/show_bug.cgi?id=1437
find images/%{jdkimage} -iname '*.jar' -exec chmod ugo+r {} \;

# remove redundant *diz and *debuginfo files
find images/%{jdkimage} -iname '*.diz' -exec rm {} \;
find images/%{jdkimage} -iname '*.debuginfo' -exec rm {} \;

popd >& /dev/null

# Install nss.cfg right away as we will be using the JRE above
export JAVA_HOME=$(pwd)/%{buildoutputdir $suffix}/images/%{jdkimage}

# Install nss.cfg right away as we will be using the JRE above
install -m 644 %{SOURCE11} $JAVA_HOME/conf/security/

%if ! 0%{?rhel}
# Use system-wide tzdata
rm $JAVA_HOME/lib/tzdb.dat
ln -s %{_datadir}/javazi-1.8/tzdb.dat $JAVA_HOME/lib/tzdb.dat
%endif

# Check unlimited policy has been used
$JAVA_HOME/bin/javac -d . %{SOURCE13}
$JAVA_HOME/bin/java TestCryptoLevel

# Check debug symbols are present and can identify code
SERVER_JVM="$JAVA_HOME/lib/%{archinstall}/server/libjvm.so"
if [ -f "$SERVER_JVM" ] ; then
  nm -aCl "$SERVER_JVM" | grep sharedRuntime.cpp
fi
CLIENT_JVM="$JAVA_HOME/lib/%{archinstall}/client/libjvm.so"
if [ -f "$CLIENT_JVM" ] ; then
  nm -aCl "$CLIENT_JVM" | grep sharedRuntime.cpp
fi
ZERO_JVM="$JAVA_HOME/lib/%{archinstall}/zero/libjvm.so"
if [ -f "$ZERO_JVM" ] ; then
  nm -aCl "$ZERO_JVM" | grep sharedRuntime.cpp
fi

# Check src.zip has all sources. See RHBZ#1130490
jar -tf $JAVA_HOME/src.zip | grep 'sun.misc.Unsafe'

# Check class files include useful debugging information
$JAVA_HOME/bin/javap -l java.lang.Object | grep "Compiled from"
$JAVA_HOME/bin/javap -l java.lang.Object | grep LineNumberTable
$JAVA_HOME/bin/javap -l java.lang.Object | grep LocalVariableTable

# Check generated class files include useful debugging information
$JAVA_HOME/bin/javap -l java.nio.ByteBuffer | grep "Compiled from"
$JAVA_HOME/bin/javap -l java.nio.ByteBuffer | grep LineNumberTable
$JAVA_HOME/bin/javap -l java.nio.ByteBuffer | grep LocalVariableTable

#build cycles
done

%install
STRIP_KEEP_SYMTAB=libjvm*

for suffix in %{build_loop} ; do

# Install the jdk
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}
cp -a %{buildoutputdir $suffix}/images/%{jdkimage} \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}


# Install symlink to default soundfont
install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/lib/audio
pushd $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/lib/audio
ln -s %{_datadir}/soundfonts/default.sf2
popd

#install jsa directories so we can owe them
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/lib/%{archinstall}/server/
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/lib/%{archinstall}/client/

pushd %{buildoutputdir $suffix}/images/%{jdkimage}

%if %{with_systemtap}
  # Install systemtap support files.
  install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/tapset
  # note, that uniquesuffix  is in BUILD dir in this case
  cp -a $RPM_BUILD_DIR/%{uniquesuffix ""}/tapset$suffix/*.stp $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/tapset/
  install -d -m 755 $RPM_BUILD_ROOT%{tapsetdir}
  pushd $RPM_BUILD_ROOT%{tapsetdir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{sdkdir $suffix}/tapset %{tapsetdir})
    ln -sf $RELATIVE/*.stp .
  popd
%endif

  # Install cacerts symlink.
  rm -f $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/lib/security/cacerts
  pushd $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/lib/security
    RELATIVE=$(%{abs2rel} %{_sysconfdir}/pki/java \
      %{_jvmdir}/%{sdkdir $suffix}/lib/security)
    ln -sf $RELATIVE/cacerts .
  popd

  # Install extension symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{jvmjardir $suffix}
  pushd $RPM_BUILD_ROOT%{jvmjardir $suffix}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{sdk $suffix}/lib %{jvmjardir $suffix})
    ln -sf $RELATIVE/jsse.jar jsse-%{version}.jar
    ln -sf $RELATIVE/jce.jar jce-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-ldap-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-cos-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-rmi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jaas-%{version}.jar
    ln -sf $RELATIVE/rt.jar jdbc-stdext-%{version}.jar
    ln -sf jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
    ln -sf $RELATIVE/rt.jar sasl-%{version}.jar
    for jar in *-%{version}.jar
    do
      if [ x%{version} != x%{javaver} ]
      then
        ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|-%{javaver}.jar|g")
      fi
      ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|.jar|g")
    done
  popd

  # Install JCE policy symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmprivdir}/%{uniquesuffix $suffix}/jce/vanilla

  # Install versioned symlinks.
  pushd $RPM_BUILD_ROOT%{_jvmdir}
    ln -sf %{sdkdir $suffix} %{jrelnk $suffix}
  popd

  pushd $RPM_BUILD_ROOT%{_jvmjardir}
    ln -sf %{sdkdir $suffix} %{jrelnk $suffix}
  popd

  # Install man pages.
  install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
  for manpage in man/man1/*
  do
    # Convert man pages to UTF8 encoding.
    iconv -f ISO_8859-1 -t UTF8 $manpage -o $manpage.tmp
    mv -f $manpage.tmp $manpage
    install -m 644 -p $manpage $RPM_BUILD_ROOT%{_mandir}/man1/$(basename \
      $manpage .1)-%{uniquesuffix $suffix}.1
  done
  # Remove man pages from jdk image
  rm -rf $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/man

popd


# Install Javadoc documentation.
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
cp -a %{buildoutputdir $suffix}/images/docs $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir $suffix}

# Install icons and menu entries.
for s in 16 24 32 48 ; do
  install -D -p -m 644 \
    jdk9/jdk/src/java.desktop/unix/classes/sun/awt/X11/java-icon${s}.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/java-%{javaver}.png
done

# Install desktop files.
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
for e in jconsole$suffix policytool$suffix ; do
    desktop-file-install --vendor=%{uniquesuffix $suffix} --mode=644 \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications $e.desktop
done

# Install /etc/.java/.systemPrefs/ directory
# See https://bugzilla.redhat.com/show_bug.cgi?id=741821
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/.java/.systemPrefs

# FIXME: remove SONAME entries from demo DSOs.  See
# https://bugzilla.redhat.com/show_bug.cgi?id=436497

# Find non-documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/sample \
  -type f -o -type l | sort \
  | grep -v README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}-demo.files"$suffix"
# Find documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/sample \
  -type f -o -type l | sort \
  | grep README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  | sed 's|^|%doc |' \
  >> %{name}-demo.files"$suffix"

# TODO find out how to use ext in jdk9

# intentionally after the files generation, as it goes to separate package
# Create links which leads to separately installed java-atk-bridge and allow configuration
# links points to java-atk-wrapper - an dependence
  #pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir $suffix}/lib/%{archinstall}
  #  ln -s %{_libdir}/java-atk-wrapper/libatk-wrapper.so.0 libatk-wrapper.so
  #popd
  #pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir $suffix}/lib/ext
  #   ln -s %{_libdir}/java-atk-wrapper/java-atk-wrapper.jar  java-atk-wrapper.jar
  #popd
  pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir $suffix}/lib/
    echo "#Config file to  enable java-atk-wrapper" > accessibility.properties
    echo "" >> accessibility.properties
    echo "assistive_technologies=org.GNOME.Accessibility.AtkWrapper" >> accessibility.properties
    echo "" >> accessibility.properties
  popd

bash %{SOURCE20} $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir $suffix} %{javaver}

# end, dual install
done

%if %{include_normal_build} 
# intentioanlly only for non-debug
%pretrans headless -p <lua>
-- see https://bugzilla.redhat.com/show_bug.cgi?id=1038092 for whole issue 

local posix = require "posix"

local currentjvm = "%{uniquesuffix %{nil}}"
local jvmdir = "%{_jvmdir %{nil}}"
local jvmDestdir = jvmdir
local origname = "%{name}"
local origjavaver = "%{javaver}"
--trasnform substitute names to lua patterns
--all percentages must be doubled for case of RPM escapingg
local name = string.gsub(string.gsub(origname, "%%-", "%%%%-"), "%%.", "%%%%.")
local javaver = string.gsub(origjavaver, "%%.", "%%%%.")
local arch ="%{_arch}"
local  debug = false;

local jvms = { }

local caredFiles = {
              "conf/logging.properties",
              "conf/net.properties",
              "conf/sound.properties",
              "conf/security/java.policy",
              "conf/security/java.security",
              "conf/security/nss.cfg",
              "lib/psfontj2d.properties",
              "lib/security/US_export_policy.jar",
              "lib/security/local_policy.jar",
}

-- TODO sort out these ones from 8
-- "jre/lib/deployment.properties",
-- "jre/lib/deployment.config",
-- "jre/lib/ext",

function splitToTable(source, pattern)
  local i1 = string.gmatch(source, pattern) 
  local l1 = {}
  for i in i1 do
    table.insert(l1, i)
  end
  return l1
end

if (debug) then
  print("started")
end;

foundJvms = posix.dir(jvmdir);
if (foundJvms == nil) then
  if (debug) then
    print("no, or nothing in "..jvmdir.." exit")
  end;
  return
end

if (debug) then
  print("found "..#foundJvms.."jvms")
end;

for i,p in pairs(foundJvms) do
-- regex similar to %{_jvmdir}/%{name}-%{javaver}*%{_arch} bash command
--all percentages must be doubled for case of RPM escapingg
  if (string.find(p, name.."%%-"..javaver..".*"..arch) ~= nil ) then
    if (debug) then
      print("matched:  "..p)
    end;
    if (currentjvm ==  p) then
      if (debug) then
        print("this jdk is already installed. exiting lua script")
      end;
      return
    end ;
    table.insert(jvms, p)
  else
    if (debug) then
      print("NOT matched:  "..p)
    end;
  end
end

if (#jvms <=0) then 
  if (debug) then
    print("no matching jdk in "..jvmdir.." exit")
  end;
  return
end;

if (debug) then
  print("matched "..#jvms.." jdk in "..jvmdir)
end;

--full names are like java-1.7.0-openjdk-1.7.0.60-2.4.5.1.fc20.x86_64
table.sort(jvms , function(a,b) 
-- version-sort
-- split on non word: . - 
  local l1 = splitToTable(a, "[^%.-]+") 
  local l2 = splitToTable(b, "[^%.-]+") 
  for x = 1, math.min(#l1, #l2) do
    local l1x = tonumber(l1[x])
    local l2x = tonumber(l2[x])
    if (l1x ~= nil and l2x ~= nil)then
--if hunks are numbers, go with them 
      if (l1x < l2x) then return true; end
      if (l1x > l2x) then return false; end
    else
      if (l1[x] < l2[x]) then return true; end
      if (l1[x] > l2[x]) then return false; end
    end
-- if hunks are equals then move to another pair of hunks
  end
return a<b

end)

if (debug) then
  print("sorted lsit of jvms")
  for i,file in pairs(jvms) do
    print(file)
  end
end

latestjvm = jvms[#jvms]


for i,file in pairs(caredFiles) do
  local SOURCE=jvmdir.."/"..latestjvm.."/"..file
  local DEST=jvmDestdir.."/"..currentjvm.."/"..file
  if (debug) then
    print("going to copy "..SOURCE)
    print("to  "..DEST)
  end;
  local stat1 = posix.stat(SOURCE, "type");
  if (stat1 ~= nil) then
  if (debug) then
    print(SOURCE.." exists")
  end;
  local s = ""
  local dirs = splitToTable(DEST, "[^/]+") 
  for i,d in pairs(dirs) do
    if (i == #dirs) then
      break
    end
    s = s.."/"..d
    local stat2 = posix.stat(s, "type");
    if (stat2 == nil) then
      if (debug) then
        print(s.." does not exists, creating")
      end;
      posix.mkdir(s)
    else
      if (debug) then
        print(s.." exists,not creating")
      end;
    end
  end
-- Copy with -a to keep everything intact
    local exe = "cp".." -ar "..SOURCE.." "..DEST
    if (debug) then
      print("executing "..exe)
    end;    
    os.execute(exe)
  else
    if (debug) then
      print(SOURCE.." does not exists")
    end;
  end
end

%post 
%{post_script %{nil}}

%post headless
%{post_headless %{nil}}

%postun
%{postun_script %{nil}}

%postun headless
%{postun_headless %{nil}}

%posttrans
%{posttrans_script %{nil}}

%post devel
%{post_devel %{nil}}

%postun devel
%{postun_devel %{nil}}

%posttrans  devel
%{posttrans_devel %{nil}}

%post javadoc
%{post_javadoc %{nil}}

%postun javadoc
%{postun_javadoc %{nil}}
%endif

%if %{include_debug_build} 
%post debug
%{post_script %{debug_suffix_unquoted}}

%post headless-debug
%{post_headless %{debug_suffix_unquoted}}

%postun debug
%{postun_script %{debug_suffix_unquoted}}

%postun headless-debug
%{postun_headless %{debug_suffix_unquoted}}

%posttrans debug
%{posttrans_script %{debug_suffix_unquoted}}

%post devel-debug
%{post_devel %{debug_suffix_unquoted}}

%postun devel-debug
%{postun_devel %{debug_suffix_unquoted}}

%posttrans  devel-debug
%{posttrans_devel %{debug_suffix_unquoted}}

%post javadoc-debug
%{post_javadoc %{debug_suffix_unquoted}}

%postun javadoc-debug
%{postun_javadoc %{debug_suffix_unquoted}}
%endif

%if %{include_normal_build} 
%files
# main package builds always
%{files_jre %{nil}}
%else
%files
# placeholder
%endif


%if %{include_normal_build} 
%files headless
# important note, see https://bugzilla.redhat.com/show_bug.cgi?id=1038092 for whole issue 
# all config/norepalce files (and more) have to be declared in pretrans. See pretrans
%{files_jre_headless %{nil}}

%files devel
%{files_devel %{nil}}

%files demo -f %{name}-demo.files
%{files_demo %{nil}}

%files src
%{files_src %{nil}}

%files javadoc
%{files_javadoc %{nil}}

%files accessibility
%{files_accessibility %{nil}}
%endif

%if %{include_debug_build} 
%files debug
%{files_jre %{debug_suffix_unquoted}}

%files headless-debug
%{files_jre_headless %{debug_suffix_unquoted}}

%files devel-debug
%{files_devel %{debug_suffix_unquoted}}

%files demo-debug -f %{name}-demo.files-debug
%{files_demo %{debug_suffix_unquoted}}

%files src-debug
%{files_src %{debug_suffix_unquoted}}

%files javadoc-debug
%{files_javadoc %{debug_suffix_unquoted}}

%files accessibility-debug
%{files_accessibility %{debug_suffix_unquoted}}
%endif


%changelog
* Tue Feb 24 2015 Omair Majid <omajid@redhat.com> - 1:1.9.0.0-0.b25
- Initial build from java-1.8.0-openjdk RPM
