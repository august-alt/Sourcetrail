Name: sourcetrail
Version: 2021.1.38
Release: alt1

Summary: Sourcetrail allows you to explore code-base using graphical interface
License: GPL-3.0+
Group: Development/Other

Url: https://github.com/CoatiSoftware/Sourcetrail
Source: %name-%version.tar.bz2

BuildRequires: cmake rpm-macros-cmake
BuildRequires: boost-asio-devel boost-filesystem-devel boost-interprocess-devel boost-locale-devel boost-program_options-devel
BuildRequires: clang11.0-devel-static libsqlite3-devel llvm11.0-devel-static python3-dev qt5-svg-devel tinyxml-devel catch2-devel
BuildRequires: gcc-c++
BuildRequires: qt5-base-devel qt5-svg-devel
BuildRequires: clang11.0-devel llvm11.0-devel llvm11.0-devel-static clang11.0-devel-static
BuildRequires: desktop-file-utils

Requires: sourcetrail-cpp-indexer = %version-%release

%package cpp-indexer
Summary: C++ indexer allows you to create projects for Sourcetrail from cmake project
Group: Development/Other

%description
Sourcetrail is a free and open-source cross-platform source explorer
that helps you get productive on unfamiliar source code.

%description cpp-indexer
Indexes compile_commands.json provided by cmake and creates
project from C/C++ sources.

%prep
%setup

%build
%cmake -DBoost_USE_STATIC_LIBS=OFF -DBUILD_CXX_LANGUAGE_PACKAGE=ON
%cmake_build VERBOSE=1

%install
cd BUILD
mkdir -p %{buildroot}/usr/bin
cp app/Sourcetrail %{buildroot}/usr/bin/sourcetrail
cp app/sourcetrail_indexer %{buildroot}/usr/bin/sourcetrail_indexer

mkdir -p %{buildroot}/usr/share/mime/packages
cp %{_builddir}/%name-%version/setup/Linux/data/sourcetrail-mime.xml %{buildroot}/usr/share/mime/packages/sourcetrail-mime.xml

mkdir -p %{buildroot}/usr/share/sourcetrail
cp -R %{_builddir}/%name-%version/bin/app/data %{buildroot}/usr/share/sourcetrail
cp -R %{_builddir}/%name-%version/bin/app/user/projects %{buildroot}/usr/share/sourcetrail/data/fallback
rm %{buildroot}/usr/share/sourcetrail/data/*_template.xml
rm -r %{buildroot}/usr/share/sourcetrail/data/install
rm -r %{buildroot}/usr/share/sourcetrail/data/fallback/projects/tictactoe_py

desktop-file-install --dir=%{buildroot}/usr/share/applications \
                     --set-key Exec --set-value %{buildroot}/bin/sourcetrail \
                     ../setup/Linux/data/sourcetrail.desktop

%files
%_bindir/sourcetrail

%_datadir/mime/packages/sourcetrail-mime.xml

%_datadir/sourcetrail/*

%_desktopdir/sourcetrail.desktop

%files cpp-indexer
%_bindir/sourcetrail_indexer

%changelog
* Tue Aug 03 2021 Vladimir Rubanov <august@altlinux.org> 2021.1.38-alt1
- initial build
