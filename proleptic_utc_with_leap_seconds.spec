Name:           proleptic_utc_with_leap_seconds
Version:        2023.12.08
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

%description
Schedule leap seconds in the distant past and far future
based on historical astronomical observations and
information from the International Earth Rotation System Service (IERS).

%prep
%autosetup -S git

%build

# Tell configure to rebuild the PDF file
%configure --enable-pdf

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

# gnuplot and texlive-scheme-full are needed to rebuild the PDF file.
# The PDF may use the Andika, Charis and Liberation Mono fonts.
BuildRequires:  gnuplot
BuildRequires:  texlive-scheme-full
BuildRequires: sil-andika-fonts
BuildRequires: sil-charis-fonts
BuildRequires: liberation-mono-fonts

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
 * Fri Dec 08 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.12.08-1 Adjust future leap seconds starting in 2199.
 * Fri Dec 01 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.12.01-1 Adjust future leap seconds starting in 2140.
 * Sat Nov 25 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.11.25-1 Adjust future leap seconds starting in 2189.
 * Fri Nov 17 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.11.17-1 Adjust future leap seconds starting in 2056.
 * Fri Nov 03 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.11.03-2 correct an oversight in the PDF file.
 * Fri Nov 03 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.11.03-1 Adjust future leap seconds starting in 2081.
 * Sun Oct 29 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.10.29-1 Adjust future leap seconds starting in 2060.
 * Fri Oct 27 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.10.27-1 Adjust future leap seconds starting in 2439.
 * Fri Oct 20 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.10.20-1 Adjust future leap seconds starting in 2029.
 * Fri Oct 13 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.10.13-1 Adjust future leap seconds starting in 2400.
 * Sat Oct 07 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.10.07-2 Remove support for not rebuilding the documentation.
 * Sat Oct 07 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.10.07-1 Adjust future leap seconds starting in 2029.
 * Fri Sep 29 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.09.29-1 Adjust future leap seconds starting in 2029.
 * Fri Sep 22 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.09.22-1 Adjust future leap seconds starting in 2029.
 * Fri Sep 15 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.09.15-1 Adjust future leap seconds starting in 2034.
 * Fri Sep 08 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.09.08-1 Adjust future leap seconds starting in 2419.
 * Fri Sep 01 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.09.01-1 Adjust future leap seconds starting in 2419.
 * Fri Aug 18 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.08.18-1 Adjust future leap seconds starting in 2132.
 * Fri Aug 11 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.08.11-1 Adjust future leap seconds starting in 2407.
 * Fri Aug 04 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.08.04-1 Adjust future leap seconds starting in 2034.
 * Fri Jul 28 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.07.28-1 Adjust future leap seconds starting in 2271.
 * Fri Jul 21 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.07.21-1 Adjust future leap seconds starting in 2033.
 * Fri Jul 14 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.07.14-1 Adjust future leap seconds starting in 2167.
 * Fri Jul 07 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.07.07-1 Adjust future leap seconds starting in 2082.
 * Fri Jun 30 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.06.30-1 Adjust future leap seconds starting in 2328.
 * Fri Jun 23 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.06.23-1 Adjust future leap seconds starting in 2033.
 * Fri Jun 16 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.06.16-1 Adjust future leap seconds starting in 2067.
 * Fri Jun 09 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.06.09-1 Adjust future leap seconds starting in 2172.
 * Fri Jun 02 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.06.02-1 Adjust future leap seconds starting in 2032.
 * Fri May 26 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.05.26-1 Adjust future leap seconds starting in 2032.
 * Fri May 19 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.05.19-1 Adjust future leap seconds starting in 2184.
 * Fri May 12 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.05.12-1 Adjust future leap seconds starting in 2031.
 * Fri May 05 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.05.05-1 Adjust future leap seconds starting in 2031.
 * Fri Apr 28 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.04.28-1 Adjust future leap seconds starting in 2119.
 * Fri Apr 21 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.04.21-1 Adjust future leap seconds starting in 2119.
 * Fri Apr 14 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.04.14-1 Adjust future leap seconds starting in 2120.
 * Fri Apr 07 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.04.07-1 Adjust future leap seconds starting in 2030.
 * Fri Mar 31 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.03.31-1 Adjust future leap seconds starting in 2117.
 * Fri Mar 24 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.03.24-1 Adjust future leap seconds starting in 2093.
 * Fri Mar 17 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.03.17-1 Adjust future leap seconds starting in 2063.
 * Fri Mar 10 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.03.10-1 Adjust future leap seconds starting in 2122.
 * Fri Mar 03 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.03.03-1 Adjust future leap seconds starting in 2030.
 * Fri Feb 24 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.02.24-1 Adjust future leap seconds starting in 2098.
 * Fri Feb 17 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.02.17-1 Adjust future leap seconds starting in 2190.
 * Fri Feb 10 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.02.10-1 Adjust future leap seconds starting in 2029.
 * Fri Feb 03 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.02.03-1 Adjust future leap seconds starting in 2229.
 * Fri Jan 27 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.01.27-1 Adjust future leap seconds starting in 2063.
 * Fri Jan 13 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.01.13-1 Adjust future leap seconds starting in 2029.
 * Fri Jan 06 2023 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2023.01.06-1 Adjust future leap seconds starting in 2038.
 * Fri Dec 30 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.12.30-1 Adjust future leap seconds starting in 2169.
 * Fri Dec 23 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.12.23-1 Adjust future leap seconds starting in 2028.
 * Fri Dec 16 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.12.16-1 Adjust future leap seconds starting in 2214.
 * Fri Dec 09 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.12.09-1 Adjust future leap seconds starting in 2037.
 * Fri Dec 02 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.12.02-1 Adjust future leap seconds starting in 2256.
 * Fri Nov 25 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.11.25-1 Adjust future leap seconds starting in 2069.
 * Fri Nov 18 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.11.18-1 Adjust future leap seconds starting in 2069.
 * Fri Nov 11 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.11.11-1 Adjust future leap seconds starting in 2028.
 * Fri Nov 04 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.11.04-1 Adjust future leap seconds starting in 2197.
 * Fri Oct 28 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.10.28-1 Adjust future leap seconds starting in 2036.
 * Fri Oct 21 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.10.21-1 Adjust future leap seconds starting in 2108.
 * Fri Oct 14 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.10.14-1 Adjust future leap seconds starting in 2027.
 * Fri Sep 16 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.09.16-1 Adjust future leap seconds starting in 2027.
 * Fri Sep 09 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.09.09-1 Adjust future leap seconds starting in 2135.
 * Fri Aug 12 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.08.12-1 Adjust future leap seconds starting in 2064.
 * Fri Aug 05 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.08.05-1 Adjust future leap seconds starting in 2064.
 * Fri Jul 22 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.07.22-1 Adjust future leap seconds starting in 2036.
 * Fri Jul 08 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.07.08-1 Adjust future leap seconds starting in 2036.
 * Fri Jul 01 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.07.01-1 Adjust future leap seconds starting in 2028.
 * Fri Jun 10 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.06.10-1 Adjust future leap seconds starting in 2037.
 * Fri May 27 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.05.27-1 Adjust future leap seconds starting in 2028.
 * Fri May 13 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.05.13-1 Adjust future leap seconds starting in 2028.
 * Fri May 06 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.05.06-1 Adjust future leap seconds starting in 2028.
 * Fri Apr 29 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.04.29-1 Adjust future leap seconds starting in 2038.
 * Fri Apr 15 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.04.15-1 Adjust future leap seconds starting in 2029.
 * Fri Apr 01 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.04.01-1 Adjust future leap seconds starting in 2029.
 * Fri Mar 18 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.03.18-1 Adjust future leap seconds starting in 2030.
 * Fri Mar 11 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.03.11-1 Adjust future leap seconds starting in 2062.
 * Fri Feb 25 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.02.25-1 Adjust future leap seconds starting in 2030.
 * Sat Feb 19 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.02.19-1 Adjust future leap seconds starting in 2068.
 * Fri Feb 18 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.02.18-1 Adjust future leap seconds starting in 2141.
 * Fri Jan 07 2022 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2022.01.07-1 Adjust future leap seconds starting in 2155.
 * Fri Dec 10 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.12.10-1 Adjust future leap seconds starting in 2030.
 * Fri Nov 19 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.11.19-1 Adjust future leap seconds starting in 2030.
 * Fri Nov 12 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.11.12-1 Adjust future leap seconds starting in 2030.
 * Fri Oct 29 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.10.29-1 Adjust future leap seconds starting in 2068.
 * Fri Oct 15 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.10.15-1 Adjust future leap seconds starting in 2062.
 * Fri Sep 24 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.09.24-1 Adjust future leap seconds starting in 2062.
 * Fri Sep 10 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.09.10-1 Adjust future leap seconds starting in 2072.
 * Fri Aug 20 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.08.20-1 Adjust future leap seconds starting in 2030.
 * Fri Jul 30 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.07.30-1 Adjust future leap seconds starting in 2076.
 * Fri Jul 23 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.07.23-1 Adjust future leap seconds starting in 2029.
 * Fri Jul 09 2021 John Sauter <John_Sauter@systemeyescomputerstore.com>
 - 2021.07.09-1 Adjust future leap seconds starting in 2412.
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
