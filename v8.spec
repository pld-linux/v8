
# For the 1.2 branch, we use 0s here
# For 1.3+, we use the three digit versions
%define		somajor 2
%define		sominor 1
%define		sobuild 2
%define		sover %{somajor}.%{sominor}.%{sobuild}

%define		snap	20100309svn4070
%define		rel		1
Summary:	JavaScript Engine
Name:		v8
Version:	2.1.2.6
Release:	0.%{snap}.%{rel}
License:	BSD
Group:		Libraries
URL:		http://code.google.com/p/v8
# No tarballs, pulled from svn
# svn export http://v8.googlecode.com/svn/trunk/ v8
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	f329539eacdd444b2517ff66561ab0fe
#Patch0:		%{name}-d8-fwrite-return.patch
Patch1:		%{name}-2.0.0-d8-allocation.patch
Patch2:		%{name}-cstdio.patch
Patch3:		%{name}-strndup.patch
BuildRequires:	gcc >= 4.0
BuildRequires:	libstdc++-devel
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
%setup -q -n %{name}
#%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%{__sed} -i -e "s,'-O3','%{rpmcxxflags}'.split(' ')," SConstruct

# create simple makefile
cat <<'EOF'> Makefile
V8_OBJS = obj/release/d8-debug.os obj/release/d8-posix.os obj/release/d8-readline.os obj/release/d8.os obj/release/d8-js.os
V8_LIBS = -lpthread -lreadline -lpthread -L. -lv8

v8:
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $@ $(V8_OBJS) $(V8_LIBS)
EOF

%build
# build library

CFLAGS="%{rpmcflags}"
CXXFLAGS="%{rpmcxxflags}"
LDFLAGS="%{rpmcflags}"
%if "%{pld_release}" == "ac"
CC=%{__cc}4
CXX=%{__cxx}4
%else
CC=%{__cc}
CXX=%{__cxx}
%endif
export CFLAGS LDFLAGS CXXFLAGS CC CXX
%scons \
	library=shared \
	snapshots=on \
	soname=off \
	console=readline \
	visibility=default \
%ifarch x86_64
	arch=x64 \
%endif
	env=CCFLAGS:"-fPIC"

# the soname=on creates soname as libv8-1.3.11.1.so, that's wrong
rm libv8.so
# Now, lets make it right.
%ifarch arm
%{__cxx} %{rpmcflags} %{rpmldflags} -fPIC -o libv8.so.%{sover} -shared -Wl,-soname,libv8.so.%{somajor} obj/release/*.os obj/release/arm/*.os -lpthread
%endif
%ifarch %{ix86}
%{__cxx} %{rpmcflags} %{rpmldflags} -fPIC -o libv8.so.%{sover} -shared -Wl,-soname,libv8.so.%{somajor} obj/release/*.os obj/release/ia32/*.os -lpthread
%endif
%ifarch %{x8664}
%{__cxx} %{rpmcflags} %{rpmldflags} -fPIC -o libv8.so.%{sover} -shared -Wl,-soname,libv8.so.%{somajor} obj/release/*.os obj/release/x64/*.os -lpthread
%endif

# We need to do this so d8 binary can link against it.
ln -sf libv8.so.%{sover} libv8.so

# build binary
%scons d8 \
	library=shared \
	snapshots=on \
	console=readline \
	visibility=default \
	%ifarch x86_64
	arch=x64 \
	%endif
	env=CCFLAGS:"-fPIC"

# Sigh. scons links all statically, relink
mv d8 d8.static

%{__make} v8 \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir}}
install -p v8 $RPM_BUILD_ROOT%{_bindir}
cp -a include/*.h $RPM_BUILD_ROOT%{_includedir}
install -p libv8.so.*.*.* $RPM_BUILD_ROOT%{_libdir}

lib=$(basename $RPM_BUILD_ROOT%{_libdir}/libv8.so.*.*.*)
ln -s $lib $RPM_BUILD_ROOT%{_libdir}/libv8.so
ln -s $lib $RPM_BUILD_ROOT%{_libdir}/libv8.so.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE
%attr(755,root,root) %{_bindir}/v8

%files libs
%attr(755,root,root) %{_libdir}/libv8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libv8.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libv8.so
%{_includedir}/*.h
