%define _disable_rebuild_configure 1

Summary:	Graphical OpenGL version of traceroute
Name:		xtraceroute
Version:	0.9.2
Release:	23
License:	GPLv2+
Group:		Monitoring
Source0:	http://www.beebgames.com/sw/%{name}-%{version}.tar.bz2
Source10:	%{name}.16.png
Source11:	%{name}.32.png
Source12:	%{name}.48.png
Patch0:		xtraceroute-0.9.2-linkage.patch
Patch1:		xtraceroute-0.9.2-fix-build.patch
Patch2:		xtraceroute-automake-1.13.patch
URL:		https://www.beebgames.com/sw/gtk-ports.html
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
%configure
%make_build

%install
mkdir -p %{buildroot}/%{_datadir}/pixmaps
%make_install

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
%doc %{_mandir}/*/*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
