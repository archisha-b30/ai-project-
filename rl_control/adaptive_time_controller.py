from datetime import datetime, time

class AdaptiveTimeController:
    """
    Time-based Adaptive Traffic Signal Controller.
    Adjusts signal patterns based on time of day (rush hour, off-peak, night).
    Optimizes for different traffic patterns throughout the day.
    """

    def __init__(self):
        # Define time periods
        self.time_periods = {
            'early_morning': {'start': time(5, 0), 'end': time(7, 0), 'factor': 0.6},
            'morning_rush': {'start': time(7, 0), 'end': time(9, 30), 'factor': 1.5},
            'mid_morning': {'start': time(9, 30), 'end': time(12, 0), 'factor': 0.9},
            'lunch': {'start': time(12, 0), 'end': time(14, 0), 'factor': 1.2},
            'afternoon': {'start': time(14, 0), 'end': time(17, 0), 'factor': 0.85},
            'evening_rush': {'start': time(17, 0), 'end': time(19, 30), 'factor': 1.6},
            'evening': {'start': time(19, 30), 'end': time(21, 0), 'factor': 1.0},
            'night': {'start': time(21, 0), 'end': time(5, 0), 'factor': 0.4}
        }
        
        # Base signal timings (seconds)
        self.base_timings = {
            'min_green': 10,
            'max_green': 60,
            'yellow': 3,
            'all_red': 2
        }

    def get_current_period(self):
        """Determine current time period"""
        current = datetime.now().time()
        
        for period_name, period_data in self.time_periods.items():
            start = period_data['start']
            end = period_data['end']
            
            # Handle night period (crosses midnight)
            if start > end:
                if current >= start or current < end:
                    return period_name
            else:
                if start <= current < end:
                    return period_name
        
        return 'night'

    def get_signal_timing_multiplier(self):
        """Get signal duration multiplier for current time"""
        period = self.get_current_period()
        return self.time_periods[period]['factor']

    def calculate_adaptive_duration(self, base_duration, vehicle_count):
        """
        Calculate adaptive signal duration based on time and traffic.
        
        Args:
            base_duration: base signal duration in seconds
            vehicle_count: current number of vehicles
        
        Returns:
            adjusted_duration: optimized signal duration
        """
        time_multiplier = self.get_signal_timing_multiplier()
        
        # Traffic-based adjustment
        traffic_factor = min(1 + (vehicle_count / 50), 2.0)  # Cap at 2x
        
        adjusted = base_duration * time_multiplier * traffic_factor
        
        # Constrain to min/max
        adjusted = max(self.base_timings['min_green'], 
                      min(adjusted, self.base_timings['max_green']))
        
        return int(adjusted)

    def get_period_strategy(self):
        """Get signal strategy recommendations for current period"""
        period = self.get_current_period()
        strategies = {
            'early_morning': {
                'description': 'Light traffic - minimal signal changes needed',
                'priority': 'efficiency',
                'recommendations': [
                    'Use shorter green phases to save energy',
                    'Allow longer cycles between signal changes'
                ]
            },
            'morning_rush': {
                'description': 'Heavy incoming traffic from residential areas',
                'priority': 'throughput',
                'recommendations': [
                    'Extend green phases for major inbound routes',
                    'Implement signal coordination for arterial roads',
                    'Increase phase time by up to 50%'
                ]
            },
            'mid_morning': {
                'description': 'Moderate traffic - balanced flow',
                'priority': 'balance',
                'recommendations': [
                    'Use normal signal timing',
                    'Monitor for congestion hotspots'
                ]
            },
            'lunch': {
                'description': 'Mixed traffic - both inbound and outbound',
                'priority': 'balance',
                'recommendations': [
                    'Coordinate signals for distributed flow',
                    'Increase flexibility in phase timing'
                ]
            },
            'afternoon': {
                'description': 'Decreasing traffic from peak',
                'priority': 'efficiency',
                'recommendations': [
                    'Gradually reduce signal timing',
                    'Optimize for secondary routes'
                ]
            },
            'evening_rush': {
                'description': 'Heavy outbound traffic',
                'priority': 'throughput',
                'recommendations': [
                    'Extend green phases for outbound routes',
                    'Implement traffic signal progression',
                    'Increase phase time by up to 60%'
                ]
            },
            'evening': {
                'description': 'Declining traffic',
                'priority': 'balance',
                'recommendations': [
                    'Return to normal timing',
                    'Prepare for night mode'
                ]
            },
            'night': {
                'description': 'Very light traffic',
                'priority': 'minimal_stops',
                'recommendations': [
                    'Use flash mode for major intersections',
                    'Minimize signal changes',
                    'Prioritize emergency vehicles'
                ]
            }
        }
        
        return strategies.get(period, strategies['afternoon'])

    def get_peak_hours(self):
        """Get peak traffic hours"""
        return ['morning_rush', 'evening_rush']

    def is_peak_hour(self):
        """Check if current time is peak hour"""
        return self.get_current_period() in self.get_peak_hours()

    def get_time_based_signal_plan(self, lanes=['north', 'south', 'east', 'west']):
        """Generate time-based signal plan for all lanes"""
        period = self.get_current_period()
        multiplier = self.time_periods[period]['factor']
        
        signal_plan = {
            'period': period,
            'multiplier': multiplier,
            'lanes': {}
        }
        
        for lane in lanes:
            base_duration = self.base_timings['max_green'] / len(lanes)
            adjusted_duration = int(base_duration * multiplier)
            
            signal_plan['lanes'][lane] = {
                'green_duration': adjusted_duration,
                'yellow_duration': self.base_timings['yellow'],
                'all_red_duration': self.base_timings['all_red']
            }
        
        return signal_plan

    def log_period_change(self):
        """Log when period changes"""
        return {
            'timestamp': datetime.now().isoformat(),
            'period': self.get_current_period(),
            'multiplier': self.get_signal_timing_multiplier()
        }
