import argparse
import os
import sys
import numpy as np

# Add current directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from simulation.traffic_simulation import TrafficSimulation
from prediction.traffic_predictor import TrafficPredictor
from rl_control.signal_controller import RLSignalController
from rl_control.traffic_env import TrafficEnvironment
from detection.vehicle_detector import VehicleDetector


def train_rl_agent(episodes=200):
    env = TrafficEnvironment(max_steps=40)
    controller = RLSignalController()
    print(f'Training RL agent for {episodes} episodes...')
    controller.train(env, episodes=episodes)
    print('RL agent training complete')
    return controller


def run_simulation():
    sample_data = [int(x) for x in np.random.normal(loc=25, scale=8, size=120).clip(min=0)]
    predictor = TrafficPredictor(seq_length=10, predict_steps=5)
    predictor.train(sample_data, epochs=80)
    predictions = predictor.predict(sample_data[-10:])

    sim = TrafficSimulation(num_intersections=3)
    print('Starting traffic simulation...')
    sim.run_simulation(80)
    metrics = sim.get_metrics()

    print('Prediction sample:', predictions)
    print('Simulation metrics:')
    for intersection, stats in metrics.items():
        if intersection == 'time_step':
            continue
        print(f"{intersection}: signal={stats['signal']}, emergency={stats['emergency_lane']}, queues={stats['queue_lengths']}")
    print('Completed. To open the dashboard, run: python api/app.py')


def run_webcam_demo():
    detector = VehicleDetector()
    print('Starting webcam traffic detection. Press q to stop.')
    detector.process_webcam(output_counts=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AI Traffic Congestion Control System')
    parser.add_argument('--mode', choices=['simulate', 'train_rl', 'webcam'], default='simulate')
    args = parser.parse_args()

    if args.mode == 'simulate':
        run_simulation()
    elif args.mode == 'train_rl':
        train_rl_agent(episodes=200)
    elif args.mode == 'webcam':
        run_webcam_demo()
