%define st_source_dir %_builddir/%name-%version
%define _cmake__builddir BUILD

# clang doesn't know used LTO flags
%define optflags_lto -flto=thin

Name: sourcetrail
Version: 2021.4.19
Release: alt1

Summary: Sourcetrail allows you to explore code-base using graphical interface
License: GPL-3.0+
Group: Development/Other

Url: https://github.com/CoatiSoftware/Sourcetrail
Source: %name-%version.tar.bz2

BuildRequires: cmake rpm-macros-cmake
BuildRequires: boost-asio-devel boost-filesystem-devel boost-interprocess-devel boost-locale-devel boost-program_options-devel
BuildRequires: libsqlite3-devel python3-dev qt5-svg-devel tinyxml-devel catch2-devel
BuildRequires: gcc-c++
BuildRequires: qt5-base-devel qt5-svg-devel
BuildRequires: clang clang-devel clang-devel-static clang-tools clangd lld lld-devel lldb llvm llvm-common llvm-devel llvm-devel-static rpm-macros-llvm-common
BuildRequires: desktop-file-utils ImageMagick-tools

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
export CC=clang
export CXX=clang++

%cmake -DBoost_USE_STATIC_LIBS=OFF -DBUILD_CXX_LANGUAGE_PACKAGE=ON -DLLVM_LINK_LLVM_DYLIB=ON -DCLANG_LINK_CLANG_DYLIB=ON -DCMAKE_EXE_LINKER_FLAGS=-fuse-ld=lld -DLLVM_DIR=$(llvm-config --cmakedir)
%cmake_build

%install
mkdir -p %buildroot%_bindir
cd %_cmake__builddir
cp app/Sourcetrail %buildroot%_bindir/sourcetrail
cp app/sourcetrail_indexer %buildroot%_bindir/sourcetrail_indexer

mkdir -p %buildroot%_datadir/mime/packages
cp %st_source_dir/setup/Linux/data/sourcetrail-mime.xml %buildroot%_datadir/mime/packages/sourcetrail-mime.xml

mkdir -p %buildroot%_datadir/sourcetrail
cp -R %st_source_dir/bin/app/data %buildroot%_datadir/sourcetrail
cp -R %st_source_dir/bin/app/user/projects %buildroot%_datadir/sourcetrail/data/fallback
rm %buildroot%_datadir/sourcetrail/data/*_template.xml
rm -r %buildroot%_datadir/sourcetrail/data/install
rm -r %buildroot%_datadir/sourcetrail/data/fallback/projects/tictactoe_py

desktop-file-install --dir=%buildroot%_datadir/applications \
                     --set-key Exec --set-value %_bindir/sourcetrail \
                     ../setup/Linux/data/sourcetrail.desktop

for size in 48 64 128 256 512; do
    mkdir -p %buildroot%_datadir/icons/hicolor/''${size}x''${size}/apps/
    convert %st_source_dir/bin/app/data/gui/icon/logo_1024_1024.png -resize ''${size}x''${size} \
    %buildroot%_datadir/icons/hicolor/''${size}x''${size}/apps/sourcetrail.png
done

%files
%doc README.md

%_bindir/sourcetrail

%_datadir/mime/packages/sourcetrail-mime.xml

%_datadir/sourcetrail/*

%_desktopdir/sourcetrail.desktop

%_datadir/icons/hicolor/48x48/apps/sourcetrail.png
%_datadir/icons/hicolor/64x64/apps/sourcetrail.png
%_datadir/icons/hicolor/128x128/apps/sourcetrail.png
%_datadir/icons/hicolor/256x256/apps/sourcetrail.png
%_datadir/icons/hicolor/512x512/apps/sourcetrail.png

%files cpp-indexer
%_bindir/sourcetrail_indexer

%changelog
* Thu Feb 03 2022 Vladimir Rubanov <august@altlinux.org> 2021.4.19-alt1
- Bump version

* Tue Aug 03 2021 Vladimir Rubanov <august@altlinux.org> 2021.1.38-alt1
- initial build