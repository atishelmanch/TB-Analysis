from ROOT import *
#from math import *
from math import fabs,sqrt,floor,ceil
from array import array
import sys
import os

def dt_plot(vset):

      gROOT.ProcessLine(".L /afs/cern.ch/work/a/atishelm/CMSSW_9_0_1/src/Oct2018TB/H4Analysis/interface/TrackTree.h")
      gROOT.ProcessLine(".L /afs/cern.ch/work/a/atishelm/CMSSW_9_0_1/src/Oct2018TB/H4Analysis/interface/PositionTree.h")

      print 'in dt_plot'
      if len(vset) != 0:
            print'Reading dictionary key items'

            combined_file = vset[1]
            elements = vset[2]
            square_side = vset[3]
            #direc_path = vset[1]
            #square_side = vset[2]
            # A1mincut = vset[3]
            # A2mincut = vset[4]
            # nb = int(vset[5]) # number of bins 
            # max_events = int(vset[6])
            # x_min = float(vset[7])
            # q_min = float(vset[8])
            # XTAL_str = vset[9]
            # note = vset[10]

      else:
            print'Reading command line arguments'
            direc_path = sys.argv[2] # directory to read files from. Ex: 120_9_Oct/reco_roots, 160_9_Oct/reco_roots, all_data
            square_side = sys.argv[3] # side of square for hodo cut when scanning data   
            A1mincut = sys.argv[4]
            A2mincut = sys.argv[5]
            nb = int(sys.argv[6])
            max_events = int(sys.argv[7])  # Max events to scan per file
            x_min = float(vset[8])
            q_min = float(vset[9])
            XTAL_str = vset[10]
            note = sys.argv[11]

      #file_paths = []
      #file_directory = direc_path

      #for file in os.listdir(str(os.getcwd()) + '/' + str(file_directory)):
      # for file in direc_path: 
      #       if '.root' in file:
      #             print '     Found File: ',os.path.join(file)
      #             file_paths.append(str(file_directory) + '/' + os.path.join(file)) 


      # Get Electronic Elements 
      e_elements = []
      for i,e in enumerate(elements.split(',')):
            print'e = ',e

            exec('element' + str(i) + ' = e')
            eval('e_elements.append(e)')
            print 'element' + str(i) + ' = ', eval('element' + str(i))
            #exec('tree_el_' + str(i) + ' = "f.digi.element' + str(i) + '"')

      MCP_dt = False

      if element0 == 'MCP1' and element1 == 'MCP2':
            MCP_dt = True

      print'e_elements = ',e_elements

      # If it's MCP1/2 dt
      if MCP_dt:
            # Define variables for each element
            variables = ['fit_time','fit_ampl','b_rms']
            #for v in variables:
                  #for e in e_elements:
                        #exec('f  v' + '[' + )
            ft0 = 'fit_time[' + element0 + ']'
            ft1 = 'fit_time[' + element1 + ']'
            fa0 = 'fit_ampl[' + element0 + ']'
            fa1 = 'fit_ampl[' + element1 + ']'
            noise0 = 'b_rms[' + element0 + ']'
            noise1 = 'b_rms[' + element1 + ']'

            yvar = ft0 + ' - ' + ft1
            xvar = 'pow( 2 / ( (1/pow( ' + fa0 + '/' + noise0 + ', 2)) + (1/pow(' + fa1 + '/' + noise1 + ',2)) ) , 0.5)'

      # Create Cut

      cuts = []

      # Assuming center is (x,y) = (-4,4)  
      cuts.append('( fabs(fitResult[0].x() + 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append('( fabs(fitResult[0].y() - 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append ('track_tree.n_tracks == 1')  
      if MCP_dt:
            cuts.append('fit_ampl[' + element0 + '] > 100')
            cuts.append('fit_ampl[' + element1 + '] > 100')
            #cuts.append('fit_chi2[' + element0 + '] < 5')
            #cuts.append('fit_ampl[C3] > 4000')
      #cuts.append('( value >= ' + str(varmin) + ' )' )
      #cuts.append('( value <= ' + str(varmax) + ' )')

      cut = ''

      for i,c in enumerate(cuts):
            cut += c 
            if i < (len(cuts) - 1):
                  cut += ' && '  # Needs to be understood by ROOT   

      # Open combined file 
      f = TFile.Open(combined_file)

      # Create Histogram

      h = TH2F('h','h',100,0,1000,300,4.5,5.3)

      f.h4.Draw( yvar + ":" + xvar + " >> h",cut)
      #h.GetYaxis().SetRangeUser(-10,10)

      # Create save path 

      if MCP_dt:
            #notes = ['MCP12',yvar + 'vs' + xvar, square_side + 'x' + square_side]
            notes = ['MCP12','dtvsA', square_side + 'x' + square_side]
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
      h.SetTitle(h_title)
      #h.GetXaxis().SetTitle(variable + '[' + element + ']')
      h.GetXaxis().SetTitle(xvar)
      if MCP_dt: 
            h.GetYaxis().SetTitle('MCP12 dt')
      #h.GetYaxis().SetTitleOffset(1.5)

      #h.SetFillColor(kBlue - 3)
      #h.Draw("COLZ1")
      #h_1.Draw("COLZ1")
      #h_1.SetMarkerStyle(kFullDotMedium)
      #h_1.SetMarkerColor(kBlue)
      h.Draw("COLZ1")
      

      c.SaveAs('/eos/user/a/atishelm/www/' + savepath + '.png')
      #h.SaveAs('/eos/user/a/atishelm/www/plots/' + savepath + '.root')

      h.SaveAs('/eos/user/a/atishelm/www/' + savepath + '.root')

      # Automatically open file
      #os.system('root -l /eos/user/a/atishelm/www/' + savepath + '.root')

      #print'h = ',h

      ####

      h.SetDirectory(0)

      #return h, scanned_events
      return h