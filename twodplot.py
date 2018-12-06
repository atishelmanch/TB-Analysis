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

      yvar = var0
      xvar = var1

      # Find Files 

      file_paths = []
      file_directory = direc_path

      #for file in os.listdir(str(os.getcwd()) + '/' + str(file_directory)):
      for file in os.listdir(file_directory):
            #print'file = ',file
            #if file.endswith(".root"):
            if '.root' in file:
                  print '     Found File: ',os.path.join(file)
                  file_paths.append(str(file_directory) + '/' + os.path.join(file)) 

      # Create Histogram
      
      #h = TH1F('h','h',nb,varmin,varmax)
      histos = []
      #if yvar == 'dt': h = TH2F('h','h',100,0,10,400,-5.2,-4.6)
     # if yvar == 't': h = TH2F('h','h',100,0,10,100,5,35)

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
      cuts.append('( fabs(hodox + 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append('( fabs(hodoy - 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append ('ntracks == 1')  
      #cuts.append('( value >= ' + str(varmin) + ' )' )
      #cuts.append('( value <= ' + str(varmax) + ' )')

      cut = ''

      for i,c in enumerate(cuts):
            cut += c 
            if i < (len(cuts) - 1):
                  cut += ' and '  

      # Booleans and Iterators 

      verbose = True
      file_i = 1
      event_i = 1
      scanned_events = 0
      e_emp = 0

      for path in file_paths:
            f = TFile.Open(path)
      #f.h4.Draw("fit_time[MCP1]:(fitResult[0].x()*fitResult[0].x() + fitResult[0].y()*fitResult[0].y()) >> h('h','h',100,0,10,100,5,35)")
            f.h4.Draw("fit_time[MCP1]:(fitResult[0].x()*fitResult[0].x() + fitResult[0].y()*fitResult[0].y()) >> h()")

      # for path in file_paths:

      #       if verbose: print 'Reading File ' + str(file_i) + '/' + str(len(file_paths)) + ': ',path
      #       event_i = 0
      #       tmp_perc = 1000

      #       f = TFile.Open(path)
      #       f = TFile.Open(file_paths[0])
      #       total_num_events = f.h4.GetEntries()
      #       if int(max_events) == -1:
      #             scanned_events += total_num_events
      #       if verbose: print 'total num events = ', total_num_events

      #       f.h4.Draw("fit_time[MCP1]:(fitResult[0].x()*fitResult[0].x() + fitResult[0].y()*fitResult[0].y()) >> h")

      """for event in f.h4:

                  # Check if fit result exists 
                  val = event.fitResult
                  val_l = len(val)
                  #print'val = ',val
                  #print'len(val) = ',len(val)

                  if val_l == 0:
                        #print'No x fit result value, skipping event' 
                        e_emp += 1
                        continue

                  # x and y positions 
                  hodox = event.fitResult[0].x() 
                  hodoy = event.fitResult[0].y() 

                  # If input y variable is dt, calculate dt 
                  if yvar == 'dt':
                        # Fit times
                        #print tree_el_0 
                        t_el0 = eval('f.digi.' + element0)
                        t_el1 = eval('f.digi.' + element1)
                        ft1 = float(event.fit_time[t_el0])
                        ft2 = float(event.fit_time[t_el1])
                        fa1 = float(event.fit_ampl[t_el0])
                        fa2 = float(event.fit_ampl[t_el1])
                        cut += 'and fa1 > 100'
                        cut += 'and fa2 > 100'

                        # If MCP1/MCP2, no correction needed
                        if element0 == 'MCP1' and element1 == 'MCP2':
                              dt = ft2 - ft1
                              yval = dt
                              #h.Fill(dt)

                  if yvar == 't':
                        t_el0 = eval('f.digi.' + element0)
                        ft = float(event.fit_time[t_el0])
                        fa1 = float(event.fit_ampl[t_el0])
                        yval = ft 
                        cut += 'and fa1 > 100'

                  # If input x variable is R, calculate R 
                  if xvar == 'R':
                        xval = sqrt(hodox**2 + hodoy**2)
                              
                  #print'xval = ',xval
                  #print'yval = ',yval

                  ntracks = int(eval('f.track_tree.n_tracks'))

                  if eval(cut):
                        #print'made cut'
                        #print'yval = ',yval
                        h.Fill(xval,yval)
                        #h2.Fill(hodox,hodoy)
                        

                  # value string 
                  #val_st = 'event.' + variable + '[' + tree_el + ']'
                  #value = eval(val_st)

                  # Add to dist

                  #if eval(cut):
                        #h.Fill(value)

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

            if file_i == max_files:
                  if verbose: print 'Max desired files reached'
                  #scanned_events += event_i
                  break

            file_i += 1"""


      # Create save path 
      #print e_emp,' events missing position data'
      #print entries,' entries'      

      #path_notes = []
      #notes = [yvar + 'vs' + xvar, element0, element1, str(scanned_events) + '_events_scanned', square_side + 'x' + square_side]
      notes = ['test']

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
      h.GetYaxis().SetTitle(yvar + '_' + element0 + '_' + element1)
      #h.GetYaxis().SetTitleOffset(1.5)

      #h.SetFillColor(kBlue - 3)
      #h.Draw("COLZ1")
      h.Draw("COLZ1")

      c.SaveAs('/eos/user/a/atishelm/www/plots/' + savepath + '.png')
      #h.SaveAs('/eos/user/a/atishelm/www/plots/' + savepath + '.root')

      h.SaveAs('/eos/user/a/atishelm/www/plots/' + savepath + '.root')

      # Automatically open file
      #os.system('evince ' + 'bin/tmp/' + savepath + '.pdf')