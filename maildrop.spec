Name:		maildrop
Summary:	Maildrop mail filter/mail delivery agent
Version:	2.7.0
Release:	0%{?dist}
License:	GPLv3
Group:		System/Servers
Url:		http://www.courier-mta.org/maildrop/
Source0:	http://sourceforge.net/projects/courier/files/maildrop/2.7.0/%{name}-%{version}.tar.bz2
Source1:	mailfilter
Source2:	subscribeIMAP.sh
BuildRequires:  pcre-devel
BuildRequires:  libidn-devel
Obsoletes:	maildrop-toaster
BuildRoot:      %{_topdir}/BUILDROOT/%{name}-%{version}-%{release}.%{_arch}

%define debug_package %{nil}

#-------------------------------------------------------------
%package devel
#-------------------------------------------------------------
Summary:	Development tools for handling E-mail messages
Group:		Development/C
Requires:	%{name} >= %{version}-%{release}

#-------------------------------------------------------------
%description
#-------------------------------------------------------------
Maildrop  is a combination  mail  filter/mail  delivery agent.
Maildrop reads  the message  to be delivered  to your mailbox,
optionally reads instructions from a file  how filter incoming
mail, then based on these  instructions may deliver mail to an
alternate  mailbox,  or  forward  it,  instead of dropping the
message into your mailbox.

Maildrop uses a structured, real, meta-programming language in
order to define filtering instructions. Its basic features are
fast and efficient.  At sites which  carry a  light  load, the
more advanced, CPU-demanding,  features  can be  used to build
very  sophisticated  mail  filters.  Maildrop deployments have
been  reported  at  sites  that  support  as  many  as  30,000
mailboxes.

#-------------------------------------------------------------
%description devel
#-------------------------------------------------------------
The maildrop-devel package contains the  libraries and  header
files that can be  useful in  developing  software that  works
with or processes E-mail messages.

Install the maildrop-devel  package  if you  want  to  develop
applications which use or process E-mail messages.

#-------------------------------------------------------------
%prep
#-------------------------------------------------------------
%setup -q

export CC="gcc %{optflags}"
export CPPFLAGS="%{optflags}"

#-------------------------------------------------------------
# Configure
#-------------------------------------------------------------
%configure \
      --disable-authlib \
      --disable-tempdir \
      --enable-maildirquota \
      --enable-maildrop-uid=root \
      --enable-maildrop-gid=vchkpw \
      --with-devel \
      --without-db

#-------------------------------------------------------------
%build
#-------------------------------------------------------------

%{__make}

#-------------------------------------------------------------
%install
#-------------------------------------------------------------
rm -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot} 

find %{buildroot}%{_mandir} ! -type d -print | perl -e '
 while (<>)
  {
    $f=$_;  
    chop $f;
    next if $f =~ /\.gz$/;
    if (-l $f)
    {
        $f2=readlink($f);
        unlink($f);
        symlink "$f2.gz", "$f.gz";
    }
    else
    {
        system("gzip <$f >$f.gz");
        unlink($f);
    }
 } '

mkdir htmldoc
cp %{buildroot}%{_datadir}/maildrop/html/* htmldoc

mkdir -p %{buildroot}%{_localstatedir}/log/maildrop

install -D %{SOURCE1}  %{buildroot}%{_sysconfdir}/mail/mailfilter
install    %{SOURCE2}  %{buildroot}%{_bindir}/subscribeIMAP.sh

#-------------------------------------------------------------
%clean
#-------------------------------------------------------------
rm -rf %{buildroot}

#-------------------------------------------------------------
%files
#-------------------------------------------------------------
%defattr(-, bin, bin)
%{_datadir}/maildrop
%attr(0755,vpopmail,vchkpw) %dir %{_localstatedir}/log/maildrop
%attr(04755, root, vchkpw)       %{_bindir}/maildrop
%attr(0755, root, vchkpw)        %{_bindir}/lockmail
%attr(0755, root, vchkpw)        %{_bindir}/deliverquota
%attr(0755, root, vchkpw)        %{_bindir}/mailbot
%attr(0755, root, vchkpw)        %{_bindir}/maildirmake
%attr(0755, root, root)          %{_bindir}/makemime
%attr(0755, root, root)          %{_bindir}/reformime
%attr(0755, root, root)          %{_bindir}/reformail
%attr(0755, vpopmail, vchkpw)    %{_bindir}/subscribeIMAP.sh
%attr(0600, vpopmail, vchkpw)    %{_sysconfdir}/mail/mailfilter

%{_mandir}/man[1578]/*

%doc libs/maildir/README.imapkeywords.html
%doc libs/maildir/README.maildirfilter.html
%doc libs/maildir/README.maildirquota.html
%doc libs/maildir/README.maildirquota.txt
%doc libs/maildir/README.sharedfolders.html
%doc libs/maildir/README.sharedfolders.txt
%doc AUTHORS ChangeLog COPYING COPYING.GPL INSTALL
%doc maildroptips.txt README README.postfix NEWS UPGRADE
%doc htmldoc/*

#-------------------------------------------------------------
%files devel
#-------------------------------------------------------------
%defattr(-, bin, bin)
%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/*

#-------------------------------------------------------------
%changelog
#-------------------------------------------------------------
* Fri Nov 15 2013 Eric Shubert <eric@datamatters.us> 2.7.0-0.qt
- Migrated to repoforge
- Removed -toaster designation
- Added CentOS 6 support
- Removed unsupported cruft
- Updated to current upstream 2.7.0
- Adapted to Dovecot
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 2.0.3-1.3.8
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Wed Jun 10 2009 Jake Vickers <jake@qmailtoaster.com> 2.0.3-1.3.8
- Added Mandriva 2009 support
* Thu Apr 23 2009 Jake Vickers <jake@qmailtoaster.com> 2.0.3-1.3.7
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
* Sat Feb 14 2009 Jake Vickers <jake@qmailtoaster.com> 2.0.3-1.3.6
- Added Suse 11.1 support
* Mon Feb 09 2009 Jake Vickers <jake@qmailtoaster.com> 2.0.3-1.3.6
- Added Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 2.0.3-1.3.5
- Add CentOS 5 i386 support
- Add CentOS 5 x86_64 support
* Tue Jan 02 2007 Erik A. Espinoza <espinoza@kabewm.com> 2.0.3-1.3.4
- Upgraded to maildrop 2.0.3
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 2.0.2-1.3.3
- Added Fedora Core 6 support
* Sat Oct 28 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 2.0.2-1.3.2
- Included fixed mailfilter script from Mark Samples
* Mon Jun 05 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 2.0.2-1.3.1
- Upgraded to maildrop 2.0.2
- Added SuSE 10.1 support
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 1.8.1-1.2.11
- Add Fedora Core 5 support
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 1.8.1-1.2.10
- Add SuSE 10.0 and Mandrivs 2006.0 support
* Sat Oct 15 2005 Nick Hemmesch <nick@ndhsoft.com> 1.8.1-1.2.9
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 1.8.1-1.2.8
- Add CentOS 4 x86_64 support
* Thu Aug 25 2005 Nick Hemmesch <nick@ndhsoft.com> 1.8.1-1.2.7
- Change file permissions for qmailtoaster
- Add preconfigured message filtering
* Fri Jul 01 2005 Nick Hemmesch <nick@ndhsoft.com> 1.8.1-1.2.6
- Add Fedora Core 4 support
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 1.8.1-1.2.5
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
* Tue May 31 2005 Nick Hemmesch <nick@ndhsoft.com> 1.8.1-1.2.4
- Update to maildrop-1.8.1
- Update to support CentOS 4 and Fedora Core 3
* Sun Jun 13 2004 Nick Hemmesch <nick@ndhsoft.com> 1.6.3-1.2.3
- Fix file permissions and ownerships so this actually works
- with qmail-scanner
* Thu Jun 03 2004 Nick Hemmesch <nick@ndhsoft.com> 1.6.3-1.2.2
- Add Fedora Core 2 support
* Thu Jun 03 2004 Nick Hemmesch <nick@ndhsoft.com> 1.6.3-1.2.1
- Update to maildrop-1.6.3
* Mon Dec 29 2003 Nick Hemmesch <nick@ndhsoft.com> 1.5.3-1.0.3
- Add Fedora Core 1 support
* Sun Nov 23 2003 Nick Hemmesch <nick@ndhsoft.com> 1.5.3-1.0.2
- Add Trustix 2.0 support
* Sat Apr 26 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.5.3-1.0.1
- Last version 1.5.3
- Clean-ups on SPEC compilation banner, better gcc detects
- Detect gcc-3.2.3
- Red Hat Linux 9.0 support (nick@ndhsoft.com)
- Gnu/Linux Mandrake 9.2 support
* Wed Apr 02 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.5.2-1.0.1
- Conectiva 7.0 support
- Cleans up
* Sun Feb 15 2003 Nick Hemmesch <nick@ndhsoft.com> 1.4.0-1.0.3
- Support for Red Hat 8.0
* Sat Feb 01 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.4.0-1.0.2
- Redo Macros to prepare supporting larger RPM OS.
  We could be able to compile (and use) packages under every RPM based
  distribution: we just need to write right requirements.
- Improved files section with right permissions and owners.
* Sat Jan 25 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.4.0-1.0.1
- Added MDK 9.1 support
- Try to use gcc-3.2.1
- Added very little patch to compile with newest GLIBC
- Support dor new RPM-4.0.4
* Thu Oct 22 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.4.0-1.0.0beta
- Toaster release
