import math
import numpy as np
from numba import jit

#compute cotangent
@jit(nopython=True)
def cot_numba(x):
    if math.sin(x) == 0.:
        return 10.**16    
    else:
        return math.cos(x)/math.sin(x)

@jit(nopython=True)
def e1_numba(dzeta,x):
    return math.exp(-2./math.pi*cot_numba(dzeta)*cot_numba(x))

@jit(nopython=True)
def e2_numba(dzeta,x):
    return math.exp(-1./math.pi*cot_numba(dzeta)**2*cot_numba(x)**2)


'''
computing equivalent geometry for a given roughness factor
'''

@jit(nopython=True)
def correct_numba(incidence, emergence, azimuth, dzeta):
    #conversion in rad
    incidence_rad=incidence*math.pi/180.
    emergence_rad=emergence*math.pi/180.
    dzeta_rad=dzeta*math.pi/180.
    
    xidz=1./math.sqrt(1.+math.pi*math.tan(dzeta_rad)**2)
    
    if azimuth >= math.pi:
        azimuth=2.*math.pi-azimuth
    """ version pas toouché
    if incidence <= emergence:
        #cosinus of incidence 
        muo=(math.cos(incidence_rad)+math.sin(incidence_rad)*math.tan(dzeta_rad)*(math.cos(azimuth)*e2_numba(dzeta_rad,emergence_rad)+math.sin(azimuth/2.)**2*e2_numba(dzeta_rad,incidence_rad))/(2.-e1_numba(dzeta_rad,emergence_rad)-(azimuth/math.pi)*e1_numba(dzeta_rad,incidence_rad)))*xidz    
        #cosinus of emergence 
        mu=(math.cos(emergence_rad)+math.sin(emergence_rad)*math.tan(dzeta_rad)*(e2_numba(dzeta_rad,emergence_rad)-math.sin(azimuth/2.)**2*e2_numba(dzeta_rad,incidence_rad))/(2.-e1_numba(dzeta_rad,emergence_rad)-(azimuth/math.pi)*e1_numba(dzeta_rad,incidence_rad)))*xidz
        #factor
        muo_b=(math.cos(incidence_rad)+math.sin(incidence_rad)*math.tan(dzeta_rad)*e2_numba(dzeta_rad,emergence_rad)/(2.-e1_numba(dzeta_rad,emergence_rad)))*xidz
        #factor
        mu_b=(math.cos(emergence_rad)+math.sin(emergence_rad)*math.tan(dzeta_rad)*e2_numba(dzeta_rad,emergence_rad)/(2.-e1_numba(dzeta_rad,emergence_rad)))*xidz

    else:
        muo=(math.cos(incidence_rad)+math.sin(incidence_rad)*math.tan(dzeta_rad)*(e2_numba(dzeta_rad,incidence_rad)-math.sin(azimuth/2.)**2*e2_numba(dzeta_rad,emergence_rad))/(2.-e1_numba(dzeta_rad,incidence_rad)-(azimuth/math.pi)*e1_numba(dzeta_rad,emergence_rad)))*xidz
        mu=(math.cos(emergence_rad)+math.sin(emergence_rad)*math.tan(dzeta_rad)*(math.cos(azimuth)*e2_numba(dzeta_rad,incidence_rad)+math.sin(azimuth/2.)**2*e2_numba(dzeta_rad,emergence_rad))/(2.-e1_numba(dzeta_rad,incidence_rad)-(azimuth/math.pi)*e1_numba(dzeta_rad,emergence_rad)))*xidz
        muo_b=(math.cos(incidence_rad)+math.sin(incidence_rad)*math.tan(dzeta_rad)*e2_numba(dzeta_rad,incidence_rad)/(2.-e1_numba(dzeta_rad,incidence_rad)))*xidz
        mu_b=(math.cos(emergence_rad)+math.sin(emergence_rad)*math.tan(dzeta_rad)*e2_numba(dzeta_rad,incidence_rad)/(2.-e1_numba(dzeta_rad,incidence_rad)))*xidz
    """
    
    muo_b=(math.cos(incidence_rad)+math.sin(incidence_rad)*math.tan(dzeta_rad)*e2_numba(dzeta_rad,incidence_rad)/(2.-e1_numba(dzeta_rad,incidence_rad)))*xidz
        #factor
    mu_b=(math.cos(emergence_rad)+math.sin(emergence_rad)*math.tan(dzeta_rad)*e2_numba(dzeta_rad,emergence_rad)/(2.-e1_numba(dzeta_rad,emergence_rad)))*xidz

    if incidence <= emergence:
        #cosinus of incidence 
        muo=(math.cos(incidence_rad)+math.sin(incidence_rad)*math.tan(dzeta_rad)*(math.cos(azimuth)*e2_numba(dzeta_rad,emergence_rad)+math.sin(azimuth/2.)**2*e2_numba(dzeta_rad,incidence_rad))/(2.-e1_numba(dzeta_rad,emergence_rad)-(azimuth/math.pi)*e1_numba(dzeta_rad,incidence_rad)))*xidz    
        #cosinus of emergence 
        mu=(math.cos(emergence_rad)+math.sin(emergence_rad)*math.tan(dzeta_rad)*(e2_numba(dzeta_rad,emergence_rad)-math.sin(azimuth/2.)**2*e2_numba(dzeta_rad,incidence_rad))/(2.-e1_numba(dzeta_rad,emergence_rad)-(azimuth/math.pi)*e1_numba(dzeta_rad,incidence_rad)))*xidz       

    else:
        muo=(math.cos(incidence_rad)+math.sin(incidence_rad)*math.tan(dzeta_rad)*(e2_numba(dzeta_rad,incidence_rad)-math.sin(azimuth/2.)**2*e2_numba(dzeta_rad,emergence_rad))/(2.-e1_numba(dzeta_rad,incidence_rad)-(azimuth/math.pi)*e1_numba(dzeta_rad,emergence_rad)))*xidz
        mu=(math.cos(emergence_rad)+math.sin(emergence_rad)*math.tan(dzeta_rad)*(math.cos(azimuth)*e2_numba(dzeta_rad,incidence_rad)+math.sin(azimuth/2.)**2*e2_numba(dzeta_rad,emergence_rad))/(2.-e1_numba(dzeta_rad,incidence_rad)-(azimuth/math.pi)*e1_numba(dzeta_rad,emergence_rad)))*xidz



    return muo, mu, muo_b, mu_b 


'''
Computing shadowing factor from Hapke model
'''

@jit(nopython=True)
def fct_S_numba(incidence, emergence, muo, mu, muo_b, mu_b, azimuth, dzeta):
    if abs(azimuth)==math.pi:
        f=0.

    else:
        f=math.exp(-2.*math.tan(azimuth/2.))

    incidence_rad=incidence/180.*math.pi
    emergence_rad=emergence/180.*math.pi
    dzeta_rad=dzeta/180.*math.pi
    xidz=1./math.sqrt(1.+math.pi*math.tan(dzeta_rad)**2) 

    # return roughness correction factor
    if incidence <= emergence:
        temp=mu_b*muo_b*(1.-f+f*xidz*math.cos(incidence_rad)/muo_b)
        
        return mu*math.cos(incidence_rad)*xidz/temp

    else:
        temp=mu_b*muo_b*(1.-f+f*xidz*math.cos(emergence_rad)/mu_b)
        return mu*math.cos(incidence_rad)*xidz/temp    

@jit(nopython=True)
def fct_phase_HG2(b, c, phase):
    return (1-c)*( 1- b**2 )/(1 + 2. * b * math.cos(phase * math.pi/180.)+b**2)**(3./2) + c*( 1- b**2 )/(1 - 2. * b * math.cos(phase * math.pi/180.)+b**2)**(3./2)


'''
Hapke parametrisation of multiple scattering function H
'''

@jit(nopython=True)
def fct_h_numba(x, gamma):
    return (1-(1-gamma**2)*x*(((1-gamma)/(1+gamma))+(0.5-x*(1-gamma)/(1+gamma))*np.log((1+x)/x)))**(-1)
    #return(1.+2*x)/(1.+2*gamma*x)


'''  
Computing the bidirectionnal reflectance of a monolayer for photometry

Imathuts: 
    - singalb : single scattering albedo

    - g : assymetry parameter of henyey greenstein phase function' -1<g<1, 0. = isotropic, >0 forward scattering

    - dzeta : Hapke mean slope roughness parameter (emergence bar)

    - B0 amplitude of opposition effect

    - h width of opposition effect

    - incidence : incidence angle (°)

    - emergence : emergence angle (°)

    - phase : phase angle (°)



Output : 
     reflectance of the surface
'''

@jit(nopython=True)
def fct_reflectance_numba(w, b, c, dzeta, B0, h, incidence, emergence, phase): #mettre b,c
    mu=math.cos(math.pi*emergence/180.) 
    muo=math.cos(math.pi*incidence/180.)
    azimuth=convert_phase_azimuth(incidence, emergence, phase)*math.pi/180.
    gamma=math.sqrt(1.-w)
    #Calculation of the roughness correction function
    if(dzeta > 0):
        muo, mu, muo_b, mu_b = correct_numba(incidence, emergence, azimuth, dzeta) #mu & muo are equiv  angles from Hapke written mu' & muo' 
                                                                                   #mu_b & muo_b are equiv  angles from Hapke written mu'^0 & muo'^0

    B = B0 / ( 1.+(1./h)*math.tan(math.pi/180.*phase/2.) )
    
    fct_reflectance=w*muo/(4.*(mu+muo)*  math.cos(math.pi*incidence/180.)) * ((1.+B)*fct_phase_HG2(b,c,phase)+fct_h_numba(muo, gamma)*fct_h_numba(mu, gamma)-1)

    #print(fct_reflectance*fct_S_numba(incidence, emergence, muo, mu,muo_b, mu_b, azimuth, dzeta))

    #correction of the roughness effect if necessary
    if (dzeta > 0.):
        fct_reflectance=fct_reflectance*fct_S_numba(incidence, emergence, muo, mu,muo_b, mu_b, azimuth, dzeta)

    #print(azimuth, fct_S_numba(incidence, emergence, muo, mu,muo_b, mu_b, azimuth, dzeta))
    return fct_reflectance

 
'''
Calculates phase angle given incidence, emergence and azimuth 
all angles are given in degrees
''' 

@jit(nopython=True)
def convert_azimuth_phase_numba(incidence, emergence, azimuth):
    mu=math.cos(math.pi*emergence/180.)   
    muo=math.cos(math.pi*incidence/180.)   
    c_azimuth=math.cos(math.pi*azimuth/180.) 

    # scattering angle (rad)
    if((muo == mu) and (azimuth == 0.)):
        phase=math.pi 

    else:
        phase=math.acos(-muo*mu-math.sqrt(1.-muo**2)*math.sqrt(1.-mu**2)*c_azimuth)

    #phase angle (deg)
    return (math.pi-phase)*180./math.pi

@jit(nopython=True)
def convert_phase_azimuth(incidence, emergence, phase):
    muo=math.cos(math.pi*incidence/180.)
    mu=math.cos(math.pi*emergence/180.)
    
    if((incidence == 0.) or (emergence == 0.) or (phase == 0.)):
        c_azimuth=1.
    
    else:
        c_azimuth=(math.cos(math.pi*phase/180.)-muo*mu)/(math.sqrt(1.-muo**2)*math.sqrt(1-mu**2))
        if(c_azimuth > 1.):
            c_azimuth=1.
        if(c_azimuth < -1.):
            c_azimuth=-1. 
    
    return math.acos(c_azimuth)*180./math.pi


'''
Computing the bidirectionnal reflectance of a monolayer for photometry using function
fct_reflectance_numba

Imathuts: 
    - singalb : single scattering albedo
    - g : assymetry parameter of henyey greenstein phase function' -1<g<1, 0. = isotropic, >0 forward scattering
    - dzeta : Hapke mean slope roughness parameter (emergence bar)
    - B0 amplitude of opposition effect
    - h width of opposition effect
    - incidence : incidence angle (°)
    - emergence : emergence angle (°)
    - azimuth : azimuth angle (°)

Output : 
     reflectance of the surface
'''

@jit(nopython=True)
def reflectance_photometry_HG2(singalb, b, c, dzeta, B0, h, incidence, emergence, azim):   
    n = np.shape(emergence)[0]
    refl = []
    for i in range(n):
        phase=convert_azimuth_phase_numba(incidence[i], emergence[i], azim[i])
        refl.append(fct_reflectance_numba(singalb, b,c, dzeta, B0, h, incidence[i], emergence[i], phase))
    return refl

@jit(nopython=True)
def reflectance_photometry_HG2_numba(singalb, b, c, dzeta, B0, h, incidence, emergence, azim):   
    phase=convert_azimuth_phase_numba(incidence, emergence, azim)
    refl=fct_reflectance_numba(singalb, b,c, dzeta, B0, h, incidence, emergence, phase)
    return refl

def direct_model(m, emergences0, emergences, azims):
    w=m[0] #single scattering albedo
    b=m[1] # assymetry parameter
    c=m[2]
    dzeta=m[3]*45 # roughness paramete
    B0=m[4] # Amplitude of opposition effect
    h=m[5] # width of opposition effect
    w, b, c, dzeta, B0, h
    
    nbgeom = len(emergences0)
    phases=np.zeros(nbgeom)
    for i in range(nbgeom):
        phases[i]=convert_azimuth_phase_numba(emergences0[i], emergences[i], azims[i])

    brdf=np.zeros(nbgeom)
    for i in range(nbgeom):
        incidence = emergences0[i] 
        emergence = emergences[i]
        azim = azims[i]
        try:
            brdf[i]=reflectance_photometry_HG2_numba(w, b, c, dzeta, B0, h, incidence, emergence, azim)
        except ZeroDivisionError:
            brdf[i]=0
    return brdf