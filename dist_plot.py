from ROOT import *
from math import fabs,sqrt
import sys
import os

def dist_plot(vset):
      
      # Read variables 

      gROOT.ProcessLine(".L /afs/cern.ch/work/a/atishelm/CMSSW_9_0_1/src/Oct2018TB/H4Analysis/interface/TrackTree.h")
      gROOT.ProcessLine(".L /afs/cern.ch/work/a/atishelm/CMSSW_9_0_1/src/Oct2018TB/H4Analysis/interface/PositionTree.h")

      if len(vset) != 0:
            print'Reading dictionary key items'

            variable = vset[1]
            element = vset[2]
            direc_path = vset[3]
            square_side = vset[4]
            varmin = float(vset[5])
            varmax = float(vset[6])
            nb = int(vset[7])
            max_events = int(vset[8])
            note = vset[9]

      else:
            print'Reading command line arguments'

            variable = sys.argv[2]
            element = sys.argv[3]
            direc_path = sys.argv[4]
            square_side = sys.argv[5]
            varmin = float(sys.argv[6])
            varmax = float(sys.argv[7])
            nb = int(sys.argv[8])
            max_events = int(sys.argv[9])
            note = sys.argv[10]

      # Find Files 

      file_paths = []
      file_directory = direc_path

      for file in os.listdir(str(os.getcwd()) + '/' + str(file_directory)):
            #if file.endswith(".root"):
            if '.root' in file:
                  print '     Found File: ',os.path.join(file)
                  file_paths.append(str(file_directory) + '/' + os.path.join(file)) 

      # Create Histogram
      
      h = TH1F('h','h',nb,varmin,varmax)

      # Create Cuts

      cuts = []

      cuts.append('( fabs(hodox + 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append('( fabs(hodoy - 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append('( value >= ' + str(varmin) + ' )' )
      cuts.append('( value <= ' + str(varmax) + ' )')

      cut = ''

      for i,c in enumerate(cuts):
            cut += c 
            if i < (len(cuts) - 1):
                  cut += ' and '           

      tree_el = 'f.digi.' + element

      verbose = True
      file_i = 1
      event_i = 1
      scanned_events = 0
      e_emp = 0

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

                  val = event.fitResult
                  val_l = len(val)
                  #print'val = ',val
                  #print'len(val) = ',len(val)

                  if val_l == 0:
                        #print'No x fit result value, skipping event' 
                        e_emp += 1
                        continue

                  # Get Event Value
                  # hodox = event.X[0]
                  # hodoy = event.Y[0]

                  hodox = event.fitResult[0].x() # new x and y positions
                  hodoy = event.fitResult[0].y() 

                  val_st = 'event.' + variable + '[' + tree_el + ']'
                  value = eval(val_st)

                  # Add to dist

                  if eval(cut):
                        h.Fill(value)

                  # Check Progress
                  
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
      print e_emp,' events missing position data'
      #print entries,' entries'      

      #path_notes = []
      notes = [variable, element, str(scanned_events) + '_events_scanned', square_side + 'x' + square_side]

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
      h.GetXaxis().SetTitle(variable + '[' + element + ']')
      h.GetYaxis().SetTitle('Events')
      h.GetYaxis().SetTitleOffset(1.5)

      h.SetFillColor(kBlue - 3)
      h.Draw()

      c.SaveAs('bin/pdfs/' + savepath + '.pdf')
      h.SaveAs('bin/roots/' + savepath + '.root')

      # Automatically open file
      os.system('evince ' + 'bin/pdfs/' + savepath + '.pdf')