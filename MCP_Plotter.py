# Plotter for MCP plots from H4Analysis reconstruction files 

# Import Modules
import os
from dtplotter import *
from amp_max_plotter import *
from res_plotter import *
from variable_dict import *
from dist_plot import *

gROOT.SetBatch(True) # Don't plot upon Draw command

# Run 
def main():
      #os.system('source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.12.06/x86_64-centos7-gcc48-opt/root/bin/thisroot.csh')

      vset = [] # variable set 

      # Get variable values from dictionary key 
      # command line: python MCP_Plotter.py key
      if len(sys.argv) == 2:
            vset = var_d(sys.argv[1])
            plot_type = vset[0]

      # Get variable values from command line 
      # command line: python MCP_Plotter.py plot_type var1 var2 var3 ... 
      else: 
            plot_type = sys.argv[1]

      if (plot_type == 'dist_plot'):
            print 'Making', str(vset[1]), '[', str(vset[2]), '] distribution plot'
            dist_plot(vset)

      if (plot_type == 'amp_max'):
            print 'Making highest amp_max plot'
            amp_max_plot(vset)

      if (plot_type == 'dt'):
            print 'Making dt plot'
            dt_plot(vset)
      
      if (plot_type == 'res'):
            print 'Making resolution plot'
            res_plot(vset) 

      print'Finished'

# If python is running this file 
if __name__ == '__main__':
      main()