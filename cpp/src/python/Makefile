TOP = ../..
include $(TOP)/configure/CONFIG

USR_INCLUDES += -I${PYTHON_BASE}/include/${PYTHON}

LIBSRCS += alarmPy.cpp
LIBSRCS += timeStampPy.cpp
LIBSRCS += controlPy.cpp
LIBSRCS += displayPy.cpp
LIBSRCS += channelRPCPy.cpp
LIBSRCS += ntnameValuePy.cpp
LIBSRCS += nttablePy.cpp
LIBSRCS += ntmultiChannelPy.cpp
LIBSRCS += gatherV3DataPy.cpp
LIBSRCS += ntscalarPy.cpp

LIBRARY = masarPy

masarPy_LIBS += gather nt pvAccess pvData Com

include $(TOP)/configure/RULES

