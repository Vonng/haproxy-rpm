%define haproxy_user    haproxy
%define haproxy_group   %{haproxy_user}
%define haproxy_home    %{_localstatedir}/lib/haproxy

%define dist %{expand:%%(/usr/lib/rpm/redhat/dist.sh --dist)}


%global _hardened_build 1

Summary: HA-Proxy reverse proxy for high availability environments
Name: haproxy
Version: %{version}
Release: %{release}%{?dist}
License: GPLv2+
Group: System Environment/Daemons
URL: http://www.haproxy.org/
Source0: http://www.haproxy.org/download/%{mainversion}/src/%{name}-%{version}.tar.gz
Source1: %{name}.cfg
Source2: %{name}.service
BuildRoot: %{_tmppath}/%{name}-%{version}-root

BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: make
BuildRequires: gcc openssl-devel
BuildRequires: openssl-devel

Requires(pre):      shadow-utils
BuildRequires:      systemd-units
BuildRequires:      systemd-devel
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
HA-Proxy is a TCP/HTTP reverse proxy which is particularly suited for high
availability environments. Indeed, it can:
- route HTTP requests depending on statically assigned cookies
- spread the load among several servers while assuring server persistence
  through the use of HTTP cookies
- switch to backup servers in the event a main one fails
- accept connections to special ports dedicated to service monitoring
- stop accepting connections without breaking existing ones
- add/modify/delete HTTP headers both ways
- block requests matching a particular pattern

It needs very little resource. Its event-driven architecture allows it to easily
handle thousands of simultaneous connections on hundreds of instances without
risking the system's stability.

https://github.com/philyuchkoff/HAProxy-2-RPM-builder

%prep
%setup -q

# We don't want any perl dependecies in this RPM:
%define __perl_requires /bin/true

%build
regparm_opts=
regparm_opts="USE_REGPARM=1"
RPM_BUILD_NCPUS="`/usr/bin/nproc 2>/dev/null || /usr/bin/getconf _NPROCESSORS_ONLN`";

# Default opts
systemd_opts=
pcre_opts="USE_PCRE=1"
USE_TFO=
USE_NS=
systemd_opts="USE_SYSTEMD=1"
pcre_opts="USE_PCRE=1 USE_PCRE_JIT=1"
USE_TFO=1
USE_NS=1


USE_PROMETHEUS="EXTRA_OBJS=addons/promex/service-prometheus.o"
%{__make} -j$RPM_BUILD_NCPUS %{?_smp_mflags} ${USE_LUA} CPU="generic" TARGET="linux-glibc" ${systemd_opts} ${pcre_opts} USE_OPENSSL=1 USE_ZLIB=1 ${regparm_opts} ADDINC="%{optflags}" USE_LINUX_TPROXY=1 USE_THREAD=1 USE_TFO=${USE_TFO} USE_NS=${USE_NS} ${USE_PROMETHEUS} ADDLIB="%{__global_ldflags}"
%{__make} admin/halog/halog OPTIMIZE="%{optflags} %{__global_ldflags}"
pushd admin/iprange
%{__make} iprange OPTIMIZE="%{optflags} %{__global_ldflags}"
popd

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_sbindir}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{__install} -d %{buildroot}%{_mandir}/man1/
%{__install} -s %{name} %{buildroot}%{_sbindir}/
%{__install} -c -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/haproxy.cfg
%{__install} -c -m 644 doc/%{name}.1 %{buildroot}%{_mandir}/man1/
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -s %{name} %{buildroot}%{_sbindir}/


%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%pre
getent group %{haproxy_group} >/dev/null || \
       groupadd -g 188 -r %{haproxy_group}
getent passwd %{haproxy_user} >/dev/null || \
       useradd -u 188 -r -g %{haproxy_group} -d %{haproxy_home} \
       -s /sbin/nologin -c "%{name}" %{haproxy_user}
exit 0


%files
%defattr(-,root,root)
%doc CHANGELOG README examples/*.cfg doc/architecture.txt doc/configuration.txt doc/intro.txt doc/management.txt doc/proxy-protocol.txt
%license LICENSE
%doc %{_mandir}/man1/*
%dir %{_sysconfdir}/%{name}
%attr(0755,root,root) %{_sbindir}/%{name}
%attr(-,root,root) %{_unitdir}/%{name}.service
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.cfg
