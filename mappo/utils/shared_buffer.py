import torch
import numpy as np

# observation and action space that go in are from the gym structures

class SharedReplayBuffer(object):
    """
        Buffer to store training data.
        :param args: (argparse.Namespace) arguments containing relevant model, policy, and env information.
        :param num_agents: (int) number of agents in the env.
        :param obs_space: (gym.Space) observation space of agents.
        :param cent_obs_space: (gym.Space) centralized observation space of agents.
        :param act_space: (gym.Space) action space for agents.
        """

    # TODO determine if we go with args or make it manual -- for now we keep it manual and then see what we can move to args
    # we initialize this class in the base runner

    #TODO rollout threads ... really required ?
    def __init__(self, args, num_agents, obs_space, cent_obs_space, act_space):
        self.episode_length = args.episode_length
        self.n_rollout_threads = args.n_rollout_threads
        self.hidden_size = args.hidden_size
        self.recurrent_N = args.recurrent_N
        self.gamma = args.gamma
        self.gae_lambda = args.gae_lambda
        self._use_gae = args.use_gae
        self._use_popart = args.use_popart
        self._use_valuenorm = args.use_valuenorm
        self._use_proper_time_limits = args.use_proper_time_limits

        # i think our obs space is a box
        # thus
        obs_shape = obs_space.shape
        share_obs_shape = cent_obs_space.shape

        #TODO : in env make shared obs space

        if type(obs_shape[-1]) == list:
            obs_shape = obs_shape[:1]

        if type(share_obs_shape[-1]) == list:
            share_obs_shape = share_obs_shape[:1]

        self.share_obs = np.zeros(
            (self.episode_length + 1, num_agents, *share_obs_shape),
            dtype=np.float32)
        self.obs = np.zeros((self.episode_length + 1, num_agents, *obs_shape),
                            dtype=np.float32)

        self.rnn_states = np.zeros(
            (self.episode_length + 1, self.n_rollout_threads, num_agents, self.recurrent_N, self.hidden_size),
            dtype=np.float32)
        self.rnn_states_critic = np.zeros_like(self.rnn_states)

        self.value_preds = np.zeros(
            (self.episode_length + 1, self.n_rollout_threads, num_agents, 1), dtype=np.float32)
        self.returns = np.zeros_like(self.value_preds)

        # hexa action space is multi discrete

        act_shape = act_space.shape

        self.actions = np.zeros(
            (self.episode_length, self.n_rollout_threads, num_agents, act_shape), dtype=np.float32)
        self.action_log_probs = np.zeros(
            (self.episode_length, self.n_rollout_threads, num_agents, act_shape), dtype=np.float32)

        self.rewards = np.zeros(
            (self.episode_length, self.n_rollout_threads, num_agents, 1), dtype=np.float32)

        #original code inclused masks but we dont need that

        self.step = 0






