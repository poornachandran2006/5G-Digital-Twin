import sys
import os
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")

# Ensure the project root is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation.towers.simulated_tower import SimulatedTower
from simulation.state.network_state import NetworkState
from simulation.engine.simple_simulator import SimpleNetworkSimulator
from ai_models.risk_analyzer import NetworkRiskAnalyzer
from simulation.engine.action_executor import NetworkActionExecutor

def main():
    logging.info("--- 5G Digital Twin: Full Lifecycle Demonstration ---")
    
    # 1. Initialization
    network_state = NetworkState()
    predictor = SimpleNetworkSimulator(network_state)
    risk_analyzer = NetworkRiskAnalyzer()
    action_executor = NetworkActionExecutor(network_state)

    towers = [
        SimulatedTower(cell_id="CELL_001"),
        SimulatedTower(cell_id="CELL_002"),
        SimulatedTower(cell_id="CELL_003")
    ]

    # 2. SENSE: Establish Baseline (5 Ticks)
    logging.info("\n[Phase 1: Sensing] Generating baseline data (5 steps)...")
    for _ in range(5):
        for tower in towers:
            tower.tick()
            network_state.update_cell(tower.snapshot())

    # 3. SNAPSHOT (BEFORE)
    logging.info("\n--- STATE BEFORE ACTION ---")
    current_state = network_state.get_all_cells()
    for cid, data in current_state.items():
        logging.info(f"  {cid}: Utilization = {data['utilization']:.4f}, Latency = {data['average_latency_ms']}ms")

    # 4. PREDICT: Forecast Future Trends (5 Steps)
    logging.info("\n[Phase 2: Prediction] Projecting 5 steps into the future...")
    future_state = predictor.simulate(steps=5)

    # 5. THINK: AI Risk Analysis
    logging.info("[Phase 3: Analysis] Running AI Risk Assessment...")
    risk_report = risk_analyzer.analyze(current_state, future_state)
    
    if risk_report["suggestions"]:
        for suggestion in risk_report["suggestions"]:
            logging.info(f"  AI Suggestion: {suggestion}")
    else:
        logging.info("  AI Verdict: Network projected to be stable.")

    # 6. ACT: Execute Approved Load Shift
    # Simulating a human-in-the-loop decision to balance load
    # Even if no risk, we shift 15% from CELL_002 to CELL_003 as a drill
    approved_action = {
        "type": "LOAD_SHIFT",
        "source_cell": "CELL_002",
        "target_cell": "CELL_001",
        "percentage": 0.15
    }
    
    logging.info(f"\n[Phase 4: Actuation] Applying Approved Action: {approved_action['type']} ({approved_action['percentage']*100}% shift from {approved_action['source_cell']} to {approved_action['target_cell']})")
    action_executor.apply_action(approved_action)

    # 7. SNAPSHOT (AFTER)
    logging.info("\n--- STATE AFTER ACTION ---")
    final_state = network_state.get_all_cells()
    for cid, data in final_state.items():
        logging.info(f"  {cid}: Utilization = {data['utilization']:.4f}, Latency = {data['average_latency_ms']}ms")

    logging.info("\n--- 5G Digital Twin: Demonstration Finished ---")

if __name__ == "__main__":
    main()


