from quick_plot_helper import quick_plot

color_to_use = ['tab:blue', 'tab:red']
threesoliddashed = ['dashed', 'dashed', 'dashed', 'solid', 'solid', 'solid', ]
all5v4 = ['Walker2d-v4', 'Humanoid-v4', 'Ant-v4', 'Hopper-v4', 'HalfCheetah-v4']

# this is a sample plot
quick_plot(
    ['SAC_no_reset', 'SAC_1_reset' ],
    [
        'reset_e1000_q2_uf1_pd20_nr0_ri100000',
        'reset_e1000_q2_uf1_pd20_nr1_ri100000',
    ],
    envs=all5v4,
    colors=color_to_use,
    linestyles=['solid','dashed'],
    save_name='SAC_with_reset',
    y_value=['AverageTestEpRet', 'AverageQ1Vals']
)



