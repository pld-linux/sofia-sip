#
# Conditional build:
%bcond_with    doxygen	# Generate documents using doxygen and dot
%bcond_with    check	# Run tests
%bcond_without openssl	# No OpenSSL (TLS)
%bcond_with    sigcomp	# with Sofia SigComp
#
Summary:	Sofia SIP User-Agent library
Summary(pl.UTF-8):	Biblioteka agenta użytkownika Sofia SIP
Name:		sofia-sip
Version:	1.12.6
Release:	1
License:	LGPL 2.1
Group:		Libraries
Source0:	http://dl.sourceforge.net/sofia-sip/%{name}-%{version}.tar.gz
# Source0-md5:	8c24a9d58179f8fa7c7edd4af7dab104
URL:		http://sf.net/projects/sofia-sip/
%if %{with doxygen}
BuildRequires:	doxygen >= 1.3.4
BuildRequires:	graphviz >= 1.9
%endif
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.7}
%if %{with sigcomp}
BuildRequires:	sofia-sigcomp-devel >= 2.5.0
Requires:	sofia-sigcomp >= 2.5.0
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%build
%configure \
	--with%{!?with_openssl:out}-openssl \
	--with%{!?with_sigcomp:out}-sigcomp

%{__make}
%{?with_check:%{__make} check}
%{?with_doxygen:%{__make} check} # ???

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_bindir}/addrinfo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHTS README RELEASE ChangeLog
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_datadir}/sofia-sip

%files devel
%defattr(644,root,root,755)
%doc TODO README.developers %{?with_doxygen:docs/*}
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
