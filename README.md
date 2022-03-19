# RPM builder for HAProxy 2.5 (CentOS 7)

Build latest haproxy binary with prometheus metrics support

* Original Repo: [philyuchkoff/HAProxy-2-RPM-builder](https://github.com/philyuchkoff/HAProxy-2-RPM-builder)

![GitHub last commit](https://img.shields.io/github/last-commit/philyuchkoff/HAProxy-2-RPM-builder?style=for-the-badge)
![GitHub All Releases](https://img.shields.io/github/downloads/Vonng/pigsty/total?style=for-the-badge)


### [HAProxy](http://www.haproxy.org/) 2.5.5 2022/03/14

Perform the following steps on a build box as a regular user:

    sudo yum -y groupinstall 'Development Tools'
    cd /opt
    sudo git clone https://github.com/philyuchkoff/HAProxy-2-RPM-builder.git
    cd ./HAProxy-2-RPM-builder

### Build:

    sudo make USE_PROMETHEUS=1


