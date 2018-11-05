from ROOT import *
from math import fabs,sqrt
import sys
import os
from array import array
from dtplotter import *

def res_plot(vset):

    gStyle.SetOptFit(1)

    print'in res plot'

    

    # Get dt_h

    # From dt_plot
    if len(vset) > 3: 
        dt_h = dt_plot(vset)
        x_min = float(vset[7])

    # From already created histogram
    else:
        f = TFile("bin/tmp/dt_vs_Aeffo_brmseff_15bins_1712025_events_scanned_3x3.root")
        dt_h = f.Get("h")

    # Create object array to store 
    fit_params = TObjArray() # store fit params vs. slice x 
    CB_fit_params = TObjArray()    
    ss_fits = TObjArray() # store individual slice fits here 
    ss_fit = TFitResultPtr() # single slice fit 

    #ss_fits.Add() 

    # Define fit function
    g = TF1('g','gaus',-5.4,-4.4) # Get bounds rom dt_h 

    # #-------------------------------------------------------------

    # ## Double sided crystal ball function
    # def double_xtal_ball(x,par):
    #     f1 = TF1('f1','crystalball')
    #     f2 = TF1('f2','crystalball')
    #     f1.SetParameters(par[0]/2, par[1], par[2], par[3], par[4])            # The trick is to share all variables except 
    #     f2.SetParameters(par[0]/2, par[1], par[2], -par[3], par[4])            # 'A', which determines the side of the tail
    #     return f1(x[0]) + f2(x[0])

    # double_xtal_ball = TF1("double_xtal_ball", double_xtal_ball, -2, 2, 5)  # -2 to 2 is my sample fit range, adjust as needed
    # double_xtal_ball.SetParNames("c","mu","sig","A","n")              # Not necessary, but helpful for clarity!
    
    # ## Set par. limits to help the minimizer converge
    # ## Perhaps overkill, but at least set A1 and A2 to have different signs, one for each tail!!!
    # ## Example values, tune based on your specific usage case. Not all limits may be necessary for you
    # double_xtal_ball.SetParLimits(0 , 0 ,99999)                               # c >= 0
    # double_xtal_ball.SetParLimits(1 ,-5 ,-4.7  )                               # mu between -2 and 2
    # double_xtal_ball.SetParLimits(2 , 0.01 ,0.5)                               # sigma between 0 and 0.5
    # double_xtal_ball.SetParLimits(3 , 0 ,99 )                               # A1 >= 0                              # A2 <= 0
    # double_xtal_ball.SetParLimits(4 , 0 ,99 )                               # n  >= 0
    # double_xtal_ball.SetParameters(180, -5, 0.05, 1, 1)                  # Some guesses to help things along 

    # #-------------------------------------------------------------

    #dt_h.FitSlicesY("double_xtal_ball",1,-1,0,"QNR",CB_fit_params) 
    #dt_h.FitSlicesY(double_xtal_ball,1,1,0,"Q",CB_fit_params) 
    #dt_h.FitSlicesY(g,1,7,0,"QNR",fit_params)

    #CB_fit = TH1F()
    #CB_fit = CB_fit_params.At(2)

    #CB_fit.Fit()

    #result__ = CB_fit.Fit('cus_f',"SQ")

    # mean = double_xtal_ball.GetParameter(1)
    # res  = double_xtal_ball.GetParameter(2)
    # mean_err = double_xtal_ball.GetParError(1)
    # res_err  = double_xtal_ball.GetParError(2)

    dt_h.FitSlicesY(g,1,-1,0,"QNR",fit_params) # 0 is underflow bin 

    nb = dt_h.GetNbinsX()
    for i in range(nb):
    #for i in range(3,4):
        dt_h_tmp = TH1F()
        dt_h_tmp = dt_h.ProjectionY('dt_h_tmp',i,i)
        dt_h_tmp.Fit(g,"Q")
        #dt_h_tmp.Fit("double_xtal_ball","Q")

        cc = TCanvas()
        dt_h_tmp.Draw()
        cc.SaveAs("bin/res/ss_fit" + str(i) + ".png")

    sig_h = fit_params.At(2)

    #cus_f = TF1("cus_f"," sqrt( pow(([0]/x),2) + 2*[1]*[1]) ",x_min,600.) # 0.001
    cus_f = TF1("cus_f"," sqrt( pow(([0]/x),2) + 2*[1]*[1]) ",30,600.) # 0.001
    cus_f.SetParameters(5, 0.05)
    sig_h.Fit('cus_f','Q')
    result = sig_h.Fit('cus_f',"SQ") # result is a TFitResultPtr
    #result = sig_h.Fit('cus_f',"SQNRO") # result is a TFitResultPtr
    print'A = ',result.Parameter(0),'+/-',result.ParError(0)
    print'C = ',result.Parameter(1),'+/-',result.ParError(1)
    chi2 = sig_h.Chisquare(cus_f)
    DOF = cus_f.GetNDF()

    c0 = TCanvas()
    sig_h.Draw()

    ymax = c0.GetUymax()

    c = TCanvas()

    gPad.DrawFrame(0.,0.,600.,0.15,"Sigma dt vs. Aeff/brmseff")
    #sig_h.GetXaxis().
    c.cd()
    #sig_h.SetTitle("Sigma dt vs. Aeff/brmseff")
    sig_h.Draw("SAME")
    
    #sig_h.GetXaxis().SetRangeUser(minimum,maximum)

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
    Alatex.SetTextSize(10)
    Alatex.DrawLatex(0.3,0.85,A_str)
    Alatex.SetTextFont(53)

    Clatex = TLatex()
    Clatex.SetNDC()
    Clatex.SetTextAngle(0)
    Clatex.SetTextColor(kBlack)
    Clatex.SetTextFont(63)
    Clatex.SetTextAlign(11)
    Clatex.SetTextSize(10)
    Clatex.DrawLatex(0.3,0.75,c_str)
    Clatex.SetTextFont(53)

    Clatex = TLatex()
    Clatex.SetNDC()
    Clatex.SetTextAngle(0)
    Clatex.SetTextColor(kBlack)
    Clatex.SetTextFont(63)
    Clatex.SetTextAlign(11)
    Clatex.SetTextSize(10)
    Clatex.DrawLatex(0.3,0.65,cs_str)
    Clatex.SetTextFont(53)

    c.SaveAs("bin/res/res_fit.pdf") 
    c.SaveAs("bin/res/res_fit.png") 
    sig_h.SaveAs("bin/res/sig_h.root")

    # Automatically open file
    #os.system('evince ' + 'plot.pdf')


















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