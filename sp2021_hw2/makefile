all : merge split

merge : merge.o
	gcc -o merge merge.o
split : split.o
	gcc -o split split.o
merge.o : merge.c
	gcc -c merge.c
split.o : split.c
	gcc -c split.c
clean:
	rm -rf *.o
	rm merge
	rm split
