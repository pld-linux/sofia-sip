# Bconds:
%bcond_with    doxygen # Generate documents using doxygen and dot
%bcond_with    check   # Run tests
%bcond_without openssl # No OpenSSL (TLS)
%bcond_with    sigcomp # with Sofia SigComp
#
Summary:	Sofia SIP User-Agent library
Name:		sofia-sip
Version:	1.11.4
Release:	1
License:	LGPL 2.1
Group:		Libraries
URL:		http://sf.net/projects/sofia-sip
Source0:	%{name}-%{version}.tar.gz
%if %{with doxygen}
BuildRequires: doxygen >= 1.3.4
BuildRequires: graphviz >= 1.9
%endif
%{?with_openssl:BuildRequires: openssl-devel >= 0.9.7}
%if %{with sigcomp}
BuildRequires: sofia-sigcomp-devel >= 2.5.0
Requires: sofia-sigcomp >= 2.5.0
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_includedir	%{_prefix}/include/sofia-sip

%description
Sofia SIP is a RFC-3261-compliant library for SIP user agents and
other network elements.

%package	devel
Summary:        Sofia-SIP Development Package
Group:     	Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description	devel
Development package for Sofia SIP UA library.

%package	static
Summary:        Sofia-SIP Development Package - static library
Group:     	Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description	static
Static library for Sofia SIP UA library.

%package	utils
Summary:        Sofia-SIP utils
Group:     	?
Requires:	sofia-sip = %{version}-%{release}

%description	utils
Command line utilities for Sofia SIP UA library.

%prep
%setup -q

%build
%configure \
	--with%{!?with_openssl:out}-openssl \
	--with%{!?with_sigcomp:out}-sigcomp 
	
%{__make}
%{?with_check:make check}
%{?with_doxygen:make check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_bindir}/addrinfo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHTS README RELEASE ChangeLog
%attr(755,root,root) %{_libdir}/libsofia-sip-ua.so.*.*

%files devel
%defattr(644,root,root,755)
%doc TODO README.developers
%{?with_doxygen:docs/*}
%{_aclocaldir}/*.m4
%{_includedir}/sofia-sip
%{_libdir}/sofia
%{_libdir}/libsofia-sip-ua.la
%{_libdir}/libsofia-sip-ua.so
%{_pkgconfigdir}/%{name}-ua.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libsofia-sip-ua.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nua_cli
%attr(755,root,root) %{_bindir}/localinfo
%attr(755,root,root) %{_bindir}/sip-options
%attr(755,root,root) %{_bindir}/sip-date
