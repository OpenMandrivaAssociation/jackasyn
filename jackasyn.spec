%define major		0 
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Name: 	 	jackasyn
Summary: 	Asynchronous capabilities for Jack audio daemon
Version: 	0.13
Release: 	%{mkrel 3}
Source:		http://gige.xdv.org/soft/libjackasyn/download/lib%{name}-%{version}.tar.gz
URL:		http://gige.xdv.org/soft/libjackasyn
License:	GPL+
Group:		Sound
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	libjack-devel
BuildRequires:	libsamplerate-devel
Requires:	jackit

%description
This is a library that allows to access the jack audio server in asynchronous
mode. The jacklaunch command launches an application by preloading
libjackasyn. This makes applications that are written for the OSS API working
with the JACK audio server.

%package -n 	%{libname}
Summary:        Dynamic libraries from %{name}
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

%package -n 	%{develname}
Summary: 	Header files and static libraries from %{name}
Group: 		Development/C
Requires: 	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%{name}-devel < %{version}-%{release}
Obsoletes:	%{mklibname jackasyn 0 -d} < %{version}-%{release}

%description -n %{develname}
Libraries and includes files for developing programs based on %{name}.

%prep
%setup -q -n lib%{name}-%{version}

%build
%configure2_5x
# parallel build doesn't work - AdamW 2008/08
make
										
%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_includedir}
mkdir -p %{buildroot}/%{_mandir}/man1
install -m 644 libjackasyn.a %{buildroot}/%{_libdir}
install -m 644 libjackasyn.so.%{version} %{buildroot}/%{_libdir}
install -m 644 libjackoss.h %{buildroot}/%{_includedir}
ln -s libjackasyn.so.%{version} %{buildroot}/%{_libdir}/libjackasyn.so.0
ln -s libjackasyn.so.%{version} %{buildroot}/%{_libdir}/libjackasyn.so
install -m 755 jacklaunch %{buildroot}/%{_bindir}
install -m 0644 jacklaunch.1 %{buildroot}/%{_mandir}/man1

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README AUTHORS CHANGELOG TODO WORKING
%{_bindir}/jacklaunch
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a

