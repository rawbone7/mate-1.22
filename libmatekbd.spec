# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.22

# Settings used for build from snapshots.
%{!?rel_build:%global commit 5e8b69cf7c6d031cbb0b0f01a7518e72146c0af1}
%{!?rel_build:%global commit_date 20151009}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           libmatekbd
Version:        %{branch}.0
%if 0%{?rel_build}
Release:        1%{?dist}
%else
Release:        0.9%{?git_rel}%{?dist}
%endif
Summary:        Libraries for mate kbd
License:        LGPLv2+
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R libmatekbd.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:  desktop-file-utils
BuildRequires:  gsettings-desktop-schemas-devel
BuildRequires:  gtk3-devel
BuildRequires:  libICE-devel
BuildRequires:  libxklavier-devel
BuildRequires:  mate-common
BuildRequires:  gobject-introspection-devel

%description
Libraries for matekbd

%package devel
Summary:  Development libraries for libmatekbd
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries for libmatekbd

%prep
%if 0%{?rel_build}
%autosetup -p1
%else
%autosetup -n %{name}-%{commit} -p1
%endif

%if 0%{?rel_build}
#NOCONFIGURE=1 ./autogen.sh
%else # 0%{?rel_build}
# for snapshots
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}

%build

%configure                   \
   --disable-static          \
   --disable-schemas-compile \
   --with-x                  \
   --enable-introspection=yes
  
make %{?_smp_mflags} V=1


%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -fv {} ';'

%find_lang %{name} --with-gnome --all-name


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_datadir}/libmatekbd
%{_datadir}/glib-2.0/schemas/org.mate.peripherals-keyboard-xkb.gschema.xml
%{_libdir}/libmatekbd.so.4*
%{_libdir}/libmatekbdui.so.4*
%{_libdir}/girepository-1.0/Matekbd-1.0.typelib
%{_datadir}/gir-1.0/Matekbd-1.0.gir

%files devel
%{_includedir}/libmatekbd
%{_libdir}/pkgconfig/libmatekbd.pc
%{_libdir}/pkgconfig/libmatekbdui.pc
%{_libdir}/libmatekbdui.so
%{_libdir}/libmatekbd.so


%changelog
* Mon Mar 04 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.0-1
- update to 1.22.0

* Wed Feb 06 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.20.2-4
- Fix F30 FTBFS

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.2-1
- update to 1.20.2

* Tue Mar 27 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-1
- update to 1.20.1

* Sat Feb 10 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.0-1
- update to 1.20.0
- drop GSettings Schema rpm scriplet
- switch to using autosetup

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 01 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.1-1
- update to 1.19.1

* Sat Sep 02 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.0-1
- update to 1.19.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr 10 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.2.1
- update to 1.18.2

* Thu Apr 06 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.1-1
- update to 1.18.1 release

* Tue Mar 14 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.0-1
- update to 1.18.0 release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 03 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.0-1
- update to 1.17.0 release

* Wed Sep 21 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.0-1
- update to 1.16.0 release

* Thu Jun 09 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.0-1
- update to 1.15.0 release
- switch to gtk+3

* Sat May 21 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.1-1
- update to 1.14.1 release
- translations update

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
- remove upstreamed patches

* Wed Feb 25 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90.1
- update to 1.9.90 release
- fix gsettings with glib-2.43

* Tue Jan 13 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.2.1
- update to 1.9.2 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1.1
- update to 1.9.1 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Sun Feb 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90 release

* Thu Feb 13 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-2
- Add autoreconf to workaround rpath issue
- Sort BRs

* Sat Jan 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.2-1
- update to 1.7.2
- use modern 'make install' macro
- remove needless gsettings convert file
- use --with-gnome --all-name for find locale
- add BR libICE-devel
- fix ld scriptlets

* Wed Dec 04 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Update to latest upstream release.

* Sat Jun 22 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-2
- Add upstream commits patch for various bugfixes

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Fri Feb 08 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
-Update to latest upstream release
-Update BR's
-Own dirs we are supposed to own
-Update configure flags

* Mon Dec 10 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-2
- Rebuild for ARM

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- change build requires style
- remove mateconf scriplets and replace with schema scriptlets
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel

* Wed Sep 26 2012 Dan Mashal <dan.mashal@fedoraproject.org>  1.4.0-6
- Remove onlyshowin from desktop-fileinstall  and mateconf_obsolete macro
- Fix date on previous changelog (I was tired, sorry).

* Mon Sep 24 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-5
- Update desktop-file-install and fix mate-conf scriptlets

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-4
- License: LGPLv2+, %%doc COPYING.LIB
- dir ownership
- don't use undefined %%{po_package} macro
- s|MATE|X-MATE| only on < f18

* Sun Aug 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Remove obsolete scriptlet from pre macro, correct schema scriptlets for mateconf and bump release version

* Sat Aug 25 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Drop libs package add scriptlets for schemas

* Sun Aug 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build
