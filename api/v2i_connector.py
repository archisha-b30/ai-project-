import json
from datetime import datetime

class V2IConnector:
    """
    Vehicle-to-Infrastructure (V2I) Communication System.
    Enables connected vehicles to communicate with traffic signal controller.
    Supports real-time traffic data exchange and signal recommendations.
    """

    def __init__(self):
        self.connected_vehicles = {}  # {vehicle_id: vehicle_data}
        self.communication_log = []
        self.signal_broadcasts = []

    def register_vehicle(self, vehicle_id, vehicle_type='car', location=None):
        """Register a connected vehicle"""
        vehicle = {
            'id': vehicle_id,
            'type': vehicle_type,  # car, bus, ambulance, etc.
            'location': location,
            'status': 'active',
            'registered_at': datetime.now()
        }
        self.connected_vehicles[vehicle_id] = vehicle
        self.log_communication('register', vehicle_id, 'Vehicle registered')
        return vehicle

    def receive_vehicle_data(self, vehicle_id, data):
        """Receive real-time data from connected vehicle"""
        if vehicle_id not in self.connected_vehicles:
            return {'error': 'Vehicle not registered'}
        
        vehicle_update = {
            'vehicle_id': vehicle_id,
            'gps': data.get('gps'),
            'speed': data.get('speed'),
            'heading': data.get('heading'),
            'is_emergency': data.get('is_emergency', False),
            'timestamp': datetime.now()
        }
        
        self.connected_vehicles[vehicle_id].update(vehicle_update)
        self.log_communication('update', vehicle_id, f"Speed: {data.get('speed')} km/h")
        return {'status': 'received'}

    def broadcast_signal_advice(self, signal_status, next_signal, countdown):
        """Broadcast signal timing info to vehicles ahead"""
        broadcast = {
            'current_light': signal_status,
            'next_light': next_signal,
            'countdown_seconds': countdown,
            'timestamp': datetime.now(),
            'vehicles_notified': len(self.connected_vehicles)
        }
        self.signal_broadcasts.append(broadcast)
        return broadcast

    def recommend_route_to_vehicle(self, vehicle_id, congested_lanes, alternative_route=None):
        """Send route recommendations to vehicle"""
        recommendation = {
            'vehicle_id': vehicle_id,
            'message': f'Avoid lanes: {congested_lanes}',
            'alternative': alternative_route,
            'priority': 'medium' if vehicle_id in self.get_emergency_vehicles() else 'low'
        }
        self.log_communication('recommendation', vehicle_id, recommendation['message'])
        return recommendation

    def get_emergency_vehicles(self):
        """Get list of emergency vehicles (ambulances, fire trucks)"""
        return [v_id for v_id, data in self.connected_vehicles.items() 
                if data.get('is_emergency', False)]

    def prioritize_emergency(self, vehicle_id):
        """Handle emergency vehicle priority"""
        if vehicle_id not in self.connected_vehicles:
            return {'error': 'Vehicle not found'}
        
        priority_signal = {
            'vehicle_id': vehicle_id,
            'action': 'all_green',
            'override': True,
            'message': 'Emergency vehicle - all lanes cleared'
        }
        self.log_communication('emergency', vehicle_id, 'Emergency priority activated')
        return priority_signal

    def log_communication(self, comm_type, vehicle_id, message):
        """Log all V2I communications"""
        log_entry = {
            'time': datetime.now().isoformat(),
            'type': comm_type,
            'vehicle_id': vehicle_id,
            'message': message
        }
        self.communication_log.append(log_entry)

    def get_statistics(self):
        """Get V2I system statistics"""
        emergency_vehicles = self.get_emergency_vehicles()
        return {
            'total_connected': len(self.connected_vehicles),
            'emergency_vehicles': len(emergency_vehicles),
            'total_communications': len(self.communication_log),
            'broadcasts_sent': len(self.signal_broadcasts)
        }

    def get_communication_log(self, limit=20):
        """Get recent communications"""
        return self.communication_log[-limit:]
