#!/bin/bash

CC=g++
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    CFLAGS="-O3 -fPIC -std=c++11 -fno-gnu-unique -B/usr/lib/x86_64-linux-gnu"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    CFLAGS="-O3 -fPIC -std=c++11 -B/usr/lib/x86_64-linux-gnu"
fi
LDFLAGS=
INCFLAGS="-Ifirmware/ap_types/"
PROJECT=myproject
LIB_STAMP=mystamp

${CC} ${CFLAGS} ${INCFLAGS} -c firmware/${PROJECT}.cpp -o ${PROJECT}.o
${CC} ${CFLAGS} ${INCFLAGS} -c ${PROJECT}_bridge.cpp -o ${PROJECT}_bridge.o
${CC} ${CFLAGS} ${INCFLAGS} -shared ${PROJECT}.o ${PROJECT}_bridge.o -o firmware/${PROJECT}-${LIB_STAMP}.so
rm -f *.o
