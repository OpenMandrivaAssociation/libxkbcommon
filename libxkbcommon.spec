%undefine _debugsource_packages
# libxkbcommon is used by sdl2, used by wine and many games
%ifarch %{x86_64}
%bcond_without compat32
%endif

# (tpg) 2023-10-27
# DEBUG: ld.lld: error: undefined symbol: __start_test_functions_section
# DEBUG: >>> referenced by xvfb-wrapper.c:153 (../test/xvfb-wrapper.c:153)
# DEBUG: >>>               lto.tmp:(main)
# DEBUG: >>> the encapsulation symbol needs to be retained under --gc-sections properly; consider -z nostart-stop-gc (see https://lld.llvm.org/ELF/start-stop-gc)
#
# As of 1.6.0 with lld 17.0.3, -Wl,--undefined-version is needed because the check
# for -Wl,--version-script is broken
%global build_ldflags %{build_ldflags} -z nostart-stop-gc -Wl,--undefined-version

%define bname xkbcommon
%define major 0
%define oldlibname %mklibname %{bname} 0
%define libname %mklibname %{bname}
%define oldlibnamex11 %mklibname %{bname}-x11 0
%define libnamex11 %mklibname %{bname}-x11
%define libname_devel %mklibname %{bname} -d
%define libnamex11_devel %mklibname %{bname}-x11 -d
%define oldlibnamereg %mklibname xkbregistry 0
%define libnamereg %mklibname xkbregistry
%define libnamereg_devel %mklibname xkbregistry -d
%define oldlib32name %mklib32name %{bname} 0
%define lib32name %mklib32name %{bname}
%define oldlib32namex11 %mklib32name %{bname}-x11 0
%define lib32namex11 %mklib32name %{bname}-x11
# 32-bit xkbregistry wasn't packaged before naming policy changes
%define lib32namereg %mklib32name xkbregistry
%define lib32name_devel %mklib32name %{bname} -d
%define lib32namex11_devel %mklib32name %{bname}-x11 -d
%define lib32namereg_devel %mklib32name xkbregistry -d

Summary:	XKB API common to servers and clients
Name:		libxkbcommon
Version:	1.12.1
Release:	1
License:	MIT
Group:		System/Libraries
Url:		https://xkbcommon.org/
Source0:	https://github.com/xkbcommon/libxkbcommon/archive/libxkbcommon-xkbcommon-%{version}.tar.gz
#Source0:	http://xkbcommon.org/download/%{name}-%{version}.tar.xz
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
BuildRequires:	pkgconfig(liblzma)
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
BuildRequires:	devel(libwayland-client)
BuildRequires:	devel(libffi)
BuildRequires:	devel(liblzma)
%if "%{name}" == "%{lib32name}"
%rename %{oldlib32name}
%endif
%endif
%if "%{name}" == "%{libname}"
%rename %{oldlibname}
%endif

%description
The %{name} package provides XKB API common to servers and clients.

%if "%{name}" != "%{libname}"
%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Requires:	xkeyboard-config
Recommends:	libx11-common
%rename %{oldlibname}

%description -n %{libname}
This package contains the libraries for %{name}.
%endif

%package -n %{libnamex11}
Summary:	Libraries for X11 bits of %{name}
Group:		System/Libraries
%rename %{oldlibnamex11}

%description -n %{libnamex11}
This package contains the libraries for X11 bits of %{name}.

%package -n %{libnamereg}
Summary:	Libraries for xkbregistry bits of %{name}
Group:		System/Libraries
%rename %{oldlibnamereg}

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
%if "%{name}" != "%{lib32name}"
%package -n %{lib32name}
Summary:	Libraries for %{name} (32-bit)
Group:		System/Libraries
Requires:	xkeyboard-config
%rename %{oldlib32name}

%description -n %{lib32name}
This package contains the libraries for %{name}.
%endif

%package -n %{lib32namex11}
Summary:	Libraries for X11 bits of %{name} (32-bit)
Group:		System/Libraries
%rename %{oldlib32namex11}

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

%package -n %{lib32namereg}
Summary:	Libraries for the XKB Registry (32-bit)
Group:		System/Libraries

%description -n %{lib32namereg}
This package contains the libraries for the XKB Registry (32-bit).

%package -n %{lib32namereg_devel}
Summary:	Header files for %{name} (32-bit)
Group:		Development/C
Requires:	%{libname_devel} = %{version}-%{release}
Requires:	%{lib32namereg} = %{version}-%{release}

%description -n %{lib32namereg_devel}
This package contains the header and pkg-config files for developing
with %{name}.
%endif

%prep
%autosetup -n libxkbcommon-xkbcommon-%{version} -p1
%if %{with compat32}
%meson32 \
	-Denable-wayland=true \
	-Denable-xkbregistry=true
%endif
%meson \
	-Denable-docs=true

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

%if %{cross_compiling}
if [ -d %{buildroot}%{_prefix}/%{_target_platform} ]; then
	# FIXME
	# bash-completions sometimes get installed in the wrong place
	# when cross compiling (depending on whether or not the HOST
	# bash-completions pkgconfig file is installed)
	# For now, let's fix it here
	mv %{buildroot}%{_prefix}/%{_target_platform}%{_datadir}/* %{buildroot}%{_datadir}
fi
%endif

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
%{_datadir}/bash-completion/completions/xkbcli
%doc %{_mandir}/man1/xkbcli*.1.*

%files doc
%doc %{_docdir}/%{name}/*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/%{name}.so.%{major}
%{_prefix}/lib/%{name}.so.%{major}.*

%files -n %{lib32namereg}
%{_prefix}/lib/libxkbregistry.so.%{major}
%{_prefix}/lib/libxkbregistry.so.%{major}.*

%files -n %{lib32namex11}
%{_prefix}/lib/%{name}-x11.so.%{major}
%{_prefix}/lib/%{name}-x11.so.%{major}.*

%files -n %{lib32name_devel}
%{_prefix}/lib/%{name}.so
%{_prefix}/lib/pkgconfig/%{bname}.pc

%files -n %{lib32namex11_devel}
%{_prefix}/lib/%{name}-x11.so
%{_prefix}/lib/pkgconfig/%{bname}-x11.pc

%files -n %{lib32namereg_devel}
%{_prefix}/lib/libxkbregistry.so
%{_prefix}/lib/pkgconfig/xkbregistry.pc
%endif
