%undefine __cmake_in_source_build
Name:           leveldb
Version:        1.23
Release:        1
Summary:        A fast and lightweight key/value database library by Google
License:        BSD-3-Clause
URL:            https://github.com/google/leveldb
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz


Patch0001:      0001-Allow-leveldbjni-build.patch
Patch0002:      0002-Added-a-DB-SuspendCompations-and-DB-ResumeCompaction.patch
Patch0003:      0003-allow-Get-calls-to-avoid-copies-into-std-string.patch
Patch0004:      0004-bloom_test-failure-on-big-endian-archs.patch
Patch0006:      0006-revert-no-rtti.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  snappy-devel
BuildRequires:  sqlite-devel

%description
LevelDB is a fast key-value storage library written at Google that provides an
ordered mapping from string keys to string values.

%package devel
Summary:        Development files for %{name}
Requires:       cmake-filesystem
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1


cat > %{name}.pc << EOF
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: %{summary}
Version: %{version}
Libs: -l%{name}
EOF


%build

export CFLAGS='-O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/generic-hardened-cc1  -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection '
export CXXFLAGS='-O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/generic-hardened-cc1  -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection '
export FFLAGS='-O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/generic-hardened-cc1  -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection  -I/usr/lib64/gfortran/modules'
export  FCFLAGS='-O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/generic-hardened-cc1  -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection  -I/usr/lib64/gfortran/modules'
export LDFLAGS='-Wl,-z,relro   -Wl,-z,now -specs=/usr/lib/rpm/generic-hardened-ld'

mkdir build && cd build


cmake  -DCMAKE_C_FLAGS_RELEASE:STRING=-DNDEBUG -DCMAKE_CXX_FLAGS_RELEASE:STRING=-DNDEBUG -DCMAKE_Fortran_FLAGS_RELEASE:STRING=-DNDEBUG -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON -DCMAKE_INSTALL_PREFIX:PATH=%_buildrootdir/usr -DINCLUDE_INSTALL_DIR:PATH=/usr/include -DLIB_INSTALL_DIR:PATH=/usr/lib64  -DSYSCONF_INSTALL_DIR:PATH=/etc -DSHARE_INSTALL_PREFIX:PATH=/usr/share -DLIB_SUFFIX=64 -DBUILD_SHARED_LIBS:BOOL=ON -DLEVELDB_BUILD_TESTS:BOOL=OFF  -DLEVELDB_BUILD_BENCHMARKS:BOOL=OFF  ..

cmake --build .

%install
install -d %{buildroot}{%{_libdir}/pkgconfig,%{_includedir}}

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -p leveldb.pc %{buildroot}%{_libdir}/pkgconfig/leveldb.pc
cp -a include/leveldb/ %{buildroot}%{_includedir}/
cp build/libleveldb.so* %{buildroot}%{_libdir}/


cd build
make install

%ldconfig_scriptlets


%post
/sbin/ldconfig

%postun
/sbin/ldconfig


%files
%license LICENSE
%doc AUTHORS README.md NEWS
%{_libdir}/lib%{name}.so.*


%files devel
%doc doc/ CONTRIBUTING.md TODO
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc



%changelog
* Fri Dec 16 2022 huyab<1229981468@qq.com> - 1.23-1
- update version to 1.23

* Tue May 10 2022 yaoxin <yaoxin30@h-partners.com> - 1.20-5
- License compliance rectification

* Fri Dec 20 2019 wangyiru <wangyiru1@huawei.com> -  1.20-4
- Package init
