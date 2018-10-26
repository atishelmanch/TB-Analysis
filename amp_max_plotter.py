from ROOT import *
from math import fabs,sqrt
import sys
import os

def amp_max_plot(vset):
      
      if len(vset) != 0:
            print'Reading dictionary key items'
            element = vset[1]
            direc_path = vset[2]
            square_side = vset[3]
            ll = vset[4]
            ul = vset[5]
            max_events = int(vset[6])
            note = vset[7]

      else:
            print'Reading command line arguments'
            element = sys.argv[2]
            direc_path = sys.argv[3]
            square_side = sys.argv[4]
            ll = sys.argv[5]
            ul = sys.argv[6]
            max_events = int(sys.argv[7])
            note = sys.argv[8]

      file_paths = []
      file_directory = direc_path

      for file in os.listdir(str(os.getcwd()) + '/' + str(file_directory)):
            #if file.endswith(".root"):
            if '.root' in file:
                  print '     Found File: ',os.path.join(file)
                  file_paths.append(str(file_directory) + '/' + os.path.join(file)) 

      # Create Histograms 
      
      h = TH2F('h','h',50,-25,25,50,-25,25)

      # Create Cuts 
      cuts = []

      cuts.append('( fabs(hodox + 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append('( fabs(hodoy - 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append('( MCP_amp_max >= ' + ll + ' )' )
      cuts.append('( MCP_amp_max <= ' + ul + ' )')

      cut = ''

      for i,c in enumerate(cuts):
            cut += c 
            if i < (len(cuts) - 1):
                  cut += ' and '  

      verbose = True
      file_i = 1
      event_i = 1
      scanned_events = 0

      for path in file_paths:

            if verbose: print 'Reading File ' + str(file_i) + '/' + str(len(file_paths)) + ': ',path
            event_i = 0
            tmp_perc = 1000

            f = TFile.Open(path)
            total_num_events = f.h4.GetEntries()
            if int(max_events) == -1:
                  scanned_events += total_num_events
            if verbose: print 'total num events = ', total_num_events

            for event in f.h4:

                  hodox = event.X[0]
                  hodoy = event.Y[0]

                  MCP = eval('f.digi.' + element)

                  MCP_amp_max = event.amp_max[MCP]

                  xbin = h.GetXaxis().FindBin(hodox)
                  ybin = h.GetYaxis().FindBin(hodoy)

                  # Place higheset value in bin 
                  if eval(cut) and (MCP_amp_max > h.GetBinContent(xbin,ybin)): 
                        h.Fill(hodox,hodoy,MCP_amp_max)
                  
                  # Check progress
                  percentage = int((float(event_i) / float(total_num_events))*100)

                  if (percentage != tmp_perc): new_percentage = True
                  else: new_percentage = False

                  tmp_perc = int((float(event_i) / float(total_num_events))*100)

                  if ( (percentage%10 == 0) and (new_percentage) ): 
                        if verbose: print int(percentage),'% Read '
                  
                  if event_i == max_events:
                        if verbose: print 'Max desired events reached'
                        scanned_events += event_i
                        break

                  event_i += 1

            file_i += 1

      # Create save path 

      #path_notes = []

      gStyle.SetStatY(0.9)                                # Y-position (fraction of pad size)                
      gStyle.SetStatX(0.3)                                # X-position         
      gStyle.SetStatW(0.2)                                # Width           
      gStyle.SetStatH(0.1)                                # Height

      notes = ['Highest_amp_max', element, str(scanned_events) + '_events_scanned', square_side + 'x' + square_side]

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
      h.GetXaxis().SetTitle('hodoscope X (mm)')
      h.GetYaxis().SetTitle('hodoscope Y (mm)')

      #h.GetYaxis().SetTitleOffset(1.5)

      h.Draw("COLZ1")

      c.SaveAs('bin/pdfs/' + savepath + '.pdf')
      h.SaveAs('bin/roots/' + savepath + '.root')

      # Automatically open file
      os.system('evince ' + 'bin/pdfs/' + savepath + '.pdf')