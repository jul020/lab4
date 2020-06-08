from __future__ import division
import numpy as np
import math
import argparse


coords100 = np.array(
    [[0.0, 0.0, 0.0],
     [0.5, 0.5, 0.0],
     [0.5, 0.0, 0.5],
     [0.0, 0.5, 0.5]]
)
coords111 = np.array(
    [[0.166666493,         0.083333001,         0.333332986],
     [0.166666493,         0.333333015,         0.333332986],
     [0.166666493,         0.583333015,         0.333332986],
     [0.166666493,         0.833333015,         0.333332986],
     [0.416666508,         0.083333001,         0.333332986],
     [0.416666508,         0.333333015,         0.333332986],
     [0.416666508,         0.583333015,         0.333332986],
     [0.416666508,         0.833333015,         0.333332986],
     [0.666666508,         0.083333001,         0.333332986],
     [0.666666508,         0.333333015,         0.333332986],
     [0.666666508,         0.583333015,         0.333332986],
     [0.666666508,         0.833333015,         0.333332986],
     [0.916666508,         0.083333001,         0.333332986],
     [0.916666508,         0.333333015,         0.333332986],
     [0.916666508,         0.583333015,         0.333332986],
     [0.916666508,         0.833333015,         0.333332986],
     [0.000000000,         0.000000000,         0.000000000],
     [0.000000000,         0.250000000,         0.000000000],
     [0.000000000,         0.500000000,         0.000000000],
     [0.000000000,         0.750000000,         0.000000000],
     [0.250000000,         0.000000000,         0.000000000],
     [0.250000000,         0.250000000,         0.000000000],
     [0.250000000,         0.500000000,         0.000000000],
     [0.250000000,         0.750000000,         0.000000000],
     [0.500000000,         0.000000000,         0.000000000],
     [0.500000000,         0.250000000,         0.000000000],
     [0.500000000,         0.500000000,         0.000000000],
     [0.500000000,         0.750000000,         0.000000000],
     [0.750000000,         0.000000000,         0.000000000],
     [0.750000000,         0.250000000,         0.000000000],
     [0.750000000,         0.500000000,         0.000000000],
     [0.750000000,         0.750000000,         0.000000000],
     [0.083333001,         0.166666493,         0.666666985],
     [0.083333001,         0.416666508,         0.666666985],
     [0.083333001,         0.666666508,         0.666666985],
     [0.083333001,         0.916666508,         0.666666985],
     [0.333333015,         0.166666493,         0.666666985],
     [0.333333015,         0.416666508,         0.666666985],
     [0.333333015,         0.666666508,         0.666666985],
     [0.333333015,         0.916666508,         0.666666985],
     [0.583333015,         0.166666493,         0.666666985],
     [0.583333015,         0.416666508,         0.666666985],
     [0.583333015,         0.666666508,         0.666666985],
     [0.583333015,         0.916666508,         0.666666985],
     [0.833333015,         0.166666493,         0.666666985],
     [0.833333015,         0.416666508,         0.666666985],
     [0.833333015,         0.666666508,         0.666666985],
     [0.833333015,         0.916666508,         0.666666985]]
)


def generate_slab(args):
    a = args.a*3
    nslab = args.nslab
    nvac = args.nvac
    k = args.k
    nlayers = nslab + nvac

    if args.miller == "100":
        pos = coords100.copy()
        calat = nlayers
    else:
        pos = coords111.copy()
        calat = nlayers * math.sqrt(6)

    pos[:, 2] = pos[:, 2] / nlayers

    coords = []
    for i in range(nslab):
        coords.extend(pos + [0, 0, i / nlayers])

    atompos = []
    for i, c in enumerate(coords):
        atompos.append("  Al %s %s %s" % tuple(c))

    atompos = "\n".join(atompos)
    conv_thr = 1e-6 * len(coords)
    with open("Al.%s.surf.pw.in.template" % args.miller) as f:
        contents = f.read()
    contents = contents.format(alat=a, calat=calat, nslab=nslab, nvac=nvac,
            k=k, atompos=atompos, nat=len(coords), conv_thr=conv_thr)

    if args.outfile:
        with open(args.outfile, "wt") as f:
            f.write(contents)
    else:
        print(contents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''Simple tool for generating fcc surface structures for PWSCF calculations.''')
    parser.add_argument(
        '-a', '--a', dest='a', type=float, required=True,
        help='a lattice parameter for cell in Bohr.')
    parser.add_argument(
        '-m', '--miller', dest='miller', type=str, required=True,
        choices=["100", "111"],
        help='Miller index for surface. Only 100 or 111 supported now.')
    parser.add_argument(
        '-k', '--k', dest='k', type=int, required=True,
        help='k points for a b direction.')
    parser.add_argument(
        '-s', '--nslab', dest='nslab', type=int, required=True,
        help='Number of layers for slab. Must be integer multiples of conventional fcc lattice.')
    parser.add_argument(
        '-v', '--nvac', dest='nvac', type=int, required=True,
        help='Number of layers for vacuum. Must be integer multiples of conventional fcc lattice.')
    parser.add_argument(
        '-o', '--outfile', dest='outfile', type=str,
        help='File to write PWSCF input file to.')
    args = parser.parse_args()
    generate_slab(args)