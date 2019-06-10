from ROOT import *
#from math import *
from math import fabs,sqrt,floor,ceil
from array import array
import sys
import os

def dt_plot(vset):

      #gROOT.ProcessLine("TH1::AddDirectory(kFALSE)")
      #gROOT.ProcessLine("TH2::AddDirectory(kFALSE)")

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
            direc_path = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3ud_160_18/compiled_roots'
            dt_type = 'XTALs'
            side = 'up'
            combined_file = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3ud_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3up.root'
      elif element0 == 'C3' and element1 == 'C2':
            direc_path = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3ud_160_18/compiled_roots'
            dt_type = 'XTALs'
            side = 'down'
            combined_file = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3ud_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3down.root'
      elif element0 == 'C3' and element1 == 'B3':
            direc_path = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3lr_160_18/compiled_roots'
            dt_type = 'XTALs'
            side = 'left'
            combined_file = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3lr_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3left.root'
      elif element0 == 'C3' and element1 == 'D3':
            direc_path = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3lr_160_18/compiled_roots'
            dt_type = 'XTALs'
            side = 'right'
            combined_file = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3lr_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3right.root'
      else:
            direc_path = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3_160_18/compiled_roots'
            dt_type = 'XTALMCP'
            combined_file = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3_without13420.root'

      print'dt type = ',dt_type

      # Separate function for each type of plot? 

      # If not MCP/MCP, need files by energy to make energy dependent amplitude cuts
      if dt_type != 'MCPs':
            file_paths = []
            energies = ['50GeV','100GeV','150GeV','200GeV','250GeV']
            #sides= ['up','down','left','right']

            #for file in os.listdir(str(os.getcwd()) + '/' + str(file_directory)):
            print'direc_path = ',direc_path
            for file in os.listdir(direc_path): 
                  #print'file = ',os.path.join(file)
                  if '.root' in file:
                        for e in energies: 
                              #print'os.path.join(file).split("_")[5] = ',os.path.join(file).split('_')[5]
                              # If file is for a given energy, append to list 
                              if os.path.join(file).split('_')[5] == e:
                                    # Check for side if between two xtals 
                                    if dt_type == 'XTALs':
                                          #for s in sides:
                                          #print'os.path.join(file).split("_")[6][2:] = ',os.path.join(file).split('_')[6][2:]
                                          if os.path.join(file).split('_')[6][2:-5] == side:
                                                print '     Found File: ',os.path.join(file)
                                                file_paths.append(direc_path + '/' + os.path.join(file)) 
                                    elif dt_type == 'XTALMCP':
                                          print '     Found File: ',os.path.join(file)
                                          file_paths.append(direc_path + '/' + os.path.join(file)) 

      # If it's MCP/MCP or XTAL/XTAL 
      if dt_type == 'MCPs' or dt_type == 'XTALs':
            # Define variables for each element
            variables = ['fit_time','fit_ampl','b_rms']
            #for v in variables:
                  #for e in e_elements:
                        #exec('f  v' + '[' + )
            ft0 = "fit_time[" + element0 + "]"
            ft1 = "fit_time[" + element1 + "]"
            fa0 = "fit_ampl[" + element0 + "]"
            fa1 = "fit_ampl[" + element1 + "]"
            noise0 = "b_rms[" + element0 + "]"
            noise1 = "b_rms[" + element1 + "]"

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
            ft0 = "fit_time[" + element0 + "]"
            ft1 = "fit_time[" + element1 + "]"
            VC_ft = "fit_time[VFE_CLK]" # VFE Clock Fit time 
            fa0 = "fit_ampl[" + element0 + "]"
            fa1 = "fit_ampl[" + element1 + "]"
            noise0 = "b_rms[" + element0 + "]"
            noise1 = "b_rms[" + element1 + "]"

            # # For 160 MHz
            correction = 'int((' + ft0 + ' - ' + ft1 +  '+' +  VC_ft + ')/6.238)*6.238' 
            print'**Using 160 MHz correction**'

            # # For 120 MHz
            # correction = int((xtal_ft - MCP1_ft + VC_ft)/8.317)*8.317 

            xvar = fa0 
            yvar = ft0 + '-' + ft1 + '+' + VC_ft + '-' + correction

            print'yvar = ',yvar
            
            # yvar = ft0 + ' - ' + ft1
            #xvar = 'pow( 2 / ( (1/pow( ' + fa0 + '/' + noise0 + ', 2)) + (1/pow(' + fa1 + '/' + noise1 + ',2)) ) , 0.5)'      

      # Create Cut

      cuts = []

      # Assuming center is (x,y) = (-4,4)  
      cuts.append('( fabs(fitResult[0].x() + 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append('( fabs(fitResult[0].y() - 4) <= ' + str(float(square_side)/2) + ')') 
      cuts.append ('track_tree.n_tracks == 1')  

      if dt_type == 'MCPs':
            cuts.append('fit_ampl[' + element0 + '] > 125')
            cuts.append('fit_ampl[' + element1 + '] > 125')

      
      elif dt_type == 'XTALs':
            print'no cuts'
            # Need to make energy dependent amplitude cuts 
            # One option may be to create hiso for each energy file then merge 
            #cuts.append('fit_ampl[' + element0 + '] > 1000')
            #cuts.append('fit_ampl[' + element1 + '] > 1000')
            #cuts.append('fit_chi2[' + element0 + '] < 5')
            #cuts.append('fit_ampl[C3] > 4000')

      elif dt_type == 'XTALMCP':
            # Need energy dependent XTAL amplitude cuts 
            #cuts.append('fit_ampl[' + element0 + '] > 1000')
            cuts.append('fit_ampl[' + element1 + '] > 100 ')

      #cuts.append('( value >= ' + str(varmin) + ' )' )
      #cuts.append('( value <= ' + str(varmax) + ' )')

      cut = ''

      for i,c in enumerate(cuts):
            cut += c 
            if i < (len(cuts) - 1):
                  cut += ' && '  # Needs to be understood by ROOT   

      # Open combined file 
      #f = TFile.Open(combined_file)

      # Create Histogram

      #if dt_type == 'MCPs': 
            #h = TH2F('h','h',nb,0,600,300,4.5,5.3) 
      #elif dt_type == 'XTALs': 
            #h = TH2F('h','h',nb,0,1600,300,-2,2) 
     # elif dt_type == 'XTALMCP': 
            #h = TH2F('h','h',nb,0,10000,300,-30,30) 

      events_scanned = 0



      
            
      #hh = TH2F('hh','hh',nb,0,1600,300,-2,2) 
      # Need histogram creation after open file? 
      #hh = TH2F('hh','hh',nb,0,1600,300,-2,2) 
      
      # f = TFile.Open(file_paths[0])
      # hh = TH2F('hh','hh',nb,0,1600,300,-2,2) 
      # f.h4.Draw( yvar + ":" + xvar + " >> hh",cut)
      # #hh.GetZaxis().SetRangeUser(0,500)
      # hh.SetMinimum(0)
      # hh.SetMaximum(500)

      # f2 = TFile.Open(file_paths[1])
      # hh2 = TH2F('hh2','hh2',nb,0,1600,300,-2,2) 
      # f2.h4.Draw( yvar + ":" + xvar + " >> hh2",cut)
      # hh2.SetMinimum(0)
      # hh2.SetMaximum(500)

      # f3 = TFile.Open(file_paths[3])
      # hh3 = TH2F('hh3','hh3',nb,0,1600,300,-2,2) 
      # f3.h4.Draw( yvar + ":" + xvar + " >> hh3",cut)
      # #hh3.GetZaxis().SetRangeUser(0,500)

      # stacks = THStack("stacks","stacked_Histo")
      # stacks.Add(hh)
      # stacks.Add(hh2)
      # #stacks.Add(hh3)

      # c0 = TCanvas()

      # #stacks.GetZaxis().SetRangeUser(0,500)
      # stacks.Draw("COL1")  
      
      # c0.Update()
      # stacks.SetMaximum(500)
      # hist = stacks.GetHistogram()
      # #stacks.GetHistogram().GetZaxis().SetRangeUser(0,500)
      # #stacks.GetHistogram(1).SetZaxis().SetRangeUser(0,500)
      # #stacks.GetHistogram(2).SetZaxis().SetRangeUser(0,500)
      
      # c0.SaveAs('/eos/user/a/atishelm/www/test0.png')
      # hist.SaveAs('/eos/user/a/atishelm/www/test.root')

      # Stacked histogram
      #stacks = THStack("stacks","stacked_Histo")

      stacks = THStack("stacks","stacked_Histo")
      histos = []

      # Draw from file(s)
      if dt_type == 'MCPs':
            bins = array('d',[20 + x*(300. - 20.)/nb for x in range(0,nb - 1)])
            bins.append(300)
            bins.append(500)
            print'bins = ',bins
            h = TH2F('h','h',nb,bins,300,4.5,5.3) 
            f = TFile.Open(combined_file)
            h4 = f.Get("h4")
            htmp = TH2F('htmp','htmp',nb,bins,300,4.5,5.3) 
            events_scanned = h4.GetEntries()
            print'entries = ',events_scanned
            print'cut = ',cut
            h4.Draw( yvar + ":" + xvar + " >> htmp",cut)
            h.Add(htmp)
            f.Close()

            cc = TCanvas()
            h.Draw("COLZ1")
            cc.SaveAs('/eos/user/a/atishelm/www/test.png')


      elif dt_type != 'MCPs':
            
            #h = TH2F('h','h',nb,0,1600,300,-2,2) 
            #exit(0)
            #colors = ['kBlue','kRed','kGreen','kYellow','kCyan']
            colors = [kBlue,kRed,kGreen,kYellow,kCyan]
            energies = ['50GeV','100GeV','150GeV','200GeV','250GeV']
            if dt_type == 'XTALs':  
                  energy_cuts = ['100','300','500','1000','1500']
                  tb = [-2,2] # time bounds 
                  bins = array('d',[x*(1200./9.) for x in range(0,nb - 1)])
                  bins.append(1200)
                  bins.append(1600)
                  print'bins = ',bins
                  h = TH2F('h','h',nb,bins,300,tb[0],tb[1])
            if dt_type == 'XTALMCP':  
                  energy_cuts = ['1200','2200','3100','4100','6000']
                  tb = [4,6]
                  #bins = array('d',[x*(1300./9.) for x in range(0,9)])
                  bins = array('d',[0 + 1200*x for x in range(0,11)])
                  #bins.append(1300)
                  #bins.append(1600)
                  print'bins = ',bins
                  h = TH2F('h','h',nb,bins,300,tb[0],tb[1])

            for i,fp in enumerate(file_paths):
                  energy = os.path.join(fp).split('/')[-1].split('_')[5]
                  print'energy = ',energy
                  #cfs = "f" + str(i) # Current File String
                  #exec(cfs + "= TFile.Open(fp)")
                  f = TFile.Open(fp)
                  h4 = f.Get("h4")
                  htmp = TH2F('htmp','h',nb,bins,300,tb[0],tb[1]) # needs to match
                  #htmp2 = TH1F()
                  #events_scanned += eval(cfs).h4.GetEntries()
                  events_scanned += h4.GetEntries()
                  print'events_scanned = ',events_scanned
                  # Check energy, add energy dependent amplitude cut 
                  for j,e in enumerate(energies):
                        if energy == e:
                              if i != 0:
                              # remove previous file amp cut
                                    cut = cut[:-prev_length]
                              if dt_type == 'XTALs':
                                    added_cut = '&& fit_ampl[' + element0 + '] > ' + energy_cuts[j] + ' && fit_ampl[' + element1 + '] > ' + energy_cuts[j]
                              elif dt_type == 'XTALMCP':
                                    added_cut = '&& fit_ampl[' + element0 + '] > ' + energy_cuts[j]
                              cut += added_cut
                              prev_length = len(added_cut)
                              #print'cut = ',cut
                              #print'hello'
                  #chs = "h" + str(i) # Current histogram string 
                  #exec(chs + "= TH2F('h" + str(i) +"','h" + str(i) + "',nb,0,1600,300,-2,2)") 
                  #eval(cfs).h4.Draw( yvar + ":" + xvar + " >> +h" + str(i),cut)
                  h4.Draw( yvar + ":" + xvar + " >>htmp",cut)
                  h.Add(htmp)
                  f.Close()
                  #h = TH2F('h','h',nb,0,1600,300,-2,2) 
                  #eval(cfs).h4.Draw(yvar + ":" + xvar + " >> +h",cut)
                  # if i == 0:
                  #       #h = TH2F('h','h',nb,0,1600,300,-2,2)  
                  #       #eval(cfs).h4.Draw(yvar + ":" + xvar + " >> h",cut)
                  #       f.h4.Draw(yvar + ":" + xvar + " >> h",cut)

                  #       cc = TCanvas()
                  #       h.Draw("COLZ1")
                  #       cc.SaveAs('/eos/user/a/atishelm/www/plots/test' + str(i) + '.png')

                  #else: #eval(cfs).h4.Draw(yvar + ":" + xvar + " >> +h",cut)
                  #f.h4.Draw(yvar + ":" + xvar + " >> h" + str(i),cut)
                  #cc = TCanvas()
                  #eval(chs).Draw("COLZ1")
                  #cc.SaveAs('/eos/user/a/atishelm/www/plots/test' + str(i) + '.png')
                  #eval(chs).SetFillColor(colors[i])
                  #histos.append(eval(chs))
                  #stacks.Add(hh)

                  #if i == 1: break 

            cc = TCanvas()
            h.Draw("COLZ1")

            # Open combined file and get average MCP sigma per bin 
            if dt_type == 'XTALMCP':
                  mcp_avgs = []
                  f = TFile.Open(combined_file)
                  h4 = f.Get("h4")
                  mcp_a = "fit_ampl[MCP1]/b_rms[MCP1]"
                  #new_y = "1000*sqrt((1.44/(" + mcp_a + "))^2 + (0.01512)^2)/(sqrt(2))"
                  new_y = "sqrt((1.44/(" + mcp_a + "))^2 + (0.01512)^2)/(sqrt(2))"
                  #new_y = "fit_ampl[MCP1]"
                  #mcpcut = ''
                  htmp2 = TH1F('htmp2','htmp2',100,0,10000)
                  for i in range(0,len(bins) - 1):
                        print'i = ',i 
                        
                        # remove previous file amp cut
                        cut = cut[:-prev_length]
                        added_cut = '&& fit_ampl[' + element0 + '] > ' + str(bins[i]) + '&& fit_ampl[' + element0 + '] < ' + str(bins[i + 1])
                        cut += added_cut
                        prev_length = len(added_cut)
                        print'cut = ',cut

                        
                        #htmp2.SetName('htmp2')
                        # Amp cut 
                        
                        
                        h4.Draw(new_y + " >> htmp2",cut)
                        mean = htmp2.GetMean()
                        mcp_avgs.append(mean)
                        print'mean = ',mean
                  

            #cc.SaveAs('/eos/user/a/atishelm/www/plots/test.png')

      print'avgs = ',mcp_avgs
      # For each bin, Get average MCP sigma 

      # print'histos = ',histos
      # for hist in histos:
      #       stacks.Add(hist)

      # #c0 = TCanvas()
      # stacks.Draw()  
      # #h = TH2F()
      # h = stacks.GetHistogram()
      
      #c0.Update()
      #stacks.SetMaximum(500)
      #hist = stacks.GetHistogram()
      #stacks.GetHistogram().GetZaxis().SetRangeUser(0,500)
      #stacks.GetHistogram(1).SetZaxis().SetRangeUser(0,500)
      #stacks.GetHistogram(2).SetZaxis().SetRangeUser(0,500)
      
      #c0.SaveAs('/eos/user/a/atishelm/www/test12.png')
      #hh = stacks.GetHistogram()

      #hh.Draw()
      #hh.SaveAs('/eos/user/a/atishelm/www/test12.root')

      #hist.SaveAs('/eos/user/a/atishelm/www/test.root')

      

      #h.SetDirectory(0)

      #c0 = TCanvas()

      #stacks.Draw("COLZ1")  
      #c0.SaveAs('/eos/user/a/atishelm/www/test.png')

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

      
      #c0 = TCanvas()
      
      
      #c0.Update()
      #stacks.SetMaximum(500)
      #hist = stacks.GetHistogram()
      #stacks.GetHistogram().GetZaxis().SetRangeUser(0,500)
      #stacks.GetHistogram(1).SetZaxis().SetRangeUser(0,500)
      #stacks.GetHistogram(2).SetZaxis().SetRangeUser(0,500)
      
      #c0.SaveAs('/eos/user/a/atishelm/www/test11.png')

      # Plot
      #c = TCanvas()

      #c = TCanvas()
      #h = TH2F()
      #print'histos = ',histos

      #h0.Draw("COLZ1")
      #c.SaveAs("test.png")

      # ii = 0
      # for hist in histos:
      #       c = TCanvas()
      #       h.Add(hist)
      #       h.Draw("COLZ1")
      #       c.SaveAs("test" + str(i) + ".png")
      #       #stacks.Add(hist)
      #       #ii += 1
      
      #h.Draw("COLZ1")
      #c.SaveAs("test.png")

      #h.Add()

      #c0 = TCanvas()
      
      #stacks.Draw("A")  
      #h = stacks
      #h = TH2F()
      #c = TCanvas()
      #h = stacks.GetHistogram()

      c0 = TCanvas()
      #h.SetDirectory(0)
      #stacks.Draw()
      #stacks.Draw("ACOL1")  
      #h = stacks.GetHistogram()
      #h.SaveAs("test.root")
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
      #h.Draw("COLZ1")

      #c.SaveAs('/eos/user/a/atishelm/www/' + savepath + '.png')
      #h.SaveAs('/eos/user/a/atishelm/www/plots/' + savepath + '.root')

      #h.SaveAs('/eos/user/a/atishelm/www/' + savepath + '.root')

      # Automatically open file
      #os.system('root -l /eos/user/a/atishelm/www/' + savepath + '.root')

      #print'h = ',h

      ####

      #print'h = ',h

      h.Draw("COLZ1")
      c0.SaveAs('/eos/user/a/atishelm/www/' + savepath + '.png')
      #c0.SaveAs('/eos/user/a/atishelm/www/' + savepath + '.jpg')
      h.SaveAs('/eos/user/a/atishelm/www/' + savepath + '.root')

      h.SetDirectory(0)

      #print'h = ',h
      # Want to also return a list of average MCP sigma t's obtained from plugging aeff/brms value into mcp fit function 
      # take average, subtract in quadrature from uncorrected sigma 

      

      return h, mcp_avgs, events_scanned, dt_type