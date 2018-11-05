def var_d(key):

    folder = 'H4Analysis/ntuples_2Nov_screen_test'
    # Define variable dictionary 
    vd = {
        "max_ampmax_v1": ['amp_max','MCP1', folder, '20', '0','10000','500','ampmax_v1'],
        "noise_dist": ['dist_plot', 'b_rms', 'MCP2', folder, '3', '0','30','60','5000','noise_dist_v1'], 
        "amp_max_dist": ['dist_plot', 'amp_max', 'MCP1', folder, '3', '0','2000','500','5000','noise_dist_v1'], 
        #"amp_max_dist": ['dist_plot', 'amp_max', 'MCP2', 'all_data', '3', '0','5000','250','-1','amp_max_dist_v1'], 
        "t_dist": ['dist_plot', 'time', 'MCP1 + CFD', 'all_data', '3', '0','1000','500','1000','noise_dist_v1'], 
        "dt_v1": ['dt','H4Analysis/ntuples_2Nov_screen_test', '3', '100','100','100','100','35','400','MCP','dt_v1'], # If want MCP1 and MCP2, enter MCP
        "res_v1": ['res', 'H4Analysis/ntuples_2Nov_screen_test', '3', '100','100','10','1000','30','400','MCP','res_v1'], # same as dt but afterwards makes sigma vs. Aeff plot # 
    }
    # Choose variable set key 
    vs = vd[key]

    return vs 

    # direc_path = vset[1]
    # square_side = vset[2]
    # A1mincut = vset[3]
    # A2mincut = vset[4]
    # nb = int(vset[5]) # number of bins 
    # max_events = int(vset[6])
    # x_min = float(vset[7])
    # q_min = float(vset[8])
    # XTAL_str = vset[9]
    # note = vset[10]