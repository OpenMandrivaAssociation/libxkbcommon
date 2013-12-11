%define major 0
%define libname %mklibname xkbcommon %{major}
%define develname %mklibname xkbcommon -d
%define staticdevelname %mklibname xkbcommon -d -s
%define snapshot 20120125

Name:		libxkbcommon
Version:	0.1.0
Release:	0.%{snapshot}.1
Summary:	Library to translate evdev keycodes to keysyms
Group:		Development/X11
License:	MIT
Source0:	%{name}-%{version}.%{snapshot}.tar.bz2
BuildRequires:	libx11-devel >= 1.0.0
BuildRequires:	x11-proto-devel >= 1.0.0
BuildRequires:	x11-util-macros >= 1.0.1
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	bison

%description
A library that translates evdev keycodes to keysyms, used by Wayland.

Wayland is a protocol for a compositor to talk to its clients as well
as a C library implementation of that protocol. The compositor can be a
standalone display server running on Linux kernel modesetting and evdev
input devices, an X application, or a wayland client itself.

%package -n %{libname}
Summary:	Library to translate evdev keycodes to keysyms
Group:		Development/X11
Provides:	%{name} = %{version}

%description -n %{libname}
A library that translates evdev keycodes to keysyms, used by Wayland.

Wayland is a protocol for a compositor to talk to its clients as well
as a C library implementation of that protocol. The compositor can be a
standalone display server running on Linux kernel modesetting and evdev
input devices, an X application, or a wayland client itself.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/X11
Requires:	%{libname} = %{version}-%{release}
Requires:	x11-proto-devel >= 1.0.0
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains development files for %{name},
a library that translates evdev keycodes to keysyms.

%package -n %{staticdevelname}
Summary:	Static development files for %{name}
Group:		Development/X11
Requires:	%{develname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}

%description -n %{staticdevelname}
This package contains static development files for %{name},
a library that translates evdev keycodes to keysyms.

%prep
%setup -q

%build
./autogen.sh
%configure2_5x \
	--x-includes=%{_includedir}\
	--x-libraries=%{_libdir}

%make

%install
%makeinstall_std

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libxkbcommon.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/libxkbcommon.so
#%{_libdir}/libxkbcommon.la
%{_libdir}/pkgconfig/xkbcommon.pc
%{_includedir}/X11/extensions/XKBcommon.h

%files -n %{staticdevelname}
%defattr(-,root,root)
%{_libdir}/libxkbcommon.a

