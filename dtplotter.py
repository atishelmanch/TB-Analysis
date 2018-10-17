from ROOT import *
from math import fabs,sqrt
import sys
import os

def dt_plot():
        
      max_events = int(sys.argv[4])  # Max events to scan per file 
      # for now elements are just MCP1 and MCP2. Will next have options for which MCP and which crystal ( two arguments )
      square_side = str(2*float(sys.argv[3])) # side of square for hodo cut when scanning data  
      direc_path = sys.argv[2] # directory to read files from. Ex: 120_9_Oct/reco_roots, 160_9_Oct/reco_roots, all_data
      note = sys.argv[5]

      file_paths = []
      file_directory = direc_path

      for file in os.listdir(str(os.getcwd()) + '/' + str(file_directory)):
            if '.root' in file:
                  print '     Found File: ',os.path.join(file)
                  file_paths.append(str(file_directory) + '/' + os.path.join(file)) 

      # Create Histogram 

      h = TH2F('h','h',200,0,2000,300,-2,-8)

      # Create Cuts 
      cuts = []

      cuts.append('( fabs(hodox + 4) < ' + square_side + ')') 
      cuts.append('( fabs(hodoy - 4) < ' + square_side + ')') 
      cuts.append('A1 > 300')
      cuts.append('A1 < 10000')
      cuts.append('A2 > 300')
      cuts.append('A2 < 10000')

      cut = ''

      for i,c in enumerate(cuts):
            cut += c 
            if i < (len(cuts) - 1):
                  cut += ' and '
            
      #print'cut = ',cut
      
      #trees = ['hodo', 'digi', 'wf', 'info', 'h4']

      #f = TFile.Open(file_paths[0])

      # for tree in trees:
      #       print 'tree = ',tree
      #       eval('f.' + tree + '.Print()')
            #f.hodo.Print()

      f = TFile.Open(file_paths[0])

      MCP1 = eval('f.digi.MCP1')
      MCP2 = eval('f.digi.MCP2')
      CFD = eval('f.digi.CFD')

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

                  # Define variables 

                  MCP1 = eval('f.digi.MCP1')
                  MCP2 = eval('f.digi.MCP2')
                  CFD = eval('f.digi.CFD')

                  A1 = float(event.amp_max[MCP1])
                  A2 = float(event.amp_max[MCP2])

                  #print'A1, A2 = ',A1,A2

                  #A_eff = ( A1 * A2 ) / ( sqrt( A1*A1 + A2*A2 ) )

                  #print'A_eff = ',A_eff

                  hodox = event.X[0]
                  hodoy = event.Y[0]

                  t1 = float(event.time[MCP1 + CFD])
                  t2 = float(event.time[MCP2 + CFD])

                  dt = t2 - t1 

                  #MCP_amp_max = event.amp_max[MCP]
                  #MCP_amp_max = event.amp_maximum[MCP]

                  # xbin = h.GetXaxis().FindBin(hodox)
                  # ybin = h.GetYaxis().FindBin(hodoy)

                  # Fill h
                  if eval(cut) and A1 != -0.0 and A2 != -0.0:
                        A_eff = ( A1 * A2 ) / ( sqrt( A1*A1 + A2*A2 ) )
                        h.Fill(A_eff,dt)
                  
                  # Check file progress
                  percentage = int((float(event_i) / float(total_num_events))*100)

                  if (percentage != tmp_perc): new_percentage = True
                  else: new_percentage = False

                  tmp_perc = int((float(event_i) / float(total_num_events))*100)

                  if ( (percentage%10 == 0) and (new_percentage) ): 
                        if verbose: print int(percentage),'% Read '
                  
                  #print'event_i = ',event_i
                  #print'max_events = ',max_events

                  if event_i == max_events:
                        if verbose: print 'Max desired events reached'
                        scanned_events += event_i
                        break

                  event_i += 1

            file_i += 1

      # Highest amp_max vs. X vs. Y
      c = TCanvas()
      h.SetStats(False)
      h.GetXaxis().SetTitle('amp_eff_MCP1_MCP2')
      h.GetYaxis().SetTitle('time[MCP1 + CFD] - time[MCP2 + CFD]')
      h.GetYaxis().SetTitleOffset(1.2)
      h.GetYaxis().SetRangeUser(-4,-6)
      h_title = 'dt Between MCPs from' + str(scanned_events) + ' Scanned Events, ' + file_directory + ' ' + note
      h.SetTitle(h_title)
      h.Draw("COLZ1")
      savepath = 'MCP_dtplot_' + note

      c.SaveAs('bin/pdfs/' + savepath + '.pdf')
      h.SaveAs('bin/roots/' + savepath + '.root')

      # Automatically open file
      os.system('evince ' + 'bin/pdfs/' + savepath + '.pdf')