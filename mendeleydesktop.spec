Name:       mendeleydesktop
Version:    1.17
# Make sure to use rpmdev-bumpspec to update this
Release:    1%{?dist}
Summary:    Unofficial Mendeley RPM package

%ifarch %{ix86}
%define pkg_arch i486
%else
%define pkg_arch %{_target_cpu}
%endif

#Group:
License:       Proprietary
URL:           https://github.com/hmaarrfk/mendeley-rpm
Source0:       README.md
Source1:       http://desktop-download.mendeley.com/download/linux/%{name}-%{version}-linux-i486.tar.bz2
Source2:       http://desktop-download.mendeley.com/download/linux/%{name}-%{version}-linux-x86_64.tar.bz2
Patch0:        mendeleydesktop-desktopfile.patch
BuildRequires: desktop-file-utils

ExclusiveArch: x86_64 %{ix86}


%description
This is a repackaged version of what is available
on the Mendeley website and attempts to make use
of system libraries instead of the ones packaged
with Mendeley.

%package devel
Summary: Development files for mendeleydesktop
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
Development files for mendeleydesktop.

%global debug_package %{nil}


%prep
%setup -q -n %{name}-%{version}-linux-%{pkg_arch} -T -b 1 -b 2
cp -p %SOURCE0 .
%patch0
ls -lah

# sensitive line
# rather unecessary and may cause things to break in future versions
# sed -i 's/install-mendeley/echo\d0ll-mendeley/' lib/mendeleydesktop/libexec/mendeleydesktop.%{ _target_cpu }



%build
# Remove unecessary libs
rm -rf lib/qt
rm -rf lib/ssl
rm -rf lib/cpp

# Remove the launching script not used in this distribution
rm -f  bin/mendeleydesktop
# and the stupid link-handler
# TODO: emulate link handler functionality in the spec file
rm -f  bin/install-mendeley-link-handler.sh

# Rename binary and move it to the proper location
mv     lib/mendeleydesktop/libexec/mendeleydesktop.%{pkg_arch} bin/mendeleydesktop

# Remove the problematic icons 48x48 and 64x64 look bad because they have a white border
rm  -rf share/icons/hicolor/48x48
rm  -rf share/icons/hicolor/64x64

# Remove libexec including the Updater binary
# Update should be done using the package manager
rm -rf lib/mendeleydesktop/libexec

# Change them as executable so that the packager treats them as such
# The packager consideres executable libraries as libraries the package provides
chmod +x lib/libPDFNetC.*
chmod +x lib/libMendeley.*


%install
mkdir -p %{buildroot}%{_defaultdocdir}
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}-%{version}
mkdir -p %{buildroot}%{_datadir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}

cp -R share/doc/%{name}/*    %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -R README.md             %{buildroot}%{_defaultdocdir}/%{name}-%{version}/README-DIST.md
cp -R share/icons           %{buildroot}%{_datadir}
cp -R share/mendeleydesktop %{buildroot}%{_datadir}
cp -R lib/*                 %{buildroot}%{_libdir}
cp -R bin/*                 %{buildroot}%{_bindir}

desktop-file-install --delete-original          \
--dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
share/applications/mendeleydesktop.desktop


%clean
rm -rf %{buildroot}


%post
# Update shared libraries
/sbin/ldconfig

/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
# Update shared libraries
/sbin/ldconfig

/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc %{_defaultdocdir}/%{name}-%{version}
%{_bindir}/*
%{_libdir}/libPDFNetC.so
%{_libdir}/*.so.*
%{_libdir}/mendeleydesktop
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/*

%files devel
%{_libdir}/libMendeley.so


# Make sure to use rpmdev-bumpspec to update this
%changelog
* Tue Oct 18 2016 Mark Harfouche <mark.harfouche@gmail.com> - 1.17
- Updated to Mendeley 1.17

* Mon Apr 25 2016 Mark Harfouche <mark.harfouche@gmail.com> - 1.16.1-2
- More compliant with rpmlint

* Wed Apr 6 2016 Mark Harfouche <mark.harfouche@gmail.com> - 1.16.1
- Updated to Mendeley 1.16.1

* Mon Feb 22 2016 Mark Harfouche <mark.harfouche@gmail.com> - 1.15.3
- Updated to Mendeley 1.15.3

* Tue Dec 8 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.15.2
- Updated to Mendeley 1.15.2

* Wed Oct 14 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.15
- Updated to Mendeley 1.15

* Wed Jul 08 2015 Mark Harfouche <mark.harfouche@gmail.com> - 1.14-2
- modified the patch, they changed the exec string

* Wed Jul 8 2015 Mark Harfouche - 1.14-1
- Updated to Mendeley 1.14

* Fri Apr 10 2015 Mark Harfouche - 1.13.8-1
- Updated to Mendeley 1.13.8

* Tue Mar 31 2015 Mark Harfouche - 1.13.6-1
- Updated to Mendeley 1.13.6

* Wed Mar 04 2015 Alexander Korsunsky <fat.lobyte9@gmail.com> - 1.13.4-2
- Allow building in Mock

* Mon Feb 23 2015 Alexander Korsunsky <fat.lobyte9@gmail.com> - 1.13.4-1
- Updated to Mendeley 1.13.4

* Mon Jan 12 2015 Mark Harfouche - 1.12.4-1
- Updated to Mendeley 1.12.4

* Tue Sep 02 2014 Mark Harfouche - 1.12.1-1
- Updated to Mendeley 1.12.1

* Wed Oct 9 2013 Mark Harfouche - 1.10.1-1
- Updated to Mendeley 1.10.1

* Wed Aug 14 2013 Mark Harfouche - 1.9.2-1
- Updated to Mendeley 1.9.2

* Sun Jul 14 2013 Mark Harfouche - 1.9.1-18
- Commented out the sensitive line

* Sun Jul 14 2013 Mark Harfouche - 1.9.1-17
- Moved the modification of the binary to the prep section like the other patch

* Sun Jul 14 2013 Mark Harfouche - 1.9.1-16
- Touched up the files section so as not to include other programs directories

* Sun Jul 14 2013 Mark Harfouche - 1.9.1-15
- Changed the mendeley binary to inhibit the execution of the link-handler
  script.

* Sun Jul 14 2013 Mark Harfouche - 1.9.1-14
- Fixed the location of the documentation

* Sun Jul 14 2013 Mark Harfouche - 1.9.1-13
- Added the /sbin/ldconfig lines to the post and postrun sections

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-12
- Spec file should be i686 compatible

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-11
- Removed the 48x48 and 64x64 icons because they looked bad (they used white
  instead of alpha making them look horrible)

* Sat Jul 13 2013 Filipe Manco - 1.9.1-10
- Cleanup spec file.

* Sat Jul 13 2013 Filipe Manco - 1.9.1-9
- Greatly simplify spec file.

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-8
- Fixed the .desktop file so that it would have the option --unix-distro-build
  at the end of the exec command

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-7
- I dont think we need the dummy launcher, mendeley seems to run well without
  it, so I moved the executable from libexec to bin

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-6
- Changed the name of the desktopfile to reflect the correct name of the wmclass

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-5
- Removed the explicit dependencies since I think the packager finds them
  automatically

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-4
- Changed the libexec name to mendeleydestop as suggested in Revision 2 but
  added the appropriate modifications to the spec file.

* Sat Jul 13 2013 Mark Harfouche - 1.9.1-3
- Undid the modifications of the previous version

* Fri Jul 12 2013 Filipe Manco - 1.9.1-2
- Binary use mendeleydesktop instead of mendelydesktop.x86_64

* Fri Jul 12 2013 Filipe Manco - 1.9.1-1
- Update to Mendeley version 1.9.1

* Sun Apr 7 2013 Chris Fallin - 1.8.4-1
- Updated to Mendeley version 1.8.4

* Thu Mar 21 2013 Chris Fallin - 1.8.3-1
- Updated to Mendeley version 1.8.3

* Wed Mar 13 2013 Mark Harfouche - 1.8.2-2
- Cleaned up the spec file

* Wed Mar 13 2013 Chris Fallin - 1.8.2-1
- Updated to Mendeley version 1.8.2

* Thu Jan 31 2013 Mark Harfouche - 1.8.0-1
- Updated to Mendeley version 1.8.0

* Tue Jan 22 2013 Mark Harfouche - 0.1.0-2
- Fixed the dependency for libpng.so.3


