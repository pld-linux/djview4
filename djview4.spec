#
# Conditional build:
%bcond_with	qt5	# Qt 5 instead of Qt 4
#
Summary:	DjVu viewer based on Qt 4+
Summary(hu.UTF-8):	DjVu nézegető Qt 4+ alapon
Summary(pl.UTF-8):	Przeglądarka DjVu oparta na Qt 4+
Name:		djview4
Version:	4.10.5
Release:	1
License:	GPL v2+
Group:		X11/Applications/Graphics
Source0:	http://downloads.sourceforge.net/djvu/djview-%{version}.tar.gz
# Source0-md5:	ae6c5b9b7292558d024eb21e8769bd03
Patch0:		%{name}-opt.patch
Patch2:		%{name}-link.patch
URL:		http://djvu.sourceforge.net/
BuildRequires:	autoconf >= 2.67
BuildRequires:	automake >= 1.6
BuildRequires:	djvulibre-devel >= 3.5.19
# rsvg tool
BuildRequires:	librsvg
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool >= 2:2.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	xorg-lib-libX11-devel
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Network-devel >= 5
BuildRequires:	Qt5OpenGL-devel >= 5
BuildRequires:	Qt5PrintSupport-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-linguist >= 5
BuildRequires:	qt5-qmake >= 5
%else
BuildRequires:	QtCore-devel >= 4.4
BuildRequires:	QtGui-devel >= 4.4
BuildRequires:	QtNetwork-devel >= 4.4
BuildRequires:	QtOpenGL-devel >= 4.4
BuildRequires:	qt4-build >= 4.4
BuildRequires:	qt4-linguist >= 4.4
BuildRequires:	qt4-qmake >= 4.4
%endif
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
%if %{without qt5}
Requires:	QtGui >= 4.4
Requires:	QtNetwork >= 4.4
Requires:	QtOpenGL >= 4.4
%endif
Requires:	djvulibre >= 3.5.19
Requires:	hicolor-icon-theme
Obsoletes:	djvulibre-djview
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DjView4 is a viewer and browser plugin for DjVu documents, based on
the DjVuLibre-3.5 library and the Qt 4+ toolkit.

%description -l hu.UTF-8
DjView4 egy nézegető és böngésző plugin DjVu dokumentumokhoz, a
DjVuLibre-3.5 könyvtárra és a Qt 4+ készletre épülve.

%description -l pl.UTF-8
DjView4 to przeglądarka i wtyczka dla przeglądarek do oglądania
dokumentów DjVu, oparta na bibliotece DjVuLibre-3.5 i toolkicie Qt 4+.

%package -n browser-plugin-%{name}
Summary:	DjView4 browser plugin
Summary(hu.UTF-8):	DjView4 böngésző plugin
Summary(pl.UTF-8):	Wtyczka DjView4 do przegląderek WWW
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
# for migrate purposes (greedy poldek upgrade)
Provides:	browser-plugin-djvulibre
Provides:	mozilla-plugin-djvulibre
Provides:	netscape-plugin-djvulibre
Obsoletes:	browser-plugin-djvulibre
Obsoletes:	djview-netscape
Obsoletes:	mozilla-plugin-djvulibre
Obsoletes:	netscape-plugin-djvulibre

%description -n browser-plugin-%{name}
DjView4 plugin for Mozilla and Mozilla-based browsers.

%description -n browser-plugin-%{name} -l hu.UTF-8
DjView4 plugin Mozilla és Mozilla-alapú böngészőkhöz.

%description -n browser-plugin-%{name} -l pl.UTF-8
Wtyczka DjView4 do przeglądarek zgodnych z Mozillą.

%prep
%setup -q -n djview-%{version}
%patch0 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%if %{with qt5}
export QTDIR=%{_libdir}/qt5
%else
export QTDIR=%{_libdir}/qt4
%endif
%configure \
	--disable-silent-rules
# --enable-npdjvu - new experimental plugin?

%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_browserpluginsdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pluginsdir=%{_browserpluginsdir}

%{__rm} $RPM_BUILD_ROOT%{_browserpluginsdir}/nsdejavu.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_icon_cache hicolor

%postun
%update_desktop_database_postun
%update_icon_cache hicolor

%post -n browser-plugin-%{name}
%update_browser_plugins

%postun -n browser-plugin-%{name}
if [ "$1" = "0" ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc COPYRIGHT NEWS README
%attr(755,root,root) %{_bindir}/djview
%{_mandir}/man1/djview.1*
%dir %{_datadir}/djvu/djview4
%lang(cs) %{_datadir}/djvu/djview4/djview_cs.qm
%lang(de) %{_datadir}/djvu/djview4/djview_de.qm
%lang(es) %{_datadir}/djvu/djview4/djview_es.qm
%lang(fr) %{_datadir}/djvu/djview4/djview_fr.qm
%lang(ru) %{_datadir}/djvu/djview4/djview_ru.qm
%lang(uk) %{_datadir}/djvu/djview4/djview_uk.qm
%lang(zh_CN) %{_datadir}/djvu/djview4/djview_zh_cn.qm
%lang(zh_TW) %{_datadir}/djvu/djview4/djview_zh_tw.qm
%{_desktopdir}/djvulibre-djview4.desktop
%{_iconsdir}/hicolor/*x*/mimetypes/djvulibre-djview4.png
%{_iconsdir}/hicolor/scalable/mimetypes/djvulibre-djview4.svgz

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/nsdejavu.so
%{_mandir}/man1/nsdejavu.1*
