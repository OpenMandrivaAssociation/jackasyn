%define name	jackasyn
%define version	0.8
%define release 1mdk

%define major	0 
%define libname %mklibname %name %major

Name: 	 	%{name}
Summary: 	Asynchronous capabilities for Jack audio daemon
Version: 	%{version}
Release: 	%{release}

Source:		lib%{name}-%{version}.tar.bz2
URL:		http://gige.xdv.org/soft/libjackasyn
License:	GPL
Group:		Sound
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	libjack-devel
Requires:	jackit

%description
This is a library that allows to access the jack audio server in asynchronous
mode. The jacklaunch command launches an application by preloading
libjackasyn. This makes applications that are written for the OSS API working
with the JACK audio server.

%package -n 	%{libname}
Summary:        Dynamic libraries from %name
Group:          System/Libraries

%description -n %{libname}
This is a library that allows to access the jack audio server in asynchronous
mode. It can be used for several purposes:
1) Make an application that uses the OSS audio API run with the jack server
via the LD_PRELOAD system.
2) You have an application that is written for asynchronous mode, probably for
several platforms and can't afford a rewrite of the whole system to fit jacks
callback architecture.
3) You want to port an application in a fast and easy way and do not care for
tight synchronisation and performance. 

%package -n 	%{libname}-devel
Summary: 	Header files and static libraries from %name
Group: 		Development/C
Requires: 	%{libname} >= %{version}
Provides: 	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%name-devel

%description -n %{libname}-devel
Libraries and includes files for developing programs based on %name.

%prep
%setup -q -n lib%name-%version

%build
%configure
%make
										
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_libdir
mkdir -p $RPM_BUILD_ROOT/%_bindir
mkdir -p $RPM_BUILD_ROOT/%_includedir
mkdir -p $RPM_BUILD_ROOT/%_mandir/man1
install -m 644 libjackasyn.a $RPM_BUILD_ROOT/%_libdir
install -m 644 libjackasyn.so.%version $RPM_BUILD_ROOT/%_libdir
install -m 644 libjackoss.h $RPM_BUILD_ROOT/%_includedir
ln -s libjackasyn.so.%version $RPM_BUILD_ROOT/%_libdir/libjackasyn.so.0
ln -s libjackasyn.so.%version $RPM_BUILD_ROOT/%_libdir/libjackasyn.so
install -m 755 jacklaunch $RPM_BUILD_ROOT/%_bindir
bzip2 jacklaunch.1
cp jacklaunch.1.bz2 $RPM_BUILD_ROOT/%_mandir/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README AUTHORS CHANGELOG COPYING TODO WORKING
%{_bindir}/jacklaunch
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a

