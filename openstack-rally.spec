%global project rally
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:             openstack-%{project}
Version:          XXX
Release:          XXX
Summary:          Benchmarking System for OpenStack

License:          ASL 2.0
URL:              http://wiki.openstack.org/wiki/Rally
Source0:          https://tarballs.openstack.org/rally/rally-%{upstream_version}.tar.gz

BuildArch:        noarch

BuildRequires:    git
BuildRequires:    python2-devel
BuildRequires:    python-pbr
BuildRequires:    python-setuptools
# BuildRequires for oslo-config-generators
BuildRequires:    python-oslo-config >= 2:3.14.0
BuildRequires:    python-oslo-log >= 1.14.0
BuildRequires:    python-decorator
BuildRequires:    python-oslo-db >= 4.10.0
BuildRequires:    python-jsonschema
BuildRequires:    python-novaclient >= 2.29.0
BuildRequires:    python-keystoneclient
BuildRequires:    python-neutronclient >= 5.1.0
BuildRequires:    python-glanceclient >= 2.3.0
BuildRequires:    python-saharaclient >= 0.18.0
BuildRequires:    python-paramiko
BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx
BuildRequires:    python-os-faults
BuildRequires:    python-subunit

Requires:         python-alembic >= 0.8.4
Requires:         python-boto
Requires:         python-decorator
Requires:         python-jinja2
Requires:         python-jsonschema
Requires:         python-netaddr
Requires:         python-oslo-config >= 2:3.14.0
Requires:         python-oslo-db >= 4.15.0
Requires:         python-oslo-i18n >= 2.1.0
Requires:         python-oslo-log >= 3.11.0
Requires:         python-oslo-serialization >= 1.19.0
Requires:         python-oslo-utils >= 3.18.0
Requires:         python-paramiko
Requires:         python-prettytable
Requires:         PyYAML
Requires:         python-gnocchiclient >= 2.7.0
Requires:         python-keystoneauth1 >= 2.18.0
Requires:         python-mistralclient >= 2.0.0
Requires:         python-glanceclient >= 1:2.5.0
Requires:         python-keystoneclient
Requires:         python-novaclient >= 1:6.0.0
Requires:         python-neutronclient >= 5.1.0
Requires:         python-cinderclient
Requires:         python-heatclient
Requires:         python-ceilometerclient
Requires:         python-ironicclient
Requires:         python-saharaclient >= 1.1.0
Requires:         python-swiftclient >= 3.2.0
Requires:         python-zaqarclient
Requires:         python-requests >= 2.10.0
Requires:         python-subunit
Requires:         python-sqlalchemy
Requires:         python-six >= 1.9.0
Requires:         python-sphinx
Requires:         python-os-faults

%description
Rally is a benchmarking tool capable of performing specific,
complex and reproducible test cases on real deployment scenarios.

%if 0%{?with_doc}
%package doc
Summary:    Documentation for OpenStack Rally

Requires:       %{name} = %{version}-%{release}

BuildRequires:  python-oslo-utils
BuildRequires:  python-prettytable
BuildRequires:  PyYAML
BuildRequires:  python-subunit
BuildRequires:  python-boto

%description doc
Rally is a benchmarking tool capable of performing specific,
complex and reproducible test cases on real deployment scenarios.

This package contains documentation files for Rally.
%endif

%prep
%autosetup -S git -n %{project}-%{upstream_version}

rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build

# for Documentation
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d
mv %{buildroot}/usr/etc/bash_completion.d/rally.bash_completion %{buildroot}/%{_sysconfdir}/bash_completion.d

# Generate tempest config
install -d -m 755 %{buildroot}%{_sysconfdir}/%{project}/
PYTHONPATH=. oslo-config-generator --config-file etc/rally/rally-config-generator.conf \
                      --output-file %{buildroot}%{_sysconfdir}/%{project}/rally.conf

# fix config permission
chmod 644 %{buildroot}%{_sysconfdir}/%{project}/rally.conf

# remove unnecessary files
rm -fr %{buildroot}%{python2_sitelib}/%{project}/deployment/engines/devstack
rm -fr %{buildroot}%{python2_sitelib}/%{project}/deployment/engines/lxc
rm -fr %{buildroot}%{python2_sitelib}/%{project}/deployment/serverprovider/providers/lxc

%files
%license LICENSE
%{python2_sitelib}/%{project}
%{python2_sitelib}/%{project}*.egg-info
%config(noreplace) %{_sysconfdir}/%{project}/%{project}.conf
%{_bindir}/%{project}
%{_bindir}/%{project}-manage
%{_sysconfdir}/bash_completion.d/rally.bash_completion

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog

