Summary:    Docker
Name:       docker
Version:    1.10.2
Release:    1%{?dist}
License:    ASL 2.0
URL:        http://docs.docker.com
Group:      Applications/File
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:	https://get.docker.com/builds/Linux/x86_64/%{name}-%{version}.tgz 
%define sha1 docker=852e82ae0057f17c9a965569989abe92d0ea1606

BuildRequires:  systemd
Requires:       systemd

%description
Docker is a platform for developers and sysadmins to develop, ship and run applications.
%prep
%setup -qn usr
%build
%install
install -vdm755 %{buildroot}/usr/bin
mv -v local/bin/* %{buildroot}/usr/bin/
chmod +x %{buildroot}/usr/bin/docker
install -vd %{buildroot}/lib/systemd/system

cat > %{buildroot}/lib/systemd/system/docker.service <<- "EOF"
[Unit]
Description=Docker Daemon
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=/bin/docker daemon -s overlay
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=always
MountFlags=slave
LimitNOFILE=1048576
LimitNPROC=1048576
LimitCORE=infinity

[Install]
WantedBy=multi-user.target

EOF

%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%preun
/bin/systemctl disable docker.service

%post
/sbin/ldconfig
#/bin/systemctl enable docker.service

%postun	-p /sbin/ldconfig


%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}
/lib/systemd/system/docker.service
%changelog
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10.2-1
-   Upgraded to version 1.10.2
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  1.9.0-2
-   Add systemd to Requires and BuildRequires.
-   Use systemctl to enable/disable service.
*   Fri Nov 06 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.9.0-1
-   Update to version 1.9.0
*   Mon Aug 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.1-1
-   Update to new version 1.8.1.
*   Fri Jun 19 2015 Fabio Rapposelli <fabio@vmware.com> 1.7.0-1
-   Update to new version.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.6.0-3
-   Update according to UsrMove.
*	Fri May 15 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.0-2
-	Updated to version 1.6
*	Mon Mar 4 2015 Divya Thaluru <dthaluru@vmware.com> 1.5.0-1
-	Initial build.	First version
