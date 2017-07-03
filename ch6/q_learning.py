import sys
from os.path import abspath, join, dirname
# add the top level package to sys.path to access utilities
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import time
from utilities import init_state_action_map, \
                      choose_epsilon_greedy_action, \
                      choose_greedy_action, \
                      generate_random_episode, \
                      generate_epsilon_greedy_episode
from Gridworld import Gridworld

def max_q(state, q):
    actions = q[state].keys()
    return max([q[state][action] for action in actions])

def q_learning(env, epsilon=0.1, alpha=0.5, gamma=1):
    q = init_state_action_map(env)
    for i in xrange(1000):
        state = env.reset()
        done = False
        while not done:
            action = choose_epsilon_greedy_action(q, state, epsilon)
            (next_state, reward, done, _) = env.step(action)
            td_error = reward + gamma * max_q(next_state, q) - q[state][action]
            q[state][action] += alpha * td_error
            state = next_state
    return q

def main():
    #env = Gridworld(kings_moves=True, wind=[0,0,0,1,1,1,2,2,1,0], stochastic_wind=False)
    env = Gridworld(kings_moves=False)
    num_episodes = 1000

    # determine the baseline performance that results from taking random moves
    avg = sum([len(generate_random_episode(env)) for _ in range(num_episodes)]) / float(num_episodes)
    print "baseline random performance: " + str(avg)

    # learn q
    print "running q-learning..."
    q = q_learning(env)
    print "q-learning complete"

    # determine post-training performance
    avg = sum([len(generate_epsilon_greedy_episode(env, q)) for _ in range(num_episodes)]) / float(num_episodes)
    print "post learning performance: " + str(avg)

    # visualize post-training episode
    state = env.reset()
    while True:
        env.render()
        time.sleep(0.25)
        action = choose_greedy_action(q, state)
        state, _, done, _ = env.step(action) # take a random action
        if done:
            env.render(close=True)
            break

main()