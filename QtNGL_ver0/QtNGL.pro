TARGET=QtNGL
OBJECTS_DIR=obj
QT+=gui opengl core

isEqual(QT_MAJOR_VERSION, 5) {
	cache()
	DEFINES +=QT5BUILD
}

MOC_DIR=moc
CONFIG-=app_bundle
SOURCES+= $$PWD/src/NGLScene.cpp \
					$$PWD/src/MainWindow.cpp \
					$$PWD/src/main.cpp \
    src/Boid.cpp

HEADERS+= $$PWD/include/NGLScene.h \
          $$PWD/include/MainWindow.h \
          $$PWD/include/WindowParams.h \
    include/Boid.h


FORMS+= $$PWD/ui/MainWindow.ui
INCLUDEPATH +=./include
DESTDIR=./

OTHER_FILES+= README.md

CONFIG += console
NGLPATH=$$(NGLDIR)
isEmpty(NGLPATH){ # note brace must be here
	message("including $HOME/NGL")
	include($(HOME)/NGL/UseNGL.pri)
}
else{ # note brace must be here
	message("Using custom NGL location")
	include($(NGLDIR)/UseNGL.pri)
}

DISTFILES +=
