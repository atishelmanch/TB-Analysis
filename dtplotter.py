from ROOT import *
from math import fabs,sqrt,floor, ceil
from array import array
import sys
import os

def dt_plot(vset):

      print 'in dt_plot'
      if len(vset) != 0:
            print'Reading dictionary key items'
            direc_path = vset[1]
            square_side = vset[2]
            A1mincut = vset[3]
            A2mincut = vset[4]
            nb = int(vset[5]) # number of bins 
            max_events = int(vset[6])
            note = vset[7]

      else:
            print'Reading command line arguments'
            direc_path = sys.argv[2] # directory to read files from. Ex: 120_9_Oct/reco_roots, 160_9_Oct/reco_roots, all_data
            square_side = sys.argv[3] # side of square for hodo cut when scanning data   
            A1mincut = sys.argv[4]
            A2mincut = sys.argv[5]
            nb = int(sys.argv[6])
            max_events = int(sys.argv[7])  # Max events to scan per file
            note = sys.argv[8]

      file_paths = []
      file_directory = direc_path

      for file in os.listdir(str(os.getcwd()) + '/' + str(file_directory)):
            if '.root' in file:
                  print '     Found File: ',os.path.join(file)
                  file_paths.append(str(file_directory) + '/' + os.path.join(file)) 

      # Create Histogram 

      # Quantile binning 

#Plts.append(["fit_time[{}]-fit_time[{}]:{}".format(self.xtal[0],self.xtal[1],self.Aeff), "resolution_vs_aeff", bins[0], bins[1], bins[2], bins[3], bins[4], bins[5]])
# p[2] = bins[0] = number of x bins 
# p[4] = max x value 
# p[3] = min x value 

      x_min = 0
      x_max = 1000
      
      tf = TFile.Open(file_paths[0])
      tree = tf.Get('h4')

      Aeff = "pow( 2 / ( (1/pow(amp_max[MCP1]/b_rms[MCP1], 2)) + (1/pow(amp_max[MCP2]/b_rms[MCP2],2)) ) , 0.5)"   

      cut = ''

      ## Hybrid quantile method. Uses fixed width bins up to aeff_min_quant, then quantiles above that
      aeff_min_quant = 850                                                                             # The Aeff value above which quantiles are used
      aeff_tmp       = TH1F('aeff',"", 100, aeff_min_quant, x_max)
      tree.Draw(Aeff+'>>aeff', cut)                                         # Creates a temporary histogram to find the quantiles
      #tree.Draw('hhh', cut) 
      nquants   = int(ceil(nb/2.)+1)                                                                      # n_quantiles = nbins / 2 + 1 (round up if odd)
      probs     = array('d', [x/(nquants-1.) for x in range(0, nquants)])                                 # Quantile proportions array
      quantiles = array('d', [0 for x in range(0, nquants)])                                              # Bin edges, initialized as all 0's
      aeff_tmp.GetQuantiles(nquants, quantiles, probs)                                                    # Overwrites 'quantiles' with bin edges positions
      nfixed_bins    = int(floor(nb/2.))                                                                  # n_fixed_bins = nbins/2 + 1 (round down if odd)
      fixed_bin_size = (aeff_min_quant-x_min)/nfixed_bins              
      bins = array('d', [fixed_bin_size*n for n in range(nfixed_bins)]) + quantiles                       # Fixed width bins up to aeff_min_quant, then uses quantiles
      #hh   = TH2F('hh', self.file_title+'_dt_vs_aeff_heatmap', p[2], bins, p[5], p[6], p[7])             # Return a TH2F with quantile binning

      #print'bins = ',bins
      #h = TH2F('h','h',nb,0,800,2000,-10,10) 
      h = TH2F('h','h',nb,bins,2000,-10,10)

      #print'h = ',h
      #print'bins = ',bins

      dth = TH1F('dth','dth',nb,-10,10)

      # Create Cuts 
      cuts = []

      cuts.append('( fabs(hodox + 4) < ' + square_side + ')') 
      cuts.append('( fabs(hodoy - 4) < ' + square_side + ')') 
      cuts.append('( A1 > ' + A1mincut + ' )' )
      #cuts.append('( A1 < 10000 )')
      cuts.append('( A2 > ' + A2mincut + ' )' )
      #cuts.append('( A2 < 10000 )')

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

                  # Define variables 

                  MCP1 = eval('f.digi.MCP1')
                  MCP2 = eval('f.digi.MCP2')
                  CFD = eval('f.digi.CFD')

                  A1 = float(event.amp_max[MCP1])
                  A2 = float(event.amp_max[MCP2])

                  brms1 = float(event.b_rms[MCP1])
                  brms2 = float(event.b_rms[MCP2])

                  hodox = event.X[0]
                  hodoy = event.Y[0]

                  t1 = float(event.time[MCP1 + CFD])
                  t2 = float(event.time[MCP2 + CFD])

                  dt = t2 - t1 

                  # Fill h
                  if eval(cut) and A1 != -0.0 and A2 != -0.0:

                        A_eff = sqrt( 2 / ( (A1/brms1)**(-2) + (A2/brms2)**(-2) ) )
                       #print'dt = ',dt
                        h.Fill(A_eff,dt)
                        dth.Fill(dt)
                  
                  # Check file progress
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
      notes = ['dt_vs_Aeffo_brmseff', str(nb) + 'bins', str(scanned_events) + '_events_scanned', square_side + 'x' + square_side]

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
      h.GetXaxis().SetTitle('(amp_eff_MCP1_MCP2) / b_rms_eff')
      h.GetYaxis().SetTitle('time[MCP1 + CFD] - time[MCP2 + CFD]')
      h.GetYaxis().SetTitleOffset(1.5)

      h.Draw("COLZ1")

      c.SaveAs('bin/pdfs/' + savepath + '.pdf')
      h.SaveAs('bin/roots/' + savepath + '.root')


      # dt distribution 

      notes = ['dt_distribution', str(nb) + 'bins', str(scanned_events) + '_events_scanned', square_side + 'x' + square_side]

      dtsavepath = ''
      dth_title = ''

      for i,note in enumerate(notes):
            dtsavepath += note 
            dth_title += note
            if i < (len(notes) - 1):
                  dtsavepath += '_' 
                  dth_title += ', '  

      c = TCanvas()
      #h.SetStats(False)
      dth.SetTitle(dth_title)
      dth.GetXaxis().SetTitle('time[MCP1 + CFD] - time[MCP2 + CFD]')
      dth.GetYaxis().SetTitle('Events')
      dth.GetYaxis().SetTitleOffset(1.5)
      dth.SetFillColor(kBlue - 3)

      dth.Draw()

      c.SaveAs('bin/pdfs/' + dtsavepath + '.pdf')
      dth.SaveAs('bin/roots/' + dtsavepath + '.root')


      # Automatically open file
      # os.system('evince ' + 'bin/pdfs/' + dtsavepath + '.pdf')

      #print'h = ',h

      h.SetDirectory(0)

      return h