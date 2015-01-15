RPM Spec for Confd
======================

Tries to follow the [packaging guidelines](https://fedoraproject.org/wiki/Packaging:Guidelines) from Fedora.

* Binary: `/usr/bin/confd`
* Config: `/etc/confd/`
* Sysconfig: `/etc/sysconfig/confd`

To Build
---------

To build the RPM (non-root user):

1. Check out this repo
2. Install rpmdevtools and mock 

    ```
    sudo yum install rpmdevtools mock
    ```
3. Set up your rpmbuild directory tree

    ```
    rpmdev-setuptree
    ```
4. Link the spec file and sources from the repository into your rpmbuild/SOURCES directory

    ```
    ln -s ${repo}/SPECS/confd.spec rpmbuild/SPECS/
    ln -s ${repo}/SOURCES/* rpmbuild/SOURCES/
    ```
5. Download remote source files

    ```
    spectool -g -R rpmbuild/SPECS/confd.spec
    ```
6. Build the RPM

    ```
    rpmbuild -ba rpmbuild/SPECS/confd.spec
    ```

To run
---------------

1. Install the rpm
2. Put config files in `/etc/confd/`
3. Start the service and tail the logs `systemctl start confd.service` and `journalctl -f`
  * To enable at reboot `systemctl enable confd.service`

More info
---------
See the [confd.io](http://www.confd.io) website.
