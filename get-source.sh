#!/bin/sh
# Usage:
# ./get-source.sh
# Author: Elan Ruusamäe <glen@pld-linux.org>

p=v8
baseurl=http://$p.googlecode.com/svn
# leave empty to use latest tag, or "trunk" for trunk
version=
specfile=$p.spec

# abort on errors
set -e
# work in package dir
dir=$(dirname "$0")
cd "$dir"

if [ "$1" ]; then
	version=$1
fi

if [ -z "$version" ]; then
	basever=$(awk '/^Version:/{split($2, v, "."); printf("%d[.]%d[.]%d\n", v[1], v[2], v[3])}' $specfile)
	echo "Looking for latest version for $basever..."
	version=$(svn ls $baseurl/tags/ | grep "^$basever\." | sort -V | tail -n1)
	version=${version%/}
fi

if [ "$version" = "trunk" ]; then
	echo "Using trunk"
	svnurl=$baseurl/trunk
	tarball=$p-$(date +%Y%m%d).tar.bz2
else
	echo "Version: $version"
	svnurl=$baseurl/tags/$version
	tarball=$p-$version.tar.bz2
fi

if [ "$svnurl" ]; then
	svn co $svnurl${revno:+@$revno} $p-$version

	tar -cjf $tarball --exclude-vcs $p-$version
	../dropin $tarball &
fi

../md5 $specfile

if [ "$url" ]; then
	release=0.1
	sed -i -e "
		s/^\(Version:[ \t]\+\)[.0-9]\+\$/\1$version/
		s/^\(Release:[ \t]\+\)[.0-9]\+\$/\1$release/
	" $specfile
fi
