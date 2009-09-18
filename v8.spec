%define snap	20090918

Summary:	JavaScript Engine
Name:		v8
Version:	1.2.13
Release:	0.%{snap}.1
License:	BSD
Group:		Libraries
URL:		http://code.google.com/p/v8
# No tarballs, pulled from svn
# svn export http://v8.googlecode.com/svn/trunk/ v8
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	736a6a7a21aa8a2834a583763d37a7af
#Patch0: %{name}-svn2430-unused-parameter.patch
#Patch1: http://codereview.chromium.org/download/issue115176_4_1002.diff
BuildRequires:	scons
ExclusiveArch:	%{ix86} x86_64 arm
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
#%patch0 -p1 -b .unused-parameter
#%patch1 -p0 -b .issue115176

%build
%scons \
	library=shared snapshots=on \
%ifarch x86_64
arch=x64 \
%endif
env=CCFLAGS:"-fPIC"
# When will people learn to create versioned shared libraries by default?
# first, lets get rid of the old .so
rm -rf libv8.so
# Now, lets make it right.
%ifarch arm
%{__cxx} %{rpmcflags} %{rpmldflags} -fPIC -o libv8.so.0.0.0 -shared -Wl,-soname,libv8.so.0 obj/release/*.os obj/release/arm/*.os
%endif
%ifarch %{ix86}
%{__cxx} %{rpmcflags} %{rpmldflags} -fPIC -o libv8.so.0.0.0 -shared -Wl,-soname,libv8.so.0 obj/release/*.os obj/release/ia32/*.os
%endif
%ifarch x86_64
%{__cxx} %{rpmcflags} %{rpmldflags} -fPIC -o libv8.so.0.0.0 -shared -Wl,-soname,libv8.so.0 obj/release/*.os obj/release/x64/*.os
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir}}


install -p include/*.h $RPM_BUILD_ROOT%{_includedir}
install -p libv8.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}

cd $RPM_BUILD_ROOT%{_libdir}
ln -sf libv8.so.0.0.0 libv8.so
ln -sf libv8.so.0.0.0 libv8.so.0
ln -sf libv8.so.0.0.0 libv8.so.0.0

chmod -x $RPM_BUILD_ROOT%{_includedir}/v8*.h

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%attr(755,root,root) %{_libdir}/*.so
