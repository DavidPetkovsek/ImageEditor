cmake_minimum_required(VERSION 3.24.0)

if(NOT DEFINED CMAKE_C_COMPILER AND WIN32)
  set(CMAKE_C_COMPILER "clang-cl.exe")
endif()
if(NOT DEFINED CMAKE_CXX_COMPILER AND WIN32)
  set(CMAKE_CXX_COMPILER "clang-cl.exe")
endif()

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
if( NOT CMAKE_BUILD_TYPE )
    set(CMAKE_BUILD_TYPE RelWithDebugInfo)
ENDIF()
file(WRITE "${CMAKE_BINARY_DIR}/BUILD_TYPE.txt" ${CMAKE_BUILD_TYPE})

# Function to read a JSON file
file(READ "${CMAKE_SOURCE_DIR}/vcpkg.json" VCPKG_JSON_FILE_CONTENT)
function(read_json key var)
  string(JSON value GET "${VCPKG_JSON_FILE_CONTENT}" "${key}")
  set("${var}" "${value}" PARENT_SCOPE)
endfunction()

# Read the vcpkg.json file
read_json(version-semver version-semver)
read_json("name" pname)
read_json(description pdescription)
read_json(homepage phomepage)

set(full_version ${version-semver})
string(REGEX REPLACE "([0-9]+)\\.([0-9]+)\\.([0-9]+).*" "\\1;\\2;\\3" version_components "${full_version}")
list(GET version_components 0 VERSION_MAJOR)
list(GET version_components 1 VERSION_MINOR)
list(GET version_components 2 VERSION_PATCH)

set(VERSION_SHORT ${VERSION_MAJOR}.${VERSION_MINOR})
set(VERSION ${VERSION_SHORT}.${VERSION_PATCH})
set(Boost_NO_SYSTEM_PATHS ON)
set(Boost_NO_WARN_NEW_VERSIONS ON)
if( NOT CMAKE_TOOLCHAIN_FILE )
  set(CMAKE_TOOLCHAIN_FILE "vcpkg/scripts/buildsystems/vcpkg.cmake" CACHE STRING "vcpkg toolchain file")
endif()
project("${pname}"
        VERSION ${VERSION}
        DESCRIPTION "${pdescription}"
        HOMEPAGE_URL "${phomepage}"
        LANGUAGES CXX C
)

message(STATUS "Building ${CMAKE_PROJECT_NAME}-${CMAKE_BUILD_TYPE} version ${CMAKE_PROJECT_VERSION}")

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(THREADS_PREFER_PTHREAD_FLAG ON)




file(GLOB_RECURSE CPP_FILES CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)
# file(GLOB_RECURSE HPP_FILES CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/include/*.hpp)

find_package(OpenCV REQUIRED)
find_package(imgui CONFIG REQUIRED)
find_package(freetype REQUIRED)
find_package(glfw3 REQUIRED)
find_package(implot CONFIG REQUIRED)
find_package(unofficial-lunasvg CONFIG REQUIRED)
find_package(OpenGL REQUIRED)


add_executable(${CMAKE_PROJECT_NAME} ${CPP_FILES})
target_include_directories(${CMAKE_PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(${CMAKE_PROJECT_NAME} PUBLIC ${OpenCV_LIBS})
target_link_libraries(${CMAKE_PROJECT_NAME} PUBLIC
  unofficial::lunasvg::lunasvg
  freetype
  glfw
  imgui::imgui
  implot::implot
  OpenGL::GL
)
 