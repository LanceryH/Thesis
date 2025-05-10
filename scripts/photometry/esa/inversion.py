import rupho as rp
import numpy as np
import mc3

def inversion(path_r: str, path_si: str, path_sr: str):
    photom_npz = np.load(path_r)
    true_params = photom_npz["params"]

    # noise = np.random.normal(0, 1, len(photom_npz["incidence"]))
    uncert = 0.1 #5% at 1sigma
    # sigma = photom_npz["reflectance"]*uncert
    # refl = photom_npz["reflectance"]+sigma*noise

    sigma = photom_npz["reflectance"]*uncert
    w = np.where(sigma<0.01)
    try:
        sigma[w] = 0.01
    except:
        pass
    refl = photom_npz["reflectance"]

    #number of parameters to inverse
    nb_p = 6 # Number of parameters. Here: w, b, c, dzeta, B0, h

    out = f"{path_si}/inv-{path_r.split('/')[-1][4:-4]}"

    func = rp.reflectance

    # List of additional arguments of func (if necessary):
    indparams = [photom_npz["incidence"], photom_npz["emergence"], photom_npz["azimuth"], photom_npz["phase"]]

    # Array of initial-guess values of fitting parameters:
    params = true_params*0.9

    # Lower and upper boundaries for the MCMC exploration:
    pmin = np.array([0., 0., 0., 0., 0., 0.])
    pmax = np.array([1., 1., 1., 1., 1., 1.])

    # Parameters' stepping behavior:
    # pstep = np.array([0.05,0.05,0.05,0.05,0.05,0.05])
    pstep = np.array([0.05,0.05,0.05,0.05,0.05,0.05])

    # Parameter prior probability distributions:
    prior    = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    priorlow = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    priorup  = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    # Parameter names:
    pnames   = ['w', 'b', 'c', 'dzeta', 'B0', 'h']
    texnames = [r'$\omega$', r'b', r'c', r'$\zeta$', r'$B_0$', r'h']

    # Sampler algorithm, choose from: 'snooker', 'demc' or 'mrw'.
    sampler = 'snooker'

    # MCMC setup:
    nchains = 5

    #samples_per_chain =  3e4
    burnin = 2000 #per chain

    #nsamples=nchains*nsamples_per_chain
    nsamples = 2e5
    ncpu = 5
    thinning = 1

    # MCMC initial draw, choose from: 'normal' or 'uniform'
    kickoff = 'normal'

    # DEMC snooker pre-MCMC sample size:
    hsize = 10

    # Optimization before MCMC, choose from: 'lm' or 'trf':
    # leastsq = 'lm'
    # chisqscale = False

    # MCMC Convergence:
    grtest = False
    grbreak = 1.01
    grnmin = 0.5

    # Logging:
    log = out + '.log'

    # File outputs:
    savefile = out + '.npz'
    plots = False
    rms = True

    # Carter & Winn (2009) Wavelet-likelihood method:
    wlike = False
    params = params

    # Run the MCMC:
    mc3_output = mc3.sample(data=refl, uncert=sigma, func=func, params=params,
                            indparams=indparams, pmin=pmin, pmax=pmax,
                            pstep=pstep, pnames=pnames, texnames=texnames,
                            prior=prior, priorlow=priorlow, priorup=priorup,
                            sampler=sampler, nsamples=nsamples,  nchains=nchains,
                            ncpu=ncpu, burnin=burnin, thinning=thinning,
                            #leastsq=leastsq, chisqscale=chisqscale,
                            grtest=grtest, grbreak=grbreak, grnmin=grnmin,
                            hsize=hsize, kickoff=kickoff, wlike=wlike,
                            log=log, plots=plots, savefile=savefile, rms=rms)

    true_params = photom_npz["params"]
    filter = mc3_output["chisq"]<30

    if (True in filter):
        posterior = mc3_output["posterior"][filter]
    else:
        posterior = -np.ones((1,nb_p))
    print(f"Posterior shape: {np.shape(posterior)}")

    # faire pour 0.01, 0.02, 0.
    born_sup = true_params+.01
    born_inf = true_params-.01
    qualitys_p01 = []

    for ind in range(4):
        qualitys_p01.append(len(posterior[:,ind][(posterior[:,ind]<born_sup[ind]) & (posterior[:,ind]>born_inf[ind])])/np.shape(posterior)[0])

    born_sup = true_params+.02
    born_inf = true_params-.02
    qualitys_p02 = []

    for ind in range(4):
        qualitys_p02.append(len(posterior[:,ind][(posterior[:,ind]<born_sup[ind]) & (posterior[:,ind]>born_inf[ind])])/np.shape(posterior)[0])

    born_sup = true_params+.1
    born_inf = true_params-.1
    qualitys_p1 = []

    for ind in range(4):
        qualitys_p1.append(len(posterior[:,ind][(posterior[:,ind]<born_sup[ind]) & (posterior[:,ind]>born_inf[ind])])/np.shape(posterior)[0])

    np.savez(f"{path_sr}/inv-{path_r.split('/')[-1][4:-4]}",
             bestp=mc3_output["bestp"],
             refl=refl,
             qualitys_p01=qualitys_p01,
             qualitys_p02=qualitys_p02,
             qualitys_p1=qualitys_p1,
             best_model=mc3_output["best_model"],
             meanp=mc3_output["meanp"],
             stdp=mc3_output["stdp"],
             uncert=sigma,
             posterior=posterior)