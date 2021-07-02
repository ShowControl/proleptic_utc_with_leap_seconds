Name:           proleptic_utc_with_leap_seconds
Version:        2021.07.02
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

%global _hardened_build 1

# Do not rebuild the PDF file on ELN, since it does not have TeX.
%if 0%{?rhel}
%global rebuild_pdf 0
%else
%global rebuild_pdf 1
%endif

%description
Schedule leap seconds in the distant past and far future
based on historical astronomical observations and
information from the International Earth Rotation System Service (IERS).

%prep
%autosetup -S git

%build

# Tell configure to rebuild the PDF file if TeX is present.
%if %{rebuild_pdf}
%configure --enable-pdf
%else
%configure
%endif

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

# gnuplot and texlive-scheme-full are needed only to rebuild the PDF file.
%if %{rebuild_pdf}
BuildRequires:  gnuplot
BuildRequires:  texlive-scheme-full
%endif

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
%exclude /usr/share/doc/%{name}/proleptic_UTC.pdf
%{_datadir}/%{name}/data/extraordinary_days.dat
%license LICENSE
%license COPYING

%files devel
%defattr(-,root,root)
%{_mandir}/man5/extraordinary_days.dat.5.*
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
 * Fri Jul 02 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.07.02-1 Adjust future leap seconds starting in 2088.
 * Fri Jun 25 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.06.25-1 Adjust future leap seconds starting in 2091.
 * Fri Jun 18 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.06.18-1 Adjust future leap seconds starting in 2353.
 * Fri Jun 11 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.06.11-1 Adjust future leap seconds starting in 2287.
 * Fri Jun 04 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.06.04-1 Adjust future leap seconds starting in 2063.
 * Sun May 30 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.05.28-4 Build PDF file, but only if TeX is available.
 * Sat May 29 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.05.28-2 Allow for a future change to the man file compression method.
 * Fri May 28 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.05.28-1 Adjust future leap seconds starting in 2182.
 * Fri May 21 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.05.21-1 Adjust future leap seconds starting in 2029.
 * Fri May 14 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.05.14-1 Adjust future leap seconds starting in 2073.
 * Fri May 07 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.05.07-1 Adjust future leap seconds starting in 2357.
 * Fri Apr 23 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.04.23-1 Adjust future leap seconds starting in 2029.
 * Fri Apr 16 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.04.16-1 Adjust future leap seconds starting in 2245.
 * Fri Apr 09 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.04.09-1 Adjust future leap seconds starting in 2063.
 * Fri Apr 02 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.04.02-1 Adjust future leap seconds starting in 2029.
 * Fri Mar 26 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.03.26-1 Adjust future leap seconds starting in 2030.
 * Fri Mar 19 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.03.19-1 Adjust future leap seconds starting in 2068.
 * Fri Mar 12 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.03.12-1 Adjust future leap seconds starting in 2030.
 * Fri Mar 05 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.03.05-1 Include the latest research on historical values of delta T.
 * Fri Feb 26 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.02.26-1 Adjust future leap seconds starting in 2104.
 * Fri Feb 19 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.02.19-1 Adjust future leap seconds starting in 2051.
 * Fri Feb 12 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.02.12-1 Adjust future leap seconds starting in 2103.
 * Fri Feb 05 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.02.05-1 Adjust future leap seconds starting in 2055.
 * Fri Jan 29 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.01.29-1 Adjust future leap seconds starting in 2089.
 * Fri Jan 22 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.01.22-1 Adjust future leap seconds starting in 2070.
 * Fri Jan 15 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.01.15-1 Adjust future leap seconds starting in 2039.
 * Fri Jan 08 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.01.08-1 There will be no leap second in June 2021.
 - Adjust future leap seconds starting in 2105.
 * Fri Jan 01 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.01.01-1 Adjust future leap seconds starting in 2064.
 * Fri Dec 25 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.12.25-1 Adjust future leap seconds starting in 2077.
 * Fri Dec 18 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.12.18-1 Adjust future leap seconds starting in 2044.
 * Fri Dec 04 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.12.04-1 Adjust future leap seconds starting in 2070.
 * Fri Nov 27 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.11.27-1 Adjust future leap seconds starting in 2097.
 * Fri Nov 20 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.11.20-1 Adjust future leap seconds starting in 2067.
 * Fri Nov 13 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.11.13-1 Delay the December 2093 leap second by six months to June 2094.
 * Fri Nov 06 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.11.06-1 Adjust future leap seconds starting in 2033.
 * Fri Oct 30 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.10.30-1 Adjust future leap seconds starting in 2033.
 * Fri Oct 23 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.10.23-1 Adjust future leap seconds starting in 2033.
 * Fri Oct 16 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.10.16-1 Adjust future leap seconds starting in 2062.
 * Fri Oct 02 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.10.02-1 Adjust future leap seconds starting in 2059.
 * Fri Sep 25 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2020.09.25-1 Adjust almost all future leap seconds starting in 2032.
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
