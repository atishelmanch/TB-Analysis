from ROOT import *
#from math import *
from math import fabs,sqrt,floor,ceil
from array import array
import sys
import os

def dt_plot(vset):

      #gSystem.AddIncludePath(" -I/afs/cern.ch/work/a/atishelm/CMSSW_9_0_1/src/Oct2018TB/H4Analysis/interface ;")
      #gSystem.AddLinkedLibs(" /afs/cern.ch/work/a/atishelm/CMSSW_9_0_1/src/Oct2018TB/H4Analysis/lib/*.so ;")

      gROOT.ProcessLine(".L /afs/cern.ch/work/a/atishelm/CMSSW_9_0_1/src/Oct2018TB/H4Analysis/interface/TrackTree.h")
      gROOT.ProcessLine(".L /afs/cern.ch/work/a/atishelm/CMSSW_9_0_1/src/Oct2018TB/H4Analysis/interface/PositionTree.h")
      #gROOT.ProcessLine(".L /afs/cern.ch/work/a/atishelm/CMSSW_9_0_1/src/Oct2018TB/H4Analysis/CfgManager/interface/CfgManager.h")
      #gROOT.ProcessLine(".L /afs/cern.ch/work/a/atishelm/CMSSW_9_0_1/src/Oct2018TB/H4Analysis/interface/Track.h")
      # #gROOT.ProcessLine(".L interface/Track.h;")
      # #gROOT.ProcessLine(".L H4Analysis/interface/*")

      print 'in dt_plot'
      if len(vset) != 0:
            print'Reading dictionary key items'
            direc_path = vset[1]
            square_side = vset[2]
            A1mincut = vset[3]
            A2mincut = vset[4]
            nb = int(vset[5]) # number of bins 
            max_events = int(vset[6])
            x_min = float(vset[7])
            XTAL_str = vset[8]
            note = vset[9]

      else:
            print'Reading command line arguments'
            direc_path = sys.argv[2] # directory to read files from. Ex: 120_9_Oct/reco_roots, 160_9_Oct/reco_roots, all_data
            square_side = sys.argv[3] # side of square for hodo cut when scanning data   
            A1mincut = sys.argv[4]
            A2mincut = sys.argv[5]
            nb = int(sys.argv[6])
            max_events = int(sys.argv[7])  # Max events to scan per file
            x_min = float(vset[8])
            XTAL_str = vset[9]
            note = sys.argv[10]

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

####

      #x_min = 20.
      x_max = 600.
      
      tf = TFile.Open(file_paths[0])
      tree = tf.Get('h4')

      Aeff = "pow( 2 / ( (1/pow(amp_max[MCP1]/b_rms[MCP1], 2)) + (1/pow(amp_max[MCP2]/b_rms[MCP2],2)) ) , 0.5)"   

      cut = ''

      ## Hybrid quantile method. Uses fixed width bins up to aeff_min_quant, then quantiles above that
      aeff_min_quant = 324
      #aeff_min_quant = 350                                                                           # The Aeff value above which quantiles are used
      aeff_tmp       = TH1F('aeff',"", 100, aeff_min_quant, x_max)
      tree.Draw(Aeff+'>>aeff', cut)                                         # Creates a temporary histogram to find the quantiles
      #tree.Draw('hhh', cut) 
      nquants   = int(ceil(nb/2.)+1)                                                                  # n_quantiles = nbins / 2 + 1 (round up if odd)
      probs     = array('d', [x/(nquants-1.) for x in range(0, nquants)])                                 # Quantile proportions array
      quantiles = array('d', [0 for x in range(0, nquants)])                                              # Bin edges, initialized as all 0's
      aeff_tmp.GetQuantiles(nquants, quantiles, probs)                                                    # Overwrites 'quantiles' with bin edges positions
      nfixed_bins    = int(floor(nb/2.))                                                                # n_fixed_bins = nbins/2 + 1 (round down if odd)
      fixed_bin_size = (aeff_min_quant-x_min)/nfixed_bins              
      bins = array('d', [fixed_bin_size*n + x_min for n in range(nfixed_bins)]) + quantiles    
      #bins = array('d', [fixed_bin_size*n + x_min for n in range(nfixed_bins)]) + quantiles                       # Fixed width bins up to aeff_min_quant, then uses quantiles
      #hh   = TH2F('hh', self.file_title+'_dt_vs_aeff_heatmap', p[2], bins, p[5], p[6], p[7])             # Return a TH2F with quantile binning


#####

      #print'bins = ',bins
      h = TH2F('h','h',nb,bins,400,-5.4,-4.4) # With quantile
      #h = TH2F('h','h',nb,x_min,x_max,800,-6,-4) # Without quantile 
      #h = TH2F('h','h',nb,x_min,x_max,400,-5.4,-4.4) # Without quantile 

      #print'h = ',h
      #print'bins = ',bins

      dth = TH1F('dth','dth',50,-10,10)
      Ah = TH1F('Ah','Ah',100,0,600)

      # Create Cuts 
      cuts = []

      cuts.append('( fabs(hodox + 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append('( fabs(hodoy - 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append('( A1 > ' + A1mincut + ' )' )
      #cuts.append('( A1 < 10000 )') # Check overflow bin? 
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
      entries = 0

      for path in file_paths:

            if verbose: print 'Reading File ' + str(file_i) + '/' + str(len(file_paths)) + ': ',path
            event_i = 0
            tmp_perc = 1000

            f = TFile.Open(path)
            total_num_events = f.h4.GetEntries()
            if int(max_events) == -1:
                  scanned_events += total_num_events
            if verbose: print 'total num events = ', total_num_events
                  
            #ii = 0
            #pos_exists = False
            e_emp = 0

            for event in f.h4:

                  #print'bool(event.fitResult[0].x()) = ',str(event.fitResult[0].x())

                  #print'val = ',event.fitResult[0].x()

                  val = event.fitResult
                  val_l = len(val)
                  #print'val = ',val
                  #print'len(val) = ',len(val)

                  if val_l == 0:
                        #print'No x fit result value, skipping event' 
                        e_emp += 1
                        continue

                  #ii += 1
                  #if (ii < 100): continue 

                  # Define variables 

                  MCP1 = eval('f.digi.MCP1')
                  MCP2 = eval('f.digi.MCP2')
                  CFD = eval('f.digi.CFD')
                  VFE_CLK = eval('f.digi.CFD')
                  CLK = eval('f.digi.CLK')
                  #hodox = float(eval(f.track_tree.fitResult[0].x()))
                  #hodoy = float(eval(f.track_tree.fitResult[0].x()))
                  
                  A1 = float(event.amp_max[MCP1])
                  A2 = float(event.amp_max[MCP2])

                  brms1 = float(event.b_rms[MCP1])
                  brms2 = float(event.b_rms[MCP2])

                  #hodox = event.X[0]
                  #hodoy = event.Y[0]

                  #print'bool = ',bool(event.fitResult[0].x())

                  hodox = event.fitResult[0].x() # new x and y positions
                  hodoy = event.fitResult[0].y() 

                  #print'hodox = ',hodox
                  #print'hodoy = ',hodoy

                  if(XTAL_str == 'MCP'): 
                        t1 = float(event.time[MCP1 + CFD])
                        t2 = float(event.time[MCP2 + CFD])
                        dt = t2 - t1

                  else: 
                        XTAL = eval('f.digi.' + XTAL_str)
                        ft = float(event.fit_time[XTAL])
                        t1 = float(event.time[MCP1 + CFD])
                        t2 = float(event.time[VFE_CLK + CLK])

                        dt = ft - t1 - t2 


                  #A_eff = sqrt( 2 / ( (A1/brms1)**(-2) + (A2/brms2)**(-2) ) )
                  # Fill h
                  #if eval(cut) and A1 != -0.0 and A2 != -0.0:
                  #if eval(cut) and A1 != -0.0 and A2 != -0.0 and A1 > 20 and A2 > 20:
                  #print'A1 = ',A1
                  #print'A2 = ',A2
                  if eval(cut) and A1 != -0.0 and A2 != -0.0:
                        entries += 1

                        A_eff = sqrt( 2 / ( (A1/brms1)**(-2) + (A2/brms2)**(-2) ) )
                        Ah.Fill(A_eff) 
                        h.Fill(A_eff,dt)
                        dth.Fill(dt)

                        #Ah.Fill(A_eff)
                        #if (A_eff > 20.):
                              #print'Aeff = ',A_eff
                              # Ah.Fill(A_eff) 
                              # h.Fill(A_eff,dt)
                              # dth.Fill(dt)
                  
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

      print e_emp,' events missing position data'
      print entries,' entries'
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
      h.SetStats(False)
      h.SetTitle(h_title)
      h.GetXaxis().SetTitle('(amp_eff_MCP1_MCP2) / b_rms_eff')
      h.GetYaxis().SetTitle('time[MCP1 + CFD] - time[MCP2 + CFD]')
      h.GetYaxis().SetTitleOffset(1.5)

      h.Draw("COLZ1")

      c.SaveAs('bin/tmp/' + savepath + '.pdf')
      h.SaveAs('bin/tmp/' + savepath + '.root')

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
      #dth.GetYaxis().SetTitleOffset(1.5)
      dth.SetFillColor(kBlue - 3)

      dth.Draw()

      c.SaveAs('bin/tmp/' + dtsavepath + '.pdf')
      dth.SaveAs('bin/tmp/' + dtsavepath + '.root')


      # A_eff / b_rms_eff distribution

      notes = ['Aeff_distribution', str(nb) + 'bins', str(scanned_events) + '_events_scanned', square_side + 'x' + square_side]

      Asavepath = ''
      Ah_title = ''

      for i,note in enumerate(notes):
            Asavepath += note 
            Ah_title += note
            if i < (len(notes) - 1):
                  Asavepath += '_' 
                  Ah_title += ', '  

      c = TCanvas()
      #h.SetStats(False)
      Ah.SetTitle(Ah_title)
      Ah.GetXaxis().SetTitle('time[MCP1 + CFD] - time[MCP2 + CFD]')
      Ah.GetYaxis().SetTitle('Events')
      #dth.GetYaxis().SetTitleOffset(1.5)
      Ah.SetFillColor(kBlue - 3)

      Ah.Draw()

      c.SaveAs('bin/tmp/' + Asavepath + '.pdf')
      Ah.SaveAs('bin/tmp/' + Asavepath + '.root')

      # Automatically open file
      os.system('evince ' + 'bin/tmp/' + savepath + '.pdf')

      #print'h = ',h

      ####

      h.SetDirectory(0)

      return h