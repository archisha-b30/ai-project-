import random
from simulation.traffic_simulation import TrafficSimulation, Vehicle

class TrafficEnvironment:
    """
    Training environment for the traffic signal RL controller.
    Uses a single intersection and returns state, reward, done.
    """

    def __init__(self, max_steps=50):
        self.max_steps = max_steps
        self.time_step = 0
        self.sim = None

    def reset(self):
        self.sim = TrafficSimulation(num_intersections=1)
        intersection = self.sim.intersections[0]
        for lane in intersection.lanes:
            for _ in range(random.randint(1, 5)):
                intersection.add_vehicle(lane, Vehicle(vehicle_type=random.choice(['car', 'truck', 'bus', 'motorcycle'])))
        self.time_step = 0
        return self._get_state()

    def _get_state(self):
        intersection = self.sim.intersections[0]
        lane_counts = intersection.get_lane_counts()
        signal_index = intersection.controller.lanes.index(intersection.signal)
        return tuple(min(int(lane_counts[lane] / 3), 4) for lane in intersection.controller.lanes) + (signal_index,)

    def step(self, action):
        intersection = self.sim.intersections[0]
        lane_counts_before = intersection.get_lane_counts()
        served = intersection.apply_action(action)
        reward = intersection.controller.calculate_reward(lane_counts_before, action, served)
        self.time_step += 1
        done = self.time_step >= self.max_steps
        next_state = self._get_state()
        return next_state, reward, done
