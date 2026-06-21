cmake_minimum_required(VERSION 4.2)
project(cosc_592_as_emb C)

set(CMAKE_C_STANDARD 11)

add_executable(cosc_592_as_emb main.c
    prime.h
    prime.c
    quadratic.c
    quadratic.h)
