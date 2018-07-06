#include <stdio.h>

int main()
{
  class bitz {
    public: 
      enum {
        abort = 1,
        footprint = 4,
        nested = 5,
        conflict_tm = 6,
        conflict_non_tm = 43,
        NUM_BITZ = 5,
      };
  };

  class mask {
    public:
      enum {
        abort = 1,
        footprint = 1,
        nested = 11,
        conflict_tm = 1,
        conflict_non_tm = 1,
        NUM_MASK = 5,
      };
  }; 
    
  class counter {
   public:
     enum {
       conflict,
       abort,
       nested,
       footprint,
       NUM_COUNTER,
     }; 
  };

  class s {
    public:
    class C {
    public:
      enum {
        x,
        y,
      };
    };
  };

  bool tm_counter[][counter::NUM_COUNTER] =
  // counters                                 confl.,  aborts, nests, footprint // bits

                                            {{ true ,  false , false, false },  // bit conflict_tm
                                             { true ,  false , false, false },  // bit conflict_non_tm
                                             { false,  true  , false, false },  // bit abort
                                             { false,  false , false, true  },  // bit footprint
                                             { true ,  false , true , false }}; // bit nested

  const int nindex_to_bit[] = { bitz::abort, bitz::footprint, bitz::nested, bitz::conflict_tm, bitz::conflict_non_tm };
  const char *nindex_to_counter_name[counter::NUM_COUNTER] = { "conflict", "abort", "nested", "footprint" };
  const int nindex_to_masksize [] = { mask::abort, mask::footprint, mask::nested, mask::conflict_tm, mask::conflict_non_tm };
  int counter;
  int bit;

  printf("x,y = %d,%d\n", s::C::x, s::C::y);
  printf("# Bits     = %d\n"  , bitz::NUM_BITZ);
  printf("# Counters = %d\n\n", counter::NUM_COUNTER);

  for (bit = 0; bit < bitz::NUM_BITZ; bit++) {
    for (counter = 0; counter < counter::NUM_COUNTER; counter++) {
      if (tm_counter[bit][counter] == true) {

        switch (nindex_to_bit[bit]) {
          case bitz::conflict_non_tm:
          case bitz::conflict_tm:
            printf("Check #1: bit %d -> counter %d (%s), mask size is %d\n",
                     nindex_to_bit[bit], counter, nindex_to_counter_name[counter], nindex_to_masksize[bit]);
            break;

          case bitz::abort:
          case bitz::footprint:
          case bitz::nested:
            printf("Check #2: bit %d -> counter %d (%s), mask size is %d\n",
                     nindex_to_bit[bit], counter, nindex_to_counter_name[counter], nindex_to_masksize[bit]);
            break;
          default:
            break;
        }
      }
    }
  }
}
