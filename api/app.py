from flask import Flask, jsonify, request
import random
import os
import sys
from collections import deque

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from detection.vehicle_detector import VehicleDetector
from detection.traffic_density import TrafficDensityAnalyzer
from prediction.traffic_predictor import TrafficPredictor
from simulation.traffic_simulation import TrafficSimulation

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
frontend_dir = os.path.join(base_dir, 'frontend')
app = Flask(__name__, static_folder=frontend_dir, static_url_path='')

sim = TrafficSimulation()
predictor = TrafficPredictor()
analyzer = TrafficDensityAnalyzer()
detector = VehicleDetector()
history = deque(maxlen=100)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/detect', methods=['GET'])
def detect():
    video_path = request.args.get('video_path')
    if video_path == 'webcam':
        frame_history = detector.process_webcam(output_counts=False)
    elif video_path and os.path.isfile(video_path):
        frame_history = detector.process_video(video_path, output_counts=False)
    else:
        frame_history = []

    if frame_history:
        latest = frame_history[-1]
        lane_counts = latest['lane_counts']
        total = sum(latest['total_counts'].values())
    else:
        lane_counts = {
            'north': {'car': random.randint(0, 10), 'truck': random.randint(0, 5), 'bus': random.randint(0, 3), 'motorcycle': random.randint(0, 4)},
            'south': {'car': random.randint(0, 10), 'truck': random.randint(0, 5), 'bus': random.randint(0, 3), 'motorcycle': random.randint(0, 4)},
            'east': {'car': random.randint(0, 10), 'truck': random.randint(0, 5), 'bus': random.randint(0, 3), 'motorcycle': random.randint(0, 4)},
            'west': {'car': random.randint(0, 10), 'truck': random.randint(0, 5), 'bus': random.randint(0, 3), 'motorcycle': random.randint(0, 4)}
        }
        total = sum(sum(l.values()) for l in lane_counts.values())

    densities = analyzer.analyze_density(lane_counts)
    history.append(total)
    return jsonify({'lane_counts': lane_counts, 'densities': densities, 'total': total})

@app.route('/predict')
def predict():
    try:
        if len(history) >= predictor.seq_length + predictor.predict_steps:
            if not predictor.trained:
                predictor.train(list(history), epochs=30)
            pred = predictor.predict(list(history))
        else:
            # Return average prediction if not enough history
            pred = [float(sum(history) / len(history)) if history else 0.0] * predictor.predict_steps
        
        return jsonify({'predictions': pred, 'history': list(history)})
    except Exception as e:
        print(f"Predict error: {e}")
        # Fallback to simple average
        pred = [float(sum(history) / len(history)) if history else 0.0] * predictor.predict_steps
        return jsonify({'predictions': pred, 'history': list(history)})

@app.route('/signal')
def signal():
    try:
        metrics = sim.get_metrics()
        intersection_0 = metrics.get('intersection_0', {})
        counts = intersection_0.get('queue_lengths', {})
        
        if not counts:
            counts = {'north': 0, 'south': 0, 'east': 0, 'west': 0}
        
        # Get signal decision from the intersection's controller
        decision = sim.intersections[0].controller.get_signal_decision(counts, sim.intersections[0].signal)
        
        return jsonify({
            'lane': decision[0], 
            'duration': decision[1], 
            'current_signal': sim.intersections[0].signal
        })
    except Exception as e:
        print(f"Signal error: {e}")
        return jsonify({'lane': 'north', 'duration': 30, 'current_signal': 'north', 'error': str(e)}), 500

@app.route('/metrics')
def metrics():
    return jsonify(sim.get_metrics())

@app.route('/step')
def step():
    sim.step()
    metrics = sim.get_metrics()
    counts = sum(metrics['intersection_0']['queue_lengths'].values())
    history.append(counts)
    return jsonify({'step': 'completed', 'counts': counts, 'metrics': metrics})

@app.route('/train_predictor', methods=['POST'])
def train_predictor():
    data = request.json.get('data', list(history))
    predictor.train(data, epochs=100)
    return jsonify({'status': 'trained', 'history_length': len(data)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
