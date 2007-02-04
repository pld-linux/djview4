Summary:	DjVu viewer based on Qt4
Summary(pl):	Przegl±darka DjVu oparta na Qt4
Name:		djview4
Version:	4.0
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/djvu/%{name}-%{version}.tar.gz
# Source0-md5:	1952637bfd96cb605e24de3f32e8cda7
Patch0:		%{name}-opt.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-link.patch
URL:		http://djvu.sourceforge.net/
BuildRequires:	QtGui-devel >= 4.0
BuildRequires:	QtNetwork-devel >= 4.0
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	djvulibre-devel >= 3.5.17
BuildRequires:	libstdc++-devel
BuildRequires:	qt4-build >= 4.0
BuildRequires:	qt4-qmake >= 4.0
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	xorg-lib-libXt-devel
Obsoletes:	djvulibre-djview
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DjView4 is a viewer and browser plugin for DjVu documents, based on
the DjVuLibre-3.5 library and the Qt4 toolkit.

%description -l pl
DjView4 to przegl±darka i wtyczka dla przegl±darek do ogl±dania
dokumentów DjVu, oparta na bibliotece DjVuLibre-3.5 i toolkicie Qt4.

%package -n browser-plugin-%{name}
Summary:	DjView4 browser plugin
Summary(pl):	Wtyczka DjView4 do przegl±derek WWW
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
# for migrate purposes (greedy poldek upgrade)
Provides:	browser-plugin-djvulibre
Provides:	mozilla-plugin-djvulibre
Provides:	netscape-plugin-djvulibre
Obsoletes:	djview-netscape
Obsoletes:	browser-plugion-djvulibre
Obsoletes:	mozilla-plugin-djvulibre
Obsoletes:	netscape-plugin-djvulibre

%description -n browser-plugin-%{name}
DjView4 plugin for Mozilla and Mozilla-based browsers.

%description -n browser-plugin-%{name} -l pl
Wtyczka DjView4 do przegl±darek zgodnych z Mozill±.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp -f /usr/share/automake/config.sub config
%{__aclocal} -I config
%{__autoconf}
export QTDIR=%{_libdir}/qt4
%configure

%{__make} \
	CXX="%{__cxx}" \
	LFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_browserpluginsdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	plugindir=%{_browserpluginsdir}

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/djview.1
echo '.so djview4.1' > $RPM_BUILD_ROOT%{_mandir}/man1/djview.1

%clean
rm -rf $RPM_BUILD_ROOT

%post -n browser-plugin-%{name}
%update_browser_plugins

%postun -n browser-plugin-%{name}
if [ "$1" = "0" ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc COPYRIGHT NEWS README TODO
%attr(755,root,root) %{_bindir}/djview
%attr(755,root,root) %{_bindir}/djview4
%{_mandir}/man1/djview.1*
%{_mandir}/man1/djview4.1*
%dir %{_datadir}/djvu/djview4
%lang(fr) %{_datadir}/djvu/djview4/djview_fr.qm
%{_desktopdir}/djvulibre-djview4.desktop
%{_iconsdir}/hicolor/32x32/apps/djvulibre-djview4.png

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/nsdejavu.so
%{_mandir}/man1/nsdejavu.1*
