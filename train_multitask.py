import gym
import numpy as np

from algs.distral import DiscreteDistral
from parse_args import parse_args
from stable_baselines3.common.logger import configure
from get_multi_envs import envs_name
from stable_baselines3.common.vec_env import DummyVecEnv
from common.callbacks import LogReturnSeparateEnvs

args = parse_args()

envs = envs_name[args.env_name]
envs = DummyVecEnv(envs)

model = DiscreteDistral("MlpPolicy",
                        envs, verbose=1, learning_rate=args.learning_rate,
                        buffer_size=args.buffer_size,
                        learning_starts=args.learning_starts,
                        batch_size=args.batch_size,
                        tau=args.tau,
                        gamma=args.gamma,
                        train_freq=args.train_freq,
                        gradient_steps=args.gradient_steps,
                        alpha=0.5,
                        beta=5)
new_logger = configure('./', ["stdout", "csv"])
model.set_logger(new_logger)

callback_return = LogReturnSeparateEnvs()

model.learn(total_timesteps=args.total_timesteps,
            log_interval=1000, callback=callback_return)
