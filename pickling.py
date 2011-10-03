import configuration as conf
import histogramProcessing as hp
import fresh,utils
import cPickle,math,os
import ROOT as r

##I/O
def writeNumbers(fileName = None, d = None) :
    outFile = open(fileName, "w")
    cPickle.dump(d, outFile)
    outFile.close()

def readNumbers(fileName) :
    inFile = open(fileName)
    d = cPickle.load(inFile)
    inFile.close()
    return d

##number collection
def effHistos(nloToLoRatios = False) :
    data = conf.data()
    binsInput = data.htBinLowerEdgesInput()
    htThresholdsInput = zip(binsInput, list(binsInput[1:])+[None])
    binsMerged =  data.htBinLowerEdges()

    d = conf.likelihood()["alphaT"]
    keys = sorted(d.keys())
    out = {}

    for iKey,key in enumerate(keys) :
        nextKey = ""
        if iKey!=len(keys)-1 :
            nextKey = keys[iKey]
        elif key :
            nextKey = "inf"
        
        nHtBins = len(d[key]["htBinMask"])
        for box,considerSignal in d[key]["samples"] :
            item = "eff%s%s"%(box.capitalize(), key)
            if not considerSignal :
                out[item] = [0.0]*nHtBins
                if nloToLoRatios : out["_LO"%item] = out[item]
                continue

    	    out[item] = [hp.effHisto(box = box, scale = "1",
                                     htLower = htLower, htUpper = htUpper,
                                     alphaTLower = key, alphaTUpper = nextKey,
                                     ) for htLower, htUpper in htThresholdsInput]
    	                 
    	    if nloToLoRatios :
    	        out[item+"_LO"] = [hp.loEffHisto(box = box, scale = "1",
                                                 htLower = htLower, htUpper = htUpper,
                                                 alphaTLower = key, alphaTUpper = nextKey,
                                                 ) for htLower, htUpper in htThresholdsInput]
    return out

def numberDict(histos = {}, data = None, point = None) :
    out = {}
    for key,value in histos.iteritems() :
        numList = []
        for item in value :
            if not hasattr(item, "GetBinContent") : break
            numList.append(item.GetBinContent(*point))
        if numList : out[key] = numList
        else : out[key] = value
        out[key] = data.mergeEfficiency(out[key])
        out[key+"Sum"] = sum(out[key])
    return out

def histoList(histos = {}) :
    out = []
    for key,value in histos.iteritems() :
        for item in value :
            if not hasattr(item, "GetBinContent") : continue
            out.append(item)
    return out

def effSums(d = {}) :
    out = {}
    for key,value in d.iteritems() :
        if key[-3:]=="Sum" :
            key2 = key.replace("eff","nEvents")
            out[key2] = value*d["nEventsIn"]
            if out[key2] :
                out[key+"UncRelMcStats"] = 1.0/math.sqrt(out[key2])
    return out

def signalDict(point = None, eff = None, xs = None, xsLo = None, nEventsIn = None, data = None, nloToLoRatios = None) :
    out = numberDict(histos = eff, data = data, point = point)

    if nloToLoRatios :
        remove = []
        for key,value in out.iteritems() :
            if key+"_LO" in out :
                out[item+"_NLO_over_LO"] = [nlo/lo if lo else 0.0 for nlo,lo in zip(out[item], out[item+"_LO"])]
                remove.append(key+"_LO")
        for item in remove : del out[item]
            
    out["xs"] = xs.GetBinContent(*point)
    if nloToLoRatios :
        if xsLo : lo = xsLo.GetBinContent(*point)
        signal["xs_NLO_over_LO"] = signal["xs"]/lo if lo else 0.0

    out["x"] = xs.GetXaxis().GetBinLowEdge(point[0])
    out["y"] = xs.GetYaxis().GetBinLowEdge(point[1])
    out["nEventsIn"] = nEventsIn.GetBinContent(*point)

    out.update(effSums(out))
    return out

def writeSignalFiles(points = []) :
    nloToLoRatios = conf.switches()["nloToLoRatios"]
    args = {"data": conf.data(),
            "nloToLoRatios": nloToLoRatios,
            "eff": effHistos(nloToLoRatios = nloToLoRatios),
            "xs": hp.xsHisto(),
            "nEventsIn": hp.nEventsInHisto(),
            }

    hp.checkHistoBinning([args["xs"]]+histoList(args["eff"]))

    def one(point) :
        writeNumbers(fileName = conf.strings(*point)["pickledFileName"]+".in",
                     d = signalDict(point = point, **args))

    map(one, points)
        
##merge functions
def mergedFile() :
    note = fresh.note(likelihoodSpec = conf.likelihood())
    return "%s_%s%s"%(conf.stringsNoArgs()["mergedFileStem"], note, ".root")

def mergePickledFiles(printExample = False) :
    example = hp.xsHisto()
    if printExample :
    	print "Here are the example binnings:"
    	print "x:",example.GetNbinsX(), example.GetXaxis().GetXmin(), example.GetXaxis().GetXmax()
    	print "y:",example.GetNbinsY(), example.GetYaxis().GetXmin(), example.GetYaxis().GetXmax()
    	print "z:",example.GetNbinsZ(), example.GetZaxis().GetXmin(), example.GetZaxis().GetXmax()

    histos = {}
    zTitles = {}
    
    for point in hp.points() :
        fileName = conf.strings(*point)["pickledFileName"]+".out"
        if not os.path.exists(fileName) :
            print "skipping file",fileName            
        else :
            d = readNumbers(fileName)
            for key,value in d.iteritems() :
                if type(value) is tuple :
                    content,zTitle = value
                else :
                    content = value
                    zTitle = ""
                if key not in histos :
                    histos[key] = example.Clone(key)
                    histos[key].Reset()
                    zTitles[key] = zTitle
                histos[key].SetBinContent(point[0], point[1], point[2], content)
            os.remove(fileName)
            os.remove(fileName.replace(".out",".in"))

    for key,histo in histos.iteritems() :
        histo.GetZaxis().SetTitle(zTitles[key])

    f = r.TFile(mergedFile(), "RECREATE")
    for histo in histos.values() :
        histo.Write()
    f.Close()
