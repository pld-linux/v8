# TODO
# - cxx is not passed to build
# - cleaner way for cxxflags
%define		snap	20090918
%define		rel		1
Summary:	JavaScript Engine
Name:		v8
Version:	1.2.13
Release:	0.%{snap}.%{rel}
License:	BSD
Group:		Libraries
URL:		http://code.google.com/p/v8
# No tarballs, pulled from svn
# svn export http://v8.googlecode.com/svn/trunk/ v8
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	736a6a7a21aa8a2834a583763d37a7af
#Patch0:	%{name}-svn2430-unused-parameter.patch
#Patch1:	http://codereview.chromium.org/download/issue115176_4_1002.diff
BuildRequires:	readline-devel
BuildRequires:	scons
ExclusiveArch:	%{ix86} %{x8664} arm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
V8 is Google's open source JavaScript engine. V8 is written in C++ and
is used in Google Chrome, the open source browser from Google. V8
implements ECMAScript as specified in ECMA-262, 3rd edition.

%package devel
Summary:	Development headers and libraries for v8
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development headers and libraries for v8.

%prep
%setup -q -n %{name}
#%patch0 -p1
#%patch1 -p0
%{__sed} -i -e "s,'-O3','%{rpmcxxflags}'.split(' ')," SConstruct

%build
%scons \
	library=shared \
	snapshots=on \
	soname=off \
	console=readline \
%ifarch x86_64
	arch=x64 \
%endif
	env=CCFLAGS:"-fPIC"

# the soname=on creates soname as libv8-1.3.11.1.so, that's wrong
rm libv8.so
# Now, lets make it right.
%ifarch arm
%{__cxx} %{rpmcflags} %{rpmldflags} -fPIC -o libv8.so.0.0.0 -shared -Wl,-soname,libv8.so.0 obj/release/*.os obj/release/arm/*.os
%endif
%ifarch %{ix86}
%{__cxx} %{rpmcflags} %{rpmldflags} -fPIC -o libv8.so.0.0.0 -shared -Wl,-soname,libv8.so.0 obj/release/*.os obj/release/ia32/*.os
%endif
%ifarch %{x8664}
%{__cxx} %{rpmcflags} %{rpmldflags} -fPIC -o libv8.so.0.0.0 -shared -Wl,-soname,libv8.so.0 obj/release/*.os obj/release/x64/*.os
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir}}
cp -a include/*.h $RPM_BUILD_ROOT%{_includedir}
install -p libv8.so.*.*.* $RPM_BUILD_ROOT%{_libdir}

lib=$(basename $RPM_BUILD_ROOT%{_libdir}/libv8.so.*.*.*)
ln -s $lib $RPM_BUILD_ROOT%{_libdir}/libv8.so
ln -s $lib $RPM_BUILD_ROOT%{_libdir}/libv8.so.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE
%attr(755,root,root) %{_libdir}/libv8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libv8.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libv8.so
%{_includedir}/*.h
