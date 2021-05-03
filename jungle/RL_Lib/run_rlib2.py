import argparse
import gym
import os
import random

import ray
from ray import tune
from ray.rllib.examples.models.shared_weights_model import \
    SharedWeightsModel1, SharedWeightsModel2, TF2SharedWeightsModel, \
    TorchSharedWeightsModel
from ray.rllib.models import ModelCatalog
from ray.rllib.utils.framework import try_import_tf
from ray.rllib.utils.test_utils import check_learning_achieved
from jungle.jungle import EmptyJungle
from jungle.rl_envs.basic import RiverExit, BoulderExit
from jungle.RL_Lib.jungle_wrapper import RLlibWrapper
from jungle.utils import ElementsEnv, Actions, Definitions
from jungle.agent import Agent

"""In simplified version, setting number of policies to 1 instead of 2, which is the number of agents at the moment
, and using easy exit """

tf1, tf, tfv = try_import_tf()

parser = argparse.ArgumentParser()

parser.add_argument("--num-agents", type=int, default=2)
parser.add_argument("--num-policies", type=int, default=1)
parser.add_argument("--use-prev-action", action="store_true")
parser.add_argument("--use-prev-reward", action="store_true")
parser.add_argument("--stop-iters", type=int, default = 9999)
parser.add_argument("--stop-reward", type=float, default  = 9999)
parser.add_argument("--stop-timesteps", type=int, default=200000)
parser.add_argument("--num-cpus", type=int, default=0)
parser.add_argument("--as-test", action="store_true")
parser.add_argument(
    "--framework", choices=["tf2", "tf", "tfe", "torch"], default="tf")

if __name__ == "__main__":
    args = parser.parse_args()

    ray.init(num_cpus=args.num_cpus or None, local_mode=True)

    # Register the models to use.

    # Get obs- and action Spaces.
    # config = {'jungle': 'RiverExit', 'size': 11}
    config = {'jungle': 'EasyExit', 'size': 11}
    single_env = RLlibWrapper(config)

    obs_space = single_env.observation_space
    act_space = single_env.action_space

    # Each policy can have a different configuration (including custom model).
    policies = {"centralized_ppo": (None, obs_space, act_space, {})}

    policy_ids = list(policies.keys())


    def select_policy(agent_id):
        if agent_id == 'white':
            return policies["centralized_ppo"]
        elif agent_id == 'black':
            return policies["centralized_ppo"]


    def policy_mapping_fn(agent_id):


        pol_id = random.choice(policy_ids)
        #print(f"mapping {agent_id} to {pol_id}")


        return pol_id


    config = {
        "env": RLlibWrapper,
        "env_config": {'jungle': 'EasyExit', "size": 11},
        "no_done_at_end": False,
        "gamma": 0.9,
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
        "num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "0")),
        "num_workers": 1,
        "train_batch_size": 200,
        "horizon": 300,
        "multiagent": {

            "policies": {
                "centralized_ppo": (None, obs_space, act_space, {})
            },
            "policy_mapping_fn": policy_mapping_fn,
        },
        "model": {

            'fcnet_hiddens': [256, 256],
            # 'vf_share_layers': True,
            'use_lstm': True,
            "lstm_cell_size": 256,
            "lstm_use_prev_action": True,
            "lstm_use_prev_reward": True,
            # "use_attention": True,

        },
        "framework": args.framework,
    }

    stop = {
        "episode_reward_mean": args.stop_reward,
        "timesteps_total": args.stop_timesteps,
        "training_iteration": args.stop_iters,
    }

    results = tune.run("PPO", stop=stop, config=config, verbose=1)
    #results = tune.run("PPO", stop={"episode_reward_mean": 100}, config=config, verbose=1)

    if args.as_test:
        check_learning_achieved(results, args.stop_reward)
    ray.shutdown()
