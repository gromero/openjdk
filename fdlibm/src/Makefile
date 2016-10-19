CFLAGS=-I../include -g -O3

%.o:	%.c
	gcc $(CFLAGS) -c $< -o $@

s_cos:  s_cos.o k_cos.o k_sin.o e_rem_pio2.o k_rem_pio2.o s_floor.o s_fabs.o call_s_cos.o
	gcc $(CFLAGS) s_cos.o k_cos.o k_sin.o e_rem_pio2.o k_rem_pio2.o s_floor.o s_fabs.o call_s_cos.o -o call_s_cos

clean:
	rm -fr perf.*
	rm -fr *.o
	rm -fr call_s_cos
	rm -fr main libfoo.so
