%define bname xkbcommon
%define major 0
%define libname %mklibname %{bname} %{major}
%define libname_devel %mklibname %{bname} -d

Summary:	XKB API common to servers and clients	
Name:		libxkbcommon
Version:	0.4.2
Release:	1
License:	MIT
Group:		System/Libraries
Url:		http://xkbcommon.org/
Source0:	http://xkbcommon.org/download/%{name}-%{version}.tar.xz
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	x11-util-macros
BuildRequires:	doxygen
# to auto-detect XKB config root
BuildRequires:	x11-data-xkbdata

%description
The %{name} package provides XKB API common to servers and clients.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains the libraries for %{name}.

%package -n %{libname_devel}
Summary:	Header files for %{name}
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{libname_devel}
This package contains the header and pkg-config files for developing
with %{name}.

%package doc
Summary:	%{name} documentation
Group:		Development/Other

%description doc
This package contains documentation of %{name}.

%prep
%setup -q -n %{srcname}
%apply_patches
autoreconf -vfi

%build
%configure2_5x \
		--disable-static

%make

%install
%makeinstall_std

rm -f %{buildroot}%{_libdir}/%{name}.la

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}
%{_libdir}/%{name}.so.%{major}.*

%files -n %{libname_devel}
%{_includedir}/%{bname}/%{bname}.h
%{_includedir}/%{bname}/%{bname}-compat.h
%{_includedir}/%{bname}/%{bname}-keysyms.h
%{_includedir}/%{bname}/%{bname}-names.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{bname}.pc

%files doc
%doc %{_docdir}/%{name}/*
