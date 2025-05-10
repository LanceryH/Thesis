import numpy as np
import rupho as rp

def photometry(
    w_list: list,
    bc_list: list,
    dzeta_list: list,
    b0_list: list,
    h_list: list,
    path_r: tuple,
    path_s: str):

    """
    Arguments:
        w_list: (float): list of w
        bc_list: (float): list of b and c
        dzeta_list: (float): list of dzeta
        b0_list: (float): list of B0
        h_list: (float): list of h
        paths: (tuple): list of paths for the geom.npz files

    Description:
        This code browse all available combination and vertically stack all given geom.npz arrays (emergence, incidence, etc..).
        It then calculates the reflectance for the given total combination.
        The results are saved in a '.npz'.

    Result:
        ph_g"IDs"_"cominations"(.npz): contains a dict with incidence, emergence, phase, azimuth, reflectance, params

    """

    incidence = []
    emergence = []
    azimuth = []
    phase = []
    name = ""

    for fle in path_r:
        geom_npz = np.load(fle)
        incidence = np.hstack((incidence,geom_npz["incidence"]))
        emergence = np.hstack((emergence,geom_npz["emergence"]))
        phase = np.hstack((phase,geom_npz["phase"]))
        azimuth = np.hstack((azimuth,geom_npz["azimuth"]))
        name += fle.split('/')[-1][:-4]+"_"

    for w in w_list:
        for b,c in bc_list:
            for z in dzeta_list:
                for o in b0_list:
                    for h in h_list:
                        micro_struct = (w, b, c, z, o, h)
                        scene_geometry = (incidence, emergence, azimuth)
                        reflectance = rp.reflectance(micro_struct,*scene_geometry)
                        path_save = f"{path_s}/pho-{name[:-1]}-{str(w)}_{str(b)}_{str(c)}_{str(z)}"
                        np.savez(file=path_save,
                                 incidence=incidence,
                                 emergence=emergence,
                                 phase=phase,
                                 azimuth=azimuth,
                                 reflectance=reflectance,
                                 params=(w,b,c,z/45,o,h))

