from quick_plot_helper import quick_plot

twocolordoulbe = ['tab:blue', 'tab:orange', 'tab:blue', 'tab:orange',]
twosoliddashed = ['dashed', 'dashed',  'solid', 'solid', ]
threecolordoulbe = ['tab:blue', 'tab:orange', 'tab:red', 'tab:blue', 'tab:orange', 'tab:red']
threesoliddashed = ['dashed', 'dashed', 'dashed', 'solid', 'solid', 'solid', ]
standard_6_colors = ('tab:red', 'tab:orange', 'tab:blue', 'tab:brown', 'tab:pink','tab:grey')

envs = ['Hopper-v3', 'HalfCheetah-v3']
data_path = '../data/'

standard_ys = ['AverageTestEpRet', 'AverageQ1Vals', 'AverageNormQBias', 'StdNormQBias', 'Time']

plot_proj2 = True
if plot_proj2:
    quick_plot(
        [
         'SAC gamma 0.98', 'SAC gamma 0.99', 'SAC gamma 0.999'],
        [
            'exp_e300_q2_uf1_lr0.0003_g0.98_p0.995_ss5000_b64_h64',
            'exp_e300_q2_uf1_lr0.0003_g0.99_p0.995_ss5000_b64_h64',
            'exp_e300_q2_uf1_lr0.0003_g0.999_p0.995_ss5000_b64_h64',
        ],
        envs=envs,
        save_name='SAC_gamma',
        base_data_folder_path=data_path,
        y_value=standard_ys
    )

