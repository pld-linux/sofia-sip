#
# Template for Sofia SIP UA RPM spec file
#
# Options:
# --with doxygen   - Generate documents using doxygen and dot
# --with check     - Run tests
# --without openssl - No OpenSSL (TLS)
# --with sigcomp   - with Sofia SigComp
#

Summary: Sofia SIP User-Agent library 
Name: sofia-sip
Version: 1.11.4
Release: 1%{?dist}
License: Lesser GNU Public License 2.1
Group: System Environment/Libraries
URL: http://sf.net/projects/sofia-sip
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Packager: Pekka.Pessi@Nokia.com

%{?_with_doxygen:BuildRequires: doxygen >= 1.3.4}
%{?_with_doxygen:BuildRequires: graphviz >= 1.9}
%{?!_without_openssl:BuildRequires: openssl-devel >= 0.9.7}

%{?_with_sigcomp:BuildRequires: sofia-sigcomp-devel >= 2.5.0}
%{?_with_sigcomp:Requires: sofia-sigcomp >= 2.5.0}

%description
Sofia SIP is a RFC-3261-compliant library for SIP user agents and other
network elements.

%prep
%setup -q -n sofia-sip-%{version}

%build
%configure --with-pic --enable-shared --disable-dependency-tracking --includedir=%{_prefix}/include/sofia-sip --with-aclocal=aclocal
#make %{_smp_mflags}
make 
%{?_with_check:make check}
%{?_with_doxygen:make check}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_prefix}/bin/addrinfo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libsofia-sip-ua.so
%{_prefix}/%{_lib}/libsofia-sip-ua.so.*
%doc AUTHORS COPYING COPYRIGHTS README

%package	devel
Summary:        Sofia-SIP Development Package
Group:     	Development/Libraries
Requires:	sofia-sip = %{version}-%{release}
Obsoletes:	sofia-devel
%description	devel
Development package for Sofia SIP UA library. This package includes 
%{?_with_doxygen:HTML documentation}, static libraries and include files.

%files devel
%defattr(-,root,root,-)
/usr/share/aclocal/sac-general.m4
/usr/share/aclocal/sac-su.m4
/usr/share/aclocal/sac-su2.m4
%{_prefix}/include/sofia-sip/*.h
%{_prefix}/include/sofia-sip/*.h.in
%{_prefix}/libexec/sofia/tag_dll.awk
%{_prefix}/libexec/sofia/msg_parser.awk
%{_prefix}/%{_lib}/libsofia-sip-ua.la
%{_prefix}/%{_lib}/libsofia-sip-ua.a
%{_prefix}/%{_lib}/pkgconfig/%{name}-ua.pc
%{?_with_doxygen:docs/*}
%doc TODO README.developers

%package	utils
Summary:        Sofia-SIP Development Package
Group:     	Development/Libraries
Requires:	sofia-sip = %{version}-%{release}
Obsoletes:	sofia-utils
%description	utils
Command line utilities for Sofia SIP UA library.

%files utils
%defattr(-,root,root,-)
%{_prefix}/bin/nua_cli
%{_prefix}/bin/localinfo
%{_prefix}/bin/sip-options
%{_prefix}/bin/sip-date

%changelog
* Thu Oct 20 2005 Pekka Pessi <Pekka.Pessi@nokia.com> - 1.11.4
- Using %{_lib} instead of lib

* Thu Oct  6 2005 Pekka Pessi <Pekka.Pessi@iki.fi> - 1.11.4
- Added sub-package utils

* Thu Oct  6 2005 Pekka Pessi <Pekka.Pessi@nokia.com> - 1.11.0
- Added %%{?dist} to release

* Sat Jul 23 2005 Pekka Pessi <Pekka.Pessi@nokia.com> - 1.10.1
- Initial build.
