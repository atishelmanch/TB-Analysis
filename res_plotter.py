from ROOT import *
from math import fabs,sqrt
import sys
import os
from array import array
from dtplotter import dt_plot

def res_plot(vset):

    print'in res plot'

    # Get dt_h
    #dt_h = dt_plot(vset)

    # I'm just gonna do it by slice since FitSlicesY doesn't seem to be working. This may just be because it had low statistics. 

    g = TF1('g','gaus',-10,0) # Get bounds rom dt_h 

    f = TFile("results/dt_vs_Aeffbrmseff_3x3.root")

    dt_h = f.Get("h")

    #xx = array('d',[])
    arr = TObjArray()

    print'before fit'
    dt_h.FitSlicesY(g,0,-1,2,"QNR",arr) # "QNR")#,2)
    print'after fit'

    c = TCanvas()
    arr.At(2).Draw()
    c.SaveAs("plot.pdf")

    

    #nb = dt_h.GetNbinsX()
    #print'number of bins = ',nb

    #res_h = TH2F('res_h','res_h',nb,0,2000,100,-10,0) # Get bounds from dt_h

    #res_h = TGraphAsymmErrors()

    # Arrays

    # x = array('d',[])
    # y = array('d',[])
    # xerr = array('d',[])
    # yerr = array('d',[])

    # # Fit function
    # g = TF1('g','gaus',-10,0) # Get bounds rom dt_h

    # for i in range(1,nb):
    #     print'On slice',i
    #     dt_h_p = dt_h.ProjectionY('dt_h_p',i,i)
    #     dt_h_p.Fit('g','R')

    #     entries = dt_h_p.GetEntries()

    #     sigma = g.GetParameter(2)

    #     x.append(dt_h.GetXaxis().GetBinLowEdge(i))

    #     if (entries != 0.0):
    #         y.append(sigma)
    #     else:
    #         y.append(0)

    #     xerr.append(0)
    #     yerr.append(g.GetParError(2))

    # res_h = TGraphAsymmErrors(nb,x,y,xerr,xerr,yerr,yerr)

    # C = TCanvas()
    # res_h.Draw()
    # C.SaveAs('plot.pdf')