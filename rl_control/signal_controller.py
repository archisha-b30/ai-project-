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

    def calculate_reward(self, lane_counts, action, served_vehicles, eco_mode=False, avg_wait_time=0):
        """
        Enhanced multi-objective reward function.
        Balances: traffic flow, congestion, wait time, environmental impact, and fairness.
        
        Args:
            lane_counts: vehicles per lane
            action: (lane, duration) tuple
            served_vehicles: number of vehicles that passed through
            eco_mode: if True, prioritize environmental impact
            avg_wait_time: average waiting time
        """
        total_queue = sum(lane_counts.values()) if isinstance(lane_counts, dict) else lane_counts
        green_lane, duration = action
        
        # Base reward: vehicles served
        reward = served_vehicles * 2.5
        
        # Penalty: total queue length
        queue_penalty = total_queue * 0.3
        reward -= queue_penalty
        
        # Penalty: signal duration (encourage shorter cycles where possible)
        duration_penalty = duration * 0.05
        reward -= duration_penalty
        
        # Penalty: average waiting time
        wait_penalty = min(avg_wait_time * 0.1, 10)
        reward -= wait_penalty
        
        # Environmental bonus (in eco mode)
        if eco_mode:
            # Reward for reducing idle time
            reward += (60 - duration) * 0.15
        
        # Fairness penalty: distribute green time fairly across lanes
        if isinstance(lane_counts, dict):
            lane_values = list(lane_counts.values())
            if lane_values:
                avg_queue = sum(lane_values) / len(lane_values)
                max_queue = max(lane_values)
                if max_queue > avg_queue * 2:
                    fairness_bonus = 2  # Reward if selecting high-queue lane
                    reward += fairness_bonus
        
        # Heavy congestion penalty
        if total_queue > 40:
            reward -= 8
        elif total_queue > 30:
            reward -= 5
        
        # Reward for good traffic flow
        if served_vehicles > 15:
            reward += 3
        
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
