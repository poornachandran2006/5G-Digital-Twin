from simulation.state.network_state import NetworkState
from simulation.engine.action_executor import NetworkActionExecutor

def test_action_execution():
    print("--- Starting Network Action Executor Verification ---")
    
    # 1. Setup State
    state_manager = NetworkState()
    state_manager.update_cell({"cell_id": "CELL_A", "utilization": 0.80})
    state_manager.update_cell({"cell_id": "CELL_B", "utilization": 0.10})
    
    print(f"Initial State: {state_manager.get_all_cells()}")

    # 2. Initialize Executor
    executor = NetworkActionExecutor(state_manager)

    # 3. Define and Apply Action
    action = {
        "type": "LOAD_SHIFT",
        "source_cell": "CELL_A",
        "target_cell": "CELL_B",
        "percentage": 0.2
    }
    
    print(f"\nApplying Action: LOAD_SHIFT 20% from CELL_A to CELL_B...")
    executor.apply_action(action)

    # 4. Verify Results
    final_a = state_manager.get_cell("CELL_A")["utilization"]
    final_b = state_manager.get_cell("CELL_B")["utilization"]
    
    print(f"Final State - CELL_A: {final_a} (Expected: 0.6)")
    print(f"Final State - CELL_B: {final_b} (Expected: 0.3)")

    assert final_a == 0.6
    assert final_b == 0.3
    
    print("\n--- Network Action Executor Verification Complete ---")

if __name__ == "__main__":
    test_action_execution()
