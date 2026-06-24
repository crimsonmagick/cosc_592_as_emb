cmake_minimum_required(VERSION 4.2)
project(cosc_592_as_emb C)

set(CMAKE_C_STANDARD 11)

add_executable(cosc_592_as_emb src/native/main.c
    src/native/functions/prime.h
    src/native/functions/prime.c
    src/native/functions/quadratic.h
    src/native/functions/quadratic.c
    src/native/functions/gcd.c
    src/native/functions/gcd.h
    src/native/functions/gcd.c
    src/native/functions/gcd.c
    src/native/functions/gcd.h
    src/native/functions/gcd.c
    src/native/functions/gcd.h
    src/native/functions/factorial.c
    src/native/functions/factorial.h
    src/native/functions/linearsearch.c
    src/native/functions/linearsearch.h
    src/native/functions/stringlength.c
    src/native/functions/stringlength.h
    src/native/functions/stddev.c
    src/native/functions/hypotenuse.c
    src/native/functions/linked_list.c)

target_link_libraries(cosc_592_as_emb PRIVATE m)