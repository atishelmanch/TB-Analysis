from ROOT import *
from math import fabs,sqrt
import sys
import os

def amp_max_plot(vset):
      
      if len(vset) != 0:
            print'Reading dictionary key items'
            element = vset[1]
            direc_path = vset[2]
            square_side = str(2*float(vset[3]))
            A1mincut = vset[4]
            A2mincut = vset[5]
            nb = int(vset[6])
            max_events = int(vset[7])
            note = vset[8]

      else:
            print'Reading command line arguments'
            max_events = int(sys.argv[5]) # Max events to scan per file 
            element = sys.argv[2] # Electronics element. Ex: MCP1 or MCP2
            square_side = str(2*float(sys.argv[4])) # side of square for hodo cut when scanning data  
            direc_path = sys.argv[3] # directory to read files from. Ex: 120_9_Oct/reco_roots, 160_9_Oct/reco_roots, all_data
            note = sys.argv[6]

      file_paths = []
      file_directory = direc_path

      for file in os.listdir(str(os.getcwd()) + '/' + str(file_directory)):
            #if file.endswith(".root"):
            if '.root' in file:
                  print '     Found File: ',os.path.join(file)
                  file_paths.append(str(file_directory) + '/' + os.path.join(file)) 

      # Create Histograms 
      
      h = TH2F('h','h',50,-25,25,50,-25,25)
      h2 = TH1F('h2','h2',50,0,5000)

      # Create Cuts 
      MCP_min_cut = 'MCP_amp_max > 300'
      MCP_max_cut = 'MCP_amp_max < 10000'

      cut = '(fabs(hodox + 4) < ' + square_side + ') and (fabs(hodoy - 4) < ' + square_side + ') and ' + MCP_min_cut + ' and ' + MCP_max_cut

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

                  #print 'eval:', (bool(eval('f.digi.' + element) is not None ))

                  MCP = eval('f.digi.' + element)
                  
                  # `else: 
                  #       print 'error'
                  #       sys.exit()`

                  MCP_amp_max = event.amp_max[MCP]
                  #MCP_amp_max = event.amp_maximum[MCP]

                  xbin = h.GetXaxis().FindBin(hodox)
                  ybin = h.GetYaxis().FindBin(hodoy)

                  # Add to dist
                  if eval(cut):
                        h2.Fill(MCP_amp_max)

                  if eval(cut) and (MCP_amp_max > h.GetBinContent(xbin,ybin)): # Place higheset value in bin 
                        #h.Fill(hodox,hodoy,MCP1_amp_max)
                        h.Fill(hodox,hodoy,MCP_amp_max)
                  
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

      # Highest amp_max vs. X vs. Y
      c = TCanvas()
      h.SetStats(False)
      h.GetXaxis().SetTitle('hodoscope X (mm)')
      h.GetYaxis().SetTitle('hodoscope Y (mm)')
      h_title = element + ' Highest amp_max Over ' + str(scanned_events) + ' Events, ' + file_directory + ' ' + note
      # + square_side + 'x' + square_side + 'mm window around (-4, +4)' 
      h.SetTitle(h_title)
      h.Draw("COLZ1")
      savepath = element + '_plot' + note #+ '.pdf'

      c.SaveAs('bin/pdfs/' + savepath + '.pdf')
      h.SaveAs('bin/roots/' + savepath + '.root')

      # Events vs. amp_max 
      c2 = TCanvas()
      h2.SetStats(False)
      h2.GetXaxis().SetTitle('amp_max (ADC)')
      h2.GetYaxis().SetTitle('Events')
      h2.GetYaxis().SetTitleOffset(1.4)
      h2_title = element + ' amp_max, ' + str(scanned_events) + ' Events Scanned, ' + file_directory + ' ' + note
      # + square_side + 'x' + square_side + 'mm window around (-4, +4)'
      h2.SetTitle(h2_title)
      h2.SetFillColor(kBlue - 3)
      h2.Draw()
      savepath2 = element + '_dist_plot' + note #+ '.pdf'

      c2.SaveAs('bin/pdfs/' + savepath2 + '.pdf')
      h2.SaveAs('bin/roots/' + savepath2 + '.root')

      # Automatically open file
      os.system('evince ' + 'bin/pdfs/' + savepath2 + '.pdf')