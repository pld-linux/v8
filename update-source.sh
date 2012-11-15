#!/bin/sh
# Usage:
# ./get-source.sh
# Author: Elan Ruusamäe <glen@pld-linux.org>

pkg=v8
baseurl=http://$pkg.googlecode.com/svn
mirror=http://commondatastorage.googleapis.com/chromium-browser-official

# leave empty to use latest tag, or "trunk" for trunk
version=
specfile=$pkg.spec

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

if [ -z "$version" ]; then
	echo >&2 "Failed to lookup version"
	exit 1
fi

if [ "$version" = "trunk" ]; then
	echo "Using trunk"
	svnurl=$baseurl/trunk/src
	tarball=$pkg-$(date +%Y%m%d).tar.bz2
else
	echo "Version: $version"
	tarball=$pkg-$version.tar.bz2
	url=$mirror/$tarball
	release=1
fi

if [ "$url" ]; then
	wget -c $url -O $tarball

	sed -i -e "
		s/^\(Version:[ \t]\+\)[.0-9]\+\$/\1$version/
		s/^\(Release:[ \t]\+\)[.0-9]\+\$/\1$release/
	" $specfile
fi

if [ "$svnurl" ]; then
	svn co $svnurl${revno:+@$revno} $pkg

	tar -cjf $tarball --exclude-vcs $pkg
	../dropin $tarball &
fi

../md5 $specfile
