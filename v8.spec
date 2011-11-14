# TODO
# - we might need bigger soname than just major version, as 3.4 ande 3.6 are
#   rather different and chrome fails to build
Summary:	JavaScript Engine by Google
Summary(pl.UTF-8):	Silnik JavaScript firmy Google
Name:		v8
Version:	3.6.6.7
Release:	3
License:	BSD
Group:		Applications
Source0:	http://commondatastorage.googleapis.com/chromium-browser-official/%{name}-%{version}.tar.bz2
# Source0-md5:	415a830ee612694895760fb02ae9273f
Patch0:		%{name}-cstdio.patch
Patch1:		%{name}-strndup.patch
Patch2:		%{name}-soname.patch
Patch3:		%{name}-dynlink.patch
URL:		http://code.google.com/p/v8/
BuildRequires:	libstdc++-devel >= 5:4.0
BuildRequires:	python >= 1:2.4
BuildRequires:	readline-devel
BuildRequires:	scons >= 1.0.0
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
ExclusiveArch:	%{ix86} %{x8664} arm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		somajor	%(v=%{version}; echo ${v%%%%.*})

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
%patch2 -p1
%patch3 -p1
%{__sed} -i -e "s,'-O3','%{rpmcxxflags}'.split(' ')," SConstruct
# some "unused-but-set" warnings
%{__sed} -i -e "s/'-Werror',//" SConstruct

%build
# build library
CFLAGS="%{rpmcflags}"
CXXFLAGS="%{rpmcxxflags}"
LDFLAGS="%{rpmldflags}"
%if "%{pld_release}" == "ac"
CC="%{__cc}4"
CXX="%{__cxx}4"
%else
CC="%{__cc}"
CXX="%{__cxx}"
%endif
export CFLAGS LDFLAGS CXXFLAGS CC CXX
%scons library d8 \
	library=shared \
	snapshots=on \
	soname=on \
	console=readline \
	visibility=default \
%ifarch %{x8664}
	arch=x64 \
%endif
	env=CCFLAGS:"-fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir}}

for lib in libv8 libv8preparser; do
	install -p ${lib}.so $RPM_BUILD_ROOT%{_libdir}/${lib}.so.%{version}
	ln -sf ${lib}.so.%{version} $RPM_BUILD_ROOT%{_libdir}/${lib}.so.%{somajor}
	ln -sf ${lib}.so.%{version} $RPM_BUILD_ROOT%{_libdir}/${lib}.so
done
cp -p include/*.h $RPM_BUILD_ROOT%{_includedir}

install -p d8 $RPM_BUILD_ROOT%{_bindir}/v8

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE LICENSE.strongtalk LICENSE.valgrind
%attr(755,root,root) %{_bindir}/v8

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libv8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libv8.so.3
%attr(755,root,root) %{_libdir}/libv8preparser.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libv8preparser.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libv8.so
%attr(755,root,root) %{_libdir}/libv8preparser.so
%{_includedir}/v8*.h
