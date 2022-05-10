Name:           leveldb
Version:        1.20
Release:        5
Summary:        A key/value database library
License:        BSD-3-Clause
URL:            https://github.com/google/leveldb
Source0:        https://github.com/google/leveldb/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0001:      0001-Allow-leveldbjni-build.patch
Patch0002:      0002-Added-a-DB-SuspendCompations-and-DB-ResumeCompaction.patch
Patch0003:      0003-allow-Get-calls-to-avoid-copies-into-std-string.patch
Patch0004:      0004-bloom_test-failure-on-big-endian-archs.patch

BuildRequires:  make gcc-c++ snappy-devel

%description
LevelDB is a fast key-value storage library written at Google that provides an
ordered mapping from string keys to string values.

%package        devel
Summary:        Development files for leveldb
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
Development files for leveldb.

%prep
%autosetup -p1
cat > leveldb.pc << EOF
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: leveldb
Description: A key/value database library
Version: %{version}
Libs: -lleveldb
EOF

%global configure() {export OPT="-DNDEBUG" export CFLAGS="%{optflags}" export CXXFLAGS="%{optflags}" export LDFLAGS="%{__global_ldflags}" }

%build
%configure
make -O -j1

%install
install -d %{buildroot}{%{_libdir}/pkgconfig,%{_includedir}}
cp -a out-shared/libleveldb.so* %{buildroot}%{_libdir}/
install -p leveldb.pc %{buildroot}%{_libdir}/pkgconfig/leveldb.pc
cp -a include/leveldb/ %{buildroot}%{_includedir}/

%check
%configure
make -j1 check

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
%{_includedir}/leveldb/
%{_libdir}/libleveldb.so
%{_libdir}/pkgconfig/leveldb.pc

%changelog
* Tue May 10 2022 yaoxin <yaoxin30@h-partners.com> - 1.20-5
- License compliance rectification

* Fri Dec 20 2019 wangyiru <wangyiru1@huawei.com> -  1.20-4
- Package init
