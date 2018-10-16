# Simple plotter for MCP plots from H4 Root files 

from ROOT import *
from math import fabs
import sys
import os

gROOT.SetBatch(True) # Don't plot upon Draw command

def main():
      os.system('source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.12.06/x86_64-centos7-gcc48-opt/root/bin/thisroot.csh')
      hodo_plot()

#def dist():
      #h1 = TH1F('h1','h1',0,5000)

def hodo_plot():
      # electronics element 
      element = sys.argv[2] # MCP 1 or 2
      square_side = str(2*int(sys.argv[3]))

      max_events = int(sys.argv[1])
      file_paths = []
      file_directory = '160_9_Oct/reco_roots'

      for file in os.listdir(str(os.getcwd()) + '/' + str(file_directory)):
            #if file.endswith(".root"):
            #if 'EC_' in file:
            if '.root' in file:
            #print '	Found File: ',os.path.join(file)
                  file_paths.append(str(file_directory) + '/' + os.path.join(file)) 

      h = TH2F('h','h',50,-25,25,50,-25,25)
      h2 = TH1F('h2','h2',50,0,5000)
      #f = TFile.Open("160_9_Oct/reco_roots/ECAL_H4_Oct2018_13220.root")
      #print sys.argv[1]
      cut = '(fabs(hodox + 4) < ' + square_side + ') and (fabs(hodoy - 4) < ' + square_side + ') and MCP_amp_max < 10000'
      
      #trees = [hodo, digi, wf, info, h4]

      #for tree in trees:
            #print f.tree.Print()

      scanned_events = 0

      for path in file_paths:

            print 'Reading File: ',path
            event_i = 0

            f = TFile.Open(path)
            total_num_events = f.h4.GetEntries()
            if int(max_events) == -1:
                  scanned_events += total_num_events
            print 'total num events = ', total_num_events

            for event in f.h4:

                  hodox = event.X[0]
                  hodoy = event.Y[0]
                  if element == 'MCP1':       MCP = f.digi.MCP1
                  if element == 'MCP2':       MCP = f.digi.MCP2
                  MCP_amp_max = event.amp_max[MCP]

                  #MCP1 = f.digi.MCP1
                  #MCP2 = f.digi.MCP2
                  #MCP1_amp_max = event.amp_max[MCP1]
                  #MCP2_amp_max = event.amp_max[MCP2]

                  xbin = h.GetXaxis().FindBin(hodox)
                  ybin = h.GetYaxis().FindBin(hodoy)

                  verbose = True

                  # Add to dist
                  if eval(cut):
                        h2.Fill(MCP_amp_max)

                  #if eval(cut) and (MCP1_amp_max > h.GetBinContent(xbin,ybin)): # Place higheset value in bin 
                  if eval(cut) and (MCP_amp_max > h.GetBinContent(xbin,ybin)): # Place higheset value in bin 
                        #h.Fill(hodox,hodoy,MCP1_amp_max)
                        h.Fill(hodox,hodoy,MCP_amp_max)

                  event_i += 1
                  percentage = float(event_i) / float(total_num_events)
                  if (event_i%10000 == 0): print 'Reading Event ',event_i
                  #if (int(percentage)%25 == 0):
                  #      print percentage*100,' percent Read '
                  
                  if event_i == max_events:
                        print 'Max desired events reached'
                        scanned_events += event_i
                        break

      c = TCanvas()
      h.SetStats(False)
      h2.SetStats(False)

      h.GetXaxis().SetTitle('hodoscope X (mm)')
      h.GetYaxis().SetTitle('hodoscope Y (mm)')

      h2.GetXaxis().SetTitle('amp_max (ADC)')
      h2.GetYaxis().SetTitle('Events')

      h_title = element + ' amp_max, ' + str(scanned_events) + ' Events Scanned, ' + square_side + 'x' + square_side + 'mm window around (-4, +4)' 
      h2_title = element + ' amp_max, ' + str(scanned_events) + ' Events Scanned, ' + square_side + 'x' + square_side + 'mm window around (-4, +4)' 

      h.SetTitle(h_title)
      h.Draw("COLZ1")

      h2.SetTitle(h2_title)


      savepath = 'bin/' + element + 'plot_.pdf'
      savepath2 = 'bin/' + element + '_dist_plot.pdf'

      c.SaveAs(savepath)

      c2 = TCanvas()
      h2.SetFillColor(kBlue - 3)
      h2.Draw()

      c2.SaveAs(savepath2)

      os.system('evince ' + savepath2)

if __name__ == '__main__':
      main()