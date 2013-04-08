#
# The Makefile for the cloud cache project in
# CS594 Cloud Computing.
# 
# The project is compiled under C++11 and Boost.

CC = g++
CFLAGS = -c -Wall -pthread -O3 -std=c++0x -g
DEPS = src/configure.h src/ccache.h src/network.h src/sharding.h src/solver.h
OBJECTS = ccache.o network.o sharding.o solver.o

all: master slave

master: master.o ccache.o network.o sharding.o solver.o
	$(CC) -pthread  master.o ccache.o network.o sharding.o solver.o -o master

slave: slave.o ccache.o network.o sharding.o solver.o
	$(CC) -pthread slave.o ccache.o network.o sharding.o solver.o -o slave

ccache.o: $(DEPS) src/ccache.cc
	$(CC) $(CFLAGS) src/ccache.cc

network.o: $(DEPS) src/network.cc
	gcc $(CFLAGS) -pthread -fpermissive src/network.cc

sharding.o: $(DEPS) src/sharding.cc
	$(CC) $(CFLAGS) src/sharding.cc

solver.o: $(DEPS) src/solver.cc
	$(CC) $(CFLAGS) src/solver.cc

master.o: $(DEPS) $(OBJECTS) src/master.cc
	$(CC) $(CFLAGS) src/master.cc

slave.o: $(DEPS) $(OBJECTS) src/slave.cc
	$(CC) $(CFLAGS) src/slave.cc

clean:
	rm *.o master slave
