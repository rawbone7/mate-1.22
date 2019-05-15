# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.22

# Settings used for build from snapshots.
%{!?rel_build:%global commit af58c2ecd98fe68360635f0e566b81e4b8c7be4d}
%{!?rel_build:%global commit_date 20151006}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:           mate-session-manager
Summary:        MATE Desktop session manager
License:        GPLv2+
Version:        %{branch}.1
%if 0%{?rel_build}
Release:        1%{?dist}
%else
Release:        0.12%{?git_rel}%{?dist}
%endif
URL:            http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-session-manager.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk3-devel
BuildRequires:  libSM-devel
BuildRequires:  mate-common
BuildRequires:  pangox-compat-devel
BuildRequires:  systemd-devel
BuildRequires:  xmlto
BuildRequires:  libXtst-devel
BuildRequires:  xorg-x11-xtrans-devel

Requires: system-logos
# Needed for mate-settings-daemon
Requires: mate-control-center
# we need an authentication agent in the session
Requires: mate-polkit
# and we want good defaults
Requires: polkit-desktop-policy
# for gsettings shemas
Requires: mate-desktop-libs
# for /bin/dbus-launch
Requires: dbus-x11

%description
This package contains a session that can be started from a display
manager such as MDM. It will load all necessary applications for a
full-featured user session.

%prep
%if 0%{?rel_build}
%autosetup -p1
%else
%autosetup -n %{name}-%{commit} -p1
%endif

%if 0%{?rel_build}
# for releases
#NOCONFIGURE=1 ./autogen.sh
%else
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif

%build
%configure                    \
    --disable-static          \
    --enable-ipv6             \
    --with-default-wm=marco   \
    --with-systemd            \
    --enable-docbook-docs     \
    --disable-schemas-compile

make %{?_smp_mflags} V=1

%install
%{make_install}

desktop-file-install                               \
        --delete-original                          \
        --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/mate-session-properties.desktop

%find_lang %{name} --with-gnome --all-name


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_mandir}/man1/*
%{_bindir}/mate-session
%{_bindir}/mate-session-inhibit
%{_bindir}/mate-session-properties
%{_bindir}/mate-session-save
%{_bindir}/mate-wm
%{_datadir}/applications/mate-session-properties.desktop
%{_datadir}/mate-session-manager
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/mate-session-properties.svg
%{_datadir}/glib-2.0/schemas/org.mate.session.gschema.xml
%{_datadir}/xsessions/mate.desktop
%if 0%{?fedora} > 22 || 0%{?rhel}
%{_docdir}/mate-session-manager/dbus/mate-session.html
%endif


%changelog
* Thu Apr 25 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.1-1
- update to 1.22.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 24 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.2-1
- update to 1.20.2 release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.20.1-1
- update to 1.20.1 release

* Sun Feb 11 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.20.0-1
- update to 1.20.0 release
- drop GSettings Schema rpm scriplet
- drop BR tcp_wrappers-devel

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 27 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.1-1
- update to 1.19.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.0-1
- update to 1.19.0

* Sun May 07 2017 Björn Esser <besser82@fedoraproject.org> - 1.18.0-5
- Updated patch to update environment for dbus and systemd user-session

* Sun May 07 2017 Björn Esser <besser82@fedoraproject.org> - 1.18.0-4
- Updated patch to update environment for dbus and systemd user-session

* Sun May 07 2017 Björn Esser <besser82@fedoraproject.org> - 1.18.0-3
- Add Requires: dbus-x11

* Sun May 07 2017 Björn Esser <besser82@fedoraproject.org> - 1.18.0-2
- Add patch to update environment for dbus and systemd user-session

* Tue Mar 14 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.0-1
- update to 1.18.0 release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.1-1
- update to 1.17.1 release

* Mon Jan 09 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.0-1
- update to 1.17.0 release

* Fri Dec 23 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.0-2
- fix resizing the startup applications preferences window
- https://github.com/mate-desktop/mate-session-manager/commit/d8da9ef

* Thu Sep 22 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.0-1
- update to 1.16.0 release

* Wed Aug 03 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.0-2
- fix for rhbz (#1354191)

* Thu Jun 09 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.0-1
- update to 1.15.0 release

* Tue Apr 05 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-1
- update to 1.14.0 release

* Sun Feb 07 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.0-1
- update to 1.13.0 release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 04 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> 1.12.1-1
- update to 1.12.1 release
- remove upstreamed patch

* Sat Nov 21 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-2
- get rid of dependency to mate-desktop
- build with gtk3

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-1
- update to 1.12.0 release

* Wed Oct 21 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.0-1
- update to 1.11.0 release

* Thu Sep 03 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2-2
- add upstream patch to disable overlay-scrollbars in mate-session

* Tue Jul 14 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2.1
- update to 1.10.2 release

* Fri Jun 19 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1.3
- set XDG_CURRENT_DESKTOP to MATE

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1.1
- update to 1.10.1 release
- removed upstreamed patches

* Tue Apr 07 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-1
- update to 1.10.0 release

* Wed Apr 01 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90-2
- fix user switching if more than 2 desktop managers are installed

* Thu Feb 26 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90-1
- update to 1.9.90 release

* Sun Nov 23 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.3-1
- update to 1.9.3 release

* Tue Nov 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.2-1
- update to 1.9.2 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1-1
- update to 1.9.1 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-1
- update to 1.8.1 release

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Tue Feb 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Thu Jan 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1
- use modern 'make install' macro
- removed upstreamed patches
- add --with-gnome --all-name for find language
- use pangox-compat-devel BR
- re-worked configure flags
- cleanup spec file

* Thu Dec 05 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Sat Nov 02 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-6
- make suspend/hibernate button work without upower

* Thu Oct 31 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-5
- disable upower support for > f20, upower-1.0 is landed

* Wed Oct 16 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-4
- switch to gnome-keyring for > f19
- add mate-session-manager_systemd-session_id.patch

* Tue Sep 10 2013 Rex Dieter <rdieter@fedoraproject.org> 1.6.1-3
- initial attempt at systemd-login1 suspend/hibernate support

* Fri Jul 26 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- drop comment out patch from spec file
- remove unnecessary BRs
- add pangox-compat-devel instead as pango-devel as BR
- add BR libXtst-devel
- add BR xorg-x11-xtrans-devel
- add BR tcp_wrappers-devel
- remove NOCONFIGURE=1 ./autogen.sh
- add some runtime requires
- remove needless gsettings convert file
- change doc dir for f20
- fix file section for 1.6.1 release

* Mon Jun 17 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-4
- Drop the caja patch
- Build against latest systemd
- Disable building docbook docs
- Clean up BRs

* Thu May 23 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-3
- Add patch for caja race condition

* Tue May 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-2
- Add systemd-devel to BR and enable systemd support
- Build docbook docs
- Own mate-session doc dir

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Fri Feb 22 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Update to latest upstream release
- Convert to old BR style

* Mon Feb 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-3
- Fix ten caja windows on login

* Fri Dec 21 2012 Nelson Marques <nmarques@fedoraproject.org> - 1.5.0-2
- Add mate-session-manager-1.5.0-fix_schema.patch: fix segfault preventing
  hibernation/suspend - BZ#888184
- Add missing dependency for pangox-devel
- Improved spec for readability

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel
- remove the desktop validate for the xsession file
- change build requires style

* Wed Oct 17 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-9
- Add mate.desktop to desktop-file-install

* Tue Oct 16 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-8
- Add MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 to install section

* Tue Oct 16 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-7
- Fix configure flags
- Remove no replace macro from schemas

* Sun Oct 07 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-6
- Remove kdm

* Sat Oct 06 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-5
- Add kdm to the requires field. mate-session-manager has no dm builtin yet

* Tue Oct 02 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-4
- Update post/postun/poststrans scriptlets to match files section for hicolor
- Update licensing to GPLv2+ only

* Sat Sep 29 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-3
- Fix buildrequires/requires field

* Wed Sep 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-2
- Fix mateconf scriptlets

* Thu Jul 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.0-1
-Initial build
