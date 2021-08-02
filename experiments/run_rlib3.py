import argparse
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
from experiments.jungle_wrapper import RLlibWrapper

"""In simplified version, setting number of policies to 1 instead of 2, which is the number of agents at the moment
, and using easy exit """

tf1, tf, tfv = try_import_tf()

parser = argparse.ArgumentParser()

parser.add_argument("--num-agents", type=int, default=2)
parser.add_argument("--num-policies", type=int, default=2)
parser.add_argument("--stop-iters", type=int, default=9999)
parser.add_argument("--stop-reward", type=float, default=9999)
parser.add_argument("--stop-timesteps", type=int, default=1000000)
parser.add_argument("--num-cpus", type=int, default=0)
parser.add_argument("--as-test", action="store_true")
parser.add_argument(
    "--framework", choices=["tf2", "tf", "tfe", "torch"], default="tf")
parser.add_argument("--logdir", type=str, default="logs")

if __name__ == "__main__":
    args = parser.parse_args()

    ray.init(num_cpus=args.num_cpus or None, local_mode=True)

    # Register the models to use.

    # Get obs- and action Spaces.
    # config = {'jungle': 'RiverExit', 'size': 11}
    config = {'jungle': 'BlackRiver', 'size': 9}
    single_env = RLlibWrapper(config)

    obs_space = single_env.observation_space
    act_space = single_env.action_space

    # Each policy can have a different configuration (including custom model).
    policies = {"black_ppo": (None, obs_space, act_space, {}),
                "white_ppo": (None, obs_space, act_space, {})}

    # Setup PPO with an ensemble of `num_policies` different policies.

    policy_ids = list(policies.keys())

    def policy_mapping_fn(agent_id):

        pol_id = random.choice(policy_ids)
        # print(f"mapping {agent_id} to {pol_id}")

        return pol_id


    def policy_mapping_fn2(agent_id):
        if agent_id == 'white':
            return policy_ids[0]
        elif agent_id == 'black':
            return policy_ids[1]


    #higher reward
    config = {
        "env": RLlibWrapper,
        "env_config": {'jungle': 'BlackRiver', "size": 9},
        "no_done_at_end": False,

        "horizon": 2500,
        "output": "logdir",
        "num_workers": 0,
        # "lr":0.0001,
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
        "num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "0")),
        "num_sgd_iter": 20,
        "multiagent": {
            "policies": policies,
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
        #"explore":True,
        #"exploration_config":{
            #"type": "Curiosity",
            #"eta": 1.0,  # Weight for intrinsic rewards before being added to extrinsic ones.
            #"lr": 0.001,  # Learning rate of the curiosity (ICM) module.
            #"feature_dim": 288,  # Dimensionality of the generated feature vectors.
            # Setup of the feature net (used to encode observations into feature (latent) vectors).
            #"feature_net_config": {
             #   "fcnet_hiddens": [],
              #  "fcnet_activation": "relu",
            #},
            #"inverse_net_hiddens": [256],  # Hidden layers of the "inverse" model.
            #"inverse_net_activation": "relu",  # Activation of the "inverse" model.
            #"forward_net_hiddens": [256],  # Hidden layers of the "forward" model.
            #"forward_net_activation": "relu",  # Activation of the "forward" model.
           # "beta": 0.2,  # Weight for the "forward" loss (beta) over the "inverse" loss (1.0 - beta)
            #"sub_exploration":{
               # "type": "StochasticSampling",
            #}
        #"exploration_config":{
            #"type": "StochasticSampling"
        #},
        "framework": args.framework,
    }
    stop = {
        "episode_reward_mean": args.stop_reward,
        "timesteps_total": args.stop_timesteps,
        "training_iteration": args.stop_iters,
    }


    results = tune.run("PPO", stop=stop, config=config,  verbose=1)


    results = tune.run("PPO", stop=stop, config=config, local_dir=args.logdir, verbose=1)

    if args.as_test:
        check_learning_achieved(results, args.stop_reward)
    ray.shutdown()
