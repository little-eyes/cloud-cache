#
# The Makefile for the cloud cache project in
# CS594 Cloud Computing.
# 
# The project is compiled under C++11 and Boost.

CC = g++
CFLAGS = -c -Wall -O3 -std=c++0x -g -fpermissive -lm
DEPS = src/configure.h src/ccache.h src/network.h src/sharding.h src/solver.h src/hiredis/hiredis.h
OBJECTS = ccache.o network.o sharding.o solver.o
# the static library for libredis
LIBC_REDIS = ./src/hiredis/libhiredis.a


all: master slave

ccache.o: $(DEPS) src/ccache.cc $(LIBC_REDIS)
	$(CC) $(CFLAGS) $(LIBC_REDIS) src/ccache.cc -o ccache.o

network.o: $(DEPS) src/network.cc
	$(CC) $(CFLAGS) src/network.cc -o network.o

sharding.o: $(DEPS) src/sharding.cc
	$(CC) $(CFLAGS) src/sharding.cc -o sharding.o

solver.o: $(DEPS) src/solver.cc
	$(CC) $(CFLAGS) src/solver.cc -o solver.o

master.o: $(DEPS) $(OBJECTS) src/master.cc
	$(CC) $(CFLAGS) src/master.cc -o master.o

slave.o: $(DEPS) $(OBJECTS) src/slave.cc
	$(CC) $(CFLAGS) src/slave.cc -o slave.o

master: master.o $(OBJECTS) $(LIBC_REDIS)
	$(CC) master.o $(OBJECTS) $(LIBC_REDIS) -o master

slave: slave.o $(OBJECTS) $(LIBC_REDIS)
	$(CC) slave.o $(OBJECTS) $(LIBC_REDIS) -o slave

clean:
	rm *.o master slave
