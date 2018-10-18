def var_d(key):

    # Define variable dictionary 
    vd = {
        "ampmax_v1": ['amp_max','MCP1', 'all_data', '1.5', '150','150','10','ampmax_v1'],
        "dt_v1": ['dt','all_data', '1.5', '150','150', '10', '20','dt_v1'],
        "res_v1": ['res', 'all_data', '1.5', '150','150','10','2000', 'res_v1'], # same as dt but afterwards makes signma vs. Aeff plot 
    }

    vs = vd[key]

    return vs # variable set 