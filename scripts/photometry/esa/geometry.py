import numpy as np

def geometry(
    OBS_lat: tuple,
    TAR_lonlat: tuple,
    SOL_lonlat: tuple,
    path_s: str=".",
    id: str="",
    n_steps: int=10000,
    observer_alt: float=50.0,
    emergence_max: float=80.0,
    moon_radius: float=1734.0,
    ):

    """
    Arguments:
        OBS_lat (tuple): Position parameter the observer orbit max and min lat in (deg).
        TAR_lonlat (tuple): Position parameter the taget lon and lat in (deg).
        SOL_lonlat (tuple): Position parameter the light lon and lat in (deg).
        path (str, optional): Path for the .npz to get saved to.
        id (int, optional): Scenario number ID. Defaults to 0.
        n_steps (int, optional): number of steps for the propagation of the orbit. Defaults to 1000.
        observer_alt (float, optional): Altitud parameter for the observer in (km). Defaults to 50.
        emergence_max (float, optional): Emergence max considered in (deg). Defaults to 89.
        moon_radius (int, optional): Radius of the moon studied in (km). Defaults to 1734.

    Description:
        Using input arguments, the observer, target and light get propagate n_steps times.
        The observer is propagated through lat=0 from OBS_lat min and max.
        The target and light are considered fix, in order to match the size of the observer array,
        their position is repeated n_steps times.
        The incidence, emergence, phase and azimuth are then calculated based on the github project main graph.
        C: Center of the moon (point)
        O: Observer (satellite point)
        T: Target (surface point)
        L: Light (Subsolar point)
        The results are saved in a '.npz'

    Result:
        g"ID"(.npz): contains a dict with incidence, emergence, phase, azimuth array

    """

    def propage_pos(alt: float, lon: tuple, lat: tuple) -> np.ndarray:
        "linear propagation of the spherical position"
        a = np.repeat(alt, n_steps)
        b = np.linspace(lon[0], lon[1], n_steps)
        c = np.linspace(lat[0], lat[1], n_steps)
        return np.vstack((a,b,c))

    def sphe_to_cart(sphe_pos: np.ndarray) -> np.ndarray:
        "calculate the cartesian position from the spherical"
        a = sphe_pos[0,:] * np.cos(np.deg2rad(sphe_pos[2,:])) * np.sin(np.deg2rad(sphe_pos[1,:]))
        b = sphe_pos[0,:] * np.cos(np.deg2rad(sphe_pos[2,:])) * np.cos(np.deg2rad(sphe_pos[1,:]))
        c = sphe_pos[0,:] * np.sin(np.deg2rad(sphe_pos[2,:]))
        return np.vstack((a,b,c))

    # Propagation of the the orbit
    sat_sphe_pos = propage_pos(moon_radius+observer_alt,(0,0),(OBS_lat[0], OBS_lat[1]))
    target_sphe_pos = propage_pos(moon_radius,(TAR_lonlat[0], TAR_lonlat[0]),(TAR_lonlat[1], TAR_lonlat[1]))
    sun_sphe_pos = propage_pos(moon_radius,(SOL_lonlat[0], SOL_lonlat[0]),(SOL_lonlat[1], SOL_lonlat[1]))
    pol_nord = propage_pos(moon_radius,(0,0),(90,90))
    
    # Calculate cartesian position
    sat_cart_pos = sphe_to_cart(sat_sphe_pos)
    target_cart_pos = sphe_to_cart(target_sphe_pos)
    sun_cart_pos = sphe_to_cart(sun_sphe_pos)
    pol_nord = sphe_to_cart(pol_nord)
    
    # Calculate all incidence angles
    incidence = np.ones(n_steps)
    for i in range(n_steps):
        CL = sun_cart_pos[:,i]
        CT = target_cart_pos[:,i]
        incidence[i] = np.rad2deg(np.arccos(np.dot(CL,CT) / (np.linalg.norm(CL) * np.linalg.norm(CT))))

    # Calculate all emergence angles
    emergence = np.ones(n_steps)
    for i in range(n_steps):
        CT = target_cart_pos[:,i]
        TO = sat_cart_pos[:,i]-target_cart_pos[:,i]
        emergence[i] = np.rad2deg(np.arccos(np.dot(CT,TO) / (np.linalg.norm(CT) * np.linalg.norm(TO))))

    # Calculate all phase angles
    phase = np.ones(n_steps)
    for i in range(n_steps):
        CL = sun_cart_pos[:,i]
        TO = sat_cart_pos[:,i]-target_cart_pos[:,i]
        phase[i] = np.rad2deg(np.arccos(np.dot(CL,TO) / (np.linalg.norm(CL) * np.linalg.norm(TO))))

    # Calculate all azimuth angles
    azimuth = np.ones(n_steps)
    azimuth_N_inc = np.ones(n_steps)
    azimuth_N_eme = np.ones(n_steps)
    for i in range(n_steps):
        CL = sun_cart_pos[:,i]
        CT = target_cart_pos[:,i]
        CO = sat_cart_pos[:,i]
        TO = CO-target_cart_pos[:,i]
        TN = pol_nord[:,i]-target_cart_pos[:,i]
        TOprim = (TO/np.linalg.norm(TO)) - np.dot((TO/np.linalg.norm(TO)), (CT/np.linalg.norm(CT)))*(CT/np.linalg.norm(CT))
        TLprim = (CL/np.linalg.norm(CL)) - np.dot((CL/np.linalg.norm(CL)), (CT/np.linalg.norm(CT)))*(CT/np.linalg.norm(CT))
        TNprim = (TN/np.linalg.norm(TN)) - np.dot((TN/np.linalg.norm(TN)), (CT/np.linalg.norm(CT)))*(CT/np.linalg.norm(CT))
        CTorth = np.cross(CT/np.linalg.norm(CT),TOprim/np.linalg.norm(TOprim))
        CTirth = np.cross(CT/np.linalg.norm(CT),TLprim/np.linalg.norm(TLprim))
        azimuth[i] = -np.sign(np.dot(TLprim, CTorth))*np.rad2deg(np.arccos(np.clip(np.dot(TLprim,TOprim)/(np.linalg.norm(TLprim)*np.linalg.norm(TOprim)), -1.0, 1.0)))
        azimuth_N_eme[i] = -np.sign(np.dot(TNprim, CTorth))*np.rad2deg(np.arccos(np.clip(np.dot(TNprim, TOprim) / (np.linalg.norm(TNprim) * np.linalg.norm(TOprim)), -1.0, 1.0)))
        azimuth_N_inc[i] = -np.sign(np.dot(TNprim, CTirth))*np.rad2deg(np.arccos(np.dot(TNprim,TLprim) / (np.linalg.norm(TNprim) * np.linalg.norm(TLprim))))

    # Calculate offnadir angles
    offnad = np.ones(n_steps)
    for i in range(n_steps):
        CO = sat_cart_pos[:,i]
        OT = sat_cart_pos[:,i]-target_cart_pos[:,i]
        offnad[i] = np.rad2deg(np.arccos(np.dot(CO,OT) / (np.linalg.norm(CO) * np.linalg.norm(OT))))

    # Filter 1 valid emergence [False, False, ..., True, True, ..., False, False]
    filter_emergence = [emergence<emergence_max][0]

    # Apply filter 1
    incidence = incidence[filter_emergence]
    emergence = emergence[filter_emergence]
    phase = phase[filter_emergence]
    azimuth = azimuth[filter_emergence]
    azimuth_N_inc = azimuth_N_inc[filter_emergence]
    azimuth_N_eme = azimuth_N_eme[filter_emergence]
    offnad = offnad[filter_emergence]
    sat_alt = sat_sphe_pos[0,:][filter_emergence]
    sat_lon = sat_sphe_pos[1,:][filter_emergence]
    sat_lat = sat_sphe_pos[2,:][filter_emergence]
    tar_lon = target_sphe_pos[1,:][filter_emergence]
    tar_lat = target_sphe_pos[2,:][filter_emergence]
    sun_lon = sun_sphe_pos[1,:][filter_emergence]
    sun_lat = sun_sphe_pos[2,:][filter_emergence]


    # Filter 1 shots from satellite in the right range of emergence
    min_arg = np.argmin(emergence) # Minimal emergence arguments post filtering
    min_inter_arg = min_arg//2 # Emergence between the minimum and the initial post filter value
    shots_args = [0, min_inter_arg,  min_arg, -min_inter_arg, -1]

    # Apply filter 2
    incidence = incidence[shots_args]
    emergence = emergence[shots_args]
    phase = phase[shots_args]
    azimuth = azimuth[shots_args]
    azimuth_N_inc = azimuth_N_inc[shots_args]
    azimuth_N_eme = azimuth_N_eme[shots_args]
    offnad = offnad[shots_args]
    sat_alt = sat_alt[shots_args]
    sat_lon = sat_lon[shots_args]
    sat_lat = sat_lat[shots_args]
    tar_lon = tar_lon[shots_args]
    tar_lat = tar_lat[shots_args]
    sun_lon = sun_lon[shots_args]
    sun_lat = sun_lat[shots_args]

    path_s = f"{path_s}/{id}"

    np.savez(file=path_s,
             incidence=incidence,
             emergence=emergence,
             phase=phase,
             azimuth=azimuth,
             offnad=offnad,
             sat_alt=sat_alt,
             sat_lon=sat_lon,
             sat_lat=sat_lat,
             tar_lon=tar_lon,
             tar_lat=tar_lat,
             sun_lon=sun_lon,
             sun_lat=sun_lat)
             
    return