Name:           confd
Version:        0.16.0
Release:        2%{?dist}
Summary:        Manage local application configuration files using templates and data from etcd or consul

Group:          System Environment/Daemons
License:        MPLv2.0
URL:            http://www.confd.io
Source0:        https://github.com/kelseyhightower/confd/releases/download/v%{version}/confd-%{version}-linux-amd64
Source1:        %{name}.sysconfig
Source2:        %{name}.service
Source3:        %{name}.init
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
BuildRequires:  systemd-units
Requires:       systemd
%endif

%description
Manage local application configuration files using templates and data from etcd or consul

%prep
mkdir -p %{buildroot}
cd %{buildroot}
rm -rf 'confd-%{version}'
/usr/bin/mkdir -p confd-%{version}
cd 'confd-%{version}'
pwd
cp %{_sourcedir}/confd-%{version}-linux-amd64 .
/usr/bin/chmod -Rf a+rX,u+w,g-w,o-w .

%install
mkdir -p %{buildroot}/%{_bindir}
cp %{SOURCE0} %{buildroot}/%{_bindir}/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/conf.d
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/templates
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
mkdir -p %{buildroot}/%{_unitdir}
cp %{SOURCE2} %{buildroot}/%{_unitdir}/
%else
mkdir -p %{buildroot}/%{_initrddir}
cp %{SOURCE3} %{buildroot}/%{_initrddir}/confd
%endif

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%else
%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/conf.d
%{_sysconfdir}/%{name}/templates
%{_sysconfdir}/sysconfig/%{name}
%{_sharedstatedir}/%{name}
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%attr(755, root, root) %{_bindir}/confd

%doc



%changelog
* Fri Dec 6 2018 Jean-Sébastien Frerot <jean-sebastien@frerot.me>
- Create and use conf.d by default in /etc/confd
- Add templates folder in /etc/confd/
* Thu Dec 5 2018 Jean-Sébastien Frerot <jean-sebastien@frerot.me>
- Fix Non working part of the spec file
* Fri Jan 16 2015 Michael Chapman <michchcap@cisco.com>
- Initial
