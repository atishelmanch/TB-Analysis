def var_d(key):

    # Define variable dictionary 
    vd = {
        "max_ampmax_v1": ['amp_max','MCP1', 'all_data', '10', '0','10000','-1','ampmax_v1'],
        "noise_dist": ['dist_plot', 'b_rms', 'MCP2', 'all_data', '3', '0','35','75','-1','noise_dist_v1'], 
        "amp_max_dist": ['dist_plot', 'amp_max', 'MCP2', 'all_data', '3', '0','5000','250','-1','amp_max_dist_v1'], 
        "t_dist": ['dist_plot', 'time', 'MCP1 + CFD', 'all_data', '3', '0','1000','500','1000','noise_dist_v1'], 
        "dt_v1": ['dt','H4Analysis/ntuples_2Nov_screen_test', '3', '100','100','100','100','35','MCP','dt_v1'], # If want MCP1 and MCP2, enter MCP
        "res_v1": ['res', 'H4Analysis/ntuples_2Nov_screen_test', '3', '100','100','15','-1','35','MCP','res_v1'], # same as dt but afterwards makes sigma vs. Aeff plot 
    }
    # Choose variable set key 
    vs = vd[key]

    return vs 