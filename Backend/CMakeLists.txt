cmake_minimum_required(VERSION 3.0)
project(RESTServer)

find_package(Boost REQUIRED COMPONENTS system)
find_package(cpprestsdk REQUIRED)
find_package(OpenSSL REQUIRED)

include_directories(${Boost_INCLUDE_DIRS})

add_executable(server main.cc)

target_link_libraries(server 
    ${Boost_LIBRARIES} 
    cpprestsdk::cpprest 
    OpenSSL::SSL 
    OpenSSL::Crypto
    -static-libstdc++ -static-libgcc
)

set(Boost_USE_STATIC_LIBS ON)
