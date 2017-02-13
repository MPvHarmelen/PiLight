CFLAGS=-Wall -O3 -g
CXXFLAGS=-Wall -O3 -g
OBJECTS=main.o gpio.o led-matrix.o thread.o
BINARIES=led-matrix
S_OBJECTS=c_server.o gpio.o led-matrix.o thread.o
S_BINARIES=server
LDFLAGS=-lrt -lm -lpthread

all : $(BINARIES) $(S_BINARIES)

led-matrix.o: led-matrix.cpp led-matrix.h
main.o: led-matrix.h
c_server.o: c_server.cpp led-matrix.h

led-matrix : $(OBJECTS)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS)

server: $(S_OBJECTS)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS)

clean:
	rm -f $(OBJECTS) $(BINARIES) $(S_OBJECTS) $(S_BINARIES)
