dtmc 
 
const double p;
const double q1;
const double q2;

module multi_param_agents_3
       // ai - state of agent i:  -1:init 0:total_failure 1:succes 2:failure_after_first_attempt
       a0 : [-1..2] init -1; 
       a1 : [-1..2] init -1; 
       a2 : [-1..2] init -1; 
       b : [0..1] init 0; 

       //  initial transition
       []   a0 = 3 & a1 = 3  & a2 = 3 -> 1.0*p*p*p: (a0'=1) & (a1'=1) & (a2'=1) + 3.0*p*p*(1-p): (a0'=1) & (a1'=1) & (a2'=2) + 3.0*p*(1-p)*(1-p): (a0'=1) & (a1'=2) & (a2'=2) + 1.0*(1-p)*(1-p)*(1-p): (a0'=2) & (a1'=2) & (a2'=2);

       // some ones, some zeros transitions
       []   a0 = 0 & a1 = 0 & a2 = 0 -> (a0'= 0) & (a1'= 0) & (a2'= 0) & (b'=1);
       []   a0 = 1 & a1 = 0 & a2 = 0 -> (a0'= 1) & (a1'= 0) & (a2'= 0) & (b'=1);
       []   a0 = 1 & a1 = 1 & a2 = 0 -> (a0'= 1) & (a1'= 1) & (a2'= 0) & (b'=1);
       []   a0 = 1 & a1 = 1 & a2 = 1 -> (a0'= 1) & (a1'= 1) & (a2'= 1) & (b'=1);

       // some ones, some twos transitions
       []   a0 = 1 & a1 = 2 & a2 = 2 -> 1.0*(1-q1)*(1-q1): (a0'=1) & (a1'=0) & (a2'=0) + 2.0*q1*(1-q1): (a0'=1) & (a1'=1) & (a2'=0) + 1.0*q1*q1: (a0'=1) & (a1'=1) & (a2'=1);
       []   a0 = 1 & a1 = 1 & a2 = 2 -> 1.0*(1-q2): (a0'=1) & (a1'=1) & (a2'=0) + 1.0*q2: (a0'=1) & (a1'=1) & (a2'=1);

       // all twos transition
       []   a0 = 2 & a1 = 2  & a2 = 2 -> (a0'= 0) & (a1'= 0) & (a2'= 0);
endmodule 

rewards "mean" 
       a0 = 0 & a1 = 0 & a2 = 0:0;
       a0 = 1 & a1 = 0 & a2 = 0:1;
       a0 = 1 & a1 = 1 & a2 = 0:2;
       a0 = 1 & a1 = 1 & a2 = 1:3;
endrewards 
rewards "mean_squared" 
       a0 = 0 & a1 = 0 & a2 = 0:0;
       a0 = 1 & a1 = 0 & a2 = 0:1;
       a0 = 1 & a1 = 1 & a2 = 0:4;
       a0 = 1 & a1 = 1 & a2 = 1:9;
endrewards 
