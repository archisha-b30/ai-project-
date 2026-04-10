import json
import os
from datetime import datetime

class ConfigManager:
    """
    Configuration Manager for the Traffic Control System.
    Centralized configuration management with validation and persistence.
    """

    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.default_config = {
            'system': {
                'mode': 'simulate',  # simulate, live, hybrid
                'debug': False,
                'log_level': 'INFO',
                'max_intersections': 3
            },
            'vehicle_detection': {
                'model': 'yolov8n.pt',
                'confidence_threshold': 0.35,
                'lane_regions': {
                    'north': [0, 0, 320, 240],
                    'south': [320, 240, 640, 480],
                    'east': [320, 0, 640, 240],
                    'west': [0, 240, 320, 480]
                },
                'enabled_classes': ['car', 'truck', 'bus', 'motorcycle', 'ambulance']
            },
            'traffic_prediction': {
                'seq_length': 10,
                'predict_steps': 5,
                'lstm_hidden_size': 50,
                'epochs': 80,
                'enabled': True
            },
            'rl_control': {
                'enabled': True,
                'alpha': 0.2,
                'gamma': 0.9,
                'epsilon': 0.15,
                'min_duration': 15,
                'max_duration': 60,
                'training_episodes': 200
            },
            'environmental': {
                'track_emissions': True,
                'track_fuel': True,
                'eco_mode': False  # Prioritize environmental impact
            },
            'v2i_communication': {
                'enabled': True,
                'broadcast_interval': 1,  # seconds
                'support_emergency': True
            },
            'api': {
                'host': '0.0.0.0',
                'port': 5000,
                'debug': False,
                'enable_cors': True
            },
            'monitoring': {
                'enable_incident_detection': True,
                'enable_alerts': True,
                'alert_threshold_queue': 20,
                'alert_threshold_wait_time': 45
            }
        }
        
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from file or use defaults"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults (user config overrides defaults)
                    return {**self.default_config, **config}
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.default_config.copy()
        return self.default_config.copy()

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def get(self, key_path, default=None):
        """
        Get configuration value using dot notation.
        Example: get('rl_control.alpha') -> returns 0.2
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value

    def set(self, key_path, value):
        """
        Set configuration value using dot notation.
        Example: set('rl_control.alpha', 0.3)
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
        return self.save_config()

    def get_section(self, section):
        """Get entire configuration section"""
        return self.config.get(section, {})

    def update_section(self, section, updates):
        """Update entire configuration section"""
        if section in self.config:
            self.config[section].update(updates)
            return self.save_config()
        return False

    def validate_config(self):
        """Validate configuration values"""
        errors = []
        
        # Validate threshold values
        if self.get('rl_control.alpha', 0) < 0 or self.get('rl_control.alpha', 1) > 1:
            errors.append("RL alpha must be between 0 and 1")
        
        if self.get('rl_control.epsilon', 0) < 0 or self.get('rl_control.epsilon', 1) > 1:
            errors.append("RL epsilon must be between 0 and 1")
        
        if self.get('vehicle_detection.confidence_threshold', 0) < 0 or \
           self.get('vehicle_detection.confidence_threshold', 1) > 1:
            errors.append("Confidence threshold must be between 0 and 1")
        
        if self.get('api.port', 0) < 1 or self.get('api.port', 65535) > 65535:
            errors.append("API port must be between 1 and 65535")
        
        return errors

    def export_config(self, filename='config_export.json'):
        """Export configuration to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False

    def import_config(self, filename):
        """Import configuration from file"""
        try:
            with open(filename, 'r') as f:
                imported = json.load(f)
            self.config.update(imported)
            return self.save_config()
        except Exception as e:
            print(f"Error importing config: {e}")
            return False

    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.default_config.copy()
        return self.save_config()

    def get_summary(self):
        """Get configuration summary"""
        return {
            'system_mode': self.get('system.mode'),
            'detection_enabled': self.get('vehicle_detection.model') is not None,
            'prediction_enabled': self.get('traffic_prediction.enabled'),
            'rl_control_enabled': self.get('rl_control.enabled'),
            'v2i_enabled': self.get('v2i_communication.enabled'),
            'incident_detection': self.get('monitoring.enable_incident_detection'),
            'alerts_enabled': self.get('monitoring.enable_alerts'),
            'api_url': f"http://{self.get('api.host')}:{self.get('api.port')}",
            'last_saved': datetime.now().isoformat()
        }
