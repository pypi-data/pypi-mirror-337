## XCS-RC

*Accuracy-based Learning Classifier Systems* with **Rule Combining** mechanism, shortly `XCS-RC` for Python3, loosely based on Martin Butz's XCS Java code (2001). Read my PhD thesis [here](https://publikationen.bibliothek.kit.edu/1000046880) for the complete algorithmic description.

*Rule Combining* is novel function that employs inductive reasoning, replacing ~~all Darwinian genetic operation like mutation and crossover~~. It can handle `binaries` and `real`, reaching better *correctness rate* and *population size* quicker than several XCS instances. My earlier papers comparing them can be obtained at [here](https://link.springer.com/chapter/10.1007/978-3-642-17298-4_30) and [here](https://dl.acm.org/citation.cfm?id=2331009).

---

## Relevant links
* [PyPI](https://pypi.org/project/xcs-rc/)
* [Github repo](https://github.com/nuggfr/xcs-rc-python)
* Examples:
    * [Classic problems: multiplexer, Markov env](https://github.com/nuggfr/xcs-rc-python)
    * [Churn dataset](https://routing.nuggfr.com/churn)
    * [Flappy Bird](https://routing.nuggfr.com/flappy)
    * [OpenAI Gym](https://routing.nuggfr.com/openai)

---

**Installation**
```
pip install xcs-rc
```

**Initialization**
```
import xcs_rc
agent = xcs_rc.Agent()
```

**Classic Reinforcement Learning cycle**
```
# input: binary string, e.g., "100110" or decimal array
state = str(randint(0, 1))

# pick methods: 0 = explore, 1 = exploit, 2 = explore_it
action = agent.next_action(state, pick_method=1)

# determine reward and apply it, e.g.,
reward = agent.maxreward if action == int(state[0]) else 0.0
agent.apply_reward(reward)
```

**Partially Observable Markov Decision Process (POMDP) environment**
```
# create env and agent
env = xcs_rc.MarkovEnv('maze4')  # maze4 is built-in
env.add_agents(num=1, tcomb=100, xmax=50)
agent = env.agents[0]

for episode in range(8000):
    steps = env.one_episode(pick_method=2)  # returns the number of taken steps
```

**Print population, save it to CSV file, or use append mode**
```
agent.pop.print(title="Population")
agent.save('xcs_population.csv', title="Final XCS Population")
agent.save('xcs_pop_every_100_cycles.csv', title="Cycle: ###", save_mode='a')
```

**Finally, inserting rules to population**
```
# automatically load the last set (important for append mode)
agent.load("xcs_population.csv", empty_first=True)
agent.pop.add(my_list_of_rules)  # from a list of classifiers
```

---

## Main Parameters

**XCS-RC Parameters**
* `tcomb`: *combining period*, number of learning cycles before the next rule combining
* `predtol`: *prediction tolerance*, maximum difference between two classifiers to be combined
* `prederrtol`: *prediction error tolerance*, threshold for deletion of inappropriately combined rules


**How to Set**
```
agent.tcomb = 50 # perform rule combining every 50 cycles
agent.predtol = 20.0 # combines rules whose prediction value differences <= 20.0
agent.prederrtol = 10.0 # remove if error > 10.0, after previously below it
```


**Latest updates**
* ~~all related to mutation and crossover is removed~~
* ~~dependencies like pandas and numpy are removed, as well as data science features~~

---

## Results

**Classical Problems: `multiplexer` and `Markov environment`:**

![Binary MP11-HIGH](https://raw.githubusercontent.com/nuggfr/xcs-rc-python/master/xcs-rc-mp11-binary.png)

![Real MP6-HIGH](https://raw.githubusercontent.com/nuggfr/xcs-rc-python/master/xcs-rc-mp6-real.png)

![Markov Maze4](https://raw.githubusercontent.com/nuggfr/xcs-rc-python/master/xcs-rc-markov-maze4.png)

**Flappy Bird from PyGame Learning Environment:**

![Flappy Bird XCS-RC plot](https://raw.githubusercontent.com/nuggfr/xcs-rc-python/master/flappy_plot.png)

[![Flappy Bird XCS-RC youtube](https://img.youtube.com/vi/Fz05s-stCbE/0.jpg)](https://youtu.be/Fz05s-stCbE)

**Youtube: CartPole-v0 Benchmark from OpenAI Gym:**

[![CartPole XCS-RC](https://img.youtube.com/vi/mJoavWV80MM/0.jpg)](https://youtu.be/mJoavWV80MM)
