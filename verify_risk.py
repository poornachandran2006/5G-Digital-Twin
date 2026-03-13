from ai_models.risk_analyzer import NetworkRiskAnalyzer

def test_risk_analysis():
    print("--- Starting AI Risk Analyzer Verification ---")
    
    analyzer = NetworkRiskAnalyzer()

    # Mock Current State
    current_state = {
        "CELL_001": {"cell_id": "CELL_001", "utilization": 0.65},
        "CELL_002": {"cell_id": "CELL_002", "utilization": 0.20}
    }

    # Mock Future State (Projected by Simulator)
    future_state = {
        "CELL_001": {"cell_id": "CELL_001", "utilization": 0.85}, # Risk!
        "CELL_002": {"cell_id": "CELL_002", "utilization": 0.10}  # Safe
    }

    print("Analyzing current vs future state...")
    risk_report = analyzer.analyze(current_state, future_state)

    print(f"High Risk Cells: {risk_report['high_risk_cells']}")
    for suggestion in risk_report['suggestions']:
        print(f"Suggestion: {suggestion}")

    # Verify logic
    assert "CELL_001" in risk_report["high_risk_cells"]
    assert len(risk_report["high_risk_cells"]) == 1
    
    print("--- AI Risk Analyzer Verification Complete ---")

if __name__ == "__main__":
    test_risk_analysis()
