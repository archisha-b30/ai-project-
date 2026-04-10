import numpy as np
from collections import deque

class IncidentDetector:
    """
    Detects traffic incidents (accidents, breakdowns) using anomaly detection.
    Monitors sudden traffic flow disruptions, congestion spikes, and stationary vehicles.
    """

    def __init__(self, window_size=10, anomaly_threshold=2.0):
        self.window_size = window_size
        self.anomaly_threshold = anomaly_threshold
        self.traffic_history = deque(maxlen=window_size)
        self.stationary_vehicles = {}
        self.incidents = []

    def update_traffic(self, lane_counts):
        """Track traffic flow over time"""
        total = sum(lane_counts.values()) if isinstance(lane_counts, dict) else lane_counts
        self.traffic_history.append(total)

    def detect_congestion_spike(self):
        """Detect sudden increase in traffic (potential accident)"""
        if len(self.traffic_history) < 3:
            return False
        
        recent = list(self.traffic_history)
        avg_recent = np.mean(recent[-3:])
        avg_historical = np.mean(recent[:5]) if len(recent) > 5 else avg_recent
        
        spike_ratio = avg_recent / (avg_historical + 1e-5)
        is_spike = spike_ratio > self.anomaly_threshold
        
        if is_spike:
            self.incidents.append({
                'type': 'congestion_spike',
                'severity': (spike_ratio - 1) * 100,
                'current_traffic': avg_recent
            })
        
        return is_spike

    def detect_stationary_congestion(self, lane_counts):
        """Detect stationary vehicles (queue buildup)"""
        incidents = []
        for lane, count in (lane_counts.items() if isinstance(lane_counts, dict) else [('all', lane_counts)]):
            if count > 20:  # High queue threshold
                if lane not in self.stationary_vehicles:
                    self.stationary_vehicles[lane] = 0
                self.stationary_vehicles[lane] += 1
                
                if self.stationary_vehicles[lane] > 5:  # Sustained high queue
                    incidents.append({
                        'lane': lane,
                        'type': 'queue_buildup',
                        'queue_length': count,
                        'duration': self.stationary_vehicles[lane]
                    })
            else:
                self.stationary_vehicles[lane] = 0
        
        return incidents

    def get_incidents(self):
        """Get all detected incidents"""
        return self.incidents

    def clear_incidents(self):
        """Clear incident history"""
        self.incidents = []

    def recommend_action(self):
        """Suggest actions based on detected incidents"""
        if not self.incidents:
            return None
        
        latest_incident = self.incidents[-1]
        
        if latest_incident['type'] == 'congestion_spike':
            return {
                'action': 'activate_incident_mode',
                'priority': 'high',
                'recommendation': 'Consider emergency signal override or rerouting'
            }
        elif latest_incident['type'] == 'queue_buildup':
            return {
                'action': 'extend_green_phase',
                'lane': latest_incident['lane'],
                'priority': 'medium',
                'recommendation': f"Extend green phase for {latest_incident['lane']} lane"
            }
        
        return None
