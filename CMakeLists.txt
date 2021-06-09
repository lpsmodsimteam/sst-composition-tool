cmake_minimum_required(VERSION 3.19)
project(sstconfiggui CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Widgets WebEngineWidgets REQUIRED)

set(HEADERS mainwindow.h)
set(SOURCES
    main.cpp
    mainwindow.cpp
)

qt5_add_resources(SOURCES index.qrc)

add_executable(sstconfiggui
    ${SOURCES}
)

target_link_libraries(sstconfiggui Qt5::Widgets)
target_link_libraries(sstconfiggui Qt5::WebEngineWidgets)
target_link_libraries(sstconfiggui Qt5::WebChannel)
