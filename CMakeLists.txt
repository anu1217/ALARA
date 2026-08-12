project(ALARA)
cmake_minimum_required(VERSION 2.8)
set (CMAKE_CXX_STANDARD 11)

find_package(Git)
execute_process(
    COMMAND ${GIT_EXECUTABLE} log -1 --format=%H
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    OUTPUT_VARIABLE GIT_COMMIT_HASH
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_QUIET
)
execute_process(
    COMMAND ${GIT_EXECUTABLE} log -1 --format=%cd
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    OUTPUT_VARIABLE GIT_COMMIT_DATE
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_QUIET
)

message(STATUS "Git commit used for build: ${GIT_COMMIT_HASH}")
message(STATUS "Git commit used for build made on: ${GIT_COMMIT_DATE}")

# Default to a release build
if (NOT CMAKE_BUILD_TYPE)
  message(STATUS "CMAKE_BUILD_TYPE not specified, defaulting to Release")
  set(CMAKE_BUILD_TYPE Release)
endif ()

# Version strings  
set(PACKAGE_VERSION 2.9.2)
set(PACKAGE_STRING "ALARA ${PACKAGE_VERSION}")
set(GIT_HASH ${GIT_COMMIT_HASH})

# Location of data directory
set(DFLT_DATADIR ${CMAKE_INSTALL_PREFIX}/data)
set(DFLT_XSDIR   ${CMAKE_INSTALL_PREFIX}/data)

# Build ALARA executable
add_subdirectory(src)

# Build other ALARA tools
add_subdirectory(tools)

# Install data files
add_subdirectory(data)

# Install sample files
add_subdirectory(sample)
