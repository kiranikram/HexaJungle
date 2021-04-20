import argparse
import os
import random
from ray.tune.registry import register_env
import ray
from ray import tune
import tensorflow
import torch
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from ray.rllib.agents import ppo
from ray.rllib.utils.test_utils import check_learning_achieved
from ray.rllib.examples.models.shared_weights_model import \
    SharedWeightsModel1, SharedWeightsModel2, TF2SharedWeightsModel, \
    TorchSharedWeightsModel
from ray.rllib.models import ModelCatalog
from jungle.jungle import EmptyJungle
from jungle.rl_envs.basic import RiverExit
from jungle.RL_Lib.jungle_wrapper import RLlibWrapper
from jungle.utils import ElementsEnv, Actions, Definitions
from jungle.agent import Agent

parser = argparse.ArgumentParser()

parser.add_argument("--num-agents", type=int, default=2)
parser.add_argument("--num-policies", type=int, default=2)
parser.add_argument("--stop-iters", type=int, default=200)
parser.add_argument("--stop-reward", type=float, default=150)
parser.add_argument("--stop-timesteps", type=int, default=100000)
parser.add_argument("--num-cpus", type=int, default=0)
parser.add_argument("--as-test", action="store_true")
parser.add_argument(
    "--framework", choices=["tf2", "tf", "tfe", "torch"], default="tf")



if __name__ == "__main__":
    args = parser.parse_args()

    ray.init(num_cpus=args.num_cpus or None)
    Jungle = EmptyJungle(size=11)
    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)
    Jungle.add_agents(agent_1, agent_2)
    register_env("jungle",
                 lambda _: RLlibWrapper({"size": 11}))
    if args.framework == "torch":
        mod1 = mod2 = TorchSharedWeightsModel
    elif args.framework in ["tfe", "tf2"]:
        mod1 = mod2 = TF2SharedWeightsModel
    else:
        mod1 = SharedWeightsModel1
        mod2 = SharedWeightsModel2
    ModelCatalog.register_custom_model("model1", mod1)
    ModelCatalog.register_custom_model("model2", mod2)

    #single_env = RLlibWrapper({"size":11})
    single_env = RLlibWrapper(Jungle)
    obs_space = single_env.observation_space
    act_space = single_env.action_space


    def gen_policy(i):
        config = {
            "model": {
                "custom_model": ["model1", "model2"][i % 2],
            },
            "gamma": random.choice([0.95, 0.99]),
        }
        return (None, obs_space, act_space, config)


    # Setup PPO with an ensemble of `num_policies` different policies.
    policies = {
        "policy_{}".format(i): gen_policy(i)
        for i in range(args.num_policies)
    }
    policy_ids = list(policies.keys())


    # 20 /4 centralized training to start off with ; give them the same policy

    # 20 / 4 add a new component to obs ;; color of other agnet - right now just append!

    # 20 /4 ADD IN WRAPPER NOT JUNGLE
    def policy_mapping_fn(agent_id):
        pol_id = random.choice(policy_ids)
        print(f"mapping {agent_id} to {pol_id}")
        return pol_id


    config = {
        "log_level": "WARN",
        "num_workers": 3,
        "num_cpus_for_driver": 1,
        "num_cpus_per_worker": 1,
        "lr": 5e-3,
        "model": {"fcnet_hiddens": [8, 8]},
        "multiagent": {
            "policies": policies,
            "policy_mapping_fn": policy_mapping_fn,
        },
        "env": "jungle",
        "env_config":{"size": 11}}

    stop = {
        "episode_reward_mean": args.stop_reward,
        "timesteps_total": args.stop_timesteps,
        "training_iteration": args.stop_iters,
    }

    results = tune.run("PPO", stop=stop, config=config, verbose=1)
