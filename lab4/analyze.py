import os
import re
import sys
import csv
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

v_nkpts=[]
v_alat=[]
v_ecut=[]
v_ene=[]
v_tf=[]


# This defines the patterns for extracting relevant data from the output
# files.
patterns = {
    "energy": re.compile(r"total energy\s+=\s+([\d\.\-]+)\sRy"),
    "ecut": re.compile(r"kinetic\-energy cutoff\s+=\s+([\d\.\-]+)\s+Ry"),
    "alat": re.compile(r"celldm\(1\)=\s+([\d\.]+)\s"),
    "nkpts": re.compile(r"number of k points=\s+([\d]+)"),
    "total_force": re.compile(r"Total force =\s+([\d\.]+)")
}

def get_results(filename):
    data = {}
    with open(filename) as f:
        for l in f:
            for k, p in patterns.items():
                m = p.search(l)
                if m:
                    
                    data[k] = float(m.group(1))
                    continue
    return data


def analyze(filenames):
    fieldnames = ['nkpts', 'alat', 'energy','total_force','ecut']
    os.system("rm Al_nslab.csv")
    with open('Al_nslab.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for f in filenames:
            r = get_results(f)
            writer.writerow(r)
    print("Results written to res.csv!")


if __name__ == "__main__":
     parser = argparse.ArgumentParser(
          description='''Tool for analysis of PWSCF calculations.''')
     parser.add_argument(
          'filenames', metavar='filenames', type=str, nargs="+",
          help='Files to process. You may use wildcards, e.g., "python analyze.py *.out".')
     args = parser.parse_args()
     analyze(args.filenames)

 
from itertools import islice
with open('Al_nslab.csv', 'r') as res1:
    for line in islice(res1, 0, None):
        data1=csv.reader(res1, delimiter=',')
        for row in data1:
             v_nkpts.append(float(row[0]))
             v_alat.append(float(row[1]))
             v_ene.append(float(row[2]))
     #       v_tf.append(float(row[3]))
             v_ecut.append(float(row[4]))
res1.close()

# make changes here
# Force 1 Ry/Bohr = 25.711043 eV/Angstrom
# Energy 1 Ry = 13.605698 eV
length=len(np.array(v_ene))
xx=np.arange(1,(length+1),1)
yy=((np.array(v_ene)-xx*4*(-12.46707456))*13.605698*1.60217733)/(2*1.619574)

#ind=np.where(yy==np.amin(yy))
#print(xx[ind])

plt.plot(xx,yy,marker='o',color='purple',linewidth=1.5,markersize=5)
plt.grid(color='b',lw=0.75)
plt.title('Number of slab vs. surface energy')
plt.xlabel('Number of slab (a.u)')
plt.ylabel('Surface energy (J/m^2)')
plt.savefig('myfig2')
plt.clf()

'''

plt.plot(xx,yy,marker='o',color='blue',linewidth=1.5,markersize=5)
plt.grid(color='b',lw=0.75)
plt.title('Cutoff vs. energy')
plt.xlabel('Cutoff energy (Ry)')
plt.ylabel('Absolute energy (meV/atom)')
plt.savefig('myfig2')
plt.clf()
'''

diff=yy[1:length:1]-yy[0:(length-1):1]
plt.plot(xx[0:(length-1):1],diff,marker='o',color='green',linewidth=1.5,markersize=5)
plt.grid(color='b',lw=0.75)
plt.title('Convergence')
plt.xlabel('Number of slab (a.u.)')
plt.ylabel('Surface energy difference (J/m^2)')
plt.savefig('myfig3')
plt.clf()

os.system("sudo fbi myfig2.png")
