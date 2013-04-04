# TODO
# - readline not working in d8 (at least arrows)
Summary:	JavaScript Engine by Google
Summary(pl.UTF-8):	Silnik JavaScript firmy Google
Name:		v8
Version:	3.15.11.17
Release:	1
License:	BSD
Group:		Applications
# Source0Download: http://gsdview.appspot.com/chromium-browser-official/?marker=v8-3.15.11.17.tar.bz2
Source0:	http://commondatastorage.googleapis.com/chromium-browser-official/%{name}-%{version}.tar.bz2
# Source0-md5:	0930164aa73e5ce94565ae1b85fac19b
Patch0:		%{name}-cstdio.patch
Patch1:		%{name}-strndup.patch
Patch3:		%{name}-dynlink.patch
URL:		http://code.google.com/p/v8/
BuildRequires:	libstdc++-devel >= 5:4.0
BuildRequires:	python >= 1:2.5
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
ExclusiveArch:	%{ix86} %{x8664} arm mips
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		sover	%(echo %{version} | cut -d. -f1-2)

%description
V8 is Google's open source JavaScript engine. V8 is written in C++ and
is used in Google Chrome, the open source browser from Google. V8
implements ECMAScript as specified in ECMA-262, 3rd edition.

This package contains the V8 developer shell.

%description -l pl.UTF-8
V8 to mający otwarte źródła silnik JavaScriptu firmy Google. V8 jest
napisany w C++ i wykorzystywany w mającej otwarte źródła przeglądarce
Google Chrome. V8 implementuje ECMAScript zgodnie ze specyfikacją
ECMA-262, edycja 3.

Ten pakiet zawiera powłokę programistyczną V8.

%package libs
Summary:	V8 JavaScript Engine shared library
Summary(pl.UTF-8):	Biblioteka współdzielona silnika JavaScriptu V8
Group:		Libraries
Conflicts:	v8 < 2.0.0

%description libs
V8 is Google's open source JavaScript engine. V8 is written in C++ and
is used in Google Chrome, the open source browser from Google. V8
implements ECMAScript as specified in ECMA-262, 3rd edition.

This package contains the shared library.

%description libs -l pl.UTF-8
V8 to mający otwarte źródła silnik JavaScriptu firmy Google. V8 jest
napisany w C++ i wykorzystywany w mającej otwarte źródła przeglądarce
Google Chrome. V8 implementuje ECMAScript zgodnie ze specyfikacją
ECMA-262, edycja 3.

Ten pakiet zawiera bibliotekę współdzieloną.

%package devel
Summary:	Development headers for V8 JavaScript engine
Summary(pl.UTF-8):	Pliki nagłówkowe silnika JavaScriptu V8
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Development headers for V8 JavaScript engine.

%description devel -l pl.UTF-8
Pliki nagłówkowe silnika JavaScriptu V8.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3 -p1

%build
# build library
CFLAGS="%{rpmcflags}"
CXXFLAGS="%{rpmcxxflags}"
LDFLAGS="%{rpmldflags}"
CC="%{__cc}"
CXX="%{__cxx}"
export CFLAGS LDFLAGS CXXFLAGS CC CXX
%{__make} native \
	library=shared \
	soname_version=%{sover} \
	console=readline

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir}}

install -p out/native/lib.target/libv8.so.%{sover} $RPM_BUILD_ROOT%{_libdir}/libv8.so.%{version}
ln -sf libv8.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libv8.so.%{sover}
ln -sf libv8.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libv8.so
cp -p include/*.h $RPM_BUILD_ROOT%{_includedir}

install -p out/native/d8 $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE LICENSE.strongtalk LICENSE.valgrind
%attr(755,root,root) %{_bindir}/d8

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libv8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libv8.so.%{sover}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libv8.so
%{_includedir}/v8*.h
