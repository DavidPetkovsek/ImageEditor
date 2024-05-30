# Image Editor

This project is to create a nice multi-os high performance image editor. It will use tools like opencv to edit the images.


## Build Instructions

> Prerequisites are for windows. It should be compatible on linux (without visual studio) `sudo apt install build-essential cmake ninja-build`.

### Prerequisites
1. Have Visual Studio installed:
    - Desktop development with C++
        1. C++ Clang Compiler for Windows
        2. MSBuild support for LLVM (clang-cl) toolset
        3. CMake
        4. git
2. Have Git installed
3. Have vcpkg.
    - *Note: the project default assumes it was cloned in the root of the project. If it is not, use `"-DCMAKE_TOOLCHAIN_FILE=${VCPKG_INSTALL_LOC}/vcpkg/scripts/buildsystems/vcpkg.cmake"` with the `cmake` command in build.*
```ps1
git clone https://github.com/microsoft/vcpkg.git -b 2024.04.26
vcpkg\bootstrap-vcpkg.bat
```

### Build

Using `Developer PowerShell for VS 20XX` from Visual Studio
```ps1
git clone https://github.com/DavidPetkovsek/ImageEditor.git
cd ImageEditor
mkdir build
cd build
cmake .. -G Ninja
ninja
```

### Run
```ps1
cd ImageEditor
bin/image-editor.exe
```
