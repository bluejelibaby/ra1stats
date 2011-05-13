#!/usr/bin/env python
import os

def switches() :
    d = {}

    d["method"] = "profileLikelihood"
    #d["method"] = "feldmanCousins"

    d["fcAdditionalNToysFactor"] = 4
    d["fcSetNBins"] = 40
    d["fcUseProof"] = False

    d["nlo"] = True
    d["signalModel"] = "T1"
    #d["signalModel"] = "tanBeta3"

    d["icQueue"] = "hepshort.q"
    #d["icQueue"] = "hepmedium.q"
    #d["icQueue"] = "heplong.q"

    d["fillHolesInEffUncRelPdf"] = True
    d["fillHolesInEfficiencyPlots"] = True
    d["fillHolesInXsLimitPlot"] = True
    
    d["debugOutput"] = False
    d["testPointsOnly"] = False
    d["listOfTestPoints"] = [(14, 9, 1)]
    
    d["twoHtBins"] = False
    d["exponentialBkg"] = True

    d["computeExpectedLimit"] = False
    d["expectedPlusMinus"] = {"OneSigma": 1.0, "TwoSigma": 2.0}
    d["nToys"] = 1000
    d["debugMedianHisto"] = False

    d["hardCodedSignalContamination"] = False
    d["assumeUncorrelatedLowHtSystematics"] = True
    d["constrainParameters"] = False

    d["Ra2SyncHack"] = False
    d["printCovarianceMatrix"] = False
    d["writeWorkspaceFile"] = False
    d["writeGraphVizTree"] = False

    d["CL"] = 0.95
    d["masterSignalMax"] = 80.0
    d["minSignalEventsForConsideration"] =  1.0
    d["maxSignalEventsForConsideration"] = 50.0

    checkAndAdjust(d)
    return d

def smsRanges() :
    d = {}

    d["smsXRange"] = (400.0, 999.9) #(min, max)
    d["smsYRange"] = (100.0, 999.9)
    d["smsXsZRangeLin"] = (0.0, 40.0, 40) #(zMin, zMax, nContours)
    d["smsXsZRangeLog"] = (0.4, 40.0, 40)
    d["smsEffZRange"]   = (0.0, 0.35, 35)

    d["smsEffUncExpZRange"] = (0.0, 0.20, 20)
    d["smsEffUncThZRange"] = (0.0, 0.40, 40)
    return d

def isCern() :
    return ("cern.ch" in os.environ["HOSTNAME"])

def checkAndAdjust(d) :
    assert d["signalModel"] in ["T1", "T2", "tanBeta3", "tanBeta10", "tanBeta50"]
    d["lateDivision"] = False
    if len(d["signalModel"])==2 :
        d["nlo"] = False
        d["minSignalEventsForConsideration"] = 1.0e-18
        d["maxSignalEventsForConsideration"] = None
        d["lateDivision"] = True

    d["suppressJobOutput"] = d["computeExpectedLimit"] and not d["debugMedianHisto"]
    if d["method"]=="feldmanCousins" :
        d["fiftyGeVStepsOnly"] = True
        d["minSignalEventsForConsideration"] = 10.0
        d["maxSignalEventsForConsideration"] = 26.0
    else :
        d["fiftyGeVStepsOnly"] = False
    return

def singleJobOnly() :
    d = switches()
    return any([d[item] for item in ["hardCodedSignalContamination"]])

def histoSpecs() :
    dir = "/afs/cern.ch/user/e/elaird/public/20_yieldHistograms" if isCern() else "/vols/cms02/elaird1/20_yieldHistograms"

    d = {}
    for model in ["tanBeta3", "tanBeta10", "tanBeta50"] :
        d[model] = {}
    
        f = "AK5Calo_PhysicsProcesses_mSUGRA_%s.root"%(model.lower())
        d[model]["sig10"]  = {"file": "%s/v5/Signal/%s"%(dir, f)}
        d[model]["muon"]   = {"file": ("%s/v6/muon/%s"%(dir, f) ).replace(".root", "_Muon.root")}
        d[model]["sig05"]  = {"file": "%s/v5/Signal/%s"%(dir, f)}
        d[model]["sig20"]  = {"file": "%s/v5/Signal/%s"%(dir, f)}
        d[model]["ht"]     = {"file": "%s/v5/QCD/QcdBkgdEst_%s.root"%(dir, model.lower())}

        for key in d[model] :
            tag = key[-2:]
            d[model][key]["beforeDir"] = "mSuGraScan_beforeAll_%s"%tag
            d[model][key]["250Dirs"  ] = []
            d[model][key]["300Dirs"  ] = []
            d[model][key]["350Dirs"  ] = ["mSuGraScan_350_%s"%tag]
            d[model][key]["450Dirs"  ] = ["mSuGraScan_450_%s"%tag]
            d[model][key]["loYield"  ] = "m0_m12_mChi_0"

        d[model]["muon"]["beforeDir"] = "mSuGraScan_beforeAll_10"
        d[model]["muon"]["350Dirs"] = ["mSuGraScan_350_10"]
        d[model]["muon"]["450Dirs"] = ["mSuGraScan_450_10"]
     
        d[model]["ht"]["beforeDir"] = None
        d[model]["ht"]["250Dirs"]   = ["Reco_Bin_250_HT_300"]
        d[model]["ht"]["300Dirs"]   = ["Reco_Bin_300_HT_350"]
        d[model]["ht"]["350Dirs"]   = ["Reco_Bin_350_HT_400", "Reco_Bin_400_HT_450"]
        d[model]["ht"]["450Dirs"]   = ["Reco_Bin_450_HT_500", "Reco_Bin_500_HT_Inf"]

    for model in ["T1", "T2"] :
        d[model] = {}

    model = "T1"
    d[model]["sig10"]  = {"file": "%s/v5/SMSFinal/AK5Calo_PhysicsProcesses_Topology%s.root"%(dir,model)}
    d[model]["muon"]   = {"file": "%s/v5/MuonSMSsamples/AK5Calo_PhysicsProcesses_Topology%s.root"%(dir,model)}
    d[model]["ht"]     = {"file": "%s/v5/QCD/QcdBkgdEst_%s.root"%(dir, model.lower())}
    d[model]["jes-"]   = {"file": "%s/v5/SMSFinal_JESMinus/AK5Calo_PhysicsProcesses_Topology%s.root"%(dir, model)}
    d[model]["jes+"]   = {"file": "%s/v5/SMSFinal_JESPlus/AK5Calo_PhysicsProcesses_Topology%s.root"%(dir, model)}
    d[model]["isr-"]   = {"file": "%s/v5/SMS_ISR_variation/v2/AK5Calo_mySUSYTopo%s_ISR.root"%(dir, model)}
    #d[model]["isr-"]   = {"file": "%s/v7/ISR-nofilter/AK5Calo_PhysicsProcesses_Topology%s_38xFall10_spadhi.root"%(dir, model)}
    
    model = "T2"
    d[model]["sig10"]  = {"file": "%s/v7/signal-filter/AK5Calo_PhysicsProcesses_Topology%s_38xFall10_spadhi_new.root"%(dir,model)}
    d[model]["muon"]   = {"file": "%s/v5/MuonSMSsamples/AK5Calo_PhysicsProcesses_Topology%s.root"%(dir,model)}
    d[model]["ht"]     = {"file": "%s/v7/lowHT-filter/AK5Calo_PhysicsProcesses_Topology%s_38xFall10_spadhi_new.root"%(dir, model)}
    d[model]["jes-"]   = {"file": "%s/v7/JESminus-filter/AK5Calo_PhysicsProcesses_Topology%s_38xFall10_spadhi_new.root"%(dir, model)}
    d[model]["jes+"]   = {"file": "%s/v7/JESplus-filter/AK5Calo_PhysicsProcesses_Topology%s_38xFall10_spadhi_new.root"%(dir, model)}
    d[model]["isr-"]   = {"file": "%s/v7/ISR-filter/AK5Calo_PhysicsProcesses_Topology%s_38xFall10_spadhi_new.root"%(dir, model)}

    for model in ["T1", "T2"] :
        
        for key in d[model] :
            tag = key[-2:]
            d[model][key]["beforeDir"] = "mSuGraScan_beforeAll_%s"%tag
            d[model][key]["250Dirs"  ] = []
            d[model][key]["300Dirs"  ] = []
            d[model][key]["350Dirs"  ] = ["mSuGraScan_350_%s"%tag]
            d[model][key]["450Dirs"  ] = ["mSuGraScan_450_%s"%tag]
            d[model][key]["loYield"  ] = "m0_m12_mChi_0"
            
        for key in ["jes-","jes+"] :
            d[model][key]["beforeDir"] = "mSuGraScan_beforeAll_10"
            d[model][key]["350Dirs"] = ["mSuGraScan_350_10"]
            d[model][key]["450Dirs"] = ["mSuGraScan_450_10"]

        for key in ["isr-"] :
            d[model][key]["beforeDir"] = "isr_unc_before"
            d[model][key]["350Dirs"  ] = ["isr_unc_350"]
            d[model][key]["450Dirs"  ] = ["isr_unc_450"]
            d[model][key]["loYield"  ] = "m0_m12"
            
        #warning: non-intuitive keys chosen to use histo bin check "for free"
        d[model]["effUncRelPdf"] = {"file": "/vols/cms02/elaird1/27_pdf_unc_from_tanja/v7/Plots_%s.root"%model, "350Dirs": ["/"], "loYield": "final_pdf_unc_error"}
            
        d[model]["muon"]["beforeDir"] = "mSuGraScan_beforeAll"
        d[model]["muon"]["350Dirs"] = ["mSuGraScan_350"]
        d[model]["muon"]["450Dirs"] = ["mSuGraScan_450"]

        d[model]["ht"]["beforeDir"] = None
        d[model]["ht"]["250Dirs"]   = ["Reco_Bin_250_HT_300"]
        d[model]["ht"]["300Dirs"]   = ["Reco_Bin_300_HT_350"]
        d[model]["ht"]["350Dirs"]   = ["Reco_Bin_350_HT_400", "Reco_Bin_400_HT_450"]
        d[model]["ht"]["450Dirs"]   = ["Reco_Bin_450_HT_500", "Reco_Bin_500_HT_Inf"]

    return d[switches()["signalModel"]]

def histoTitle() :
    if switches()["signalModel"]=="T1" :
        return ";m_{gluino} (GeV);m_{LSP} (GeV)"
    if switches()["signalModel"]=="T2" :
        return ";m_{squark} (GeV);m_{LSP} (GeV)"
    else :
        return ";m_{0} (GeV);m_{1/2} (GeV)"

def mergedFile(outputDir, switches) :
    out  = "%s/"%outputDir
    out += "_".join([switches["method"],
                     switches["signalModel"],
                     "nlo" if switches["nlo"] else "lo",
                     "2HtBins" if switches["twoHtBins"] else "1HtBin",
                     "expR" if switches["exponentialBkg"] else "constantR",
                     ])
    for item in ["Ra2SyncHack", "computeExpectedLimit"] :
        if switches[item] : out += "_%s"%item
    out += ".root"
    return out

def stringsNoArgs() :
    d = {}

    d["sourceFiles"] = ["RooMyPdf.cxx", "SlimPdfFactory.C"]
    d["subCmd"] = "bsub" if isCern() else "qsub -q %s"%switches()["icQueue"]
    d["envScript"] = "env.sh" if isCern() else "envIC.sh"

    #internal names
    d["workspaceName"]   = "Combine"
    d["modelConfigName"] = "Combine"
    if switches()["twoHtBins"] :
        d["pdfName"] = "TopLevelPdf"
        d["dataName"] = "ObservedNumberCountingDataWithSideband"
        d["signalVar"] = "masterSignal"
    else :
        d["pdfName"] = "total_model"
        d["dataName"] = "obsDataSet"
        d["signalVar"] = "s"

    #output name options
    d["outputDir"]      = "output"
    d["logDir"]         = "log"
    d["plotStem"]       = "%s/Significance"%d["outputDir"]
    d["workspaceStem"]  = "%s/%s"%(d["outputDir"], d["workspaceName"])
    d["logStem"]        = "%s/job"%d["logDir"]
    d["mergedFile"]     = mergedFile(d["outputDir"], switches())
    return d

def strings(xBin, yBin, zBin) :
    d = stringsNoArgs()
    #output name options
    d["tag"]               = "m0_%d_m12_%d_mZ_%d"%(xBin, yBin, zBin)
    d["pickledFileName"]   = "%s_%s.pickled"%(d["plotStem"], d["tag"])
    d["workspaceFileName"] = "%s_%s.root"%(d["workspaceStem"], d["tag"])
    return d
