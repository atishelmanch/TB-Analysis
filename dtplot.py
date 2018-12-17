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
            nb = int(vset[4])
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
            #print'e = ',e

            exec('element' + str(i) + ' = e')
            eval('e_elements.append(e)')
            print 'element' + str(i) + ' = ', eval('element' + str(i))
            #exec('tree_el_' + str(i) + ' = "f.digi.element' + str(i) + '"')

      # Dt type depends on two electronic elements 
      dt_type = ''

      #combined_file = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3_without13420.root'

    # Other Combined Files:

    # /eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3ud_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3down.root
    # /eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3ud_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3up.root
    # /eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3lr_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3left.root
    # /eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3lr_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3right.root

      if element0 == 'MCP1' and element1 == 'MCP2':
            dt_type = 'MCPs' 
            combined_file = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3_without13420.root'
      elif element0 == 'C3' and element1 == 'C4':
            #dt_type = 'C3u'
            dt_type = 'XTALs'
            combined_file = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3ud_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3up.root'
      elif element0 == 'C3' and element1 == 'C2':
            #dt_type = 'C3d'
            dt_type = 'XTALs'
            combined_file = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3ud_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3down.root'
      elif element0 == 'C3' and element1 == 'B3':
            #dt_type = 'C3l'
            dt_type = 'XTALs'
            combined_file = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3lr_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3left.root'
      elif element0 == 'C3' and element1 == 'D3':
            #dt_type = 'C3r'
            dt_type = 'XTALs'
            combined_file = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3lr_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3right.root'
      else:
            dt_type = 'XTALMCP'
            combined_file = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3_without13420.root'

      print'dt type = ',dt_type

      # If it's MCP/MCP or XTAL/XTAL 
      if dt_type == 'MCPs' or dt_type == 'XTALs':
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

      # Only other option is XTAL/MCP 
      else:
            print'not mcp/mcp or xtal/xtal'
            # Define variables for each element
            #variables = ['fit_time','fit_ampl','b_rms']
            #for v in variables:
                  #for e in e_elements:
                        #exec('f  v' + '[' + )
            ft0 = 'fit_time[' + element0 + ']'
            ft1 = 'fit_time[' + element1 + ']'
            VC_ft = 'fit_time[VFE_CLK]' # VFE Clock Fit time 
            fa0 = 'fit_ampl[' + element0 + ']'
            fa1 = 'fit_ampl[' + element1 + ']'
            noise0 = 'b_rms[' + element0 + ']'
            noise1 = 'b_rms[' + element1 + ']'

            # # For 160 MHz
            correction = 'int((' + ft0 + ' - ' + ft1 +  '+' +  VC_ft + ')/6.238)*6.238' 
            print'**Using 160 MHz correction**'

            # # For 120 MHz
            # correction = int((xtal_ft - MCP1_ft + VC_ft)/8.317)*8.317 

            xvar = fa0 
            yvar = ft0 + '-' + ft1 + '+' + VC_ft + '-' + correction
            
            # yvar = ft0 + ' - ' + ft1
            #xvar = 'pow( 2 / ( (1/pow( ' + fa0 + '/' + noise0 + ', 2)) + (1/pow(' + fa1 + '/' + noise1 + ',2)) ) , 0.5)'      

      # Create Cut

      cuts = []

      # Assuming center is (x,y) = (-4,4)  
      cuts.append('( fabs(fitResult[0].x() + 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append('( fabs(fitResult[0].y() - 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append ('track_tree.n_tracks == 1')  

      if dt_type == 'MCPs':
            cuts.append('fit_ampl[' + element0 + '] > 100')
            cuts.append('fit_ampl[' + element1 + '] > 100')

      
      elif dt_type == 'XTALs':
            # Need to make energy dependent amplitude cuts 
            # One option may be to create hiso for each energy file then merge 
            cuts.append('fit_ampl[' + element0 + '] > 1000')
            cuts.append('fit_ampl[' + element1 + '] > 1000')
            #cuts.append('fit_chi2[' + element0 + '] < 5')
            #cuts.append('fit_ampl[C3] > 4000')

      elif dt_type == 'XTALMCP':
            # Need energy dependent XTAL amplitude cuts 
            cuts.append('fit_ampl[' + element0 + '] > 1000')
            cuts.append('fit_ampl[' + element1 + '] > 100')

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

      if dt_type == 'MCPs': 
            h = TH2F('h','h',nb,0,600,300,4.5,5.3) 
      elif dt_type == 'XTALs': 
            h = TH2F('h','h',nb,200,1600,300,-2,2) 
      elif dt_type == 'XTALMCP': 
            h = TH2F('h','h',nb,0,10000,300,-30,30) 

      #print'entries = ',f.h4.GetEntries()
      events_scanned = f.h4.GetEntries()

      f.h4.Draw( yvar + ":" + xvar + " >> h",cut)
      #h.GetYaxis().SetRangeUser(-10,10)

      # Create save path 

      if dt_type == 'MCPs':
            notes = ['MCP12','dtvsAeff', str(events_scanned) + 'eventscanned', square_side + 'x' + square_side]
      elif dt_type == 'XTALs':
            notes = [element0 + element1,'dtvsAeff', str(events_scanned) + 'eventscanned', square_side + 'x' + square_side]
      elif dt_type == 'XTALMCP':
            notes = [element0 + element1,'dtvsXTALAmp', str(events_scanned) + 'eventscanned', square_side + 'x' + square_side]
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
      #h.GetXaxis().SetTitle(xvar)
      if dt_type == 'MCPs': 
            h.GetYaxis().SetTitle('MCP12 dt')
            h.GetXaxis().SetTitle('MCP12 Aeff/brmseff')
      elif dt_type == 'XTALs': 
            h.GetYaxis().SetTitle(element0 + element1 + ' dt')
            h.GetXaxis().SetTitle(element0 + element1 + ' Aeff/brmseff')
      elif dt_type == 'XTALMCP': 
            h.GetYaxis().SetTitle(element0 + element1 + ' dt')
            h.GetXaxis().SetTitle('fit_ampl[' + element0 + ']')
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

      return h, events_scanned, dt_type