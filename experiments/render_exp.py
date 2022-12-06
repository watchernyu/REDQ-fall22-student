# will render saved agents
# you can do the rendering with an interactive compute node.
import gym
from PIL import Image
import os.path as osp
import joblib
import numpy as np

def render_agent(agent, test_env, max_ep_len, logger, n_eval=1, save_folder='./', save_name_prefix=''):
    """
    This will test the agent's performance by running <n_eval> episodes
    During the runs, the agent should only take deterministic action
    This function assumes the agent has a <get_test_action()> function
    And will also render the agent and save the rendered frames to disk
    :param agent: agent instance
    :param test_env: the environment used for testing
    :param max_ep_len: max length of an episode
    :param logger: logger to store info in
    :param n_eval: number of episodes to run the agent
    :param save_folder: folder path to save images into
    :param save_name_prefix: name prefix of saved image files
    :return: test return for each episode as a numpy array
    """
    ep_return_list = np.zeros(n_eval)
    for j in range(n_eval):
        o, r, d, ep_ret, ep_len = test_env.reset(), 0, False, 0, 0
        while not (d or (ep_len == max_ep_len)):
            # Take deterministic actions at test time
            a = agent.get_test_action(o)
            o, r, d, _ = test_env.step(a)
            ep_ret += r
            ep_len += 1

            frame = test_env.render(mode='rgb_array', width=1024, height=768)
            im = Image.fromarray(frame)
            im_path = osp.join(save_folder, '%s_%d_%d.jpeg' % (save_name_prefix, j, ep_len))
            im.save(im_path)
        ep_return_list[j] = ep_ret
        if logger is not None:
            logger.store(TestEpRet=ep_ret, TestEpLen=ep_len)
    return ep_return_list

exp_name = 'exp_e300_q2_uf1_lr0.0003_g0.99_p0.995_ss5000_b128_h128'
seed = 1
env_name = 'Hopper-v3'
epoch = 300
save_name_prefix = 'sac_b128_h128_ep300'

exp_env_name = '%s_%s' % (exp_name, env_name)
seed_name = '%s_s%d' % (exp_env_name, seed)
exp_subfolder_path = osp.join('../data', exp_env_name, seed_name)
vars_path = osp.join(exp_subfolder_path, 'vars%d.pkl' % epoch)
print(vars_path)
state_dict = joblib.load(vars_path)
agent = state_dict['agent']

e = gym.make(env_name)
e.reset()

render_agent(agent, e, 1000, None, 1, exp_subfolder_path, save_name_prefix)
