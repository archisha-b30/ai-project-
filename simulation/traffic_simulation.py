import random
from rl_control.signal_controller import RLSignalController

class Vehicle:
    def __init__(self, vehicle_type='car'):
        self.type = vehicle_type
        self.waiting_time = 0

class Intersection:
    def __init__(self, lanes=None, max_queue=40):
        self.lanes = {lane: [] for lane in (lanes or ['north', 'south', 'east', 'west'])}
        self.signal = 'north'
        self.controller = RLSignalController(lanes=list(self.lanes.keys()))
        self.waiting_times = {lane: 0 for lane in self.lanes}
        self.emergency_lane = None
        self.max_queue = max_queue

    def add_vehicle(self, lane, vehicle):
        if len(self.lanes[lane]) < self.max_queue:
            self.lanes[lane].append(vehicle)

    def get_lane_counts(self):
        return {lane: len(queue) for lane, queue in self.lanes.items()}

    def get_queue_lengths(self):
        return self.get_lane_counts()

    def detect_emergency(self):
        for lane, queue in self.lanes.items():
            if any(v.type == 'ambulance' for v in queue):
                self.emergency_lane = lane
                return lane
        self.emergency_lane = None
        return None

    def apply_action(self, action):
        if self.detect_emergency():
            action = (self.emergency_lane, 15)
        self.signal = action[0]
        duration = action[1]
        served_capacity = max(1, min(len(self.lanes[self.signal]), int(duration / 15)))
        served = 0
        for _ in range(served_capacity):
            if self.lanes[self.signal]:
                self.lanes[self.signal].pop(0)
                served += 1
        for lane in self.lanes:
            for vehicle in self.lanes[lane]:
                vehicle.waiting_time += 1
            self.waiting_times[lane] = sum(v.waiting_time for v in self.lanes[lane])
        for lane in self.lanes:
            if random.random() < 0.25:
                self.add_vehicle(lane, Vehicle(vehicle_type=random.choice(['car', 'truck', 'bus', 'motorcycle'])))
        return served

class TrafficSimulation:
    """
    Simulates multi-intersection traffic system.
    """

    def __init__(self, num_intersections=3):
        self.intersections = [Intersection() for _ in range(num_intersections)]
        self.connections = [(i, i + 1) for i in range(num_intersections - 1)]
        self.time_step = 0

    def step(self):
        for intersection in self.intersections:
            intersection.apply_action(intersection.controller.get_signal_decision(intersection.get_lane_counts(), intersection.signal))
        for source_idx, dest_idx in self.connections:
            source = self.intersections[source_idx]
            dest = self.intersections[dest_idx]
            if source.signal == 'south' and len(dest.lanes['north']) < dest.max_queue * 0.8:
                transfers = min(2, len(source.lanes['south']))
                for _ in range(transfers):
                    vehicle = source.lanes['south'].pop(0)
                    dest.add_vehicle('north', vehicle)
        self.time_step += 1

    def run_simulation(self, steps=100):
        for _ in range(steps):
            self.step()

    def get_metrics(self):
        metrics = {}
        for idx, inter in enumerate(self.intersections):
            metrics[f'intersection_{idx}'] = {
                'waiting_times': inter.waiting_times,
                'queue_lengths': inter.get_queue_lengths(),
                'signal': inter.signal,
                'emergency_lane': inter.emergency_lane,
                'lane_counts': inter.get_lane_counts()
            }
        metrics['time_step'] = self.time_step
        return metrics