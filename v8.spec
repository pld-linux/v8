#
# TODO: fix readline
#

%define		sover	%(v=%{version}; echo ${v%.*})
%define		somajor	%(v=%{version}; echo ${v%%%%.*})
Summary:	JavaScript Engine
Name:		v8
Version:	3.3.6.1
Release:	1
License:	New BSD License
Group:		Libraries
URL:		http://code.google.com/p/v8
# No tarballs, pulled from svn
# svn export http://v8.googlecode.com/svn/tags/%{version} v8-%{version}
Source0:	http://distfiles.gentoo.org/distfiles/%{name}-%{version}.tar.gz
# Source0-md5:	b8504e98681669c95738724717c4e93f
#Patch1:		%{name}-2.0.0-d8-allocation.patch
Patch2:		%{name}-cstdio.patch
Patch3:		%{name}-strndup.patch
Patch4:		%{name}-soname.patch
Patch5:		%{name}-dynlink.patch
BuildRequires:	libstdc++-devel >= 5:4.0
BuildRequires:	readline-devel
BuildRequires:	scons
ExclusiveArch:	%{ix86} %{x8664} arm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
V8 is Google's open source JavaScript engine. V8 is written in C++ and
is used in Google Chrome, the open source browser from Google. V8
implements ECMAScript as specified in ECMA-262, 3rd edition.

This package contains the command line program.

%package libs
Summary:	V8 JavaScript Engine shared library
Group:		Libraries
Conflicts:	v8 < 2.0.0

%description libs
V8 is Google's open source JavaScript engine. V8 is written in C++ and
is used in Google Chrome, the open source browser from Google. V8
implements ECMAScript as specified in ECMA-262, 3rd edition.

This package contains the shared library.

%package devel
Summary:	Development headers and libraries for v8
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development headers and libraries for v8.

%prep
%setup -q
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%{__sed} -i -e "s,'-O3','%{rpmcxxflags}'.split(' ')," SConstruct

%build
# build library

CFLAGS="%{rpmcflags}"
CXXFLAGS="%{rpmcxxflags}"
LDFLAGS="%{rpmcflags}"
%if "%{pld_release}" == "ac"
CC="%{__cc}4"
CXX="%{__cxx}4"
%else
CC="%{__cc}"
CXX="%{__cxx}"
%endif
export CFLAGS LDFLAGS CXXFLAGS CC CXX
%scons \
	library=shared \
	snapshots=on \
	soname=on \
	console=readline \
	visibility=default \
%ifarch x86_64
	arch=x64 \
%endif
	env=CCFLAGS:"-fPIC"

mv libv8.so libv8.so.%{sover}

# We need to do this so d8 binary can link against it.
ln -sf libv8.so.%{sover} libv8.so

# build binary
%scons d8 \
	library=shared \
	snapshots=on \
	console=dumb \
	visibility=default \
	%ifarch x86_64
	arch=x64 \
	%endif
	env=CCFLAGS:"-fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir}}
install -p d8 $RPM_BUILD_ROOT%{_bindir}/v8
cp -a include/*.h $RPM_BUILD_ROOT%{_includedir}
install -p libv8.so.*.*.* $RPM_BUILD_ROOT%{_libdir}

lib=$(basename $RPM_BUILD_ROOT%{_libdir}/libv8.so.*.*.*)
ln -s $lib $RPM_BUILD_ROOT%{_libdir}/libv8.so
ln -s $lib $RPM_BUILD_ROOT%{_libdir}/libv8.so.%{somajor}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE
%attr(755,root,root) %{_bindir}/v8

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libv8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libv8.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libv8.so
%{_includedir}/*.h
