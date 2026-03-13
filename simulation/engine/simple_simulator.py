import copy
from config import Config

class SimpleNetworkSimulator:
    """
    Provides deterministic "What-If" forecasting for the 5G Digital Twin.
    It projects future network states based on current trends without impacting the live system.
    """

    def __init__(self, network_state):
        """
        Initializes the simulator with a reference to the live NetworkState.
        """
        self.network_state = network_state

    def simulate(self, steps: int) -> dict:
        """
        Projects the network state forward by a fixed number of steps.
        
        Rules:
        - If utilization > Threshold: Increases by 0.05 per step.
        - If utilization <= Threshold: Decreases by 0.05 per step.
        - Latency is updated proportionally to utilization.
        
        Returns a dictionary representing the projected future state.
        """
        # 1. Create a deep copy of the current state to avoid side effects
        future_state = copy.deepcopy(self.network_state.get_all_cells())

        # 2. Project forward for 'steps' iterations
        for _ in range(steps):
            for cell_id, snapshot in future_state.items():
                current_util = snapshot.get("utilization", 0.0)

                # Trend logic
                if current_util > Config.CONGESTION_UTILIZATION_THRESHOLD:
                    new_util = current_util + 0.05
                else:
                    new_util = current_util - 0.05

                # Clamp values
                new_util = max(Config.MIN_UTILIZATION, min(Config.MAX_UTILIZATION, new_util))
                snapshot["utilization"] = round(new_util, 4)

                # Proportional latency update (Base 10ms + 50ms congestion factor)
                snapshot["average_latency_ms"] = round(10.0 + (new_util * 50.0), 2)
                
                # Advance timestamp in the projection
                snapshot["timestamp"] += 1

        return future_state
