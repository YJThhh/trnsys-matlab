import argparse
import os.path
import time
from copy import deepcopy

import matlab.engine

import gym
import numpy as np
import torch

from tqdm import tqdm
from models.DDPG import DDPG
from simulink.HeatPump import HeatPump
from util import get_output_folder

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='PyTorch on TORCS with Multi-modal')

    parser.add_argument('--mode', default='train', type=str, help='support option: train/test')
    parser.add_argument('--env', default='Pendulum-v1', type=str, help='open-ai gym environment')
    parser.add_argument('--hidden1', default=400, type=int, help='hidden num of first fully connect layer')
    parser.add_argument('--hidden2', default=300, type=int, help='hidden num of second fully connect layer')
    parser.add_argument('--rate', default=0.001, type=float, help='learning rate')
    parser.add_argument('--prate', default=0.0001, type=float, help='policy net learning rate (only for DDPG)')
    parser.add_argument('--warmup', default=100, type=int, help='time without training but only filling the replay memory')
    parser.add_argument('--discount', default=0.99, type=float, help='')
    parser.add_argument('--bsize', default=64, type=int, help='minibatch size')
    parser.add_argument('--rmsize', default=6000000, type=int, help='memory size')
    parser.add_argument('--window_length', default=1, type=int, help='')
    parser.add_argument('--tau', default=0.001, type=float, help='moving average for target network')
    parser.add_argument('--ou_theta', default=0.15, type=float, help='noise theta')
    parser.add_argument('--ou_sigma', default=0.2, type=float, help='noise sigma')
    parser.add_argument('--ou_mu', default=0.0, type=float, help='noise mu')
    parser.add_argument('--validate_episodes', default=20, type=int, help='how many episode to perform during validate experiment')
    parser.add_argument('--max_episode_length', default=500, type=int, help='')
    parser.add_argument('--validate_steps', default=2000, type=int, help='how many steps to perform a validate experiment')
    parser.add_argument('--output', default='output', type=str, help='')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--init_w', default=0.003, type=float, help='')
    parser.add_argument('--train_iter', default=200000, type=int, help='train iters each timestep')
    parser.add_argument('--epsilon', default=50000, type=int, help='linear decay of exploration policy')
    parser.add_argument('--seed', default=-1, type=int, help='')
    parser.add_argument('--resume', default='default', type=str, help='Resuming model path for testing')
    # parser.add_argument('--l2norm', default=0.01, type=float, help='l2 weight decay') # TODO
    # parser.add_argument('--cuda', dest='cuda', action='store_true') # TODO

    args = parser.parse_args()
    args.output = get_output_folder(args.output, args.env)
    if args.resume == 'default':
        args.resume = 'output/{}-run0'.format(args.env)

    start = time.time()
    # Step 1: Init
    heatPumpSimModel = HeatPump(os.getcwd() + "/../../matlab")

    agent = DDPG(9, 1, args)

    EPISODE_PER_BATCH = 5  # 每蒐集 5 個 episodes 更新一次 agent
    NUM_BATCH = 400  # 總共更新 400 次
    EXP_NAME = "exp_1"


    avg_total_rewards, avg_final_rewards = [], []

    prg_bar = range(NUM_BATCH)
    for batch in tqdm(prg_bar):

        log_probs, rewards = [], []
        total_rewards, final_rewards = [], []

        # 蒐集訓練資料
        for episode in range(EPISODE_PER_BATCH):

            heatPumpSimModel.Reset()
            state = heatPumpSimModel.Init()
            total_reward, total_step = 0, 0

            while True:
                total_step += 1
                action = agent.select_action(state)
                state = heatPumpSimModel.Step(action)
                done = False
                if total_step > 100:
                    done = True

                reward = 0
                agent.observe(reward, deepcopy(state), done)

                if total_step > args.warmup:
                    agent.update_policy()


    save_path = os.path.join('./experiments', EXP_NAME)
    agent.save_model(save_path)
