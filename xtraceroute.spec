%define debug_package %{nil}

Summary:	Graphical OpenGL version of traceroute
Name:		xtraceroute
Version:	0.9.2
Release:	16
License:	GPLv2+
Group:		Monitoring
Source0:	http://www.beebgames.com/sw/%{name}-%{version}.tar.bz2
Source10:	%{name}.16.png
Source11:	%{name}.32.png
Source12:	%{name}.48.png
Patch0:		xtraceroute-0.9.2-linkage.patch
Patch1:		xtraceroute-0.9.2-fix-build.patch
Patch2:		xtraceroute-automake-1.13.patch
URL:		http://www.beebgames.com/sw/gtk-ports.html
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gtkgl-2.0)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	traceroute
BuildRequires:	bind-utils
BuildRequires:	recode
BuildRequires:	gettext-devel
BuildRequires:	desktop-file-utils
Requires:	traceroute
Requires:	bind-utils

%description
Xtraceroute is a graphical traceroute utility that shows the path your IP
packets travel on a 3 dimensional rendered globe. Be sure to download the NDG
data files mentioned in the INSTALL document too.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1 -b .am13~
sed -i -e 's,%{name}.png,%{name},g' %{name}.desktop

# otherwise autoreconf doesn't work - AdamW 2008/01
cp %{_datadir}/gettext/config.rpath .

%build
autoreconf -fi
%configure2_5x
%make

%install
mkdir -p %{buildroot}/%{_datadir}/pixmaps
%makeinstall_std

install xtraceroute.png %{buildroot}%{_datadir}/pixmaps
touch %{buildroot}%{_datadir}/xtraceroute/hosts.cache
touch %{buildroot}%{_datadir}/xtraceroute/site_hosts.cache
touch %{buildroot}%{_datadir}/xtraceroute/site_networks.cache

mv %{buildroot}/%{_bindir}/%{name} %{buildroot}/%{_bindir}/%{name}.real
cat > %{buildroot}/%{_bindir}/%{name} << EOF
#!/bin/sh
if [ ! -d \$HOME/.xt ]; then
		mkdir \$HOME/.xt
fi
%{_bindir}/%{name}.real "\$@"
EOF
chmod a+x %{buildroot}/%{_bindir}/%{name}

# icon
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install %{SOURCE10} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install %{SOURCE11} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install %{SOURCE12} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

recode ISO-8859-15..UTF-8 %{name}.desktop

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="System" \
  --add-category="Monitor" \
  --dir %{buildroot}%{_datadir}/applications %{name}.desktop

%files
%doc AUTHORS ChangeLog NEWS README TODO
%{_bindir}/*
%{_datadir}/xtraceroute
%{_datadir}/pixmaps/xtraceroute.png
%{_mandir}/*/*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png


%changelog
* Sat May 07 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-9mdv2011.0
+ Revision: 671372
- mass rebuild

* Sat Dec 04 2010 Funda Wang <fwang@mandriva.org> 0.9.2-8mdv2011.0
+ Revision: 609505
- fix build

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-7mdv2010.1
+ Revision: 524473
- rebuilt for 2010.1

* Mon Apr 13 2009 Funda Wang <fwang@mandriva.org> 0.9.2-6mdv2009.1
+ Revision: 366737
- fix linkage

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 0.9.2-5mdv2009.0
+ Revision: 218427
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sun Jan 13 2008 Adam Williamson <awilliamson@mandriva.org> 0.9.2-5mdv2008.1
+ Revision: 151073
- rebuild for new era
- fix .desktop file (no icon extension)
- replace file-based buildrequires / requires with package-based
- copy config.rpath from gettext into topdir before running autoreconf or else it fails
- fd.o icons
- new license policy
- spec clean

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Thu Jan 18 2007 Olivier Blin <oblin@mandriva.com> 0.9.2-4mdv2007.0
+ Revision: 110134
- drop unused icon (and fix upload, #28272)
- bunzip2 png files
- remove old menu
- remove unneeded perl requires

* Thu Nov 02 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.9.2-3mdv2007.1
+ Revision: 75965
- add BuildRequires: gettext-devel desktop-file-utils
- Import xtraceroute

* Fri Sep 08 2006 Olivier Blin <blino@n4.mandriva.com> 0.9.2-2mdv2007.0
- use UTF-8 encoding for the desktop file (#25084)

* Sat Aug 05 2006 Olivier Thauvin <nanardon@mandriva.org> 0.9.2-1mdv2007.0
- from Cris Boylan <crisuk@yahoo.com>:
  - 0.9.2

* Sat Jul 08 2006 Olivier Blin <oblin@mandriva.com> 0.9.1-14mdv2007.0
- from Cris Boylan <crisuk@yahoo.com>:
  o gtk2 port (#23570)
  o use gtk2 BuildRequires
- split gtk2 port diff as Patch0
- add XDG menu

* Sat Sep 10 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.9.1-13mdk
- menudir

* Fri Nov 19 2004 Olivier Blin <blino@mandrake.org> 0.9.1-12mdk
- birthday rebuild

