from datetime import datetime, timedelta
from enum import Enum
import json

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class AlertType(Enum):
    HIGH_CONGESTION = "high_congestion"
    INCIDENT_DETECTED = "incident_detected"
    LONG_WAIT_TIME = "long_wait_time"
    QUEUE_BUILDUP = "queue_buildup"
    EMERGENCY_VEHICLE = "emergency_vehicle"
    SIGNAL_MALFUNCTION = "signal_malfunction"
    ENVIRONMENTAL_ALERT = "environmental_alert"
    PREDICTION_SPIKE = "prediction_spike"

class TrafficAlert:
    """Represents a single traffic alert"""
    
    def __init__(self, alert_type, severity, message, lane=None, data=None):
        self.alert_type = alert_type
        self.severity = severity
        self.message = message
        self.lane = lane
        self.data = data or {}
        self.created_at = datetime.now()
        self.acknowledged = False
        self.id = f"{int(self.created_at.timestamp() * 1000)}"

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.alert_type.value,
            'severity': self.severity.value,
            'message': self.message,
            'lane': self.lane,
            'data': self.data,
            'created_at': self.created_at.isoformat(),
            'acknowledged': self.acknowledged
        }

class AlertManager:
    """
    Centralized Alert Management System.
    Monitors traffic conditions and generates proactive alerts.
    """

    def __init__(self, max_alerts=100):
        self.alerts = []
        self.max_alerts = max_alerts
        self.alert_subscriptions = {}  # For alert notifications
        self.threshold_config = {
            'queue_length': 20,
            'wait_time': 45,
            'congestion_spike': 1.5,
            'emission_warning': 5000
        }

    def create_alert(self, alert_type, severity, message, lane=None, data=None):
        """Create a new alert"""
        alert = TrafficAlert(alert_type, severity, message, lane, data)
        
        # Prevent duplicate alerts within 30 seconds
        if not self._is_duplicate(alert):
            self.alerts.append(alert)
            
            # Keep only max_alerts recent alerts
            if len(self.alerts) > self.max_alerts:
                self.alerts = self.alerts[-self.max_alerts:]
            
            # Notify subscribers
            self._notify_subscribers(alert)
            return alert
        
        return None

    def acknowledge_alert(self, alert_id):
        """Mark alert as acknowledged"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                return True
        return False

    def _is_duplicate(self, new_alert):
        """Check if similar alert exists within 30 seconds"""
        cutoff_time = datetime.now() - timedelta(seconds=30)
        
        for alert in self.alerts:
            if (alert.alert_type == new_alert.alert_type and
                alert.lane == new_alert.lane and
                alert.created_at > cutoff_time):
                return True
        
        return False

    def _notify_subscribers(self, alert):
        """Notify subscribed systems of new alert"""
        if alert.alert_type in self.alert_subscriptions:
            for callback in self.alert_subscriptions[alert.alert_type]:
                try:
                    callback(alert)
                except Exception as e:
                    print(f"Error notifying subscriber: {e}")

    def subscribe_to_alerts(self, alert_type, callback):
        """Subscribe to specific alert types"""
        if alert_type not in self.alert_subscriptions:
            self.alert_subscriptions[alert_type] = []
        self.alert_subscriptions[alert_type].append(callback)

    def check_high_congestion(self, lane_counts):
        """Check for high congestion conditions"""
        for lane, count in lane_counts.items():
            if count > self.threshold_config['queue_length']:
                message = f"High congestion on {lane} lane: {count} vehicles"
                self.create_alert(
                    AlertType.HIGH_CONGESTION,
                    AlertSeverity.WARNING,
                    message,
                    lane,
                    {'queue_length': count}
                )

    def check_wait_time(self, lane_wait_times):
        """Check for excessive wait times"""
        for lane, wait_time in lane_wait_times.items():
            if wait_time > self.threshold_config['wait_time']:
                message = f"Long wait time on {lane}: {wait_time:.1f} seconds"
                self.create_alert(
                    AlertType.LONG_WAIT_TIME,
                    AlertSeverity.WARNING,
                    message,
                    lane,
                    {'wait_time': wait_time}
                )

    def check_incident(self, incident_data):
        """Alert about detected incidents"""
        severity = AlertSeverity.CRITICAL if incident_data.get('severity', 0) > 50 else AlertSeverity.WARNING
        
        message = f"Incident detected: {incident_data.get('type', 'unknown')}"
        self.create_alert(
            AlertType.INCIDENT_DETECTED,
            severity,
            message,
            data=incident_data
        )

    def check_emergency_vehicle(self, vehicle_id, vehicle_type):
        """Alert about emergency vehicles"""
        message = f"Emergency vehicle detected: {vehicle_type} (ID: {vehicle_id})"
        self.create_alert(
            AlertType.EMERGENCY_VEHICLE,
            AlertSeverity.CRITICAL,
            message,
            data={'vehicle_id': vehicle_id, 'type': vehicle_type}
        )

    def check_prediction_spike(self, predicted_traffic, current_traffic, threshold_multiplier=1.5):
        """Alert about predicted traffic spikes"""
        if predicted_traffic > current_traffic * threshold_multiplier:
            spike_percent = ((predicted_traffic - current_traffic) / current_traffic) * 100
            message = f"Traffic spike predicted: +{spike_percent:.0f}% in next forecast period"
            self.create_alert(
                AlertType.PREDICTION_SPIKE,
                AlertSeverity.WARNING,
                message,
                data={
                    'current': current_traffic,
                    'predicted': predicted_traffic,
                    'spike_percent': spike_percent
                }
            )

    def check_environmental_impact(self, eco_score):
        """Alert about poor environmental impact"""
        if eco_score < 40:
            message = f"Low eco score: {eco_score:.0f}/100 - High emissions detected"
            self.create_alert(
                AlertType.ENVIRONMENTAL_ALERT,
                AlertSeverity.WARNING,
                message,
                data={'eco_score': eco_score}
            )

    def get_alerts(self, alert_type=None, severity=None, since=None):
        """Get alerts with optional filtering"""
        filtered_alerts = self.alerts
        
        if alert_type:
            filtered_alerts = [a for a in filtered_alerts if a.alert_type == alert_type]
        
        if severity:
            filtered_alerts = [a for a in filtered_alerts if a.severity == severity]
        
        if since:
            filtered_alerts = [a for a in filtered_alerts if a.created_at > since]
        
        return [alert.to_dict() for alert in filtered_alerts]

    def get_unacknowledged_alerts(self):
        """Get all unacknowledged alerts"""
        return [alert.to_dict() for alert in self.alerts if not alert.acknowledged]

    def get_alerts_by_severity(self):
        """Get alert count by severity"""
        severity_count = {
            'info': len([a for a in self.alerts if a.severity == AlertSeverity.INFO]),
            'warning': len([a for a in self.alerts if a.severity == AlertSeverity.WARNING]),
            'critical': len([a for a in self.alerts if a.severity == AlertSeverity.CRITICAL])
        }
        return severity_count

    def get_alert_summary(self):
        """Get summary of recent alerts"""
        return {
            'total_alerts': len(self.alerts),
            'unacknowledged': len([a for a in self.alerts if not a.acknowledged]),
            'by_severity': self.get_alerts_by_severity(),
            'recent': self.get_alerts()[-5:] if self.alerts else []
        }

    def clear_old_alerts(self, days=1):
        """Clear alerts older than specified days"""
        cutoff_time = datetime.now() - timedelta(days=days)
        self.alerts = [a for a in self.alerts if a.created_at > cutoff_time]

    def export_alerts(self, filename='alerts_export.json'):
        """Export all alerts to file"""
        try:
            with open(filename, 'w') as f:
                alerts_data = [alert.to_dict() for alert in self.alerts]
                json.dump(alerts_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error exporting alerts: {e}")
            return False
