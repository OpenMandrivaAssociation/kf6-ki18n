%define major %(echo %{version} |cut -d. -f1-2)
%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)

%define libname %mklibname KF6I18n
%define devname %mklibname KF6I18n -d
#define git 20240217

Name: kf6-ki18n
Version: 6.15.0
Release: %{?git:0.%{git}.}1
%if 0%{?git:1}
Source0: https://invent.kde.org/frameworks/ki18n/-/archive/master/ki18n-master.tar.bz2#/ki18n-%{git}.tar.bz2
%else
Source0: http://download.kde.org/%{stable}/frameworks/%{major}/ki18n-%{version}.tar.xz
%endif
Summary: KDE libraries for internationalization
URL: https://invent.kde.org/frameworks/ki18n
License: CC0-1.0 LGPL-2.0+ LGPL-2.1 LGPL-3.0
Group: System/Libraries
BuildRequires: cmake
BuildRequires: cmake(ECM)
BuildRequires: python
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6QmlTools)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6QmlCore)
BuildRequires: cmake(Qt6GuiTools)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: doxygen
BuildRequires: cmake(Qt6ToolsTools)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: pkgconfig(iso-codes)
BuildRequires: gettext
Requires: %{libname} = %{EVRD}
Requires: iso-codes

%description
KDE libraries for internationalization

%package -n %{libname}
Summary: KDE libraries for internationalization
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
KDE libraries for internationalization

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}
# KI18n cmake rules rely on msg* tools
Requires: gettext

%description -n %{devname}
Development files (Headers etc.) for %{name}.

KDE libraries for internationalization

%prep
%autosetup -p1 -n ki18n-%{?git:master}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%find_lang %{name} --all-name --with-qt --with-html

for i in %{buildroot}%{_datadir}/locale/*/LC_SCRIPTS/*; do
	L=$(echo $i |rev |cut -d/ -f3 |rev)
	echo "%lang($L) %{_datadir}/locale/$L/LC_SCRIPTS/ki18n6" >>%{name}.lang
done

%files -f %{name}.lang
%{_datadir}/qlogging-categories6/ki18n.*

%files -n %{devname}
%{_includedir}/KF6/KI18n
%{_includedir}/KF6/KI18nLocaleData
%{_libdir}/cmake/KF6I18n

%files -n %{libname}
%{_libdir}/libKF6I18n.so*
%{_libdir}/libKF6I18nQml.so*
%{_libdir}/libKF6I18nLocaleData.so*
%{_qtdir}/plugins/kf6/ktranscript.so
%{_qtdir}/qml/org/kde/i18n
