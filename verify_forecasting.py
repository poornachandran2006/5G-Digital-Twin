from simulation.state.network_state import NetworkState
from simulation.engine.simple_simulator import SimpleNetworkSimulator

def test_forecasting():
    print("--- Starting Predictor Engine Verification ---")
    
    # Setup initial state
    state_manager = NetworkState()
    state_manager.update_cell({
        "cell_id": "BUSY_CELL", 
        "utilization": 0.65, 
        "average_latency_ms": 42.5, 
        "timestamp": 10
    })
    state_manager.update_cell({
        "cell_id": "QUIET_CELL", 
        "utilization": 0.20, 
        "average_latency_ms": 20.0, 
        "timestamp": 10
    })

    print(f"Current State: {state_manager.get_all_cells()}")

    # Initialize Predictor
    predictor = SimpleNetworkSimulator(state_manager)

    # Forecast 5 steps into the future
    print("\nProjecting 5 steps into the future...")
    future_data = predictor.simulate(steps=5)

    for cell_id, data in future_data.items():
        print(f"[{cell_id}] Future Util: {data['utilization']} | Future Latency: {data['average_latency_ms']}ms | Future Time: {data['timestamp']}")

    # Verify isolation (live state should NOT have changed)
    print(f"\nVerifying isolation (Live state after simulation):")
    print(f"BUSY_CELL timestamp: {state_manager.get_cell('BUSY_CELL')['timestamp']} (should be 10)")
    
    print("--- Predictor Engine Verification Complete ---")

if __name__ == "__main__":
    test_forecasting()
