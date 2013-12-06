%define major		0 
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d
%define debug_package          %{nil}

Name:	 	jackasyn
Summary:		Asynchronous capabilities for Jack audio daemon
Version:		0.13
Release:		5
Source0:		http://gige.xdv.org/soft/libjackasyn/download/lib%{name}-%{version}.tar.gz
URL:		http://gige.xdv.org/soft/libjackasyn
License:		GPLv2+
Group:		Sound
BuildRequires:	jackit-devel
BuildRequires:	libsamplerate-devel
Requires:	jackit

%description
This is a library that allows to access the jack audio server in
asynchronous mode. The jacklaunch command launches an application by
preloading libjackasyn. This makes applications that are written for the
OSS API working with the JACK audio server.


%package -n	%{libname}
Summary:		Dynamic libraries from %{name}
Group:		System/Libraries

%description -n %{libname}
This is a library that allows to access the jack audio server in
asynchronous mode. It can be used for several purposes:
  1) Make an application that uses the OSS audio API run with the jack
     server via the LD_PRELOAD system.
  2) You have an application that is written for asynchronous mode,
     probably for several platforms and can't afford a rewrite of the whole
     system to fit jackit callback architecture.
  3) You want to port an application in a fast and easy way and do not care
     for tight synchronisation and performance. 


%package -n	%{develname}
Summary:		Header files and static libraries from %{name}
Group: 		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes:	%{name}-devel < %{version}-%{release}
#Obsoletes:	%%{_lib}jackasyn0-devel < %%{version}-%%{release}

%description -n %{develname}
Libraries and includes files for developing programs based on %{name}.


%prep
%setup -qn lib%{name}-%{version}

%build
%configure2_5x
# parallel build doesn't work - AdamW 2008/08
make


%install
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_includedir}
mkdir -p %{buildroot}/%{_mandir}/man1
install -m 644 libjackasyn.a %{buildroot}/%{_libdir}
install -m 755 libjackasyn.so.%{version} %{buildroot}/%{_libdir}
install -m 644 libjackoss.h %{buildroot}/%{_includedir}
ln -s libjackasyn.so.%{version} %{buildroot}/%{_libdir}/libjackasyn.so.0
ln -s libjackasyn.so.%{version} %{buildroot}/%{_libdir}/libjackasyn.so
install -m 755 jacklaunch %{buildroot}/%{_bindir}
install -m 0644 jacklaunch.1 %{buildroot}/%{_mandir}/man1


%files
%doc README AUTHORS CHANGELOG TODO WORKING
%{_bindir}/jacklaunch
%{_mandir}/man1/*


%files -n %{libname}
%doc README
%{_libdir}/*.so.%{major}*


%files -n %{develname}
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a



%changelog
* Fri Nov 02 2012 Giovanni Mariani <mc2374@mclink.it> 0.13-4
- Dropped BuildRoot, %%mkrel, %%defattr and %%clean section
- Fixed BReq for jackit devel package
- Massaged the Description texts to make sure they have lines < 76
  chars lenght
- Make rpmlint happy about library executable perms

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0.13-3mdv2010.0
+ Revision: 429579
- rebuild

* Sun Aug 24 2008 Adam Williamson <awilliamson@mandriva.org> 0.13-2mdv2009.0
+ Revision: 275567
- comment non-parallel build
- try disabling parallel build, looks like it breaks
- protect major in file list
- don't package COPYING
- don't manually compress manpage
- s,$RPM_BUILD_ROOT,${buildroot}
- version obsoletes
- make {} use consistent
- br libsamplerate-devel
- new license policy
- correct source location
- new devel policy
- drop unnecessary defines
- new release 0.13
- import jackasyn


* Tue Jul 15 2003 Austin Acton <aacton@yorku.ca> 0.8-1mdk
- 0.8

* Sun May 25 2003 Austin Acton <aacton@yorku.ca> 0.7-1mdk
- initial package
