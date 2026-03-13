import random

class SimulatedTower:
    """
    Represents a simulated 5G Cell Tower (gNodeB) in the Digital Twin.
    It manages its own state and updates metrics in a realistic feedback loop.
    """

    def __init__(self, cell_id: str):
        # Identity
        self.cell_id = cell_id
        
        # State Variables (Initial Defaults)
        self.active_users = 25  # Moderate initial load
        self.traffic_demand_mbps = 50.0  # Mbps
        self.utilization = 0.25  # 25% utilized
        self.average_latency_ms = 10.0  # 10ms base latency
        self.packet_loss_rate = 0.01  # 0.01% initial loss
        self.timestamp = 0

    def tick(self):
        """
        Advances the simulation by one time step.
        Updates metrics based on logical relationships and random noise.
        """
        self.timestamp += 1

        # 1. Update Active Users (Small random fluctuation)
        # Randomly add/remove up to 2 users
        user_change = random.randint(-2, 2)
        self.active_users = max(0, self.active_users + user_change)

        # 2. Update Traffic Demand 
        # Roughly 2 Mbps per active user + some noise
        base_demand = self.active_users * 2.0
        noise = random.uniform(-1.0, 1.0)
        self.traffic_demand_mbps = max(0.0, base_demand + noise)

        # 3. Update Utilization
        # Assuming a total capacity of 100 Mbps for this simple simulation
        capacity_mbps = 100.0
        self.utilization = min(1.0, self.traffic_demand_mbps / capacity_mbps)

        # 4. Update Average Latency
        # Logic: Base latency + congestion delay
        # Congestion delay increases significantly as utilization approaches 1.0
        congestion_delay = self.utilization * 50.0 
        jitter = random.uniform(-1.0, 1.0)
        self.average_latency_ms = max(5.0, 10.0 + congestion_delay + jitter)

        # 5. Update Packet Loss Rate
        # Logic: Higher latency leads to slightly higher packet loss
        # If latency is > 40ms, loss increases more rapidly
        if self.average_latency_ms > 40.0:
            loss_noise = random.uniform(0.0, 0.5)
        else:
            loss_noise = random.uniform(0.0, 0.05)
            
        # Cumulative loss effect tied to utilization
        self.packet_loss_rate = max(0.0, (self.utilization * 0.1) + loss_noise)

    def snapshot(self) -> dict:
        """
        Returns the current state of the tower as a dictionary.
        """
        return {
            "cell_id": self.cell_id,
            "timestamp": self.timestamp,
            "active_users": self.active_users,
            "traffic_demand_mbps": round(self.traffic_demand_mbps, 2),
            "utilization": round(self.utilization, 4),
            "average_latency_ms": round(self.average_latency_ms, 2),
            "packet_loss_rate": round(self.packet_loss_rate, 4)
        }
