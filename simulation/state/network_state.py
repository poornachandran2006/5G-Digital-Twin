class NetworkState:
    """
    Manages the in-memory state of all cells in the 5G Digital Twin.
    Acts as a central repository for the latest snapshots of simulated components.
    """

    def __init__(self):
        # Internal storage: {cell_id: latest_snapshot_dict}
        self._cell_data = {}

    def update_cell(self, snapshot: dict):
        """
        Extracts the cell_id from the snapshot and stores/overwrites the state.
        """
        cell_id = snapshot.get("cell_id")
        if cell_id:
            self._cell_data[cell_id] = snapshot

    def get_cell(self, cell_id: str) -> dict:
        """
        Returns the latest snapshot for the given cell_id, or None if not found.
        """
        return self._cell_data.get(cell_id)

    def get_all_cells(self) -> dict:
        """
        Returns the complete dictionary of all cell states.
        """
        return self._cell_data

    def get_average_utilization(self) -> float:
        """
        Computes the average of "utilization" across all cells.
        Returns 0.0 if no cells exist.
        """
        if not self._cell_data:
            return 0.0
        
        total_util = sum(cell.get("utilization", 0.0) for cell in self._cell_data.values())
        return total_util / len(self._cell_data)

    def get_most_congested_cell(self) -> dict:
        """
        Returns the snapshot (dict) of the cell with the highest utilization.
        Returns None if no cells exist.
        """
        if not self._cell_data:
            return None
        
        return max(self._cell_data.values(), key=lambda x: x.get("utilization", 0.0))

    def is_network_congested(self, threshold: float = 0.75) -> bool:
        """
        Returns True if the average utilization across all cells meets or exceeds the threshold.
        """
        return self.get_average_utilization() >= threshold
