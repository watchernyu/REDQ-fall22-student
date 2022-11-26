from train_redq_sac import redq_sac as function_to_run ## here make sure you import correct function
import time
from redq.utils.run_utils import setup_logger_kwargs
from grid_utils import get_setting_and_exp_name

if __name__ == '__main__':
    import argparse
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--setting', type=int, default=0)
    args = parser.parse_args()
    data_dir = '../data'

    exp_prefix = 'exp'
    # this wi
    settings = ['env_name','',['Hopper-v3'],
                'seed','',[0],
                'epochs','e',[35],
                'num_Q','q',[2],
                'utd_ratio','uf',[1],
                'lr', 'lr', [3e-4],
                'gamma', 'g', [0.99],
                'polyak', 'p', [0.995],
                'start_steps', 'ss', [5000],
                'batch_size', 'b', [4],
                'hidden_unit', 'h', [4],
                ]

    indexes, actual_setting, total, exp_name_full = get_setting_and_exp_name(settings, args.setting, exp_prefix)
    print("##### TOTAL NUMBER OF VARIANTS: %d #####" % total)

    logger_kwargs = setup_logger_kwargs(exp_name_full, actual_setting['seed'], data_dir)
    function_to_run(logger_kwargs=logger_kwargs, **actual_setting)
    print("Total time used: %.3f hours." % ((time.time() - start_time)/3600))

"""
before you submit the jobs:
- quick test your code to make sure things will run without bug
- compute the number of jobs, make sure that is consistent with the array number in the .sh file
- in the .sh file make sure you are running the correct python file 
"""
