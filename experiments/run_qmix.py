import argparse
from gym.spaces import Tuple, MultiDiscrete, Dict, Discrete
import os

import ray
from ray import tune
from ray.tune import register_env, grid_search
from ray.rllib.env.multi_agent_env import ENV_STATE
from ray.rllib.examples.env.two_step_game import TwoStepGame
from ray.rllib.utils.test_utils import check_learning_achieved
from experiments.jungle_wrapper import RLlibWrapper

parser = argparse.ArgumentParser()
parser.add_argument("--run", type=str, default="QMIX")
parser.add_argument("--num-cpus", type=int, default=0)
parser.add_argument("--as-test", action="store_true")
parser.add_argument("--torch", action="store_true")
parser.add_argument("--stop-reward", type=float, default=7.0)
parser.add_argument("--stop-timesteps", type=int, default=50000)

if __name__ == "__main__":
    args = parser.parse_args()

    config = {'jungle': 'RiverExit', 'size': 11}
    single_env = RLlibWrapper(config)

    grouping = {
        "group_1": [0, 1],
    }
    obs_space = Tuple([
        single_env.observation_space,
        single_env.observation_space

    ])
    act_space = Tuple([
        single_env.action_space,
        single_env.action_space,
    ])
    register_env(
        "jungleqmix",
        lambda config: single_env.with_agent_groups(
            grouping, obs_space=obs_space, act_space=act_space))

    if args.run == "contrib/MADDPG":
        obs_space_dict = {
            "agent_1": Discrete(6),
            "agent_2": Discrete(6),
        }
        act_space_dict = {
            "agent_1": TwoStepGame.action_space,
            "agent_2": TwoStepGame.action_space,
        }
        config = {
            "env":RLlibWrapper.with_agent_groups(grouping, obs_space=obs_space, act_space=act_space),
            "learning_starts": 100,
            "env_config": {
                "actions_are_logits": True,
            },
            "multiagent": {
                "policies": {
                    "pol1": (None, Discrete(6), TwoStepGame.action_space, {
                        "agent_id": 0,
                    }),
                    "pol2": (None, Discrete(6), TwoStepGame.action_space, {
                        "agent_id": 1,
                    }),
                },
                "policy_mapping_fn": lambda x: "pol1" if x == 0 else "pol2",
            },
            "framework": "torch" if args.torch else "tf",
            # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
            "num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "0")),
        }
        group = False
    elif args.run == "QMIX":
        config = {


            "rollout_fragment_length": 4,
            "train_batch_size": 32,
            "exploration_config": {
                "epsilon_timesteps": 5000,
                "final_epsilon": 0.05,
            },
            "num_workers": 0,
            "mixer": grid_search([None, "qmix", "vdn"]),

            # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
            "num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "0")),
            "framework": "torch" if args.torch else "tf",
        }
        group = True
    else:
        config = {
            # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
            "num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "0")),
            "framework": "torch" if args.torch else "tf",
        }
        group = False

    ray.init(num_cpus=args.num_cpus or None)

    stop = {
        "episode_reward_mean": args.stop_reward,
        "timesteps_total": args.stop_timesteps,
    }

    #config = dict(config, **{
        #"env": "grouped_twostep" if group else TwoStepGame,
    #})

    results = tune.run(args.run, stop=stop, config=config, verbose=1)

    if args.as_test:
        check_learning_achieved(results, args.stop_reward)

    ray.shutdown()
