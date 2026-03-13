from config import Config

class NetworkRiskAnalyzer:
    """
    Analyzes current and future network states to identify potential risks.
    Provides decision support by suggesting mitigations for predicted congestion.
    """

    def analyze(self, current_state_data: dict, future_state_data: dict) -> dict:
        """
        Compares current and future network snapshots to identify high-risk cells.
        
        Inputs:
        - current_state_data: Dictionary of {cell_id: snapshot} (from NetworkState.get_all_cells())
        - future_state_data: Dictionary of {cell_id: snapshot} (from SimpleNetworkSimulator.simulate())
        
        Returns:
        - A dictionary containing high-risk cell IDs and mitigation suggestions.
        """
        results = {
            "high_risk_cells": [],
            "suggestions": []
        }

        # Iterate through cells in the future state
        for cell_id, future_snapshot in future_state_data.items():
            future_util = future_snapshot.get("utilization", 0.0)
            
            # Check if this cell is present in current state to observe the trend
            current_snapshot = current_state_data.get(cell_id, {})
            current_util = current_snapshot.get("utilization", 0.0)

            # Identification Rule: High Risk if future utilization >= Threshold
            if future_util >= Config.CONGESTION_UTILIZATION_THRESHOLD:
                results["high_risk_cells"].append(cell_id)
                
                # Generate Suggestion
                trend_msg = ""
                if future_util > current_util:
                    trend_msg = f" (Utilization increasing from {current_util:.2f} to {future_util:.2f})"
                
                suggestion = f"Predicted congestion in {cell_id}{trend_msg}. Consider load balancing."
                results["suggestions"].append(suggestion)

        return results
