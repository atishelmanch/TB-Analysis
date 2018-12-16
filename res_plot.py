from ROOT import *
from math import fabs,sqrt
import sys
import os
from array import array
from dtplot import *

def res_plot(vset):

    # if len(vset) > 2:

    #     direc_path = vset[1]
    #     square_side = vset[2]
    #     A1mincut = vset[3]
    #     A2mincut = vset[4]
    #     nb = int(vset[5]) # number of bins 
    #     max_events = int(vset[6])
    #     x_min = float(vset[7])
    #     q_min = float(vset[8])
    #     XTAL_str = vset[9]
    #     note = vset[10]

    gStyle.SetOptFit(1)

    print'in res plot'

    # Get dt_h

    # From dt_plot
    if len(vset) > 3: 
        dt_h = dt_plot(vset)
        #dt_h, scanned_events = dt_plot(vset)
        #x_min = float(vset[7])

    # From already created histogram
    else:
        f = TFile("bin/tmp/dt_vs_Aeffo_brmseff_10bins_Qstart_250_350000_events_scanned_3x3.root") 
        #f = TFile("bin/tmp/dt_vs_Aeffo_brmseff_1000bins_Qstart_-1_225541_events_scanned_3x3.root")
        
        dt_h = f.Get("h")

    # Create object array to store 
    fit_params = TObjArray() # store fit params vs. slice x 
    CB_fit_params = TObjArray()    
    ss_fits = TObjArray() # store individual slice fits here 
    ss_fit = TFitResultPtr() # single slice fit 

    #ss_fits.Add() 

    # Define fit function
    g = TF1('g','gaus',-5.4,-4.4) # Get bounds from dt_h. This is typical MCP12 bounds for dt  
    #g = TF1('g','gaus',2,2.5)

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

    dt_h.GetYaxis().SetRangeUser(2, 2.7)
    dt_h.FitSlicesY(g,1,-1,0,"QRO",fit_params) # 0 is underflow bin 
    sig_h = fit_params.At(2)    
    nb = dt_h.GetNbinsX()
    print'nb = ',nb
    for i in range(1, nb + 1): # + 1 to add underflow bin 
    #for i in range(3,4):
        print'i = ',i
        dt_h_tmp = TH1F()
        dt_h_tmp = dt_h.ProjectionY('dt_h_tmp',i,i)
        dt_h_tmp.Fit(g,"QROB")
        #dt_h_tmp.Fit("double_xtal_ball","Q")

        cc = TCanvas()
        dt_h_tmp.Draw()
        cc.SaveAs("bin/res/ss_fit" + str(i) + ".png")
        #os.system('evince' + " bin/res/ss_fit" + str(i) + ".png"

    # sig_h_tmp = fit_params.At(2)
    # sig_h = TGraphErrors()
    # sig_h.SetName("sig_h")
    # #energies = [50, 100, 150, 200, 250]
    # for i in range(1, nb + 1):
    #     sig_h.SetPoint(i-1, energies[i-1], sig_h_tmp.GetBinContent(i))
    #     sig_h.SetPointError(i-1, energies[i-1]*0.01, sig_h_tmp.GetBinError(i))
        
    #sig_h = g.GetParameter(2)

    #cus_f = TF1("cus_f"," sqrt( pow(([0]/x),2) + 2*[1]*[1]) ",x_min,600.) # 0.001
    #cus_f = TF1("cus_f"," sqrt( pow(([0]/x),2) + 2*[1]*[1]) ",30,600.) # 0.001 MCP12
    #cus_f = TF1("cus_f"," sqrt( pow(([0]/x),2) + [1]*[1]) ",20,300) # C3 MCP1
    #cus_f = TF1("cus_f"," sqrt( pow(([0]/x),2) + 2*[1]*[1]) ",30,600) # MCP12
    cus_f = TF1("cus_f"," sqrt( pow(([0]/x),2) + 2*[1]*[1]) ",40,400) # MCP12
    cus_f.SetParameters(5, 0.05)
    cus_f.SetParLimits(0,0,5000)
    sig_h.Fit('cus_f','QR')
    result = sig_h.Fit('cus_f',"SQR") # result is a TFitResultPtr
    #result = sig_h.Fit('cus_f',"SQNRO") # result is a TFitResultPtr
    print'A = ',result.Parameter(0),'+/-',result.ParError(0)
    print'C = ',result.Parameter(1),'+/-',result.ParError(1)
    chi2 = sig_h.Chisquare(cus_f)
    DOF = cus_f.GetNDF()

    c0 = TCanvas()
    #sig_h.Draw("AP")

    ymax = c0.GetUymax()

    c = TCanvas()

    #gPad.DrawFrame(0.,0.,600.,0.15,"Sigma dt vs. Aeff/brmseff") # For MCP1 
    #sig_h.GetXaxis()
    #c.cd()
    sig_h.SetTitle("Sigma dt vs. Aeff/brmseff")
    sig_h.GetYaxis().SetTitle("MCP1/2 sigma dt")
    sig_h.GetXaxis().SetTitle("MCP1/2 Aeff/brmseff")
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

    if len(vset) > 2:

        qinfo = str(q_min)
        if qinfo == '0.0':
            qinfo = 'NoQuant'
        else:
            qinfo = 'Qstart_' + str("{0:.0f}".format(q_min))

        #notes = ['Resolution', str(nb) + 'bins', qinfo, str(scanned_events) + '_events_scanned', square_side + 'x' + square_side]

        savepath = ''
        h_title = ''

        for i,note in enumerate(notes):
                savepath += note 
                h_title += note
                if i < (len(notes) - 1):
                    savepath += '_' 
                    h_title += ', ' 
    else:
        savepath = 'resonly' 

    c.SaveAs("bin/res/" + savepath + ".pdf") 
    c.SaveAs("bin/res/" + savepath + ".png") 
    sig_h.SaveAs("bin/res/" + savepath + ".root")

    # Automatically open file
    #os.system('evince bin/res/' + savepath + '.pdf')
