# write out a numpy array of values into a siemens dir forma
# array should have format [ [x1, y1, z1], [x2, y2, z2], ... ]

import numpy as np
import matplotlib.pyplot as plt

class SiemensDir:
    def __init__(self):
        print("SiemensDir CJE Oct 2021")

#  plot functions    
    def plotabs(self):
        print("Dimensions: ", self.dims)
        print("Directions: ", self.ndirs)
        print("Vector max :", np.amax(self.gabs))
        print("Vector min :", np.amin(self.gabs))
        tmp = np.unique(self.gabsrnd, False, False, True)
        print "Grad scalings: ", tmp[0]
        print "Number of Dirs:", tmp[1]
        fig =  plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        ax1.plot(self.gabs)
        plt.show()

    def plotbval(self, maxb):
        print "Dimensions: ", self.dims
        print "Directions: ", self.ndirs
        print "Vector max :", np.amax(self.gabs)
        print "Vector min :", np.amin(self.gabs)
        # first element is unique grad scalings, second element is number of occurences
        tmp = np.unique(self.gabsrnd, False, False, True)
        print "b values:       ", maxb*np.power(tmp[0],2)
        print "Number of dirs: ", tmp[1]
        fig =  plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        ax1.plot(maxb*np.power(self.gabs,2), 'o-')
        plt.show()

# setdir gets the directions from a numpy array (passed from another program)
    def setdir(self, gvec):
        self.gvec = np.array(gvec)
        #print self.gvec
        self.gabs = np.linalg.norm(gvec, None, 1)
        self.gabsrnd = np.around(self.gabs,decimals=3)  #rounded, for checking shells
        self.dims = self.gvec.shape
        print(self.dims[0])
        self.ndirs = self.dims[0]

#add b0 scans every b0gap volumes 
    def addb0(self, b0gap):
        nb0 = np.fix(self.ndirs/b0gap) # num of b0
        newdirs = self.ndirs + nb0
        tempvec = self.gvec
        print self.ndirs, nb0, newdirs
        for ii in range(0,int(newdirs), b0gap):
            tempvec = np.insert(tempvec, ii, [ 0, 0, 0 ], axis = 0)
        self.setdir(tempvec)

    def getdir(self):
        return self.gvec
        
# readdirfile gets directions from existing Siemens dir file.
    def readdirfile(self, filename):
        veclist = []
        ff = open(filename, "r")
        for lne in ff:
            if "vector" in lne:
                vecstr = lne[12:-1].replace('(', '').replace(')','').replace(' ','').replace('\r','')
                vecstr = vecstr.replace('=','').split(',')
                vecflt = [float(j) for j in vecstr]
                veclist.append(vecflt[0:3])   # three values, in case of poorly formatted input file
        vecarr = np.array(veclist)
        self.setdir(vecarr)

# write out in Siemens format
    def writedirfile(self):
        with open("dirout.dir", 'w') as fout:
            print "Opened dirout.dir for writing"
            fout.write("# written by siemensdirclass.py  CJE 7/10/21\n\n")
            fout.write("[directions=" + str(self.ndirs) + "]\n")
            fout.write("Normalisation = none\n")
            fout.write("CoordinateSystem = xyz\n\n")
            for ii in range(0,self.ndirs):
                fout.write("vector[" + str(ii) + "] = (" \
                           + str(self.gvec[ii][0]) + "," \
                           + str(self.gvec[ii][1]) + "," \
                           + str(self.gvec[ii][2])  \
                           + ")\n")
            
        
