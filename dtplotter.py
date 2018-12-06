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
            direc_path = vset[1]
            square_side = vset[2]
            A1mincut = vset[3]
            A2mincut = vset[4]
            nb = int(vset[5]) # number of bins 
            max_events = int(vset[6])
            x_min = float(vset[7])
            q_min = float(vset[8])
            XTAL_str = vset[9]
            note = vset[10]

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
      #x_max = 600.
      x_max = 12000
      
      tf = TFile.Open(file_paths[0])
      tree = tf.Get('h4')

      Aeff = "pow( 2 / ( (1/pow(amp_max[MCP1]/b_rms[MCP1], 2)) + (1/pow(amp_max[MCP2]/b_rms[MCP2],2)) ) , 0.5)"   

      cut = ''

      if (float(q_min) > 0):

            ## Hybrid quantile method. Uses fixed width bins up to aeff_min_quant, then quantiles above that
            aeff_min_quant = q_min
            #aeff_min_quant = 350                                                                           # The Aeff value above which quantiles are used
            aeff_tmp       = TH1F('aeff',"", 100, aeff_min_quant, x_max)
            tree.Draw(Aeff+'>>aeff', cut)                                         # Creates a temporary histogram to find the quantiles
            #tree.Draw('hhh', cut) 
            #nquants   = int(ceil(nb/2.)+1)          
            nquants   = int(ceil(nb/2.)+1) - 2                                                                 # n_quantiles = nbins / 2 + 1 (round up if odd)
            probs     = array('d', [x/(nquants-1.) for x in range(0, nquants)])                                 # Quantile proportions array
            quantiles = array('d', [0 for x in range(0, nquants)])                                              # Bin edges, initialized as all 0's
            aeff_tmp.GetQuantiles(nquants, quantiles, probs)                                                    # Overwrites 'quantiles' with bin edges positions
            #nfixed_bins    = int(floor(nb/2.))   
            nfixed_bins    = int(floor(nb/2.)) + 2                                                                      # n_fixed_bins = nbins/2 + 1 (round down if odd)
            fixed_bin_size = (aeff_min_quant-x_min)/nfixed_bins              
            bins = array('d', [fixed_bin_size*n + x_min for n in range(nfixed_bins)]) + quantiles    
            #bins = array('d', [fixed_bin_size*n + x_min for n in range(nfixed_bins)]) + quantiles                       # Fixed width bins up to aeff_min_quant, then uses quantiles
            #hh   = TH2F('hh', self.file_title+'_dt_vs_aeff_heatmap', p[2], bins, p[5], p[6], p[7])             # Return a TH2F with quantile binning

            print'bins = ',bins
            #h = TH2F('h','h',nb,bins,400,-5.4,-4.4) # With quantile
            h = TH2F('h','h',nb,bins,1600,0,4) # With quantile

      else:   
            bins = array('d', [0,3000,6000,8000,10000,12000])   
            #h = TH2F('h','h',nb,x_min,x_max,400,-5.4,-4.4) # Without quantile 
            #h = TH2F('h','h',nb,bins,1200,0,4) # Without quantile 
            h = TH2F('h','h',5,bins,1200,0,4) # Without quantile, with bins array
            #h = TH2F('h','h',nb,x_min,x_max,1200,0,4)
      #h = TH2F('h','h',nb,x_min,x_max,400,-5.4,-4.4) # Without quantile 

      #print'h = ',h
      #print'bins = ',bins

      dth = TH1F('dth','dth',1600,0,4)
      Ah = TH1F('Ah','Ah',100,0,10000)

      # Histograms for testing
      corr_good = TH1F('cg','cg',1000,500,600)
      corr_bad = TH1F('cb','cb',1000,500,600)


      # Create Cuts 
      cuts = []

      # Add ntracks == 1

      cuts.append('( fabs(hodox + 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append('( fabs(hodoy - 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append('( A1 > ' + A1mincut + ' )' )
      cuts.append('( time_maximum > 500 )' ) # Adding by hand to keep only one peak of times. Otherwise dt is off 
      #cuts.append('( A1 < 10000 )') # Check overflow bin? 
      #cuts.append('( A2 > ' + A2mincut + ' )' )
      cuts.append ('ntracks == 1')
      cuts.append( 'xtal_ft-int(xtal_ft/6.238)*6.238 < 1.5' ) # phase cut for now. This is for 160 MHz. 
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

      e_emp = 0

      for path in file_paths:

            if verbose: print 'Reading File ' + str(file_i) + '/' + str(len(file_paths)) + ': ',path
            event_i = 0
            tmp_perc = 1000

            f = TFile.Open(path)
            total_num_events = f.h4.GetEntries()

            #tfile    = TFile(self.file)
            infotree = f.Get("info")
            infotree.GetEntry(0)
            energy = infotree.Energy

            print'energy = ',energy 

            amp_cut = 0

            if (energy - 20.) < 50 < (energy + 20): amp_cut = 1000.
            if (energy - 20.) < 100 < (energy + 20): amp_cut = 2000.
            if (energy - 20.) < 150 < (energy + 20): amp_cut = 4000. # 6000 ?
            if (energy - 20.) < 200 < (energy + 20): amp_cut = 4500. # 8000 ?
            if (energy - 20.) < 250 < (energy + 20): amp_cut = 6000. # 8500 ?
            if (energy == 0):
                  print'energy = 0'
                  run_num = path.split('.')[-2].split('_')[-1]
                  print'run number = ',run_num
                  if run_num == '13267': amp_cut = 1000.
                  if run_num == '13266': amp_cut = 1000.
                  if run_num == '13232': amp_cut = 4500.
                  if run_num == '13231': amp_cut = 4500.

            print'amp_cut = ',amp_cut 
            # If not the first scanned file
            if file_i != 1:
                  # remove previous file amp cut
                  cut = cut[:-25]

            # Add current file amp cut
            cut += ' and A2 > float(amp_cut) '

            #print'cut = ',cut

            #for i in f.h4:
                  #print'i = ',i
            if int(max_events) == -1:
                  scanned_events += total_num_events
            if verbose: print 'total num events = ', total_num_events

            # May want to add something faster than going event by event. Just a way to add all events with tchain or something then draw. Is there a benefit to doing event by event? 

            for event in f.h4:

                  val = event.fitResult
                  val_l = len(val)
                  #print'val = ',val
                  #print'len(val) = ',len(val)

                  if val_l == 0:
                        #print'No x fit result value, skipping event' 
                        e_emp += 1
                        continue

                  # Define variables 

                  MCP1 = eval('f.digi.MCP1')
                  MCP2 = eval('f.digi.MCP2')
                  CFD = eval('f.digi.CFD')
                  VFE_CLK = eval('f.digi.VFE_CLK')
                  CLK = eval('f.digi.CLK')

                  #hodox = float(eval(f.track_tree.fitResult[0].x()))
                  #hodoy = float(eval(f.track_tree.fitResult[0].x()))
                  
                  #A1 = float(event.amp_max[MCP1])
                  #A2 = float(event.amp_max[MCP2])
                  A1 = float(event.fit_ampl[MCP1])
                  A2 = float(event.fit_ampl[MCP2])
                  #A2 = float(event.fit_ampl[])

                  brms1 = float(event.b_rms[MCP1])
                  brms2 = float(event.b_rms[MCP2])

                  #hodox = event.X[0]
                  #hodoy = event.Y[0]

                  #print'bool = ',bool(event.fitResult[0].x())

                  hodox = event.fitResult[0].x() # new x and y positions
                  hodoy = event.fitResult[0].y() 
                  ntracks = int(eval('f.track_tree.n_tracks'))

                  #print'hodox = ',hodox
                  #print'hodoy = ',hodoy

                  if(XTAL_str == 'MCP'): 

                        t1 = float(event.fit_time[MCP1])
                        t2 = float(event.fit_time[MCP2])

                        dt = t2 - t1
                        #print'dt = ',dt

                  else: 
                        XTAL = eval('f.digi.' + XTAL_str)
                        A2 = float(event.fit_ampl[XTAL])
                        brms2 = float(event.b_rms[XTAL])

                        time_maximum = float(event.time_maximum[XTAL])
                        #print'time max = ',time_maximum 

                        #A2eff = A2 / brms2 # ? 

                        xtal_ft = float(event.fit_time[XTAL])
                        MCP1_ft = float(event.fit_time[MCP1])
                        VC_ft = float(event.fit_time[VFE_CLK])

                        # 160 MHz
                        #print'xtal_ft = ',xtal_ft
                        #print'MCP1_ft = ',MCP1_ft
                        #print'VC_ft = ',VC_ft
                        correction = int((xtal_ft - MCP1_ft + VC_ft)/6.238)*6.238 

                        dt = xtal_ft - MCP1_ft + VC_ft - correction #int((xtal_ft - MCP1_ft + VC_ft)/6.238)*6.238 

                        # 120 MHz
                        #dt = xtal_ft - MCP1_ft + VC_ft - int((xtal_ft - MCP1_ft + VC_ft)/8.317)*8.317 
                        #print'dt = ',dt


                  #A_eff = sqrt( 2 / ( (A1/brms1)**(-2) + (A2/brms2)**(-2) ) )
                  # Fill h
                  #if eval(cut) and A1 != -0.0 and A2 != -0.0:
                  #if eval(cut) and A1 != -0.0 and A2 != -0.0 and A1 > 20 and A2 > 20:
                  #print'A1 = ',A1
                  #print'A2 = ',A2
                  #print'cut = ',cut
                  if eval(cut) and A1 != -0.0 and A2 != -0.0:
                        entries += 1
                        #A_eff = sqrt( 2 / ( (A1/brms1)**(-2) + (A2/brms2)**(-2) ) )
                        #print'A2 = ',A2
                        if (dt < 2):
                              print'dt = ',dt
                              print'correction = ',correction
                              corr_bad.Fill(correction)
                              # print'time_maximum = ',time_maximum
                              # print'fit_ampl[C3] = ',xtal_ft
                              # print'MCP1_ft = ',MCP1_ft
                              # print'VC_ft = ',VC_ft
                              #print'A2 = ',A2
                              #print'A2eff = ',A2eff
                        else:
                              corr_good.Fill(correction)
                        h.Fill(A2,dt)
                        Ah.Fill(A2) 
                        dth.Fill(dt)

                        #print'dt = ',dt
                        #print'A_eff = ',A_eff

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

      qinfo = str(q_min)
      if qinfo == '0.0':
            qinfo = 'NoQuant'
      else:
            qinfo = 'Qstart_' + str("{0:.0f}".format(q_min))

      #path_notes = []
      notes = ['dt_vs_Aeffo_brmseff', str(nb) + 'bins', qinfo, str(scanned_events) + '_events_scanned', square_side + 'x' + square_side]

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
      if(XTAL_str == 'MCP'): h.GetXaxis().SetTitle('(amp_eff_MCP1_MCP2) / b_rms_eff')
      else: h.GetXaxis().SetTitle('fit_ampl[' + XTAL_str + ']')
      if(XTAL_str == 'MCP'): h.GetYaxis().SetTitle('time[MCP1 + CFD] - time[MCP2 + CFD]')
      else: h.GetYaxis().SetTitle('fit_time[' + XTAL_str + '] - fit_time[MCP1] + fit_time[VFE_CLK] - correction')
      h.GetYaxis().SetTitleOffset(1.35)

      h.Draw("COLZ1")

      c.SaveAs('bin/tmp/' + savepath + '.pdf')
      c.SaveAs('bin/tmp/' + savepath + '.png')
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
      if(XTAL_str == 'MCP'): dth.GetXaxis().SetTitle('fit_time[MCP1] - fit_time[MCP2]')
      else: dth.GetXaxis().SetTitle('fit_time[' + XTAL_str + '] - fit_time[MCP1] + fit_time[VFE_CLK] - correction')
      dth.GetYaxis().SetTitle('Events')
      dth.GetYaxis().SetTitleOffset(1.4)
      dth.SetFillColor(kBlue - 3)

      dth.Draw()

      c.SaveAs('bin/tmp/' + dtsavepath + '.pdf')
      c.SaveAs('bin/tmp/' + dtsavepath + '.png')
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
      if(XTAL_str == 'MCP'): Ah.GetXaxis().SetTitle('(amp_eff_MCP1_MCP2) / b_rms_eff')
      else: Ah.GetXaxis().SetTitle('fit_ampl[' + XTAL_str + ']')
      Ah.GetYaxis().SetTitle('Events')
      Ah.GetYaxis().SetTitleOffset(1.4)
      Ah.SetFillColor(kBlue - 3)

      Ah.Draw()

      c.SaveAs('bin/tmp/' + Asavepath + '.pdf')
      c.SaveAs('bin/tmp/' + Asavepath + '.png')
      Ah.SaveAs('bin/tmp/' + Asavepath + '.root')

      # Automatically open file
      os.system('evince ' + 'bin/tmp/' + savepath + '.pdf')

      ccc = TCanvas()
      corr_good.Draw()
      ccc.SaveAs('corr_good.png')

      cccc = TCanvas()
      corr_bad.Draw()
      cccc.SaveAs('corr_bad.png')

      #print'h = ',h

      ####

      h.SetDirectory(0)

      return h, scanned_events