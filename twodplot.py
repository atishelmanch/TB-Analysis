from ROOT import *
from math import fabs,sqrt
import sys
import os

def TwoD_plot(vset):
      
      # Read variables 

      gROOT.ProcessLine(".L /afs/cern.ch/work/a/atishelm/CMSSW_9_0_1/src/Oct2018TB/H4Analysis/interface/TrackTree.h")
      gROOT.ProcessLine(".L /afs/cern.ch/work/a/atishelm/CMSSW_9_0_1/src/Oct2018TB/H4Analysis/interface/PositionTree.h")

      if len(vset) != 0:
            print'Reading dictionary key items'

            variables = vset[1]
            elements = vset[2]
            direc_path = vset[3]
            square_side = vset[4]
            #nb = int(vset[5])
            #varmin = float(vset[6])
            #varmax = float(vset[7])
            max_events = int(vset[5])
            max_files = int(vset[6])
            note = vset[7]

      else:
            print'Reading command line arguments'

            variable = sys.argv[2]
            element = sys.argv[3]
            direc_path = sys.argv[4]
            square_side = sys.argv[5]
            nb = int(sys.argv[6])
            varmin = float(sys.argv[7])
            varmax = float(sys.argv[8])
            max_events = int(sys.argv[9])
            note = sys.argv[10]
         
      # Get Elements 
      for i,e in enumerate(elements.split(',')):
            print'e = ',e

            exec('element' + str(i) + ' = e')
            print 'element' + str(i) + ' = ', eval('element' + str(i))
            #exec('tree_el_' + str(i) + ' = "f.digi.element' + str(i) + '"')

      # Get Variables 
      for i,v in enumerate(variables.split(',')):
            exec('var' + str(i) + ' = v')
            print 'variable' + str(i) + ' = ', eval('var' + str(i))
            #eval('tree_el_' + i + ' = f.digi.element' + i)

      yvar_name = var0
      xvar_name = var1

      # Find Files 

      file_paths = []
      file_directory = direc_path

      #for file in os.listdir(str(os.getcwd()) + '/' + str(file_directory)):

      # for file in os.listdir(file_directory):
      #       #print'file = ',file
      #       #if file.endswith(".root"):
      #       if '.root' in file:
      #             print '     Found File: ',os.path.join(file)
      #             file_paths.append(str(file_directory) + '/' + os.path.join(file)) 

      # Create Histogram
      
      #h = TH1F('h','h',nb,varmin,varmax)
      histos = []
      #if yvar_name == 'dt': h = TH2F('h','h',100,0,10,400,-5.2,-4.6)
     # if yvar_name == 't': h = TH2F('h','h',100,0,10,100,5,35)

      #h = TH2F('h','h',100,0,10,400,-5.2,-4.6)
      #h2 = TH3F('h2','h2',20,-10,10,20,-10,10,100,-5.5,-4)
      #h2 = TH2F('h2','h2',20,-10,10,20,-10,10)

      #histos.append(h)
      #histos.append(h2)

      #h.SetName("h")
      #h.SetTitle("h")

      # Create Cuts

      cuts = []

      # Assuming center is (x,y) = (-4,4)  
      cuts.append('( fabs(fitResult[0].x() + 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append('( fabs(fitResult[0].y() - 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append ('track_tree.n_tracks == 1')  
      if yvar_name == 't': 
            cuts.append('fit_ampl[' + element0 + '] > 200')
            cuts.append('fit_chi2[' + element0 + '] < 5')
            cuts.append('fit_ampl[C3] > 4000')
      #cuts.append('( value >= ' + str(varmin) + ' )' )
      #cuts.append('( value <= ' + str(varmax) + ' )')

      cut = ''

      for i,c in enumerate(cuts):
            cut += c 
            if i < (len(cuts) - 1):
                  cut += ' && '  # Needs to be understood by ROOT 

      # Booleans and Iterators 

      verbose = True
      file_i = 1
      event_i = 1
      scanned_events = 0
      e_emp = 0

      # Make a histogram for each file then combine 
      #h = TH2F('h','h',100,0,10,100,3,35)
      #h.SetName('h')

      if xvar_name == 'R':
            xvar = 'sqrt((fitResult[0].x() + 4)**2 + (fitResult[0].y() - 4)**2)'
      if yvar_name == 't':
            yvar = 'fit_time[' + element0 + '] - time[TRG + LED]' 

      #h = TH2F('h','h',100,0,100,100,0,40)

      #TObjHist

      #os.system('')
      # os_command = 'hadd combined.root'
      # for i,path in enumerate(file_paths):
      #       os_command += ' ' + path
      #       if i == 0: break 
      
      #os.system(os_command)

      #h = TH2F('h','',10,0,10,100,22,26)
      f = TFile.Open('/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3_without13420.root')
      #f.h4.Draw( yvar + ":" + xvar + " >> h('h','h',100,0,100,100,0,40)",cut)
      #f.h4.Draw( yvar + ":" + xvar + " >> h('h','h',10,0,10,100,22,26)",cut)
      #f.h4.Draw( yvar + ":" + xvar + " >> h(15,0,10,100,22,26)",cut)
      f.h4.Draw( yvar + ":" + xvar + " >> h()",cut)
      # f.h4.Draw("fitResult[0].x()*fitResult[0].x()  >> h2()",cut)
      # c1 = TCanvas()
      # h2.Draw()
      # c1.SaveAs('/eos/user/a/atishelm/www/plots/hodox.png')

      # f.h4.Draw("fitResult[0].y()**2  >> h3()",cut)
      # c2 = TCanvas()
      # h3.Draw()
      # c2.SaveAs('/eos/user/a/atishelm/www/plots/hodoy.png')
      #h.GetXaxis().SetRangeUser(0,10)
      #h.GetYaxis().SetRangeUser(0,40)
      h.FitSlicesY()
     # h_1.SetMarkerStyle(kDot)
     # h_1.SetMarkerColor(kBlue)

      #h_1.GetYaxis().SetRangeUser(23.5,25)

      #f.h4.Draw( xvar + " >> h()",cut)
      #os.system('hadd h.root histo0.root histo1.root')

      # path iterator, path 
      #for pi,path in enumerate(file_paths):
            #f = TFile.Open('combined.root')
            #f.h4.Draw("fit_time[MCP1]:(fitResult[0].x()*fitResult[0].x() + fitResult[0].y()*fitResult[0].y()) >> h('h','h',100,0,10,100,5,35)")
             
           # exec("h" + str(pi) + " = TH2F('h" + str(pi) + "','h" + str(pi) + "',100,0,100,100,0,40)")

           # h_temp = eval("h" + str(pi)) 

            #print'h_temp = ',h_temp

            #h_temp.SaveAs("histo" + str(pi) + ".root") 

            #histos.append(h_temp)
            #histos.append('') 
            #histos[pi] = h_temp 
            #print'histos = ',histos
            #histos.append(eval("h" + str(pi)))

            # Fill histogram  
            #print'cut = ',cut
            #f.h4.Draw( yvar + ":" + xvar + " >> h()",TCut(cut))
            #h = TH2F('h','h',100,0,100,100,0,40)
            #f.h4.Draw( yvar + ":" + xvar + " >> h" + str(pi),cut)

            #if pi + 1 == max_files:
                  #if verbose: print 'Max desired files reached'
                  #break

            #file_i += 1

      # Combine histograms 

      # for i,histo in enumerate(histos):
      #       print'histo = ',histo
      #       histo.SaveAs("histo" + str(i) + ".root") 

      #os.system('hadd h.root histo0.root histo1.root')



      # Create save path 
      #print e_emp,' events missing position data'
      #print entries,' entries'      

      #path_notes = []
      #notes = [yvar_name + 'vs' + xvar_name, element0, element1, str(scanned_events) + '_events_scanned', square_side + 'x' + square_side]
      if yvar_name == 't':
            notes = [yvar_name + 'vs' + xvar_name, element0, square_side + 'x' + square_side]
      #notes = ['test']

      savepath = ''
      h_title = ''

      for i,note in enumerate(notes):
            savepath += note 
            h_title += note
            if i < (len(notes) - 1):
                  savepath += '_' 
                  h_title += ', '  

      
      # Plot
      c = TCanvas()
      #h.SetStats(False)
      h_1.SetTitle(h_title)
      #h.GetXaxis().SetTitle(variable + '[' + element + ']')
      h_1.GetXaxis().SetTitle(xvar_name)
      if yvar_name == 't': h_1.GetYaxis().SetTitle(yvar_name + '_' + element0)
      #h.GetYaxis().SetTitleOffset(1.5)

      #h.SetFillColor(kBlue - 3)
      #h.Draw("COLZ1")
      #h_1.Draw("COLZ1")
      h_1.SetMarkerStyle(kFullDotMedium)
      h_1.SetMarkerColor(kBlue)
      h_1.Draw()
      

      c.SaveAs('/eos/user/a/atishelm/www/' + savepath + '.png')
      #h.SaveAs('/eos/user/a/atishelm/www/plots/' + savepath + '.root')

      h_1.SaveAs('/eos/user/a/atishelm/www/' + savepath + '.root')

      # Automatically open file
      os.system('root -l /eos/user/a/atishelm/www/' + savepath + '.root')