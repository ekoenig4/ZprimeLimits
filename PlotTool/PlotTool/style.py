from ROOT import *

colormap = {
    '1':kRed,
    '10':kAzure+10,
    '50':kViolet,
    '100':kBlack,
    '150':kOrange-2,
    '500':kGreen,
    '1000':kBlue
}
def getLegend(xmin=0.5,ymin=0.65,xmax=0.7,ymax=0.887173):
    leg = TLegend(xmin,ymin,xmax,ymax,"")
    leg.SetFillColor(kWhite);
    leg.SetFillStyle(0);
    leg.SetTextSize(0.025);
    return leg
def getCMSText(year):
    x1,y1 = 0.62,0.907173
    texS = TLatex(x1,y1,("XX fb^{-1} (13 TeV, %s)" % year));#VS
    texS.SetNDC();
    texS.SetTextFont(42);
    texS.SetTextSize(0.040);
    texS.Draw();

    x2,y2 = 0.15,0.837173
    texS1 = TLatex(x2,y2,"#bf{CMS} #it{Preliminary}"); 
    texS1.SetNDC();
    texS1.SetTextFont(42);
    texS1.SetTextSize(0.040);
    texS1.Draw();
    return texS,texS1
def data_style(graph):
    graph.SetTitle("")
    graph.SetMarkerStyle(20)
def fit_style(hs,color):
    hs.SetTitle("")
    hs.GetYaxis().SetTitle("Events")
    hs.SetLineColor(color)
    hs.SetLineWidth(2)
    hs.SetFillStyle(0)
    hs.SetFillColor(0)
def set_bounds(hs):
    ymin = min( hs[ibin] for ibin in range(1,hs.GetNbinsX()+1) if hs[ibin] != 0)
    ymax = max( hs[ibin] for ibin in range(1,hs.GetNbinsX()+1) if hs[ibin] != 0)

    hs.SetMinimum(0.05)
    hs.SetMaximum(ymax*(10**2.5))
def ratio_style(ratio,color,rymin=0.65,rymax=1.35,name='Data/MC'):
    gPad.SetGridy();
    ratio.SetMarkerStyle(20)
    ratio.SetMarkerColor(color)
    ratio.SetTitle("")
    ratio.GetYaxis().SetRangeUser(rymin,rymax);
    if type(ratio) == TH1: ratio.SetStats(0);
    ratio.GetYaxis().CenterTitle();
    ratio.GetYaxis().SetTitle(name)
    ratio.SetMarkerStyle(20);
    ratio.SetMarkerSize(1);
    ratio.GetYaxis().SetLabelSize(0.14);
    ratio.GetYaxis().SetTitleSize(0.14);
    ratio.GetYaxis().SetLabelFont(42);
    ratio.GetYaxis().SetTitleFont(42);
    ratio.GetYaxis().SetTitleOffset(0.25);
    ratio.GetYaxis().SetNdivisions(4);
    ratio.GetYaxis().SetTickLength(0.05);
    
    ratio.GetXaxis().SetLabelSize(0.1);
    ratio.GetXaxis().SetTitleSize(0.1);
    ratio.GetXaxis().SetLabelFont(42);
    ratio.GetXaxis().SetTitleFont(42);
    ratio.GetXaxis().SetTitleOffset(1.2);
    ratio.GetXaxis().SetTickLength(0.05);
def pull_style(pull,color,pymin=-3,pymax=3):
    gPad.SetGridy();
    # pull.SetMarkerStyle(20)
    pull.SetFillStyle(1001)
    pull.SetFillColor(color)
    pull.SetLineColor(color)
    pull.SetTitle("")
    pull.GetYaxis().SetRangeUser(pymin,pymax);
    pull.SetStats(0);
    pull.GetYaxis().CenterTitle();
    pull.GetYaxis().SetTitle("#frac{(Data-MC)}{#sigma}")
    pull.SetMarkerStyle(20);
    pull.SetMarkerSize(1);
    pull.GetYaxis().SetLabelSize(0.1);
    pull.GetYaxis().SetTitleSize(0.1);
    pull.GetYaxis().SetLabelFont(42);
    pull.GetYaxis().SetTitleFont(42);
    pull.GetYaxis().SetTitleOffset(0.35);
    pull.GetYaxis().SetNdivisions(4);
    pull.GetYaxis().SetTickLength(0.05);
    
    pull.GetXaxis().SetLabelSize(0.1);
    pull.GetXaxis().SetTitleSize(0.1);
    pull.GetXaxis().SetLabelFont(42);
    pull.GetXaxis().SetTitleFont(42);
    pull.GetXaxis().SetTitleOffset(1.2);
    pull.GetXaxis().SetTickLength(0.05);