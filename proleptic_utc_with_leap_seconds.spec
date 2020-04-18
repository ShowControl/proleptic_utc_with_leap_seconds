Name:           proleptic_utc_with_leap_seconds
Version:        2020.04.18
Release:        1%{?dist}
Summary:        Schedule leap seconds

License:        GPLv3+
URL:            https://github.com/ShowControl/proleptic_UTC_with_leap_seconds
Source0:        https://github.com/ShowControl/proleptic_UTC_with_leap_seconds-%{version}.tar.gz

BuildArch: noarch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3 >= 3.5
BuildRequires:  git

%global _hardened_build 1

%description
Schedule leap seconds based on historical astronomical observations and
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

%package doc
Summary: Comprehensive documentation for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description doc
The %{name}-doc package contains the documentation for %{name}-devel
in the form of a PDF file which describes why it is useful to schedule
leap seconds and presents some of the results.
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
%license LICENSE
%license COPYING


%files doc
%defattr(-,root,root)
%doc proleptic_UTC.pdf
%license LICENSE
%license COPYING

%changelog
* Sat Apr 18 2020 John Sauter <John_Sauter@systemeyescomputerstore.com>
- 2020.04.18-1 Initial version of the spec file.
