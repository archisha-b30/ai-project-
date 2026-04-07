import numpy as np

class TrafficDensityAnalyzer:
    """
    Analyzes traffic density per lane.
    Classifies as LOW, MEDIUM, HIGH.
    Maintains historical data.
    """

    def __init__(self, lane_areas=None):
        # Assume area for each lane
        if lane_areas is None:
            self.lane_areas = {'north': 100, 'south': 100, 'east': 100, 'west': 100}  # arbitrary units
        else:
            self.lane_areas = lane_areas
        self.history = []  # list of dicts

    def analyze_density(self, lane_counts):
        """
        lane_counts: dict of lane: dict of vehicle types
        Returns: dict of lane: density, classification
        """
        densities = {}
        for lane, counts in lane_counts.items():
            total_vehicles = sum(counts.values())
            density = total_vehicles / self.lane_areas[lane]
            if density < 0.5:
                level = 'LOW'
            elif density < 1.0:
                level = 'MEDIUM'
            else:
                level = 'HIGH'
            densities[lane] = {'density': density, 'level': level, 'count': total_vehicles}
        self.history.append(densities)
        return densities

    def get_historical_data(self):
        return self.history