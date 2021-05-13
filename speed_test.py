from jungle.jungles.basic import FullJungle, RiverOnlyJungle , WhiteJungle, DifficultJungle
from jungle.jungles.rl import EasyExit
from jungle.agent import Agent
from jungle.utils import Actions
import matplotlib.pyplot as plt

import time

agent_1 = Agent(range_observation=5)
agent_2 = Agent(range_observation=5)

env = DifficultJungle(size=15)
env.add_agents(agent_1, agent_2)

t0 = time.time()
n_steps = 10000

for ts in range(n_steps):
    # print(ts)
    # print(agent_1.position, agent_2.position)

    actions = {
        agent_1: agent_1.get_random_actions(),
        agent_2: agent_2.get_random_actions()
    }

    obs, rew, dones = env.step(actions)

print(n_steps / (time.time() - t0))
print(obs)
print(rew)
print(dones)

#
#
print(env)

obs = env.reset()
actions = {
    agent_1: {
        Actions.ROTATE: 1,
        Actions.FORWARD: 0
    },
    agent_2: {
        Actions.ROTATE: 1,
        Actions.FORWARD: 0
    }
}

# obs, _, _ = env.step(actions)

# obs, _, _ = env.step(actions)

# obs, _, dones = env.step(actions)
#
# print(dones)
# print(env)
#
# for o in obs:
# print(o, o.position, o.angle, obs[o])
print(obs)
plt.imshow(env.display() / 255.)
plt.show()

# print(env.agent_black.position)
