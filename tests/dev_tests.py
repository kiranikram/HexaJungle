import random

from jungle.agent import Agent
from jungle.jungle import EmptyJungle
from jungle.utils import Actions, ElementsEnv
from RL_Lib.jungle_wrapper import RLlibWrapper

from jungle.exp_trainer import run_one_episode
from jungle.rl_envs.basic import RiverExit, BoulderExit


def generate_actions():
    fwd = random.choice([-1, 0, 1])
    rot = random.choice([1, 0])
    climb = random.choice([1, 0])
    agent_actions = {Actions.FORWARD: fwd, Actions.ROTATE: rot, Actions.CLIMB: climb}

    return agent_actions


def test_run_check():
    agent_1 = Agent()
    agent_2 = Agent()
    agents = [agent_1, agent_2]

    actions = {}

    for agent in agents:
        actions[agent] = generate_actions()
    print(actions)

    return actions


# TODO make a really small env with one easy exit --
# set the engine loop with actions/terminations/episodes

def test_engine():
    agent_1 = Agent(range_observation=3)
    agent_2 = Agent(range_observation=3)

    simple_jungle = EmptyJungle(size=5)

    simple_jungle.add_agents(agent_1, agent_2)
    simple_jungle.add_object(ElementsEnv.EXIT_EASY, (0, 4))
    print(agent_1.grid_position, agent_2.grid_position)

    run_one_episode(100, simple_jungle.agents, simple_jungle, agent_1, agent_2)


def test_instantiation():
    agent_1 = Agent(range_observation=3)
    agent_2 = Agent(range_observation=3)

    new_jungle = BoulderExit(size=9)
    new_jungle.add_agents(agent_1, agent_2)

    # @MG run function can be found in exp_trainer.py
    run_one_episode(400, new_jungle.agents, new_jungle, agent_1, agent_2)


def test_wrapper():
    Jungle = EmptyJungle(size=11)
    agent_1 = Agent(range_observation=3)
    agent_2 = Agent(range_observation=3)
    Jungle.add_agents(agent_1, agent_2)

    env = RLlibWrapper(Jungle)
    print('sample', env.action_space.sample())

    actions = {"agent_1": [1, 1, 1], "agent_2": [1, 0, 0]}
    obs, rew, done = env.step(actions)
    # print(obs)

    obs = env.reset()
    print(obs)


def test_riverexit_wrapper():
    # Jungle = RiverExit(size=11)
    # agent_1 = Agent(range_observation=3)
    # agent_2 = Agent(range_observation=3)
    # Jungle.add_agents(agent_1, agent_2)
    actions = {"white": [1, -1, 1], "black": [1, 1, 1]}
    config = {'jungle': 'EasyExit', 'size': 11}
    env = RLlibWrapper(config)
    print(env)

    obs, rew, done, _ = env.step(actions)
    obs, rew, done, _ = env.step(actions)

    assert isinstance(obs, dict)
    assert isinstance(rew, dict)
    assert isinstance(done, dict)

    #new_obs = env.reset()
    #assert isinstance(new_obs, dict)


def test_RiverExit():
    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)
    env = RiverExit(size=11)
    env.add_agents(agent_1, agent_2)
    size = 11
    print(env)
    exits = [(1, 1), (size - 2, 1), (1, size - 2), (size - 2, size - 2)]

    potential_exits = env.cell_type(exits[0][0], exits[0][1]) == ElementsEnv.EXIT_DIFFICULT.value or \
                      env.cell_type(exits[1][0], exits[1][1]) == ElementsEnv.EXIT_DIFFICULT.value or \
                      env.cell_type(exits[2][0], exits[2][1]) == ElementsEnv.EXIT_DIFFICULT.value or \
                      env.cell_type(exits[3][0], exits[3][1]) == ElementsEnv.EXIT_DIFFICULT.value

    assert potential_exits

    env.reset()

    potential_exits = env.cell_type(exits[0][0], exits[0][1]) == ElementsEnv.EXIT_DIFFICULT.value or \
                      env.cell_type(exits[1][0], exits[1][1]) == ElementsEnv.EXIT_DIFFICULT.value or \
                      env.cell_type(exits[2][0], exits[2][1]) == ElementsEnv.EXIT_DIFFICULT.value or \
                      env.cell_type(exits[3][0], exits[3][1]) == ElementsEnv.EXIT_DIFFICULT.value

    assert potential_exits

def test_agent_sees_exit():
    pass


