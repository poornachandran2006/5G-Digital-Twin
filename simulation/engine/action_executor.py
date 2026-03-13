class NetworkActionExecutor:
    """
    Executes approved network actions to modify the 5G Digital Twin's live state.
    This acts as the actuation layer (the "Hands") of the Digital Twin.
    """

    def __init__(self, network_state):
        """
        Initializes the executor with a reference to the live NetworkState.
        """
        self.network_state = network_state

    def apply_action(self, action: dict):
        """
        Applies a specific network optimization action.
        
        Supported Types:
        - LOAD_SHIFT: Moves utilization percentage from a source cell to a target cell.
        """
        action_type = action.get("type")
        
        if action_type == "LOAD_SHIFT":
            source_id = action.get("source_cell")
            target_id = action.get("target_cell")
            percentage = action.get("percentage", 0.0)

            # Get snapshots from the live state
            source_snapshot = self.network_state.get_cell(source_id)
            target_snapshot = self.network_state.get_cell(target_id)

            if source_snapshot and target_snapshot:
                # 1. Update Source Cell (Decrease)
                new_source_util = source_snapshot.get("utilization", 0.0) - percentage
                source_snapshot["utilization"] = max(0.0, round(new_source_util, 4))
                
                # 2. Update Target Cell (Increase)
                new_target_util = target_snapshot.get("utilization", 0.0) + percentage
                target_snapshot["utilization"] = min(1.0, round(new_target_util, 4))

                # Note: We modify the snapshot dictionary directly because 
                # NetworkState stores references to these dictionaries.
                # In a more strict system, we would call update_cell() again.
                self.network_state.update_cell(source_snapshot)
                self.network_state.update_cell(target_snapshot)
