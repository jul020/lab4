import os
import shutil
import numpy as np

# Load the Si.pw.in.template file as a template.
with open("H2.pw.in.template") as f:
    template = f.read()

# Set default values for various parameters
k = 18 # k-point grid of 16x16x16
alat = 15.118 # The lattice parameter for the cell in Bohr.
ecut = 50
ecutrho = ecut*10
x = 0.742/0.529177208/alat
y = 0
z = 0

# Loop through different k-points.
for k in np.arange(18, 26, 2):
    # This generates a string from the template with the parameters replaced
    # by the specified values.
    s = template.format(k=k, alat=alat, ecut=ecut, ecutrho=ecutrho, x=x, y=y, z=z)

    # Let's define an easy jobname.
    jobname = "H2_%s_%s_%s" % (k, alat, ecut)

    # Write the actual input file for PWSCF.
    with open("%s.pw.in" % jobname, "w") as f:
        f.write(s)

    #Print some status messages.
    # print("Running with alat = %s..." % (alat))
    # Run PWSCF. Modify the pw.x command accordingly if needed.
    os.system("pw.x -inp {jobname}.pw.in > {jobname}.out".format(jobname=jobname))

    print("Done. Output file is %s.out." % jobname)

# This just does cleanup. For this lab, we don't need the files that are
# dumped into the tmp directory.
shutil.rmtree("tmp")
