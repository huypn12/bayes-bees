dtmc

// pMC
const double p;


module die

	// local state
	s : [0..7] init 0;
	// value of the die
	d : [0..6] init 0;

	[] s=0 -> p : (s'=1) + (1 - p) : (s'=2);
	[] s=1 -> p : (s'=3) + (1 - p) : (s'=4);
	[] s=2 -> p : (s'=5) + (1 - p) : (s'=6);
	[] s=3 -> p : (s'=1) + (1 - p) : (s'=7) & (d'=1);
	[] s=4 -> (1 - p) : (s'=7) & (d'=2) + p : (s'=7) & (d'=3);
	[] s=5 -> (1 - p) : (s'=7) & (d'=4) + p : (s'=2);
	[] s=6 -> (1 - p) : (s'=7) & (d'=5) + p : (s'=7) & (d'=6);
	[] s=7 -> (s'=7);
	
endmodule