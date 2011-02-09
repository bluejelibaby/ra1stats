#!/usr/bin/env python
import math

def numbers() :
    d = {}
    d["seed"]             = 4357 #seed for RooRandom::randomGenerator()
    d["lumi"]             = 35.0 #/pb
    d["_lumi"]            = 1.0
    d["_lumi_sys"]        = 0.11
                          
    d["n_signal"]         = (8, 5) #number of events measured at HT > 350 GeV and alphaT > 0.55
    d["sigma_SigEff"]     = 0.12    #systematic uncertainty on signal acceptance*efficiency*luminosity //added single uncertainties quadratically
    d["_accXeff"]         = 1.0
    d["_accXeff_sys"]     = 0.1
    d["pdfUncertainty"]   = 0.1
    
    d["n_htcontrol"]      = (33, 11, 8, 5)
    d["n_bar_htcontrol"]  = (844459, 331948, 225649, 110034)
    d["sigma_x"]          = 0.11 #systematic uncertainty on inclusive background estimation (uncertainty on the assumpotion that rhoprime = rho*rho)
    d["_lowHT_sys_1"]     = 0.08
    d["_lowHT_sys_2"]     = 0.14

    d["n_muoncontrol"]    = (      5,      2) #number of events measured in muon control sample
    d["mc_muoncontrol"]   = (    4.1,    1.9) #MC expectation in muon control sample
    d["mc_ttW"]           = (  3.415,  1.692) #MC expectation in hadronic sample
    d["sigma_ttW"]        = 0.3               #systematic uncertainty on tt+W background estimation
                          
    d["n_photoncontrol"]  = (      6,      1) #number of events measured in photon control sample
    d["mc_photoncontrol"] = (    4.4,    2.1) #MC expectation in photon control sample
    d["mc_Zinv"]          = (  2.586,  1.492) #MC expectation in photon control sample
    d["sigma_Zinv"]       = 0.4     #systematic uncertainty on Zinv background estimation

    ##changes to synchronize to RA2
    #muF = 9.3/5.9
    #d["n_muoncontrol"]    = (      5*muF,   2*muF) #number of events measured in muon control sample
    #d["mc_muoncontrol"]   = (    4.1*muF, 1.9*muF) #MC expectation in muon control sample
    #d["sigma_Zinv"]       = math.sqrt(0.172**2+0.2**2+0.2**2+0.05**2) #using box for theory uncertainty

    #place-holder values; used only when switches["ignoreSignalContamination"]=True; otherwise overridden
    d["sFrac"]         = (0.25, 0.75) #assumed fraction of signal in each bin (in case of no model)
    d["_muon_cont_1"]  = 0.2
    d["_muon_cont_2"]  = 0.2
    d["_lowHT_cont_1"] = 0.2
    d["_lowHT_cont_2"] = 0.2

    return d
