Summary:	Graphical OpenGL version of traceroute
Name:		xtraceroute
Version:	0.9.2
Release:	%mkrel 5
License:	GPLv2+
Group:		Monitoring
Source0:	http://www.beebgames.com/sw/%{name}-%{version}.tar.bz2
Source10:	%{name}.16.png
Source11:	%{name}.32.png
Source12:	%{name}.48.png
URL:		http://www.beebgames.com/sw/gtk-ports.html
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	gtkglarea2-devel
BuildRequires:	Mesa-common-devel
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
sed -i -e 's,%{name}.png,%{name},g' %{name}.desktop

# otherwise autoreconf doesn't work - AdamW 2008/01
cp %{_datadir}/gettext/config.rpath .

autoreconf

%build
%configure2_5x
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/pixmaps
%makeinstall xtraceroutedatadir=%{?buildroot:%{buildroot}}%{_datadir}/%{name}

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

%find_lang %{name}

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README TODO
%{_bindir}/*
%{_datadir}/xtraceroute
%{_datadir}/pixmaps/xtraceroute.png
%{_mandir}/*/*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
