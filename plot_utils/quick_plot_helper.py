import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from collections import OrderedDict
from redq_plot_helper import *
from pathlib import Path

# the path leading to where the experiment file are located
DEFAULT_BASE_PATH = '../data/'
DEFAULT_SAVE_PATH = '../figures/'
DEFAULT_ENVS = ('Ant-v4',)
DEFAULT_LINESTYLES = tuple(['solid' for _ in range(6)])
DEFAULT_COLORS = ('tab:red', 'tab:orange', 'tab:blue', 'tab:brown', 'tab:pink','tab:grey')
DEFAULT_Y_VALUE = 'AverageTestEpRet'
DEFAULT_SMOOTH = 10
y_to_y_label = {
    'AverageTestEpRet':'Performance',
    'AveragePreTanh':'Avg Abs Pretanh',
    'MaxPreTanh':'Max Abs Pretanh',
    'AverageNormQBias':'Avg Normalized Q Bias',
    'AverageQ1Vals':'Avg Q1 Value',
    'StdNormQBias':'Std Normalized Q Bias',
    'AverageAlpha':'Alpha'
}

# TODO we provide a number of things to a function to do plotting
#  labels, the data folder for each label, the colors, the dashes
#  and then, the y label to use
#  and also what name to save and where to save (we put default values as macros in a certain file? )

def do_smooth(x, smooth):
    y = np.ones(smooth)
    z = np.ones(len(x))
    smoothed_x = np.convolve(x, y, 'same') / np.convolve(z, y, 'same')
    return smoothed_x

def combine_data_in_seeds(seeds, column_name, skip=0, smooth=1):
    vals_list = []
    for d in seeds:
        if isinstance(d,pd.DataFrame):
            vals_to_use = d[column_name].to_numpy().reshape(-1)
        else:
            vals_to_use = d[column_name].reshape(-1)
        # yhat = savgol_filter(vals_to_use, 21, 3)  # window size 51, polynomial order 3
        # TODO might want to use sth else...
        if smooth > 1 and smooth <= len(vals_to_use):
            yhat = do_smooth(vals_to_use, smooth)
        else:
            yhat = vals_to_use

        if skip > 1:
            yhat = yhat[::skip]
        vals_list.append(yhat)
    return np.concatenate(vals_list)

def quick_plot(labels, data_folders, colors=DEFAULT_COLORS, linestyles=DEFAULT_LINESTYLES, envs=DEFAULT_ENVS, base_data_folder_path=DEFAULT_BASE_PATH,
               save_name='test_save_figure', save_folder_path=DEFAULT_SAVE_PATH, y_value=DEFAULT_Y_VALUE, verbose=True, ymin=None, ymax=None):
    label2seeds = OrderedDict()
    for env in envs:
        data_folders_with_env = []
        for data_folder in data_folders:
            data_folders_with_env.append(data_folder + '_' + env)

        for i, label in enumerate(labels): # for each variant
            seeds = []
            data_folder_full_path = os.path.join(base_data_folder_path, data_folders_with_env[i])
            print("check data folder:", data_folder_full_path)
            for subdir, dirs, files in os.walk(data_folder_full_path):
                if 'progress.txt' in files:
                    # load progress file
                    progress_file_path = os.path.join(subdir, 'progress.txt')
                    seeds.append(pd.read_table(progress_file_path))
                    # seeds.append(np.genfromtxt(progress_file_path, dtype=float, delimiter='\t', names=True))

            label2seeds[label] = seeds

        save_name_with_env = save_name + '_' + env
        if not isinstance(y_value, list):
            y_value = [y_value,]

        for y_to_plot in y_value:
            for i, (label, seeds) in enumerate(label2seeds.items()):
                x = combine_data_in_seeds(seeds, 'TotalEnvInteracts')
                y = combine_data_in_seeds(seeds, y_to_plot, smooth=DEFAULT_SMOOTH)
                ax = sns.lineplot(x=x, y=y, n_boot=10, label=label, color=colors[i], linestyle=linestyles[i], linewidth = 2)
            plt.xlabel('Number of Data')
            y_label = y_to_y_label[y_to_plot] if y_to_plot in y_to_y_label else y_to_plot
            plt.ylabel(y_label)
            ax.set_ylim([ymin, ymax])
            plt.tight_layout()
            plt.tight_layout()
            save_folder_path_with_y = os.path.join(save_folder_path, y_to_plot)
            if save_folder_path is not None:
                if not os.path.isdir(save_folder_path_with_y):
                    path = Path(save_folder_path_with_y)
                    path.mkdir(parents=True)
                save_path_full = os.path.join(save_folder_path_with_y, save_name_with_env + '_' + y_to_plot + '.png')
                plt.savefig(save_path_full)
                if verbose:
                    print(save_path_full)
                plt.close()
            else:
                plt.show()
