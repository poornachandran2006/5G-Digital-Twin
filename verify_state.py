from simulation.state.network_state import NetworkState

def test_network_state():
    print("--- Starting NetworkState Verification ---")
    state_manager = NetworkState()
    
    # Mock snapshots
    s1 = {"cell_id": "TOWER_A", "utilization": 0.45, "timestamp": 1}
    s2 = {"cell_id": "TOWER_B", "utilization": 0.10, "timestamp": 1}
    
    # Test update
    print("Updating state with TOWER_A and TOWER_B...")
    state_manager.update_cell(s1)
    state_manager.update_cell(s2)
    
    # Test retrieval
    print(f"Retrieving TOWER_A: {state_manager.get_cell('TOWER_A')}")
    print(f"Retrieving TOWER_C (non-existent): {state_manager.get_cell('TOWER_C')}")
    
    # Test all cells
    print(f"All Cells: {state_manager.get_all_cells()}")
    
    # Test overwrite
    s1_v2 = {"cell_id": "TOWER_A", "utilization": 0.99, "timestamp": 2}
    print("Overwriting TOWER_A with new snapshot...")
    state_manager.update_cell(s1_v2)
    print(f"New TOWER_A state: {state_manager.get_cell('TOWER_A')}")
    
    # Test Analytics
    print("\n--- Testing Analytics ---")
    avg_util = state_manager.get_average_utilization()
    most_congested = state_manager.get_most_congested_cell()
    congested_flag = state_manager.is_network_congested(threshold=0.5)
    
    print(f"Average Utilization: {avg_util:.4f}")
    print(f"Most Congested Cell: {most_congested['cell_id']} ({most_congested['utilization']})")
    print(f"Is Network Congested (Threshold 0.5): {congested_flag}")
    
    # Test with empty state
    print("\nTesting with empty state...")
    empty_manager = NetworkState()
    print(f"Empty Average: {empty_manager.get_average_utilization()}")
    print(f"Empty Most Congested: {empty_manager.get_most_congested_cell()}")
    
    print("--- NetworkState Verification Complete ---")

if __name__ == "__main__":
    test_network_state()
