# Plotter for MCP plots from H4Analysis reconstruction files 

# Types of plots I want:
# amp_max distribution
# highest amp_max(X,Y)
# dt vs. amp_eff_MCP1_MCP2
# sigma vs. amp_eff (with b_rms)

# Command line arguments
# python plot.py direc_path element square_side/2 note amp_max_min amp_max_max max_events

# Import Modules
# from ROOT import *
# from math import fabs,sqrt
# import sys
import os
from dtplotter import *
from amp_max_plotter import *
from res_plotter import *
from variable_dict import *

gROOT.SetBatch(True) # Don't plot upon Draw command

# Run 
def main():
      #os.system('source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.12.06/x86_64-centos7-gcc48-opt/root/bin/thisroot.csh')
      #plot_type = sys.argv[1]

      vset = [] # variables set 

      # Get variables from dictionary key 
      if len(sys.argv) == 2: # command line: python MCP_Plotter.py key
            vset = var_d(sys.argv[1])
            plot_type = vset[0]

      # Get variables from command line 
      else: 
            plot_type = sys.argv[1]

      if (plot_type == 'amp_max'):
            print 'Making amp_max plots'
            amp_max_plot(vset)

      if (plot_type == 'dt'):
            print 'Making dt plot'
            dt_plot(vset)
      
      if (plot_type == 'res'):
            print 'Making resolution plot'
            res_plot(vset) # vs (variables) needs to contain dt vars 


      print'Finished'

# If python is running this file 
if __name__ == '__main__':
      main()