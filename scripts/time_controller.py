import time
import sys
import os
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")

# Ensure the project root is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config

from simulation.towers.simulated_tower import SimulatedTower
from simulation.state.network_state import NetworkState
from simulation.engine.simple_simulator import SimpleNetworkSimulator
from ai_models.risk_analyzer import NetworkRiskAnalyzer

def main():
    """
    Autonomous heartbeat that ticks towers, predicts the future, 
    and analyzes network risk in real-time.
    """
    logging.info("--- 5G Digital Twin: AI-Driven Heartbeat Started ---")
    
    # 1. Initialize Components
    network_state = NetworkState()
    predictor = SimpleNetworkSimulator(network_state)
    risk_analyzer = NetworkRiskAnalyzer()

    towers = [
        SimulatedTower(cell_id="CELL_001"),
        SimulatedTower(cell_id="CELL_002"),
        SimulatedTower(cell_id="CELL_003")
    ]
    
    # 2. Run the loop
    try:
        for i in range(1, 21):
            # Step A: Sense (Tick Towers)
            for tower in towers:
                tower.tick()
                network_state.update_cell(tower.snapshot())
            
            # Step B: Memory (Get Current Snapshot)
            current_data = network_state.get_all_cells()
            avg_util = network_state.get_average_utilization()

            # Step C: Forecast (Look 10 steps into the future)
            future_data = predictor.simulate(steps=10)

            # Step D: Analyze (AI Decision Support)
            risk_report = risk_analyzer.analyze(current_data, future_data)
            
            # Step E: Report (Display the Terminal Dashboard)
            logging.info(f"\n--- [Step {i:02d}] Digital Twin Loop ---")
            logging.info(f"Network Health: Average Utilization = {avg_util:.2%}")
            
            if risk_report["high_risk_cells"]:
                logging.info(f"🚨 PREDICTIVE ALERT: {len(risk_report['high_risk_cells'])} cells at risk!")
                for suggestion in risk_report["suggestions"]:
                    logging.info(f"  -> AI Suggestion: {suggestion}")
            else:
                logging.info("✅ Future Status: All towers projected to stay stable.")
            
            time.sleep(Config.TICK_INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        logging.info("\n--- Heartbeat stopped by user ---")
    
    logging.info("\n--- 5G Digital Twin: AI-Driven Heartbeat Finished ---")

if __name__ == "__main__":
    main()


