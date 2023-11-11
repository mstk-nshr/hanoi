# hanoi
A program that solves the 'Tower of Hanoi' problem written in Python.  
It displays disk moves graficaly in ANSI terminal.  

# Usage
<pre>
$ python hanoi.py  [#_of_disks  [us_delay]]
  #_of_disks: number of disks.
  us_delay: delay in micro-seconds.  default = 5,000 us
  e.g.) $ hanoi            ... print usage
        $ hanoi 6 30_000   ... solves 6 disks problem with 30,000us delay
        $ hanoi 7          ... solves 7 disks problem with default 5,000us delay

hanoi.py 3 10000

     |       |      =|=
     |       |     ==|==
     |       |    ===|===
 =========================
   7:d1:1->3

</pre>
