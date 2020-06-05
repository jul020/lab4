import os
import shutil
import numpy as np

# Load the Si.pw.in.template file as a template.
with open("Al.111.H4.et0.template") as f:
    template = f.read()

# Set default values for various parameters
i=0

# Loop through different k-points.
for i in np.arange(0, 10, 10):
    # This generates a string from the template with the parameters replaced
    # by the specified values.
    # s = template.format(k1=k1, k3=k3, alat=alat, ecut=ecut)

    # Let's define an easy jobname.
    jobname = "Al_111_H4_hole_A_site_%s" % (i)

    # Write the actual input file for PWSCF.
    with open("%s.pw.in" % jobname, "w") as f:
        f.write(template)

    #Print some status messages.
    # print("Running with ecut = %s..." % (ecut))
    # Run PWSCF. Modify the pw.x command accordingly if needed.
    os.system("pw.x -inp {jobname}.pw.in > {jobname}.out".format(jobname=jobname))

    print("Done. Output file is %s.out." % jobname)

# This just does cleanup. For this lab, we don't need the files that are
# dumped into the tmp directory.
shutil.rmtree("tmp")
