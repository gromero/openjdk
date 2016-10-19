%.o:	%.s
	gcc -c $< -o $@

all:	nocmpldi.o cmpldi.o
	gcc nocmpldi.o -o nocmpldi
	gcc cmpldi.o -o cmpldi
	
clean:
	rm -fr *.o
	rm -fr nocmpldi cmpldi
	
