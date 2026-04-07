import random

class RLSignalController:
    """
    Reinforcement Learning Signal Controller using Q-learning.
    Optimizes traffic signals to minimize waiting time and congestion.
    """

    def __init__(self, lanes=None, durations=None):
        self.lanes = lanes or ['north', 'south', 'east', 'west']
        self.durations = durations or [15, 30, 45]
        self.actions = [(lane, dur) for lane in self.lanes for dur in self.durations]
        self.q_table = {}
        self.alpha = 0.2
        self.gamma = 0.9
        self.epsilon = 0.15

    def get_state(self, lane_counts, current_signal):
        counts = [min(int(lane_counts.get(lane, 0) / 3), 4) for lane in self.lanes]
        signal_index = self.lanes.index(current_signal) if current_signal in self.lanes else 0
        return tuple(counts + [signal_index])

    def choose_action(self, state):
        if random.random() < self.epsilon or state not in self.q_table:
            return random.choice(self.actions)
        return max(self.q_table[state], key=self.q_table[state].get)

    def update_q(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0.0 for a in self.actions}
        old_value = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values())
        self.q_table[state][action] = old_value + self.alpha * (reward + self.gamma * next_max - old_value)

    def get_signal_decision(self, lane_counts, current_signal):
        state = self.get_state(lane_counts, current_signal)
        return self.choose_action(state)

    def calculate_reward(self, lane_counts, action, served_vehicles):
        total_queue = sum(lane_counts.values())
        green_lane, duration = action
        reward = served_vehicles * 2 - total_queue - duration * 0.05
        if total_queue > 30:
            reward -= 5
        return reward

    def train(self, env, episodes=500, max_steps=50):
        for episode in range(episodes):
            state = env.reset()
            done = False
            step_count = 0
            while not done and step_count < max_steps:
                action = self.choose_action(state)
                next_state, reward, done = env.step(action)
                self.update_q(state, action, reward, next_state)
                state = next_state
                step_count += 1

    def get_best_action(self, lane_counts, current_signal):
        state = self.get_state(lane_counts, current_signal)
        if state not in self.q_table:
            return random.choice(self.actions)
        return max(self.q_table[state], key=self.q_table[state].get)
