Summary:        Usermode tools for VmWare virts
Name:           open-vm-tools
Version:        10.0.5
Release:        4%{?dist}
License:        LGPLv2+
URL:            https://github.com/vmware/open-vm-tools
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/vmware/open-vm-tools/archive/%{name}-%{version}.tar.gz
%define sha1 open-vm-tools=9d29a17cce539b032317d0a8c55977666daa137e
Source1:        gosc-scripts.tar.gz
%define sha1 gosc-scripts=a87bb5b95f78923ac6053513b3364a119795a5d0
Source2:        vmtoolsd.service
Source3:        vgauthd.service
Patch0:         open-vm-tools-service-link.patch
Patch1:         open-vm-tools-GOSC-photon.patch
Patch2:         GOSC-VCA.patch
Patch3:         GOSC-return-code.patch
Patch4:         GOSC-NFS-MOUNT.patch
Patch5:         skipreboot.patch
Patch6:         GOSC-counterBug.patch
Patch7:         LighwaveHostPatch.patch
Patch8:         GOSC-ssh-support.patch
Patch9:         GOSC-vcenter-photon.patch
Patch10:        GOSC-preserve-network-onboot.patch
BuildRequires:  glib-devel
BuildRequires:  xerces-c-devel
BuildRequires:  xml-security-c-devel
BuildRequires:  libdnet
BuildRequires:  libmspack
BuildRequires:  Linux-PAM
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  fuse-devel
BuildRequires:  systemd
Requires:       fuse
Requires:       xerces-c
Requires:       libdnet
Requires:       libmspack
Requires:       glib
Requires:       xml-security-c
Requires:       openssl
Requires:       systemd
%description
VmWare virtualization user mode tools
%prep
%setup -q
%setup -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p1
%patch6 -p0
%patch7 -p0
%patch8 -p0
%patch9 -p0
%patch10 -p0
%build
touch ChangeLog
autoreconf -i
sh ./configure --prefix=/usr --without-x --without-kernel-modules --without-icu --disable-static
make %{?_smp_mflags}
%install

#collecting hacks to manually drop the vmhgfs module
install -vdm 755 %{buildroot}/lib/systemd/system
install -vdm 755 %{buildroot}/usr/share/open-vm-tools/GOSC/
cp -r gosc-scripts %{buildroot}/usr/share/open-vm-tools/GOSC
install -p -m 644 %{SOURCE2} %{buildroot}/lib/systemd/system
install -p -m 644 %{SOURCE3} %{buildroot}/lib/systemd/system

make DESTDIR=%{buildroot} install
rm -f %{buildroot}/sbin/mount.vmhgfs
mkdir -p %{buildroot}/etc/pam.d
mv %{buildroot}/usr/etc/pam.d/* %{buildroot}/etc/pam.d/
rmdir %{buildroot}/usr/etc/pam.d
chmod -x %{buildroot}/etc/pam.d/vmtoolsd
# Move vm-support to /usr/bin
mv %{buildroot}%{_sysconfdir}/vmware-tools/vm-support %{buildroot}%{_bindir}

%post
/sbin/ldconfig
%systemd_post vgauthd.service
%systemd_post vmtoolsd.service

%preun
%systemd_preun vmtoolsd.service
%systemd_preun vgauthd.service
# Tell VMware that open-vm-tools is being uninstalled
if [ "$1" = "0" -a                      \
     -e %{_bindir}/vmware-checkvm -a    \
     -e %{_bindir}/vmware-rpctool ] &&  \
     %{_bindir}/vmware-checkvm &> /dev/null; then
   %{_bindir}/vmware-rpctool 'tools.set.version 0' &> /dev/null || /bin/true
fi

%postun 
/sbin/ldconfig
%systemd_postun_with_restart vmtoolsd.service
%systemd_postun_with_restart vgauthd.service

%files 
%defattr(-,root,root)
%{_libdir}/open-vm-tools/plugins/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_bindir}/*
%{_sysconfdir}/*
%{_datadir}/*
/lib/*
%{_sbindir}/*


%changelog
*       Tue Feb 09 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 10.0.5-4
-       Preserve network onboot config.
*       Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> 10.0.5-3
-       Add vgauthd service.
*       Tue Feb 02 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-2
-       Making interface file name according to convention.
*       Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 10.0.5-1
-       Upgrade version.
*       Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 10.0.0-13
-       Edit post script.
*       Fri Nov 27 2015 Sharath George <sharathg@vmware.com> 10.0.0-12
-       Correcting path of pam file.
*       Tue Sep 15 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-11
-       Adding ssh RSA public support for password-less login.
*       Wed Sep 09 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-10
-       Adding option to modify /etc/hosts for lightwave on optional basis.
*       Wed Sep 09 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-9
-       Fixing once in while issue related to customization failure.
*       Wed Sep 02 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-8
-       Fixing systemd cloud-init and GOSC cloud-init race.
*       Tue Sep 01 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-7
-       Fixing GOSC counter bug.
*       Wed Aug 26 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-6
-       Avoiding reboot after successful customization.
*       Tue Aug 25 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-5
-       Adding support for NFS mount in GOSC scripts.
*       Thu Aug 20 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-4
-       Fixing GOSC-libdeploy return code problem.
*       Thu Aug 13 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-3
-       Combining all GOSC patches and adding support for lightwave.
*       Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 10.0.0-2
-       Build with fuse support.
*       Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 10.0.0-1
-       Update version to 10.0.0.
*       Tue Aug 11 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-7
-       VCA initial login password issue fix.
*       Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-6
-       Adding preun and post install commands.
*       Thu Jul 30 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-5
-       Adding Blob configuation support to GOSC scripts.
*       Thu Jul 09 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-4
-       Fixing GOSC to work on VCA.
*       Tue Apr 21 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-3
-       Adding guest optimizations support for photon.
*       Tue Apr 21 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.0-2
-       Added open-vm-tools-stderr_r-fix upstream patch and removed glibc patch.
*       Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 9.10.0-1
-       Initial version
