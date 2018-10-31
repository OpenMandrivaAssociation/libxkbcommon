%define bname xkbcommon
%define major 0
%define libname %mklibname %{bname} %{major}
%define libnamex11 %mklibname %{bname}-x11 %{major}
%define libname_devel %mklibname %{bname} -d
%define libnamex11_devel %mklibname %{bname}-x11 -d

Summary:	XKB API common to servers and clients
Name:		libxkbcommon
Version:	0.8.2
Release:	2
License:	MIT
Group:		System/Libraries
Url:		http://xkbcommon.org/
Source0:	http://xkbcommon.org/download/%{name}-%{version}.tar.xz
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	x11-util-macros
BuildRequires:	doxygen
BuildRequires:	pkgconfig(xcb-xkb)
BuildRequires:	pkgconfig(xkeyboard-config)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-scanner)
BuildRequires:	pkgconfig(wayland-protocols)
# to auto-detect XKB config root
BuildRequires:	x11-data-xkbdata

%description
The %{name} package provides XKB API common to servers and clients.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries

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

%package -n %{libname_devel}
Summary:	Header files for %{name}
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

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

%package doc
Summary:	%{name} documentation
Group:		Development/Other

%description doc
This package contains documentation of %{name}.

%prep
%setup -q
%apply_patches
autoreconf -vfi

%build
%configure \
    --disable-static

%make

%install
%makeinstall_std

rm -f %{buildroot}%{_libdir}/%{name}.la

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}
%{_libdir}/%{name}.so.%{major}.*

%files -n %{libnamex11}
%{_libdir}/%{name}-x11.so.%{major}
%{_libdir}/%{name}-x11.so.%{major}.*

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

%files doc
%doc %{_docdir}/%{name}/*
