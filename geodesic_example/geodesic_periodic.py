from carmm.build.neb.geodesic_utils import timing

@timing
def run_geodesic_interpolator(initial, final):

    from carmm.build.neb.geodesic import GeodesicInterpolator

    # Test the initialised path
    geodesic = GeodesicInterpolator(initial, final, 6)
    geodesic.init_path()

    # Test the iteratively smoothed path
    geodesic.sweep_iterative(sweeperiter=5)

    return geodesic.images

@timing
def run_linear_interpolator(initial, final):

    from ase.neb import NEB

    images = [initial]
    images += [initial.copy() for i in range(4)]
    images += [final]
    neb = NEB(images)

    neb.interpolate()

    return neb.images

@timing
def run_idpp_interpolator(initial, final):

    from ase.neb import NEB

    images = [initial]
    images += [initial.copy() for i in range(4)]
    images += [final]
    neb = NEB(images)

    neb.interpolate(method='idpp')

    return neb.images

if __name__ == "__main__":

    from ase.io import read, write
    from carmm.analyse.neighbours import neighbours    

    initial = read("zeolite_reaction.traj", index=0)
    final = read("zeolite_reaction.traj", index=-1)

    cha_nat=108
    centers = [19]
    adsorption_centers, junk = neighbours(initial[:cha_nat], centers, 4)
    movers = adsorption_centers+[*range(cha_nat, len(final), 1)]

    mask = [atom.index not in movers for atom in initial]
    
    linear_path = run_linear_interpolator(initial, final)
    write("linear_path_zeolite.traj", linear_path)

    idpp_path = run_idpp_interpolator(initial, final)
    write("idpp_path_zeolite.traj", idpp_path)
    
    geodesic_path = run_geodesic_interpolator(initial, final)
    write("geodesic_path_zeolite.traj", geodesic_path)
