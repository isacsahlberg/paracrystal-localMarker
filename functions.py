import math
import numpy as np


def heart(x_, y_, x0=0, y0=0):
    """Simple equation of the heart"""
    x = x_-x0
    y = y_-y0
    return (x**2 + y**2 - 1)**3 <= x**2 * y**3


def giveChosenHeart(X_in, Y_in):
    """From any set of (x,y)-coordinates,
    get a cutout which is heart-shaped (boolean array)
    """
    assert X_in.shape == Y_in.shape, 'Coordinate pairs do not match in length'
    
    # Find the middle of the lattice
    x0, y0, idx_mid, _ = find_mid_point(X_in, Y_in)
    X_ = X_in - X_in.mean()
    Y_ = Y_in - Y_in.mean()
    X = 1.37*X_/(X_.max())
    Y = 1.3*Y_/(Y_.max())+0.15
    chosen_heart = np.full(X.shape, False)
    for i,(x,y) in enumerate(zip(X, Y)):
        chosen_heart[i] = heart(x, y)
    return chosen_heart


def find_mid_point(X, Y, xy_tuple_0=None):
    """Find the closest (x,y)-point to the middle, or the input tuple"""
    assert len(X)==len(Y), 'arrays X,Y need to be of same len()'

    # Around what point are we considering
    if not xy_tuple_0 is None:
        x0, y0 = xy_tuple_0
    else:
        x0, y0 = np.mean(X), np.mean(Y)  # if nothing given, take center of the points in both directions
    
    e = 1e-3  # small bias
    # List of distances to the fixed point (x0,y0), w/ slight bias for smaller x, [and then] smaller y
    dists = [math.dist((x,y),(x0,y0))+e*(x+y+e*y) for (x,y) in zip(X,Y)]
    # Now we have unique distances, and we can take the min
    idx_mid = np.argmin(dists)
    return X[idx_mid], Y[idx_mid], idx_mid, round(dists[idx_mid],2)


def getSubsystemCutout(Lx, Ly, Xvec_full, Yvec_full):
    """Cut out a box of size Lx-by-Ly from the given set of (x,y)-coordinates"""
    # The "full" system has an extent
    Lx_full = max(Xvec_full) - min(Xvec_full)  # the extent in x direction
    Ly_full = max(Yvec_full) - min(Yvec_full)
    
    # The borders are of size
    border_x = (Lx_full-Lx)/2
    border_y = (Ly_full-Ly)/2
    box_x_max, box_x_min = max(Xvec_full)-border_x, min(Xvec_full)+border_x  # can be used to draw the borders
    box_y_max, box_y_min = max(Yvec_full)-border_y, min(Yvec_full)+border_y

    # The boolean array for the desired points is 
    chosen_points = (box_x_min<=Xvec_full) & (Xvec_full<=box_x_max) & (box_y_min<=Yvec_full) & (Yvec_full<=box_y_max)
    Xvec_in = Xvec_full[chosen_points]
    Yvec_in = Yvec_full[chosen_points]
    return Xvec_in, Yvec_in, chosen_points, (box_x_min, box_x_max), (box_y_min, box_y_max)


def chooseRandomBulkPoints(Xvec, Yvec, Lx, Npoints, seed=None, border=5):
    """Randomly choose points from given set of (x,y)-coordinates

    Exlcuding borders of thickness 'border', randomly choose some points
    from the given set of (x,y)-coordinates.
    If Npoints > len(Xvec), then the maximum number of points is chosen (still exluding borders)
    """    
    # Create an RNG generator, and use it to draw random numbers
    rng = np.random.default_rng(seed)
    
    # Choose a box from the center which excludes the borders
    Lx_in = max(2, Lx-2*border)
    # _, _, chosen_points_all, (box_x_min,box_x_max), (box_y_min,box_y_max) = getSubsystemCutout(Lx_in, Lx_in, Xvec, Yvec)
    _, _, chosen_points_all, _, _ = getSubsystemCutout(Lx_in, Lx_in, Xvec, Yvec)
    
    # Randomly pick N_points indices from the indices that are True here
    Npoints = Npoints if Npoints < chosen_points_all.sum() else chosen_points_all.sum()
    ix_chosen_points = rng.choice(np.where(chosen_points_all)[0], size=Npoints, replace=False)
    
    # Create an array of False values, and set to True the ones that have been picked
    chosen_points = np.full(Xvec.shape, False)  # np.zeros(Xvec.shape, dtype=bool)
    chosen_points[ix_chosen_points] = True
    return chosen_points