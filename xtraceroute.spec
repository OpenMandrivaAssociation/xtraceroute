%define name xtraceroute
%define version 0.9.2
%define prefix %{_prefix}

Summary: Graphical OpenGL version of traceroute
Name: %{name}
Version: %{version}
Release: %mkrel 4
License: GPL
Group: Monitoring
Source0: http://www.beebgames.com/sw/%{name}-%{version}.tar.bz2
Source10: %{name}.16.png
Source11: %{name}.32.png
Source12: %{name}.48.png
URL: http://www.beebgames.com/sw/gtk-ports.html
BuildRequires: autoconf2.5
BuildRequires: libgdk_pixbuf2.0-devel
BuildRequires: gtkglarea2-devel
BuildRequires: Mesa-common-devel traceroute
BuildRequires: /usr/bin/host
BuildRequires: recode
BuildRequires: gettext-devel
BuildRequires: desktop-file-utils
Requires: traceroute /usr/bin/host

%description
Xtraceroute is a graphical traceroute utility that shows the path your IP
packets travel on a 3 dimensional rendered globe. Be sure to download the NDG
data files mentioned in the INSTALL document too.

%prep
%setup -q
autoreconf

%build
%configure2_5x
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/pixmaps
%makeinstall xtraceroutedatadir=%{?buildroot:%{buildroot}}%{_datadir}/%{name}

install xtraceroute.png $RPM_BUILD_ROOT%{_datadir}/pixmaps
touch $RPM_BUILD_ROOT%{_datadir}/xtraceroute/hosts.cache
touch $RPM_BUILD_ROOT%{_datadir}/xtraceroute/site_hosts.cache
touch $RPM_BUILD_ROOT%{_datadir}/xtraceroute/site_networks.cache

mv $RPM_BUILD_ROOT/%{_bindir}/%{name} $RPM_BUILD_ROOT/%{_bindir}/%{name}.real
cat > $RPM_BUILD_ROOT/%{_bindir}/%{name} << EOF
#!/bin/sh
if [ ! -d \$HOME/.xt ]; then
		mkdir \$HOME/.xt
fi
%{_bindir}/%{name}.real "\$@"
EOF
chmod a+x $RPM_BUILD_ROOT/%{_bindir}/%{name}

# icon
install -d $RPM_BUILD_ROOT/%{_miconsdir}
install -d $RPM_BUILD_ROOT/%{_liconsdir}
install %{SOURCE10} $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
install %{SOURCE11} $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
install %{SOURCE12} $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png

recode ISO-8859-15..UTF-8 %{name}.desktop

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="System" \
  --add-category="Monitor" \
  --add-category="X-MandrivaLinux-System-Monitoring" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications %{name}.desktop

%find_lang %{name}

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING TODO
%{_bindir}/*
%{_datadir}/xtraceroute
%{_datadir}/pixmaps/xtraceroute.png
%{_mandir}/*/*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png


