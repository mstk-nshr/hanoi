#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy, sys, time

# %% --------------------------------------------------------------------------
def prUsage():
    print("""hanoi  version 23.11.10
'Tower Of Hanoi' problem solver written in python3.  
It displays disk moves graficaly in ANSI terminal.  

Usage:
$ python hanoi.py  [#_of_disks  [us_delay]]
  #_of_disks: number of disks.
  us_delay: delay in micro-seconds.  default = 5,000 us
  e.g.) $ hanoi            ... print usage
        $ hanoi 6 30_000   ... solves 6 disks problem with 30,000us delay
        $ hanoi 7          ... solves 7 disks problem with default 5,000us delay
""")

# %% --------------------------------------------------------------------------
class hanoi():
    mvnum = 0
    kDisk = "="     # "█"     #"\u2550"    "="
    kDisk2 = "|"    # "█"    #"\u254b"    "\u256a"   # "+"
    kVbar = "|"     # "┃"     #"\u2503"    "|"
    kBase = "="     # "█"     #"\u2501"    "="
    kBase2 = "="    # "█"    #"\u253b"    "┴"

    def __init__(self, ndisks=6, usdelay=5000):
        self.ndisks = ndisks
        self.sdelay = usdelay * 0.000001
        self.empty = " "*ndisks + " " + " "*ndisks
        self.disk = []
        for rr in range(ndisks+1):
            if rr == 0: self.disk.append(" " * ndisks + self.kVbar + " " * ndisks) # "|"
            else: self.disk.append(" " * (ndisks - rr) + self.kDisk * rr + self.kDisk2 + self.kDisk * rr + " " * (ndisks - rr)) # "="  "|"
        print("hanoi", *gPrms, sep=' ')

        self.view = [list(range(ndisks, 0, -1)), [], []]
        self.dspView(self.view)
        print(" %s\n\n" % (self.kBase +  self.kBase * self.ndisks + self.kBase2 + self.kBase * self.ndisks + 
                           self.kBase +  self.kBase * self.ndisks + self.kBase2 + self.kBase * self.ndisks + 
                           self.kBase +  self.kBase * self.ndisks + self.kBase2 + self.kBase * self.ndisks + self.kBase))
        print("\x1b[2A", end='')        # cursor UP
        print("\x1b7", end='')          # save cursor position
        print(" ")
        print("\x1b[?25l", end='')      # set cursor invisible
        print("\x1b7", end='')          # save cursor position
        print("\x1b[A                                ")  # erase prompt
        self.mvDisks(ndisks, 0, 2, 1, self.view)
        #if dtype == 0: print("\x1b7", end='')          # save cursor position

    def dspView(self, vw):
        vw0 = copy.deepcopy(vw)
        zz = [0] * self.ndisks
        for ii in range(3):
            aa = vw0[ii] + zz
            vw0[ii] = aa[:self.ndisks]
        print("  ")
        for rr in reversed(range(self.ndisks)):
            print("  ", end='')
            for cc in range(3):
                print(self.disk[vw0[cc][rr]],end=' ')
            print("")

    def move1(self, dk, fr, to, vw):
        vw99 = copy.deepcopy(vw)
        a = vw99[fr].pop()
        vw99[to].append(a)
        
        # print moving view
        self.mvnum += 1
        vw0 = copy.deepcopy(vw)
        vw990 = copy.deepcopy(vw99)
        zz = [0] * self.ndisks
        for ii in range(3):
            aa = vw0[ii] + zz
            vw0[ii] = aa[:self.ndisks]
            aa = vw990[ii] + zz
            vw990[ii] = aa[:self.ndisks]
        print("\x1b[%dA" % (self.ndisks+2), end='') # UP

        for rr in reversed(range(self.ndisks)):
            print("  ", end='')
            for cc in range(3):
                print(self.disk[vw0[cc][rr]], end=' ')
            print("")
        print("\n%4d:d%d:%d->%d " % (self.mvnum, dk, fr + 1, to + 1))

        # UP
        for rr in range(self.ndisks):  # BOTTOM [0(d4),1(d3),2(d2),3(d1),4(0)] TOP
            v = vw0[fr][rr]
            if v == dk: vw0[fr][rr] = 0
            else: continue
            if rr + 1 < self.ndisks: vw0[fr][rr+1] = dk
            print("\x1b[%dA" % (self.ndisks+3), end='')  # move cursor to home position
            #
            self.dspView(vw0)
            if rr + 1 < self.ndisks: time.sleep(self.sdelay * 2)
            print("\n")
        
        # MOVE HORIZONTAL
        empty = self.empty
        sp = [empty,empty,empty]
        print("\x1b[%dA" % (self.ndisks+3), end='')  # move cursor to home position
        sp[fr] = self.disk[dk]
        aa = "  %s %s %s " % (sp[0],sp[1],sp[2])
        aa = aa.replace(self.kDisk2, self.kDisk).replace('.',' ')
        print(aa, end='\r')
        time.sleep(self.sdelay)
        sp[fr] = empty
        
        if fr < to: # move right
            dist = (to - fr) * (self.ndisks * 2 + 2)
            for ii in range(dist):
                aa = " " + aa[:-1]
                print(aa, end='\r')
                time.sleep(self.sdelay)
        else: # move right
            dist = (fr - to) * (self.ndisks * 2 + 2)
            for ii in range(dist):
                aa = aa[1:] + ' '
                print(aa, end='\r')
                time.sleep(self.sdelay)

        # DOWN
        print("  %s %s %s " % (sp[0],sp[1],sp[2]), end='\r')
        for rr in reversed(range(self.ndisks)):  # BOTTOM [4(0),3(d1),2(d2),1(d3),0(d4)] TOP
            v = vw0[to][rr]
            if v == 0: vw0[to][rr] = dk
            else: continue
            if rr + 1 < self.ndisks: vw0[to][rr+1] = 0
            #
            self.dspView(vw0)
            print("\n")
            print("\x1b[%dA" % (self.ndisks+3), end='')  # cursor to HOME
            time.sleep(self.sdelay * 2)
        pass

        # LAST
        time.sleep(self.sdelay)
        print("  %s %s %s " % (sp[0],sp[1],sp[2]), end='\r')
        self.dspView(vw990)
        print("\n")
        
        return vw99

    def mvDisks(self, nd, fr, to, work, vw):  # move disks(1..nd) from pole-fr to pole-to.
        if nd == 1:
            vw3 = self.move1(nd, fr, to, vw)
        else:
            vw1 = self.mvDisks(nd - 1, fr, work, to, vw)
            vw2 = self.move1(nd, fr, to, vw1)
            vw3 = self.mvDisks(nd - 1, work, to, fr, vw2)
        return vw3
    
# %% --------------------------------------------------------------------------
def main():
    global gPrms
    gPrms = sys.argv[1:]
    if len(gPrms) == 0:
        prUsage()
        gPrms = [3, 10_000]
    try:
        print("\x1b7", end='')          # save cursor position
        arg_err = True
        gPrms = [int(i) for i in gPrms]
        arg_err = False
        hanoi(*gPrms)
        print("\x1b8")                  # restore cursor position
    except:
        print("\x1b8")                  # restore cursor position
        if arg_err:
            prUsage()
    print("\x1b[?25h", end='')      # set cursor visible

# %% --------------------------------------------------------------------------
if __name__ == "__main__":
    main()
