import numpy as np

class EnvironmentalTracker:
    """
    Tracks environmental impact of traffic patterns.
    Calculates CO2 emissions, fuel consumption, and provides eco-friendly signal optimization.
    """

    def __init__(self):
        # Emission factors (g CO2 per km)
        self.emission_factors = {
            'car': 120,
            'bus': 60,      # Per passenger (assume 40 passengers)
            'truck': 250,
            'motorcycle': 80
        }
        
        # Fuel consumption factors (L per 100 km)
        self.fuel_consumption = {
            'car': 7.0,
            'bus': 25.0,
            'truck': 30.0,
            'motorcycle': 3.5
        }
        
        self.total_emissions = 0
        self.total_fuel_consumed = 0
        self.idling_time = 0  # Vehicles idling at signals
        self.emission_history = []
        self.avg_speed = 20  # Default average speed in km/h

    def calculate_emissions_for_vehicles(self, vehicle_counts, distance=1.0):
        """
        Calculate CO2 emissions for current traffic snapshot.
        
        Args:
            vehicle_counts: dict with vehicle types and counts
            distance: distance traveled (km)
        
        Returns:
            emissions_data: dict with total and per-vehicle emissions
        """
        total_emissions = 0
        emissions_by_type = {}
        
        for vehicle_type, count in vehicle_counts.items():
            if vehicle_type not in self.emission_factors:
                continue
            
            emissions = count * self.emission_factors[vehicle_type] * distance
            emissions_by_type[vehicle_type] = emissions
            total_emissions += emissions
        
        self.total_emissions += total_emissions
        self.emission_history.append(total_emissions)
        
        return {
            'total_emissions_g': total_emissions,
            'total_emissions_kg': total_emissions / 1000,
            'by_vehicle_type': emissions_by_type
        }

    def calculate_idling_emissions(self, vehicle_counts, time_seconds):
        """
        Calculate emissions from idling vehicles at traffic signals.
        Idling produces 2-3x normal emissions.
        """
        idling_multiplier = 2.5
        total_idling_emissions = 0
        
        for vehicle_type, count in vehicle_counts.items():
            if vehicle_type not in self.emission_factors:
                continue
            
            # Idling produces less CO2 (0.25 g CO2 per second per vehicle)
            idling_emissions = count * time_seconds * 0.25 * idling_multiplier
            total_idling_emissions += idling_emissions
        
        self.idling_time += time_seconds
        self.total_emissions += total_idling_emissions
        
        return total_idling_emissions

    def calculate_fuel_consumption(self, vehicle_counts, distance=1.0):
        """Calculate fuel consumption for current traffic"""
        total_fuel = 0
        fuel_by_type = {}
        
        for vehicle_type, count in vehicle_counts.items():
            if vehicle_type not in self.fuel_consumption:
                continue
            
            fuel = (count * self.fuel_consumption[vehicle_type] * distance) / 100
            fuel_by_type[vehicle_type] = fuel
            total_fuel += fuel
        
        self.total_fuel_consumed += total_fuel
        return {
            'total_liters': total_fuel,
            'by_vehicle_type': fuel_by_type,
            'co2_from_fuel': total_fuel * 2.31  # 1L fuel ≈ 2.31 kg CO2
        }

    def calculate_eco_score(self, lane_counts, average_wait_time):
        """
        Calculate environmental friendliness score (0-100).
        Lower waiting time and smoother flow = lower emissions.
        """
        # Normalize wait time (0-60 seconds is normal)
        wait_penalty = min(average_wait_time / 60 * 50, 50)
        
        # Calculate emissions per vehicle
        total_vehicles = sum(lane_counts.values()) if isinstance(lane_counts, dict) else lane_counts
        emissions_per_vehicle = self.total_emissions / (total_vehicles + 1)
        
        # Normalize emissions (baseline: 500g per vehicle)
        emission_penalty = min(emissions_per_vehicle / 500 * 50, 50)
        
        eco_score = 100 - wait_penalty - emission_penalty
        return max(0, min(100, eco_score))

    def get_emission_report(self):
        """Generate comprehensive emission report"""
        avg_emissions = np.mean(self.emission_history) if self.emission_history else 0
        
        return {
            'total_emissions_kg': self.total_emissions / 1000,
            'total_fuel_liters': self.total_fuel_consumed,
            'idling_time_seconds': self.idling_time,
            'average_emissions': avg_emissions,
            'estimated_trees_needed': (self.total_emissions / 1000) / 20,  # 1 tree absorbs ~20kg CO2/year
            'equivalent_car_km': (self.total_emissions / 1000) / (120 / 1000)  # Equivalent km for car
        }

    def recommend_eco_optimization(self, current_eco_score):
        """Recommend actions to improve environmental impact"""
        recommendations = []
        
        if current_eco_score < 40:
            recommendations.append("High emissions detected - Consider extending green phases to reduce stop-and-go")
        
        if self.idling_time > 3600:  # Over 1 hour
            recommendations.append("Excessive idling detected - Optimize signal timing to reduce waiting")
        
        if self.total_fuel_consumed > 100:
            recommendations.append("High fuel consumption - Prioritize public transport routes")
        
        if current_eco_score >= 80:
            recommendations.append("Excellent! Current signal timing is eco-friendly")
        
        return recommendations

    def reset_tracking(self):
        """Reset all tracking data"""
        self.total_emissions = 0
        self.total_fuel_consumed = 0
        self.idling_time = 0
        self.emission_history = []
