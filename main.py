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
from rl_control.adaptive_time_controller import AdaptiveTimeController
from detection.vehicle_detector import VehicleDetector
from detection.incident_detector import IncidentDetector
from detection.environmental_tracker import EnvironmentalTracker
from api.v2i_connector import V2IConnector
from api.alert_manager import AlertManager, AlertType, AlertSeverity
from config_manager import ConfigManager


def train_rl_agent(episodes=200):
    env = TrafficEnvironment(max_steps=40)
    controller = RLSignalController()
    print(f'Training RL agent for {episodes} episodes...')
    controller.train(env, episodes=episodes)
    print('RL agent training complete')
    return controller


def run_simulation():
    print("=" * 60)
    print("🚦 AI TRAFFIC CONTROL SYSTEM - ENHANCED DEMO")
    print("=" * 60)
    
    # Initialize all new components
    print("\n📦 Initializing components...")
    config = ConfigManager()
    incident_detector = IncidentDetector()
    environmental_tracker = EnvironmentalTracker()
    v2i_connector = V2IConnector()
    alert_manager = AlertManager()
    adaptive_controller = AdaptiveTimeController()
    
    print("✓ Config Manager initialized")
    print("✓ Incident Detector ready")
    print("✓ Environmental Tracker active")
    print("✓ V2I Communication enabled")
    print("✓ Alert Manager online")
    print("✓ Adaptive Time Controller running")
    
    # Run traffic simulation
    print("\n🚗 Starting traffic simulation...")
    sample_data = [int(x) for x in np.random.normal(loc=25, scale=8, size=120).clip(min=0)]
    
    # Train predictor
    predictor = TrafficPredictor(seq_length=10, predict_steps=5)
    predictor.train(sample_data, epochs=80)
    predictions = predictor.predict(sample_data[-10:])
    
    # Run simulation
    sim = TrafficSimulation(num_intersections=3)
    sim.run_simulation(80)
    metrics = sim.get_metrics()
    
    print("✓ Simulation completed")
    
    # Demonstrate new features
    print("\n" + "=" * 60)
    print("📊 NEW FEATURES DEMONSTRATION")
    print("=" * 60)
    
    # 1. INCIDENT DETECTION
    print("\n🚨 1. INCIDENT DETECTION")
    print("-" * 40)
    test_lane_counts = {'north': 35, 'south': 28, 'east': 22, 'west': 18}
    incident_detector.update_traffic(sum(test_lane_counts.values()))
    incident_detector.update_traffic(50)  # Spike
    if incident_detector.detect_congestion_spike():
        print("⚠️  Congestion spike detected!")
        incidents = incident_detector.get_incidents()
        if incidents:
            print(f"   Severity: {incidents[-1]['severity']:.1f}%")
    
    # 2. ENVIRONMENTAL TRACKING
    print("\n♻️  2. ENVIRONMENTAL TRACKING")
    print("-" * 40)
    emissions_data = environmental_tracker.calculate_emissions_for_vehicles(
        {'car': 10, 'bus': 2, 'truck': 1}, distance=0.5
    )
    print(f"CO2 Emissions: {emissions_data['total_emissions_kg']:.2f} kg")
    
    eco_score = environmental_tracker.calculate_eco_score(test_lane_counts, avg_wait_time=35)
    print(f"Eco Score: {eco_score:.1f}/100")
    
    # 3. ADAPTIVE TIME-BASED SIGNALS
    print("\n⏰ 3. ADAPTIVE TIME-BASED SIGNALS")
    print("-" * 40)
    period = adaptive_controller.get_current_period()
    multiplier = adaptive_controller.get_signal_timing_multiplier()
    strategy = adaptive_controller.get_period_strategy()
    print(f"Current Period: {period} (multiplier: {multiplier}x)")
    print(f"Strategy: {strategy['description']}")
    print(f"Priority: {strategy['priority']}")
    
    # 4. V2I COMMUNICATION
    print("\n📡 4. VEHICLE-TO-INFRASTRUCTURE (V2I)")
    print("-" * 40)
    v2i_connector.register_vehicle('V001', vehicle_type='car')
    v2i_connector.register_vehicle('V002', vehicle_type='ambulance')
    
    v2i_connector.receive_vehicle_data('V001', {
        'gps': (40.7128, -74.0060),
        'speed': 35,
        'heading': 180,
        'is_emergency': False
    })
    
    v2i_connector.broadcast_signal_advice('red', 'green', 15)
    v2i_stats = v2i_connector.get_statistics()
    print(f"Connected Vehicles: {v2i_stats['total_connected']}")
    print(f"Emergency Vehicles: {v2i_stats['emergency_vehicles']}")
    print(f"V2I Communications: {v2i_stats['total_communications']}")
    
    # 5. TRAFFIC ALERTS
    print("\n🔔 5. TRAFFIC ALERT SYSTEM")
    print("-" * 40)
    alert_manager.check_high_congestion(test_lane_counts)
    alert_manager.check_wait_time({'north': 50, 'south': 35})
    alert_manager.check_incident({'type': 'accident', 'severity': 75})
    
    alert_summary = alert_manager.get_alert_summary()
    print(f"Total Alerts: {alert_summary['total_alerts']}")
    print(f"Critical: {alert_summary['by_severity']['critical']}")
    print(f"Warnings: {alert_summary['by_severity']['warning']}")
    
    # 6. CONFIGURATION MANAGEMENT
    print("\n⚙️  6. CONFIGURATION MANAGEMENT")
    print("-" * 40)
    config_summary = config.get_summary()
    print(f"System Mode: {config_summary['system_mode']}")
    print(f"Prediction Enabled: {config_summary['prediction_enabled']}")
    print(f"V2I Enabled: {config_summary['v2i_enabled']}")
    print(f"Alerts Enabled: {config_summary['alerts_enabled']}")
    print(f"API Endpoint: {config_summary['api_url']}")
    
    # Original simulation results
    print("\n" + "=" * 60)
    print("📈 ORIGINAL SIMULATION RESULTS")
    print("=" * 60)
    print('\nPrediction sample:', predictions)
    print('\nSimulation metrics:')
    for intersection, stats in metrics.items():
        if intersection == 'time_step':
            continue
        print(f"{intersection}: signal={stats['signal']}, emergency={stats['emergency_lane']}, queues={stats['queue_lengths']}")
    
    print('\n' + "=" * 60)
    print("✅ ENHANCED DEMO COMPLETED")
    print("=" * 60)
    print('\nTo open the dashboard, run: python api/app.py')


def run_webcam_demo():
    detector = VehicleDetector()
    print('Starting webcam traffic detection. Press q to stop.')
    detector.process_webcam(output_counts=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AI Traffic Congestion Control System')
    parser.add_argument('--mode', choices=['simulate', 'train_rl', 'webcam', 'enhanced'], default='enhanced')
    args = parser.parse_args()

    if args.mode == 'simulate':
        run_simulation()
    elif args.mode == 'train_rl':
        train_rl_agent(episodes=200)
    elif args.mode == 'webcam':
        run_webcam_demo()
    elif args.mode == 'enhanced':
        run_simulation()
