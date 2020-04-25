#!/bin/bash
# File: build_RPMs.sh, author: John Sauter, date: April 25, 2020.
# Build the RPMs for proleptic_UTC_with_leap_seconds.

# Requires fedora-packager, rpmdevtools, copr-cli.
# Don't forget to tell copr-cli about your copr API token.
# See https://developer.fedoraproject.org/deployment/copr/copr-cli.html.

rm -rf ~/rpmbuild
mkdir -p ~/rpmbuild
mkdir -p ~/rpmbuild/SOURCES
mkdir -p ~/rpmbuild/SRPMS
mkdir -p ~/rpmbuild/RPMS/noarch

pushd ~/rpmbuild
# Set the umask so files created will not have strange permissions.
umask 022
# Clean out any old versions of the application.
rm -f SOURCES/*
rm -f SRPMS/*
rm -f RPMS/noarch/*
# Copy in the new tarball.
popd
cp -v proleptic_utc_with_leap_seconds-*.tar.gz ~/rpmbuild/SOURCES/
pushd ~/rpmbuild/SOURCES
chmod 0644 proleptic_utc_with_leap_seconds-*.tar.gz
# Build and test the source RPM.
rpmbuild -ta proleptic_utc_with_leap_seconds-*.tar.gz
# Copy back the source RPM so it can be copied to github.
popd
cp -v ~/rpmbuild/SRPMS/proleptic_utc_with_leap_seconds-*.src.rpm .
# Perform validity checking on the RPMs.
pushd ~/rpmbuild/SRPMS
rpmlint proleptic_utc_with_leap_seconds-*.src.rpm
pushd ../RPMS/noarch/
rpmlint proleptic_utc_with_leap_seconds-*.rpm
# Make sure the application  will build from the source RPM.
popd
mock -r fedora-31-x86_64 proleptic_utc_with_leap_seconds-*.src.rpm
# now that all local tests have passed, build it in copr.
copr-cli build proleptic_utc_with_leap_seconds \
	 proleptic_utc_with_leap_seconds-*.src.rpm

# End of file build_RPMs.sh
