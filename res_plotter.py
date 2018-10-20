from ROOT import *
from math import fabs,sqrt
import sys
import os
from array import array
from dtplotter import *

def res_plot(vset):

    print'in res plot'

    # Get dt_h

    # From dt_ploy
    #if len(vset) > 3: dt_h = dt_plot(vset)

    dt_h = dt_plot(vset)
    #print'dt_h = ',dt_h

    # From already created histogram
    # else:
    #f = TFile("bin/roots/dt_vs_Aeffo_brmseff_10bins_2900_events_scanned_3x3.root")
    #dt_h = f.Get("h")

    #print'dt_plot(vset) = ',dt_plot(vset)
    #dt_h = dt_plot(vset)
    #print'dt_h = ',dt_h

    fits = TObjArray()

    # Define fit function
    g = TF1('g','gaus',-10,0) # Get bounds rom dt_h 

    #DOF = dt_h.GetNbinsX() - 2

    #dt_h.FitSlicesY(g,0,-1,0,"QNR",fits) 
    dt_h.FitSlicesY(g,0,-1,0,"QNR",fits) 

    sig_h = fits.At(2)

    # Custom fit function
    cus_f = TF1("cus_f","([0]/x) + sqrt(2)*[1]",0.00001,800)

    cus_f.SetParameters(1, 0.05)

    # x[0] = N, x[1] = C

    sig_h.Fit('cus_f','Q')

    result = sig_h.Fit('cus_f',"SQ") # result is a TFitResultPtr

    #print'A = ',result.Parameter(0),'+/-',result.ParError(0)
    #print'C = ',result.Parameter(1),'+/-',result.ParError(1)

    chi2 = sig_h.Chisquare(cus_f)
    DOF = cus_f.GetNDF()

    c = TCanvas()
    sig_h.Draw()

    print'chi2 = ',chi2
    print'DOF = ',DOF

    A_str = 'A = ' +  "{0:.4f}".format(result.Parameter(0)*1000) + '+/-' + "{0:.4f}".format(result.ParError(0)*1000) + 'ps'
    c_str = 'c = ' + "{0:.4f}".format(result.Parameter(1)*1000) + '+/-' + "{0:.4f}".format(result.ParError(1)*1000) + 'ps'
    cs_str = 'reduced chi2 = ' + "{0:.4f}".format(chi2 / DOF)
    

    Alatex = TLatex()
    Alatex.SetNDC()
    Alatex.SetTextAngle(0)
    Alatex.SetTextColor(kBlack)
    Alatex.SetTextFont(63)
    Alatex.SetTextAlign(11)
    Alatex.SetTextSize(22)
    Alatex.DrawLatex(0.5,0.5,A_str)
    Alatex.SetTextFont(53)

    Clatex = TLatex()
    Clatex.SetNDC()
    Clatex.SetTextAngle(0)
    Clatex.SetTextColor(kBlack)
    Clatex.SetTextFont(63)
    Clatex.SetTextAlign(11)
    Clatex.SetTextSize(22)
    Clatex.DrawLatex(0.5,0.4,c_str)
    Clatex.SetTextFont(53)

    Clatex = TLatex()
    Clatex.SetNDC()
    Clatex.SetTextAngle(0)
    Clatex.SetTextColor(kBlack)
    Clatex.SetTextFont(63)
    Clatex.SetTextAlign(11)
    Clatex.SetTextSize(22)
    Clatex.DrawLatex(0.5,0.3,cs_str)
    Clatex.SetTextFont(53)

    c.SaveAs("plot.pdf") 

    # Automatically open file
    os.system('evince ' + 'plot.pdf')

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