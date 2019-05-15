# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.22

# Settings used for build from snapshots.
%{!?rel_build:%global commit 838555a41dc08a870b408628f529b66e2c8c4054}
%{!?rel_build:%global commit_date 20140222}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           mate-panel
Version:        %{branch}.1
%if 0%{?rel_build}
Release:        3%{?dist}
%else
Release:        0.9%{?git_rel}%{?dist}
%endif
Summary:        MATE Desktop panel and applets
#libs are LGPLv2+ applications GPLv2+
License:        GPLv2+
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-panel.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

Source1:        mate-panel_fedora-30.layout
Source2:        mate-panel_fedora-28.layout
Source3:        mate-panel_rhel.layout

# https://github.com/mate-desktop/mate-panel/pull/816
Patch1:         mate-panel_0001-struts-Create-struts-for-panels-on-inside-edges-of-m.patch
Patch2:         mate-panel_0002-struts-Use-inside-edge-panels-only-on-Marco-and-Meta.patch
# https://github.com/mate-desktop/mate-panel/pull/958
Patch3:         mate-panel_0001-Fix-panel-applet-keyboard-focus-trap.patch

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
#for fish
# Recommends:     fortune-mod
# rhbz (#1007219)
Requires:       caja-schemas

BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk3-devel
BuildRequires:  libcanberra-devel
BuildRequires:  libmateweather-devel
BuildRequires:  libwnck3-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libSM-devel
BuildRequires:  mate-common
BuildRequires:  mate-desktop-devel
BuildRequires:  mate-menus-devel
BuildRequires:  yelp-tools

%description
MATE Desktop panel applets

%package libs
Summary:     Shared libraries for mate-panel
License:     LGPLv2+
Requires:    %{name}%{?_isa} = %{version}-%{release}

%description libs
Shared libraries for libmate-desktop

%package devel
Summary:     Development files for mate-panel
Requires:    %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development files for mate-panel

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

#libexecdir needed for gnome conflicts
%configure                                        \
           --disable-static                       \
           --disable-schemas-compile              \
           --libexecdir=%{_libexecdir}/mate-panel \
           --enable-introspection                 \
           --disable-gtk-doc                      \
           --with-in-process-applets=none

# remove unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make  %{?_smp_mflags} V=1


%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -rf {} ';'
find %{buildroot} -name '*.a' -exec rm -rf {} ';'

desktop-file-install \
        --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/mate-panel.desktop

%if 0%{?fedora} && 0%{?fedora} >= 30
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/mate-panel/layouts/fedora.layout
%endif
%if 0%{?fedora} && 0%{?fedora} == 29
install -D -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/mate-panel/layouts/fedora.layout
%endif
%if 0%{?fedora} && 0%{?fedora} == 28
install -D -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/mate-panel/layouts/fedora.layout
%endif
%if 0%{?rhel}
install -D -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/mate-panel/layouts/rhel.layout
%endif

%find_lang %{name} --with-gnome --all-name


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_mandir}/man1/*
%{_bindir}/mate-desktop-item-edit
%{_bindir}/mate-panel
%{_bindir}/mate-panel-test-applets
%{_libexecdir}/mate-panel
%{_datadir}/glib-2.0/schemas/org.mate.panel.*.xml
%{_datadir}/applications/mate-panel.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/mate-panel
%{_datadir}/dbus-1/services/org.mate.panel.applet.ClockAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.FishAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.NotificationAreaAppletFactory.service
%{_datadir}/dbus-1/services/org.mate.panel.applet.WnckletFactory.service

%files libs
%doc COPYING.LIB
%{_libdir}/libmate-panel-applet-4.so.1*
%{_libdir}/girepository-1.0/MatePanelApplet-4.0.typelib

%files devel
%doc %{_datadir}/gtk-doc/html/mate-panel-applet/
%{_libdir}/libmate-panel-applet-4.so
%{_includedir}/mate-panel-4.0
%{_libdir}/pkgconfig/libmatepanelapplet-4.0.pc
%{_datadir}/gir-1.0/MatePanelApplet-4.0.gir


%changelog
* Wed May 15 2019 Robin Edser <dev@edsies.net> - 1.22.1-3
- fix srpm build on el7 (no support for Recommends in spec)

* Thu May 09 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.1-2
- fix panel-applets keyboard focus trap

* Thu Apr 25 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.1-1
- update to 1.22.1

* Sun Apr 07 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.0-3
- really add volume-applet to fedora layout

* Mon Apr 01 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.0-2
- add volume-applet to fedora layout

* Mon Mar 04 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.0-1
- update to 1.22.0

* Mon Feb 04 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.5-1
- update to 1.20.5

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 22 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.4-1
- update to 1.20.4
- fix https://github.com/mate-desktop/mate-panel/issues/303
- partially fix for https://github.com/mate-desktop/mate-panel/issues/803
- fix https://github.com/mate-desktop/marco/issues/135

* Sun Sep 09 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.3-2
- build all applets out-of-process for gtk+-3.24

* Wed Aug 08 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.3-1
- update to 1.20.3 release
- build wnck and clock applet with-in-process, fix rhbz (#1590569)
- fix ld scriptlets in spec file

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 01 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.2-1
- update to 1.20.2

* Sun May 20 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-7
- switch back to build applets out of process

* Fri Apr 27 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-6
- update fix for https://github.com/mate-desktop/mate-panel/issues/786

* Thu Apr 19 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-5
- bump version

* Thu Apr 19 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-4
- fix https://github.com/mate-desktop/mate-panel/issues/786

* Thu Apr 19 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-3
- fix menubar if using panel auto-hide
- fix https://github.com/mate-desktop/mate-panel/issues/773
- fiz rhbz (#1493289)
- recommends  fortune-mod

* Tue Mar 27 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-1
- update to 1.20.1

* Sat Mar 03 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.20.0-4
- fixes multi-monitor-setup for HIDPI

* Mon Feb 26 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.20.0-3
- update fedora layout for f28

* Tue Feb 13 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.20.0-2
- build applets as in-process for better HDPI support
- drop IconCache rpm scriplet

* Sun Feb 11 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.20.0-1
- update to 1.20.0 release
- drop desktop-database rpm scriptlet
- drop GSettings Schema rpm scriplet
- switch to using autosetup

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.5-1
- update to  1.19.5

* Mon Jan 01 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.4-1
- update to 1.19.4

* Fri Sep 29 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.3-2
- use https://github.com/mate-desktop/mate-panel/commit/4a25da5
- use https://github.com/mate-desktop/mate-panel/commit/57d3c8f
- use https://github.com/mate-desktop/mate-panel/commit/2dbcb02
- use https://github.com/mate-desktop/mate-panel/commit/4fbe8e2
- use https://github.com/mate-desktop/mate-panel/commit/8a158fe
- use https://github.com/mate-desktop/mate-panel/commit/c13f02a
- use https://github.com/mate-desktop/mate-panel/commit/cfb9e30

* Mon Aug 14 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.3-1
- update to 1.19.3
- add upstream patch for disable SNI support

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.2-1
- update to 1.19.2
- disable gtkdoc to fix build s390x arch

* Tue Jun 27 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.1-1
- update to 1.19.1

* Wed May 24 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.0-3
- fix rhbz (#1440513) , hopefully!
- fix https://github.com/mate-desktop/mate-panel/issues/520
- fix https://github.com/mate-desktop/mate-panel/issues/570

* Tue May 16 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.0-2
- use https://github.com/mate-desktop/mate-panel/pull/575

* Thu May 11 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.0-1
- update to 1.19.0

* Tue Apr 25 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.1-2
- add some upstream patches
- properly fit expanded panel to smaller screen size
- status-notifier: Do not hide passive items
- Run dialog: Fix wrong history order
- Use new GTK bookmarks location if using GTK+-3

* Wed Apr 05 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.1-1
- update to 1.18.1

* Tue Mar 14 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.0-1
- update to 1.18.0 release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.1-1
- update to 1.17.1 release

* Sat Dec 10 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.0-2
- remove dependency to mate-session-manager

* Sat Dec 03 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.0-1
- update to 1.17.0 release
- build with --with-in-process-applets=none

* Thu Oct 20 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.0-2
- fix for clock-applet
- https://github.com/mate-desktop/mate-panel/issues/491

* Thu Sep 22 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.0-1
- update to 1.16.0 release

* Fri Sep 02 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.1-1
- update to 1.15.1 release

* Mon Aug 08 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.0-2
- Remove popup-menu for items in applications menu,
- does not really work without freezing the menu with gtk3
- https://github.com/mate-desktop/mate-panel/issues/305

* Thu Jun 09 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.0-1
- update to 1.15.0 release
- switch to gtk+3

* Sat May 21 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-2
- upstream fix for rhbz (#1238820) and (#1279101)

* Tue Apr 05 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-1
- update to 1.14.0 release

* Sun Mar 27 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.2-1
- update to 1.13.2 release

* Mon Feb 22 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.1-1
- 1.13.1 release

* Sun Feb 07 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.0-1
- update to 1.13.0 release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 04 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> 1.12.1-1
- update to 1.12.1 release

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-1
- update to 1.12.0 release

* Tue Oct 27 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.1-1
- update to 1.11.1 release

* Wed Oct 21 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.0-1
- update to 1.11.0 release
- disable patch for initial-setup

* Sat Jul 11 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1-1
- update to 1.10.1 release
- remove upstreamed patches

* Fri Jul 03 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-5
- use complete old help from 1.8
- fix drawer applet
- fix kill applet (gtk3)
- some more upstream patches

* Sun Jun 28 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-4
- add help from 1.8.x

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-2
- add upstream patch
- clean fedora panel layout
- remove unrecognized options --enable-network-manager
- remove libnm-gtk BR

* Tue May 05 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-1
- update to 1.10.0-1 release

* Thu Apr 09 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.91-1
- update to 1.9.91-1 release
- remove upstreamed patches

* Wed Mar 18 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1-9.90-2
- fix rhbz (#1192722)

* Mon Mar 02 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90-1
- update to 1.9.90 release

* Mon Dec 08 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.4.1
- update to 1.9.4

* Sun Nov 23 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.3-2
- fix rhbz (#1023604)
- timezone fix

* Sun Nov 23 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.3-1
- update to 1.9.3 release

* Tue Nov 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.2-1
- update to 1.9.2 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 07 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1-2
- update default panel layout

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1-1
- update to 1.9.1 release
- remove patch already in release

* Wed Jun 25 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0.3
- try fix rhbz (#1023604)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Sat Feb 22 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.91-0.1.git20140222.838555a
- update to git snapshot from 2014.02.22
- use new panel layout file

* Tue Feb 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90
- add --enable-gtk-doc configure flag
- move autoreconf to the right place

* Thu Feb 13 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-2
- Add autoreconf -fi to work around rpath.

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Tue Jan 14 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1 release
- use gtk-docs for release build
- remove obsolete BR --disable-scrollkeeper

* Sat Dec 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.2.git20131212.f4c7c8f
- make Maintainers life easier and use better git snapshot usage, Thanks to Björn Esser
- use requires caja-schemas
- use isa tag for -libs subpackage
- use modern 'make install' macro
- fix usage of %%{buildroot} or $RPM_BUILD_ROOT
- use better macro for SOURCE1
- move rpm scriptlets for -libs subpackage to the right place
- fix unused-direct-shlib-dependency rpmlint warning
- move %%{_libdir}/girepository-1.0/MatePanelApplet-4.0.typelib to -libs subpackage
- improve find language command for yelp-tools

* Thu Dec 12 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.1.gitbeb21bb
- update to latest git snapshot
- fix refer to cairo-gobject, noticed by M.Schwendt
- fix usage of wrong git snapshot tarball, 1.7.0 is released!
- no need of calling autotools when using autogen.sh

* Fri Dec 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1.1.gitd2a24b9
- Update to 1.7.0
- Use latest upstream git as released version fails to build with gtk2

* Thu Sep 12 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-4
- add runtime require mate-file-manager-schemas, fix rhbz (#1007219)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-2
- update panel-default-layout.dist for caja-1.6.2

* Thu Jul 18 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- update to 1.6.1
- add upstream patch to fix partially
- https://github.com/mate-desktop/mate-panel/issues/111
- remove needless BR gsettings-desktop-schemas-devel

* Sat Jun 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-3
- remove gsettings convert file

* Fri May 31 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-2
- set default panel layout, add panel-default-layout.dist file
- add requires hicolor-icon-theme

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Wed Mar 27 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.6-2
- Remove ---with-in-process-applets configure flag as per upstream advice

* Tue Mar 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.6-1
- Update to latest upstream release

* Fri Feb 08 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.5-1
-Update to latest upstream release

* Sun Jan 20 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.4-1
- Update to latest upstream release
- Convert back to old BR style and sort BRs

* Fri Dec 21 2012 Nelson Marques <nmarques@fedoraproject.org> - 1.5.3-1
- Update to version 1.5.3
- Remove deprecated patches
- Improved readability without harming current style

* Tue Dec 18 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.5.2-5
- Fix crash on panel delete

* Tue Nov 27 2012 Rex Dieter <rdieter@fedoraproject.org> 1.5.2-4
- fix -libs subpkg, %%doc COPYING.LIB
- spec cleanup (whitespace mostly)
- fix icon scriptlet

* Mon Nov 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-2
- Move libmate-panel-applet-4.so to separate libs package as mate-power-manager depends on it

* Thu Nov 22 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2 release

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-1
- update to 1.5.1 release
- add schema scriptlets and remove mateconf scriptlets
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel and dconf-devel
- move .gir file to devel package
- clean up spec file
- patch for new dconf api

* Mon Oct 22 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-12
- Remove un-needed %%check section

* Mon Oct 22 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-11
- add requires mate-session-manager
- change style for build requirements

* Wed Oct 10 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-10
- remove ugly hack
- set panel-default-setup.entries

* Sun Oct 07 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-9
- Change %%define to %%global
- Tidy up schema scriplets
- Tidy up %%build section

* Sun Oct 07 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-8
- Add ugly hack for panel-default-setup.entries

* Sat Oct 06 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-7
- Add enable-introspection and --with-x to configure flags
- Update desktop-file-install macro
- Update BR
- Turn desktop-file-validate back on
- Add fortune-mod to requires for fish to work properly.

* Wed Oct 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-6
- Add posttrans scriptlet to update icon cache and fix ordering of scriptlets
- Add comment about licensing

* Wed Oct 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-5
- Fix typo for netowrkmanager devel package on f18

* Tue Oct 02 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-4
- Fix directory ownership, fix libexec configure flag
- Fix schema installation.. totally off

* Tue Oct 02 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Fix buildrequires for networkmanager rename in f18 as per juhp

* Wed Sep 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Fix mateconf scriptlets

* Sat Sep 01 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
-Initial build
