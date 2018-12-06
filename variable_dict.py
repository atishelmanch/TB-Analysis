def var_d(key):

    # Data folder path 
    #folder = 'H4Analysis/good_ntuples'
    #folder = 'H4Analysis/ntuples'
    #folder = 'H4Analysis/ntuples_25NovC3_MaxEvents'
    #folder = 'H4Analysis/ntuples_27NovC3'
    #folder = 'ntuples_C3'
    folder = 'ntuples_C3_OnePerEnergy'

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
        "dt_v4": ['dt',folder, '3', '150','500','1000','500','0','-1','C3','dt_v4'], # If want MCP1 and MCP2, enter MCP
        #"res_v1": ['res', folder, '3', '100','100','15','-1','30','425','MCP','res_v1'], # same as dt but afterwards makes sigma vs. Aeff plot 
        "res_v1": ['res', folder, '3', '100','100','15','-1','30','425','MCP','res_v1'], # same as dt but afterwards makes sigma vs. Aeff plot 
        "res_v2": ['res',folder, '3', '150','500','1000','10000','0','-1','C3','dt_v4'], # If want MCP1 and MCP2, enter MCP
        "res_v3": ['res',folder, '3', '150','500','1000','5000','0','-1','C3','dt_v4'], # If want MCP1 and MCP2, enter MCP
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