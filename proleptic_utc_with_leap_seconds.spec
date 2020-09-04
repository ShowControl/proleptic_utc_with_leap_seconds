Name:           proleptic_utc_with_leap_seconds
Version:        2020.09.04
Release:        1%{?dist}
Summary:        Schedule leap seconds

License:        GPLv3+
URL:            https://github.com/ShowControl/proleptic_UTC_with_leap_seconds
Source0:        https://github.com/ShowControl/proleptic_utc_with_leap_seconds/blob/master/proleptic_utc_with_leap_seconds-%{version}.tar.gz
                
BuildArch: noarch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3 >= 3.5
BuildRequires:  git
BuildRequires:  python3-jdcal
BuildRequires:  python3-numpy
BuildRequires:  python3-scipy
BuildRequires:  python3-pandas

# gnuplot and texlive-scheme-full are needed only to rebuild the PDF file.
#BuildRequires:  gnuplot
#BuildRequires:  texlive-scheme-full

%global _hardened_build 1

%description
Schedule leap seconds in the distant past and far future
based on historical astronomical observations and
information from the International Earth Rotation System Service (IERS).

%prep
%autosetup -S git

%build
%configure
%make_build

%install
%make_install

%check
make check VERBOSE=1

%package devel
Summary: Schedule leap seconds in the distant past and far future
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package
contains the man file for %{name}.

%package doc
Summary: Comprehensive documentation for %{name}
Requires: %{name} = %{version}-%{release}

%description doc
The %{name}-doc package contains the documentation
for %{name}
in the form of a PDF file which describes why it is useful to schedule
leap seconds in the distant past and the far future
and presents some of the results.
Included in the PDF file using embedding are all of the
files and instructions needed to create the source tarball, which
includes the RPM spec file.

%files
%defattr(-,root,root)
%exclude /usr/share/doc/%{name}/AUTHORS
%exclude /usr/share/doc/%{name}/COPYING
%exclude /usr/share/doc/%{name}/ChangeLog
%exclude /usr/share/doc/%{name}/INSTALL
%exclude /usr/share/doc/%{name}/NEWS
%exclude /usr/share/doc/%{name}/README
%exclude /usr/share/doc/%{name}/LICENSE
%{_datadir}/%{name}/data/extraordinary_days.dat
%license LICENSE
%license COPYING

%files devel
%defattr(-,root,root)
%{_mandir}/man5/extraordinary_days.dat.5.gz
%doc AUTHORS ChangeLog NEWS README
%license LICENSE
%license COPYING

%files doc
%defattr(-,root,root)
%doc proleptic_UTC.pdf
%doc AUTHORS ChangeLog NEWS README
%license LICENSE
%license COPYING

%changelog
 * Fri Sep 04 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.09.04-1 Adjust almost all future leap seconds.
 * Fri Aug 28 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.08.28-1 Adjust future leap seconds starting in 2089.
 * Fri Aug 21 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.08.21-1 Adjust future leap seconds starting in 2031.
 * Fri Aug 14 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.08.14-1 Adjust future leap seconds starting in 2073.
 * Fri Aug 07 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.08.07-1 Adjust future leap seconds starting in 2114.
 * Fri Jul 31 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.07.31-1 Adjust future leap seconds starting in 2120.
 * Fri Jul 24 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.07.24-1 Adjust future leap seconds starting in 2055.
 * Wed Jul 22 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.07.17-9 Provide NEWS, etc. files.
 * Fri Jul 17 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.07.17-1 Adjust future leap seconds starting in 2080.
 * Fri Jul 10 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.07.10-1 Update to IERS Bulletin C 60.
                Adjust many future leap seconds starting in 2066.
 * Fri Jul 03 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
- 2020.07.03-1 Adjust many future leap seconds starting in 2025.
 * Fri Jun 26 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
- 2020.06.26-1 Adjust many future leap seconds starting in 2068.
 * Fri Jun 19 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
- 2020.06.19-1 Adjust many future leap seconds starting in 2063.
 * Fri Jun 12 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
- 2020.06.12-1 Adjust many future leap seconds starting in 2098.
 * Fri Jun 05 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
- 2020.06.05-1 Adjust many future leap seconds starting in 2087.
 * Fri May 29 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
- 2020.05.29-1 Adjust many future leap seconds starting in 2106.
 * Thu May 21 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
- 2020.05.21-1 Adjust several distant future leap seconds.
 * Thu May 14 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
- 2020.05.14-1 Adjust five distant future leap seconds.
 * Thu May 07 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
- 2020.05.07-1 Adjust five distant future leap seconds.
 * Thu Apr 30 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.04.30-1 Convert the PDF to the Libertine font and adjust several
   far future leap seconds.
 * Fri Apr 24 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
- 2020.04.24-1 Embed the missing files in the PDF.
 * Thu Apr 23 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
- 2020.04.23-1 Advance three far future leap seconds by three or six months.
 * Sat Apr 18 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
- 2020.04.18-1 Initial version of the spec file.
