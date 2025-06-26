cmake_minimum_required(VERSION 3.15)
project(icmp_x86 C)

#win32
set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_PROCESSOR x86)
set(CMAKE_C_COMPILER    i686-w64-mingw32-gcc)
set(CMAKE_FIND_ROOT_PATH /usr/i686-w64-mingw32)

# Use C11
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
 
# Build the 32-bit client executable
add_executable(icmp_x86
    icmp_x86.c
)
 
# Suppress deprecated Winsock warnings
target_compile_definitions(icmp_x86 PRIVATE
    _WINSOCK_DEPRECATED_NO_WARNINGS
)
 
# Link against WinSock2
target_link_libraries(icmp_x86 PRIVATE
    ws2_32
)

# set exe to be output to parent dir 
get_filename_component(PARENT_DIR "${CMAKE_BINARY_DIR}" PATH)
set_target_properties(icmp_x86 PROPERTIES 
    RUNTIME_OUTPUT_DIRECTORY "${PARENT_DIR}"
)

# build with:
# mkdir build && cd build
# cmake ..
# cmake --build .