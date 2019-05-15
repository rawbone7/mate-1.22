# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.22

# Settings used for build from snapshots.
%{!?rel_build:%global commit 06e062693b16189373584801b056079eafac0034}
%{!?rel_build:%global commit_date 20160831}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:          libmateweather
Version:       %{branch}.0
%if 0%{?rel_build}
Release:       2%{?dist}
%else
Release:       0.7%{?git_rel}%{?dist}
%endif
Summary:       Libraries to allow MATE Desktop to display weather information
License:       GPLv2+ and LGPLv2+
URL:           http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R libmateweather.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

Patch1:        libmateweather_0001-locations-change-weather-station-for-Rostov-on-Don-R.patch

BuildRequires: glib2-devel
BuildRequires: gtk3-devel
BuildRequires: libsoup-devel
BuildRequires: libxml2-devel
BuildRequires: mate-common

Requires:      %{name}-data = %{version}-%{release}

%description
Libraries to allow MATE Desktop to display weather information

%package data
Summary: Data files for the libmateweather
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description data
This package contains shared data needed for libmateweather.

%package devel
Summary:  Development files for libmateweather
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for libmateweather


%prep
%if 0%{?rel_build}
%autosetup -p1
%else
%autosetup -n %{name}-%{commit} -p1
%endif

%if 0%{?rel_build}
#NOCONFIGURE=1 ./autogen.sh
%else # 0%{?rel_build}
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}

%build
%configure --disable-static           \
           --disable-schemas-compile  \
           --enable-gtk-doc-html

# fix unused-direct-shlib-dependency
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool 

make %{?_smp_mflags} V=1

%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -fv {} ';'
find %{buildroot} -name '*.a' -exec rm -fv {} ';'

%find_lang %{name} --with-gnome --all-name


%files
%doc AUTHORS COPYING README
%{_datadir}/glib-2.0/schemas/org.mate.weather.gschema.xml
%{_libdir}/libmateweather.so.1*

%files data -f %{name}.lang
%{_datadir}/icons/mate/*/status/*
%{_datadir}/libmateweather/

%files devel
%%doc %{_datadir}/gtk-doc/html/libmateweather/
%{_libdir}/libmateweather.so
%{_includedir}/libmateweather/
%{_libdir}/pkgconfig/mateweather.pc


%changelog
* Sat May 04 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.0-2
- fix rhbz (#1705339)

* Mon Mar 04 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.0-1
- update to 1.22.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 07 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.2-1
- update to 1.20.2 release
- update build requires

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-1
- update to 1.20.1 release
- drop IconCache rpm scriplet

* Sat Feb 10 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.0-1
- update to 1.20 release
- drop GSettings Schema rpm scriplet
- switch to using autosetup

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.1-4
- fixing clock-applet crashes, rhbz (#1529899), (#1529897)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.1-1
- update to 1.19.1 release

* Fri May 19 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.0-1
- update to 1.19.0 release

* Tue Mar 14 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.0-1
- update to 1.18.0 release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 25 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.0-1
- update to 1.17.0 release

* Tue Nov 15 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.1-1
- update to 1.16.1 release

* Wed Sep 21 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.0-1
- update to 1.16.0 release

* Fri Sep 09 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.1-1
- update to 1.15.1 release

* Sun Sep 04 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.2-0.1.git20160831.06e0626
- update to latest git snapshot from 2016-08-31

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 09 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.0-1
- update to 1.15.0 release
- switch to gtk+3

* Tue Apr 05 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-1
- update to 1.14.0 release

* Sun Feb 07 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.0-1
- update to 1.13.0 release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 04 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.1-1
- update to 1.12.1 release

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-1
- update to 1.12.0 release

* Wed Oct 21 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.0-1
- update to 1.11.0 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-1
- update to 1.10.0 release

* Wed Feb 25 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90.1
- update to 1.9.90 release

* Fri Oct 03 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1-1
- update to 1.9.1 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Mon Feb 17 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90 release
- use --with-gnome --all-name for find locale
- enable python bindings, add BR pygtk2-devel

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Wed Dec 04 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Fri Sep 13 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-3
- add requires to -data package, fix rhbz (#1007706)

* Mon Sep 02 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-2
- disable python bindings
- add --disable-schemas-compile configure flag
- use modern make install macro
- fix unused-direct-shlib-dependency
- add LGPLv2+ license
- move huge data in /usr/share in -data subpackage

* Sat Aug 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-1
- remove BR gsettings-desktop-schemas-devel
- fix icon-cache scriptlets
- remove autogen call

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Apr 13 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Update to latest upstream release

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Update to latest release 
- Update configure flags

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- change build requires style
- remove mateconf scriplets and replace with schema scriptlets
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel
- move gtk-doc files to devel package

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-5
- fix deps, a few cosmetics

* Sat Aug 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-4
- Fix mateconf scriptlets for schemas, bump release version

* Sat Aug 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-3
- Move python files to main package, drop libs subpackage, update mateconf scriptlets, move shared library to devel package

* Sat Aug 18 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-2
- Fix directory ownership

* Sun Aug 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-1
- Initial build
