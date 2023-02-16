#
# Conditional build:
%bcond_with    doxygen	# doxygen+dot based documentation
%bcond_with    check	# testing
%bcond_without openssl	# TLS support via OpenSSL
%bcond_with    sigcomp	# with Sofia SigComp [Nokia proprietary?]
#
Summary:	Sofia SIP User-Agent library
Summary(pl.UTF-8):	Biblioteka agenta użytkownika Sofia SIP
Name:		sofia-sip
Version:	1.13.13
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/freeswitch/sofia-sip/releases
Source0:	https://github.com/freeswitch/sofia-sip/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	52802d92562e776d2eb14e38efbf0fcc
Patch0:		%{name}-link.patch
URL:		https://sofia-sip.sourceforge.net/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.7
%if %{with doxygen}
BuildRequires:	doxygen >= 1.3.4
BuildRequires:	graphviz >= 1.9
%endif
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libtool >= 1:1.4
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.7}
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
%if %{with sigcomp}
BuildRequires:	sofia-sigcomp-devel >= 2.5.0
Requires:	sofia-sigcomp >= 2.5.0
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	__cxx

%description
Sofia SIP is a RFC-3261-compliant library for SIP user agents and
other network elements.

%description -l pl.UTF-8
Sofia SIP to zgodna z RFC-3261 biblioteka dla agentów użytkownika SIP
i innych elementów sieciowych.

%package devel
Summary:	Sofia-SIP Development Package
Summary(pl.UTF-8):	Pakiet programistyczny Sofia-SIP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.0
%{?with_openssl:Requires:	openssl-devel >= 0.9.7}

%description devel
Development package for Sofia SIP UA library.

%description devel -l pl.UTF-8
Pakiet programistyczny dla biblioteki Sofia SIP UA.

%package static
Summary:	Sofia-SIP Development Package - static library
Summary(pl.UTF-8):	Statyczna biblioteka Sofia-SIP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static library for Sofia SIP UA library.

%description static -l pl.UTF-8
Statyczna biblioteka Sofia SIP UA.

%package utils
Summary:	Sofia-SIP utils
Summary(pl.UTF-8):	Narzędzia Sofia-SIP
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}

%description utils
Command line utilities for Sofia SIP UA library.

%description utils -l pl.UTF-8
Działające z linii poleceń narzędzia do biblioteki Sofia SIP UA.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env awk,/bin/awk,' \
	libsofia-sip-ua/msg/msg_parser.awk \
	libsofia-sip-ua/su/tag_dll.awk

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-openssl%{!?with_openssl:=no} \
	--with-sigcomp%{!?with_sigcomp:=no}

%{__make} \
	SOFIA_SILENT=

%{?with_check:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_bindir}/addrinfo
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsofia-sip-ua*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHTS ChangeLog ChangeLog.ext-trees README RELEASE
%attr(755,root,root) %{_libdir}/libsofia-sip-ua.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsofia-sip-ua.so.0
%attr(755,root,root) %{_libdir}/libsofia-sip-ua-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsofia-sip-ua-glib.so.3
%{_datadir}/sofia-sip

%files devel
%defattr(644,root,root,755)
%doc TODO README.developers %{?with_doxygen:docs/*}
%attr(755,root,root) %{_libdir}/libsofia-sip-ua.so
%attr(755,root,root) %{_libdir}/libsofia-sip-ua-glib.so
%{_includedir}/sofia-sip-1.13
%{_pkgconfigdir}/sofia-sip-ua.pc
%{_pkgconfigdir}/sofia-sip-ua-glib.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libsofia-sip-ua.a
%{_libdir}/libsofia-sip-ua-glib.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/localinfo
%attr(755,root,root) %{_bindir}/sip-date
%attr(755,root,root) %{_bindir}/sip-dig
%attr(755,root,root) %{_bindir}/sip-options
%attr(755,root,root) %{_bindir}/stunc
