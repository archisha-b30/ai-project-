# AI Traffic Congestion Control System

This project implements an AI-powered traffic congestion control system using computer vision, machine learning, and reinforcement learning to detect traffic, predict congestion, and dynamically control traffic signals across multiple intersections.

## Features

- **Real-time Vehicle Detection**: Uses YOLOv8 to detect cars, trucks, buses, motorcycles from video input.
- **Traffic Density Analysis**: Computes density per lane and classifies as LOW, MEDIUM, HIGH.
- **Traffic Prediction**: Implements LSTM for time-series prediction of future traffic (next 10-15 minutes).
- **Reinforcement Learning Signal Controller**: Uses Q-learning to optimize traffic signals, minimizing waiting time and queue length.
- **Multi-Intersection Simulation**: Simulates 2-3 connected intersections with coordination.
- **Emergency Vehicle Detection**: Detects ambulances and overrides green signal priority.
- **Flask Backend API**: Provides endpoints for detection, prediction, signal decisions, metrics, simulation steps, and predictor training.
- **Web Dashboard**: Displays live vehicle count, density classification, prediction chart, signal status, and simulation metrics.

## Tech Stack

- Python
- OpenCV, YOLOv8 (Ultralytics)
- PyTorch
- NumPy, Pandas
- Flask
- HTML, CSS, JavaScript, Chart.js

## Project Structure

```
/project
├── detection/
│   ├── vehicle_detector.py
│   └── traffic_density.py
├── prediction/
│   └── traffic_predictor.py
├── rl_control/
│   └── signal_controller.py
├── simulation/
│   └── traffic_simulation.py
├── api/
│   └── app.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── data/  # For sample data
├── main.py
├── requirements.txt
└── README.md
```

## Installation

1. Ensure Python 3.8+ is installed.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. The YOLOv8 model (`yolov8n.pt`) will be downloaded automatically on first use.

## Usage

### Running the Simulation (Console)

```
python main.py
```

This trains the predictor on sample data and runs a simulation, printing metrics.

### Running the Web Dashboard

```
python api/app.py
```

Open http://localhost:5000 in your browser to access the dashboard.

- Click "Detect Vehicles" to simulate detection.
- "Update Predictions" to refresh the prediction chart.
- "Get Signal" for current signal decision.
- "Run Step" to advance the simulation.
- "Update Metrics" to view current stats.

### Using with Real Video

Modify `detection/vehicle_detector.py` to accept video paths, and update `api/app.py` to handle file uploads.

## API Endpoints

- `GET /detect`: Simulates or processes a video path for vehicle detection and density analysis.
- `GET /predict`: Returns traffic predictions for the next forecast window.
- `GET /signal`: Returns the current RL-based signal decision and current active phase.
- `GET /metrics`: Returns intersection metrics including waiting times, queue lengths, and emergency lane status.
- `GET /step`: Advances the simulated multi-intersection environment by one time step.
- `POST /train_predictor`: Trains or retrains the prediction model using provided history data.

## Metrics Calculated

- Average waiting time per vehicle
- Queue length per lane
- Traffic throughput (vehicles passed per time)
- Prediction accuracy (compared to actual if available)

## Example Output

Dashboard displays:
- Live vehicle counts per lane
- Prediction graph (line chart)
- Current signal status
- Simulation metrics in JSON format

## Code Quality

- Modular, object-oriented design
- Clear comments in each module
- Error handling and logging (basic)
- Sample data generation for demo

## Future Improvements

- Train RL on real traffic data
- Integrate real camera feeds
- Add more vehicle classes and emergency types
- Implement DQN for better RL performance
- Add user authentication for dashboard
- Deploy to cloud with real-time data

## License

MIT License