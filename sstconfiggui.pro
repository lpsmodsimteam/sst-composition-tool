QT += \
    widgets \
    webenginewidgets \
    webchannel

HEADERS = \
    util.hpp \
    window.hpp
SOURCES =   main.cpp \
    util.cpp \
    window.cpp
RESOURCES = index.qrc
# Disable Qt Quick compiler because the example doesn't use QML, but more importantly so that
# the source code of the .js files is not removed from the embedded qrc file.
CONFIG -= qtquickcompiler

# install
target.path = $$[QT_INSTALL_EXAMPLES]/webenginewidgets/contentmanipulation
INSTALLS += target

DISTFILES += \
    docs/beautiful.css \
    docs/drawflow-element.html \
    docs/drawflow-element.js \
    docs/drawflow.gif \
    docs/index.html
