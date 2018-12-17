def var_d(key):

    # Data folder path 
    #folder = 'H4Analysis/good_ntuples'
    #folder = 'H4Analysis/ntuples'
    #folder = 'H4Analysis/ntuples_25NovC3_MaxEvents'
    #folder = 'H4Analysis/ntuples_27NovC3'
    #folder = 'ntuples_C3'
    #folder = 'ntuples_C3_OnePerEnergy'
    #folder = 'ntuples_v1'
    folder = '/afs/cern.ch/work/m/mplesser/public/new_matrix_recos/C3_160_18'
    
    # Root file combining desired runs 
    combined_file = '/eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3_without13420.root'

    # Other Combined Files:

    # /eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3ud_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3down.root
    # /eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3ud_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3up.root
    # /eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3lr_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3left.root
    # /eos/user/m/mplesser/matrix_time_analysis_recos/ntuples_C3lr_160_18/compiled_roots/ECAL_H4_Oct2018_160MHz_18deg_compiled_C3right.root


    # Define variable dictionary 
    vd = {
        "highest_ampmax": ['amp_max','MCP2', folder, '20', '0','10000','-1','ampmax_v1'],
        "noise_dist": ['dist_plot', 'b_rms', 'MCP2', folder, '3', '200','0','25','-1','noise_dist_v1'], 
        "amp_max_dist": ['dist_plot', 'amp_max', 'MCP2', folder, '3', '200','0','3000','-1','noise_dist_v1'], 
        "t_dist": ['dist_plot', 'time', 'MCP1 + CFD', 'all_data', '3', '0','1000','500','1000','noise_dist_v1'], 
        #"dt": ['dt',folder, '3', '0','0','1000','-1','0','400','MCP','dt_v1'], # If want MCP1 and MCP2, enter MCP
        "dt_v1": ['dt',folder, '3', '0','0','1000','-1','0','400','MCP','dt_v1'], # If want MCP1 and MCP2, enter MCP
        "dt_v2": ['dt',folder, '3', '0','0','1000','-1','0','400','MCP','dt_v1'], # If want MCP1 and MCP2, enter MCP
        "dt_v3": ['dt',folder, '3', '0','0','1000','-1','0','-1','C3','dt_v3'], # If want MCP1 and MCP2, enter MCP
        "dt_v4": ['dt',folder, '3', '250','500','50','5000','0','-1','C3','dt_v4'], # If want MCP1 and MCP2, enter MCP
        #"res_v1": ['res', folder, '3', '100','100','15','-1','30','425','MCP','res_v1'], # same as dt but afterwards makes sigma vs. Aeff plot 
        "res_v1": ['res', folder, '3', '100','100','15','-1','30','425','MCP','res_v1'], # same as dt but afterwards makes sigma vs. Aeff plot 
        "res_v2": ['res',folder, '3', '150','500','1000','10000','0','-1','C3','dt_v4'], # If want MCP1 and MCP2, enter MCP
        "res_v3": ['res',folder, '3', '200','500','1000','10000','0','-1','C3','dt_v4'], # If want MCP1 and MCP2, enter MCP
        "MCP12_res": ['res',folder, '3', '200','200','10','-1','40','-1','MCP','MCP12_res'], # If want MCP1 and MCP2, enter MCP
        "cc": ['2d','t,R','MCP2,MCP2',folder,'10','-1','3','cc'], # Calibration Curves
        "MCP_res": ['res',combined_file,'MCP1,MCP2','3','10'],
        "C3u_res": ['res',combined_file,'C3,C4','3','10'],
        "C3MCP_res": ['res',combined_file,'C3,MCP1','3','10']

    }
    # Choose variable set key 
    vs = vd[key]

    return vs 

    # Res/dt:
    #
    # direc_path = vset[1]
    # square_side = vset[2]
    # A1mincut = vset[3]
    # A2mincut = vset[4]
    # nb = int(vset[5]) # number of bins 
    # max_events = int(vset[6])
    # x_min = float(vset[7])
    # q_min = float(vset[8]) make negative for no quantile
    # XTAL_str = vset[9]
    # note = vset[10]