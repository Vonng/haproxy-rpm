# RPM builder for HAProxy 2.5 (CentOS 7)

Build latest haproxy binary with prometheus metrics support

* Original Repo: [philyuchkoff/HAProxy-2-RPM-builder](https://github.com/philyuchkoff/HAProxy-2-RPM-builder)


![GitHub last commit](https://img.shields.io/github/last-commit/Vonng/pigsty?style=for-the-badge)
![GitHub All Releases](https://img.shields.io/github/downloads/Vonng/pigsty/total?style=for-the-badge)

### [HAProxy](http://www.haproxy.org/) 2.5.7 2022/05/13

Perform the following steps on a build box as a regular user:


```bash
sudo yum -y groupinstall 'Development Tools'
cd /opt
sudo git clone https://github.com/Vonng/haproxy-rpm
cd ./haproxy-rpm
make build
```
