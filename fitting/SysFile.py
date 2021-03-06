from ROOT import *

gSystem.Load("libHiggsAnalysisCombinedLimit.so")

dirmap = {"sr":"signal","ze":"Zee","zm":"Zmm","we":"Wen","wm":"Wmn","ga":"gjets"}
procmap = {"data":"data_obs","zjets":"ZJets","wjets":"WJets","zll":"DYJets","gjets":"GJets","top":"TTJets","diboson":"DiBoson","qcd":"QCD","axial":"axial","ggh":"ggh","vbf":"vbf","wh":"wh","zh":"zh","zprime":"zprime"}

yearlist = ["2016","2017","2018"]
lumimap = {"2016":35900,"2017":41486,"2018":59699}
catypes = ["monojet","monov","zprime"]
varmap = {
    "monojet":RooRealVar("recoil","recoil",250,1400),
    "zprime":RooRealVar("ChNemPtFrac","ChNemPtFrac",0.,1.0)
}

class SysRegion(TDirectoryFile):
    def __init__(self,region,syscat):
        TDirectoryFile.__init__(self,region,region+"_"+syscat.year)
        self.cat = syscat.cat
        self.year = syscat.year
        self.lumi = lumimap[self.year]
        for key in syscat.tdir.GetListOfKeys():
            r,p = key.GetName().split("_")
            if dirmap[region] != r: continue
            if p == "sumofbkg": continue
            procname = procmap[p]
            process = syscat.tdir.Get(key.GetName()).Clone(procname)
            self.Add(process)
class SysCat:
    def __init__(self,tdir):
        self.tdir = tdir
        self.cat = next( cat for cat in catypes if cat in self.tdir.GetName() )
        self.year = next( year for year in yearlist if year in self.tdir.GetName() )
        self.lumi = lumimap[self.year]
        self.var = varmap[self.cat]
        self.varlist = RooArgList(self.var)
    def GetRegion(self,region):
        self.sysregion = SysRegion(region,self)
        return self.sysregion
    def GetName(self): return "%s_%s.sys.root" % (self.var.GetTitle(),self.year)

class SysFile(TFile):
    def __init__(self,*args,**kwargs):
        TFile.__init__(self,*args,**kwargs)
        self.categories = { category.GetName():SysCat(self.GetDirectory(category.GetName())) for category in self.GetListOfKeys() if self.GetDirectory(category.GetName()) }
        if not any(self.categories): self.categories = { self.GetName():SysCat(self) }
if __name__ == "__main__":
    import sys
    sysfile = SysFile(sys.argv[1])
    
    syscat = sysfile.categories["category_monojet_2017"]
    sysregion = syscat.GetRegion("sr")
    sysregion.Print()
