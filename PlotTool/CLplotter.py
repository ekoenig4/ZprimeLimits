#!/usr/bin/env python
from ROOT import *
import os
from argparse import ArgumentParser
import json
from array import array
from PlotTool import *
import re

gROOT.SetBatch(1)

outdir_base = "/afs/hep.wisc.edu/home/ekoenig4/public_html/MonoZprimeJet/Plots%s/ExpectedLimits/"
home = os.getcwd()
def checkdir(dir):
    if not os.path.isdir(dir): os.mkdir(dir)
#####################################################################
def exclude(data):
    exclude_mx = ['1','150','500','1000']
    exclude_mx = []
    exclude_mv = ['15','10000']

    for mx in exclude_mx:
        if mx in data: data.pop(mx)
    for mv in exclude_mv:
        for _,mvlist in data.items():
            if mv in mvlist: mvlist.pop(mv) 
#####################################################################
def drawPlot2D(data):
    print 'Plotting 2D'
    lumi = data.lumi
    year = data.year
    variable = data.variable
    cut = data.cut
    extra = data.extra
    limit,mxlist,mvlist = Plot2D(data)
    xbins = len(mvlist)
    ybins = len(mxlist)
    ######################################################################
    c = TCanvas("c","c",800,800)
    c.SetMargin(0.15,0.15,0.15,0.08)
    gStyle.SetOptStat(0);
    gStyle.SetLegendBorderSize(0);
    gStyle.SetPaintTextFormat("4.3f")

    limit.Draw('COLZ TEXT89')
    limit.SetStats(0)

    limit.GetZaxis().SetTitle("95% CL limit on #sigma/#sigma_{theory}")
    limit.GetZaxis().SetTitleOffset(1.2)
    
    ################################################################
    lumi_label = '%s' % float('%.3g' % (lumi/1000.)) + " fb^{-1}"
    texS = TLatex(0.55,0.93,("#sqrt{s} = 13 TeV, "+lumi_label));
    texS.SetNDC();
    texS.SetTextFont(42);
    texS.SetTextSize(0.035);
    texS.Draw();
    texS1 = TLatex(0.15,0.93,"#bf{CMS} : #it{Preliminary} (%s)" % year);
    texS1.SetNDC();
    texS1.SetTextFont(42);
    texS1.SetTextSize(0.035);
    texS1.Draw();
    ################################################################
    c.Modified()
    c.Update()

    outdir = outdir_base % year
    checkdir(outdir)
    subdir = variable
    outdir += '/%s' % subdir
    checkdir(outdir)
    fname = '%s%s_%s2D.png' % (variable,cut,''.join(extra))
    c.SaveAs( '%s/%s' % (outdir,fname) )
#####################################################################
def drawPlot1D(data):
    print 'Plotting 1D'
    lumi = data.lumi
    year = data.year
    variable = data.variable
    cut = data.cut
    extra = data.extra
    plots,mxlist = Plot1D(data)

    class Bounds:
        def __init__(self):
            self.xmax = None
            self.xmin = None
            self.ymax = None
            self.ymin = None
        def setBounds(self,x,y):
            if self.xmax is None: self.xmax = x
            if self.xmin is None: self.xmin = x
            if self.ymax is None: self.ymax = y
            if self.ymin is None: self.ymin = y

            self.xmax = max(self.xmax,x)
            self.xmin = min(self.xmin,x)
            self.ymax = max(self.ymax,y)
            self.ymin = min(self.ymin,y)
        def getBounds(self): return self.xmin,self.xmax,self.ymin,self.ymax
        def __str__(self): return 'x: [%f-%f] y: [%f-%f]' % (self.xmin,self.xmax,self.ymin,self.ymax)
    bounds = Bounds()
    for mx,graph in plots.iteritems():
        x,y = Double(0),Double(0)
        for i in range(graph.GetN()):
            graph.GetPoint(i,x,y)
            bounds.setBounds(float(x),float(y))

    minX,maxX,minY,maxY = bounds.getBounds()
    ######################################################################
    c = TCanvas("c","c",800,800)
    c.SetLogy()
    # c.SetMargin(0.15,0.15,0.15,0.08)
    gStyle.SetOptStat(0);
    gStyle.SetLegendBorderSize(0);
    # gStyle.SetPalette(kRainBow)

    limits = TMultiGraph()
    legend = TLegend(0.4,0.65,0.65,0.82,"")
    legend.SetTextSize(0.02)
    legend.SetFillColor(0)
    for mx in mxlist:
        limit = plots[mx]
        legend.AddEntry(limit,'m_{#chi} = '+mx+' GeV','l')
        limit.SetLineWidth(3)
        limits.Add(limit)
    limits.Draw('a l plc')
    limits.GetXaxis().SetRangeUser(minX,maxX)
    limits.GetYaxis().SetRangeUser(minY*(10**-0.2),maxY*(10**1))
    limits.GetXaxis().SetTitle("m_{med} (GeV)")
    limits.GetYaxis().SetTitle("95% CL limit on #sigma/#sigma_{theor}")
    limits.GetXaxis().SetTitleSize(0.04)
    limits.GetYaxis().SetTitleSize(0.04)
    limits.GetXaxis().SetTitleOffset(0.92)
    limits.GetYaxis().SetTitleOffset(0.92)
    limits.GetXaxis().SetLabelSize(0.03)
    limits.GetYaxis().SetLabelSize(0.03)
    ################################################################

    lumi_label = '%s' % float('%.3g' % (lumi/1000.)) + " fb^{-1}"
    texS = TLatex(0.20,0.837173,("#sqrt{s} = 13 TeV, "+lumi_label));
    texS.SetNDC();
    texS.SetTextFont(42);
    texS.SetTextSize(0.040);
    texS.Draw('same');
    texS1 = TLatex(0.12092,0.907173,"#bf{CMS} : #it{Preliminary} (%s)" % year);
    texS1.SetNDC();
    texS1.SetTextFont(42);
    texS1.SetTextSize(0.040);
    texS1.Draw('same');

    legend.Draw('same')

    line = TLine(minX,1,maxX,1)
    line.SetLineStyle(8)
    line.Draw('same')
    
    c.Modified()
    c.Update()

    outdir = outdir_base % year
    checkdir(outdir)
    subdir = variable
    outdir += '/%s' % subdir
    checkdir(outdir)
    fname = '%s%s_%s1D.png' % (variable,cut,''.join(extra))
    c.SaveAs( '%s/%s' % (outdir,fname) )
#####################################################################
def plotLimits(path,verlist):
    print path
    data = Limits(path)
    for ver in verlist:
        if   ver == '1D': drawPlot1D(data)
        elif ver == '2D': drawPlot2D(data)
#####################################################################
def getargs():
    def directory(arg):
        if os.path.isdir(arg): return arg
        else: raise ValueError('Directories only')
    def version(arg):
        if '1D' in arg or '2D' == arg:  return arg
        else:  return None
    parser = ArgumentParser(description="Plot limit information from specified directory")
    parser.add_argument("-d","--dir",help='Specify the directory to read limits from',action='store',nargs='+',type=directory,default=None,required=True)
    parser.add_argument("-v","--version",help='Specify the version of plot (1D or 2D)',action='store',type=version,default=None)
    try: arg = parser.parse_args()
    except:
        parser.print_help()
        exit()
    return parser.parse_args()
#####################################################################
if __name__ == "__main__":
    args = getargs()
    if args.dir == None:
        print "Please specify a director to run limits in."
        exit()
    if args.version == None: version = ('1D','2D')
    else:  version = (args.version,)
    for path in args.dir: plotLimits(path,version)
