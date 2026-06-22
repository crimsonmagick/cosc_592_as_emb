cmake_minimum_required(VERSION 4.2)
project(cosc_592_as_emb C)

set(CMAKE_C_STANDARD 11)

add_executable(cosc_592_as_emb src/native/main.c
    src/native/math/simple/prime.h
    src/native/math/simple/prime.c
    src/native/math/complex/quadratic.h
    src/native/math/complex/quadratic.c
    src/native/math/simple/gcd.c
    src/native/math/simple/gcd.h
    src/native/math/simple/gcd.c
    src/native/math/simple/gcd.c
    src/native/math/simple/gcd.h
    src/native/math/simple/gcd.c
    src/native/math/simple/gcd.h
    src/native/math/simple/factorial.c
    src/native/math/simple/factorial.h
    src/native/math/simple/linearsearch.c
    src/native/math/simple/linearsearch.h
    src/native/math/simple/stringlength.c
    src/native/math/simple/stringlength.h)

target_link_libraries(cosc_592_as_emb PRIVATE m)