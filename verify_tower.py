from simulation.towers.simulated_tower import SimulatedTower

def test_tower():
    print("--- Starting SimulatedTower Verification ---")
    tower = SimulatedTower("TOWER_001")
    
    print(f"Initial State: {tower.snapshot()}")
    
    for i in range(1, 11):
        tower.tick()
        state = tower.snapshot()
        print(f"Tick {i:02d}: Users: {state['active_users']:02d} | Util: {state['utilization']:.2f} | Latency: {state['average_latency_ms']}ms | Loss: {state['packet_loss_rate']}%")

if __name__ == "__main__":
    test_tower()
