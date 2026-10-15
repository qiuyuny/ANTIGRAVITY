all: dict1 dict2

dict1: dict1.o dict.o
	gcc -Wall -o dict1 dict1.o dict.o

dict2: dict2.o tree.o dict.o
	gcc -Wall -o dict2 dict2.o tree.o dict.o

dict1.o: dict1.c dict.h
	gcc -Wall -c dict1.c

dict2.o: dict2.c dict.h tree.h
	gcc -Wall -c dict2.c

tree.o: tree.c tree.h dict.h
	gcc -Wall -c tree.c

dict.o: dict.c dict.h
	gcc -Wall -c dict.c

clean:
	rm -f *.o dict1 dict2
