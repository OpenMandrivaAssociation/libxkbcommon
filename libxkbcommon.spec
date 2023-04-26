# libxkbcommon is used by sdl2, used by wine and many games
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define bname xkbcommon
%define major 0
%define libname %mklibname %{bname} %{major}
%define libnamex11 %mklibname %{bname}-x11 %{major}
%define libname_devel %mklibname %{bname} -d
%define libnamex11_devel %mklibname %{bname}-x11 -d
%define libnamereg %mklibname xkbregistry %{major}
%define libnamereg_devel %mklibname xkbregistry -d
%define lib32name %mklib32name %{bname} %{major}
%define lib32namex11 %mklib32name %{bname}-x11 %{major}
%define lib32name_devel %mklib32name %{bname} -d
%define lib32namex11_devel %mklib32name %{bname}-x11 -d

Summary:	XKB API common to servers and clients
Name:		libxkbcommon
Version:	1.5.0
Release:	3
License:	MIT
Group:		System/Libraries
Url:		http://xkbcommon.org/
Source0:	http://xkbcommon.org/download/%{name}-%{version}.tar.xz
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	x11-util-macros
BuildRequires:	doxygen
BuildRequires:	meson
BuildRequires:	pkgconfig(xcb-xkb)
BuildRequires:	pkgconfig(xkeyboard-config)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-scanner)
BuildRequires:	pkgconfig(wayland-protocols)
# to auto-detect XKB config root
BuildRequires:	x11-data-xkbdata
BuildRequires:	pkgconfig(libxml-2.0)
%if %{with compat32}
BuildRequires:	devel(libxcb-xkb)
BuildRequires:	devel(libX11-xcb)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libxml2)
%endif

%description
The %{name} package provides XKB API common to servers and clients.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Requires:	xkeyboard-config
Recommends:	libx11-common

%description -n %{libname}
This package contains the libraries for %{name}.

%package -n %{libnamex11}
Summary:	Libraries for X11 bits of %{name}
Group:		System/Libraries
# (tpg) fix update from 2014.x
Provides:	%{_lib}xkbcommon-x110 = 0.4.2-4
Obsoletes:	%{_lib}xkbcommon-x110 < 0.4.2-4

%description -n %{libnamex11}
This package contains the libraries for X11 bits of %{name}.

%package -n %{libnamereg}
Summary:	Libraries for xkbregistry bits of %{name}
Group:		System/Libraries

%description -n %{libnamereg}
This package contains the libraries for xkbregistry bits of %{name}.

%package -n %{libname_devel}
Summary:	Header files for %{name}
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n %{libname_devel}
This package contains the header and pkg-config files for developing
with %{name}.

%package -n %{libnamex11_devel}
Summary:	Header files for X11 bits of %{name}
Group:		Development/C
Requires:	%{libnamex11} = %{version}-%{release}
Requires:	%{libname_devel} = %{version}-%{release}

%description -n %{libnamex11_devel}
This package contains the header and pkg-config files for developing
with X11 bits of %{name}.

%package -n %{libnamereg_devel}
Summary:	Header files for xkbregistry bits of %{name}
Group:		Development/C
Requires:	%{libnamereg} = %{version}-%{release}
Requires:	%{libname_devel} = %{version}-%{release}

%description -n %{libnamereg_devel}
This package contains the header and pkg-config files for developing
with xkbregistry bits of %{name}.

%package doc
Summary:	%{name} documentation
Group:		Development/Other

%description doc
This package contains documentation of %{name}.

%package utils
Summary:	X.Org X11 XKB parsing utilities
Requires:	%{libname}

%description utils
%{name}-utils is a set of utilities to analyze and test XKB parsing.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Libraries for %{name} (32-bit)
Group:		System/Libraries
Requires:	xkeyboard-config

%description -n %{lib32name}
This package contains the libraries for %{name}.

%package -n %{lib32namex11}
Summary:	Libraries for X11 bits of %{name} (32-bit)
Group:		System/Libraries

%description -n %{lib32namex11}
This package contains the libraries for X11 bits of %{name}.

%package -n %{lib32name_devel}
Summary:	Header files for %{name} (32-bit)
Group:		Development/C
Requires:	%{libname_devel} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{lib32name_devel}
This package contains the header and pkg-config files for developing
with %{name}.

%package -n %{lib32namex11_devel}
Summary:	Header files for X11 bits of %{name} (32-bit)
Group:		Development/C
Requires:	%{libnamex11_devel} = %{version}-%{release}
Requires:	%{lib32namex11} = %{version}-%{release}
Requires:	%{lib32name_devel} = %{version}-%{release}

%description -n %{lib32namex11_devel}
This package contains the header and pkg-config files for developing
with X11 bits of %{name}.
%endif

%prep
%autosetup -p1
%if %{with compat32}
# FIXME at some point, we'll probably want to enable wayland.
# For now, wine and steam games don't do wayland anyway.
%meson32 \
	-Denable-wayland=false \
	-Denable-xkbregistry=false
%endif
%meson

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%meson_build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%meson_install

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}
%{_libdir}/%{name}.so.%{major}.*

%files -n %{libnamex11}
%{_libdir}/%{name}-x11.so.%{major}
%{_libdir}/%{name}-x11.so.%{major}.*

%files -n %{libnamereg}
%{_libdir}/libxkbregistry.so.%{major}
%{_libdir}/libxkbregistry.so.%{major}.*

%files -n %{libname_devel}
%{_includedir}/%{bname}/%{bname}.h
%{_includedir}/%{bname}/%{bname}-compat.h
%{_includedir}/%{bname}/%{bname}-compose.h
%{_includedir}/%{bname}/%{bname}-keysyms.h
%{_includedir}/%{bname}/%{bname}-names.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{bname}.pc

%files -n %{libnamex11_devel}
%{_includedir}/%{bname}/%{bname}-x11.h
%{_libdir}/%{name}-x11.so
%{_libdir}/pkgconfig/%{bname}-x11.pc

%files -n %{libnamereg_devel}
%{_includedir}/xkbcommon/xkbregistry.h
%{_libdir}/libxkbregistry.so
%{_libdir}/pkgconfig/xkbregistry.pc

%files utils
%{_bindir}/xkbcli
%{_libexecdir}/xkbcommon/xkbcli-*
%doc %{_mandir}/man1/xkbcli*.1.*

%files doc
%doc %{_docdir}/%{name}/*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/%{name}.so.%{major}
%{_prefix}/lib/%{name}.so.%{major}.*

%files -n %{lib32namex11}
%{_prefix}/lib/%{name}-x11.so.%{major}
%{_prefix}/lib/%{name}-x11.so.%{major}.*

%files -n %{lib32name_devel}
%{_prefix}/lib/%{name}.so
%{_prefix}/lib/pkgconfig/%{bname}.pc

%files -n %{lib32namex11_devel}
%{_prefix}/lib/%{name}-x11.so
%{_prefix}/lib/pkgconfig/%{bname}-x11.pc
%endif
