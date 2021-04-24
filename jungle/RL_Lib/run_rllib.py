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

tf1, tf, tfv = try_import_tf()

parser = argparse.ArgumentParser()

parser.add_argument("--num-agents", type=int, default=2)
parser.add_argument("--num-policies", type=int, default=2)
parser.add_argument("--stop-iters", type=int, default=100)
parser.add_argument("--stop-reward", type=float, default=15)
parser.add_argument("--stop-timesteps", type=int, default=100)
parser.add_argument("--num-cpus", type=int, default=0)
parser.add_argument("--as-test", action="store_true")
parser.add_argument(
    "--framework", choices=["tf2", "tf", "tfe", "torch"], default="tf")

if __name__ == "__main__":
    args = parser.parse_args()

    ray.init(num_cpus=args.num_cpus or None, local_mode=True)

    # Register the models to use.
    if args.framework == "torch":
        mod1 = mod2 = TorchSharedWeightsModel
    elif args.framework in ["tfe", "tf2"]:
        mod1 = mod2 = TF2SharedWeightsModel
    else:
        mod1 = SharedWeightsModel1
        mod2 = SharedWeightsModel2
    ModelCatalog.register_custom_model("model1", mod1)
    ModelCatalog.register_custom_model("model2", mod2)

    # Get obs- and action Spaces.
    # config = {'jungle': 'RiverExit', 'size': 11}
    config = {'jungle': 'EasyExit', 'size': 11}
    single_env = RLlibWrapper(config)

    obs_space = single_env.observation_space
    act_space = single_env.action_space


    # Each policy can have a different configuration (including custom model).
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
    print('policies DICT')
    print(policies)
    policy_ids = list(policies.keys())


    def policy_mapping_fn2(agent_id):
        print('AGENT ID in policy mapping function')
        print(agent_id)

        pol_id = random.choice(policy_ids)
        print(f"mapping {agent_id} to {pol_id}")

        print('RETURNS pol_id')
        print(pol_id)
        return pol_id


    def policy_mapping_fn(agent_id):
        if agent_id == 'white':
            return policy_ids[0]
        elif agent_id == 'black':
            return policy_ids[1]


    config = {
        "env": RLlibWrapper,
        "env_config": {'jungle': 'RiverExit', "size": 11},
        "no_done_at_end": True,
        "lr": tune.grid_search([1e-4, 1e-6]),
        # "lr":0.0001,
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
        "num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "0")),
        "num_sgd_iter": 10,
        "multiagent": {
            "policies": policies,
            "policy_mapping_fn": policy_mapping_fn,
        },
        "framework": args.framework,
    }
    stop = {
        "episode_reward_mean": args.stop_reward,
        "timesteps_total": args.stop_timesteps,
        "training_iteration": args.stop_iters,
    }

    results = tune.run("PPO", stop=stop, config=config, verbose=1)
    print(results)

    if args.as_test:
        check_learning_achieved(results, args.stop_reward)
    ray.shutdown()
