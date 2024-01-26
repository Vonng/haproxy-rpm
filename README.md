# RPM builder for HAProxy 2.8 (CentOS 7/8/9)

Build latest haproxy binary with prometheus metrics support

![GitHub last commit](https://img.shields.io/github/last-commit/Vonng/pigsty?style=for-the-badge)
![GitHub All Releases](https://img.shields.io/github/downloads/Vonng/pigsty/total?style=for-the-badge)

[Download](https://github.com/Vonng/haproxy-rpm/releases/tag/v2.9.3) latest v2.9.3 rpm for EL7 | EL8 | EL9

Original Repo: [philyuchkoff/HAProxy-2-RPM-builder](https://github.com/philyuchkoff/HAProxy-2-RPM-builder)



### [HAProxy](http://www.haproxy.org/) 2.9.3 2024/01/18

Perform the following steps on a build box as a regular user:

```bash
yum -y groupinstall 'Development Tools'
yum install -y pcre-devel make gcc openssl-devel rpm-build systemd-devel wget sed zlib-devel

cd /opt
git clone https://github.com/Vonng/haproxy-rpm
cd ./haproxy-rpm
make build
```


## Manual Build

<details>

```bash
cd /opt ; tar -xf haproxy-rpm.tar.gz ; cd haproxy-rpm
rm -rf rpmbuild/SOURCES ; mkdir -p rpmbuild/SOURCES ; cp -r ./SOURCES/* ./rpmbuild/SOURCES/
rm -rf rpmbuild/SPECS ; mkdir -p rpmbuild/SPECS ; cp -r ./SPECS/* ./rpmbuild/SPECS/

rpmbuild --nodebuginfo -ba SPECS/haproxy.spec \
	--define "mainversion 2.8" \
	--define "version 2.9.3" \
	--define "release 1" \
	--define "_topdir %(pwd)/rpmbuild" \
	--define "_builddir %{_topdir}/BUILD" \
	--define "_buildroot %{_topdir}/BUILDROOT" \
	--define "_rpmdir %{_topdir}/RPMS" \
	--define "_srcrpmdir %{_topdir}/SRPMS" \
	--define "_use_lua 0" \
	--define "_use_prometheus 1"

cp -f rpmbuild/RPMS/x86_64/haproxy-* /tmp/
```

</details>