class BloodBank:
    def __init__(self, max_shelf_life):
        self.max_shelf_life = max_shelf_life
        # Index represents the remaining shelf life in days.
        # index 0: expired blood
        # index 1: 1 day left before expiring
        # index max_shelf_life: freshly donated blood
        self.inventory = [0] * (self.max_shelf_life + 1)
        
        # Trackers for metrics
        self.total_spoilage = 0
        self.total_shortage = 0
        
    def receive_blood(self, amount):
        """Adds deeply donated blood to the maximum shelf life slot."""
        self.inventory[self.max_shelf_life] += amount

    def fulfill_demand(self, demand):
        """
        Fulfills demand using FIFO logic.
        Uses oldest blood first (lowest index > 0).
        """
        unmet_demand = demand
        
        # Iterate from oldest (1 day left) to freshest (max_shelf_life days left)
        for i in range(1, self.max_shelf_life + 1):
            if unmet_demand == 0:
                break
                
            available = self.inventory[i]
            if available > 0:
                if available >= unmet_demand:
                    # We have enough at this age to fulfill the rest of the demand
                    self.inventory[i] -= unmet_demand
                    unmet_demand = 0
                else:
                    # We use all blood at this age and still need more
                    unmet_demand -= self.inventory[i]
                    self.inventory[i] = 0
                    
        # If we went through all inventory and still have unmet demand, record it as a shortage
        if unmet_demand > 0:
            self.total_shortage += unmet_demand
            
    def end_of_day_aging(self):
        """
        Ages all blood by 1 day.
        Blood that reaches index 0 is spoiled.
        """
        # Blood that was at index 1 is now at index 0 (spoiled)
        spoiled_today = self.inventory[1]
        self.total_spoilage += spoiled_today
        
        # Shift everything down by 1 day
        for i in range(1, self.max_shelf_life):
            self.inventory[i] = self.inventory[i + 1]
            
        # The freshest slot is now empty, ready for tomorrow's donations
        self.inventory[self.max_shelf_life] = 0
        
    def get_total_inventory(self):
        """Returns the total usable blood in the system."""
        return sum(self.inventory[1:])


def simulate_deterministic(days, max_shelf_life, daily_donations, daily_demand):
    """
    Runs a deterministic simulation (fixed daily values, no randomness)
    to verify the FIFO logic and aging mechanics.
    """
    bank = BloodBank(max_shelf_life)
    
    print(f"--- Starting Deterministic Run ({days} Days) ---")
    print(f"Max Shelf Life: {max_shelf_life} days")
    print(f"Daily Donations: {daily_donations} units")
    print(f"Daily Demand: {daily_demand} units\n")
    
    for day in range(1, days + 1):
        # 1. Start of Day: Receive Blood
        bank.receive_blood(daily_donations)
        
        # 2. Fulfill Demand
        bank.fulfill_demand(daily_demand)
        
        # 3. End of Day: Age blood and calculate spoilage
        bank.end_of_day_aging()
        
        # Optional: Print daily status for a small number of days to track it manually
        if days <= 10:
            print(f"Day {day} End - Inventory: {bank.get_total_inventory()}, Total Shortage: {bank.total_shortage}, Total Spoilage: {bank.total_spoilage}")
            
    print("\n--- Final Results ---")
    print(f"Total Shortage over {days} days: {bank.total_shortage} units")
    print(f"Total Spoilage over {days} days: {bank.total_spoilage} units")
    print("---------------------------------------------")

if __name__ == "__main__":
    # Test Scenario 1: Perfect Equilibrium
    # 10 units in, 10 units out.
    # Result should be 0 shortage, 0 spoilage.
    print("TEST 1: Equilibrium")
    simulate_deterministic(days=50, max_shelf_life=35, daily_donations=10, daily_demand=10)
    
    # Test Scenario 2: Overstocking
    # 12 units in, 10 units out. 2 surplus per day.
    # After 35 days, the first surplus units will start expiring.
    print("\nTEST 2: Overstocking (Spoilage Expected)")
    simulate_deterministic(days=50, max_shelf_life=35, daily_donations=12, daily_demand=10)
    
    # Test Scenario 3: Understocking
    # 8 units in, 10 units out. 2 deficit per day.
    # Shortages should accrue immediately since we start with 0 stock.
    print("\nTEST 3: Understocking (Shortages Expected)")
    simulate_deterministic(days=10, max_shelf_life=35, daily_donations=8, daily_demand=10)
