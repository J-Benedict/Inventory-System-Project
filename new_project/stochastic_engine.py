import random
import math
from core_engine import BloodBank

def generate_poisson(lam):
    """
    Generates a random drawing from a Poisson distribution with mean lam.
    Uses Knuth's algorithm. Perfect for simulating stochastic events like
    daily walk-in donations or sudden emergencies.
    """
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= random.uniform(0, 1)
    return k - 1

def simulate_stochastic(days, max_shelf_life, avg_donations, avg_sched_demand, avg_emer_demand,
                        reorder_point=None, order_quantity=None):
    """
    Runs a stochastic simulation with randomness in supply and demand.
    Adds a queuing/priority system: Emergencies are fulfilled before scheduled operations.
    Can also implement a simple inventory policy (ROP/OQ).
    """
    bank = BloodBank(max_shelf_life)
    
    # We will track emergencies and scheduled shortages separately
    total_emer_shortage = 0
    total_sched_shortage = 0
    total_spoilage = 0
    
    # For reporting
    total_donations_received = 0
    total_emer_demand = 0
    total_sched_demand = 0
    
    print(f"--- Starting Stochastic Run ({days} Days) ---")
    print(f"Averages -> Donations: {avg_donations}, Sched. Demand: {avg_sched_demand}, Emer. Demand: {avg_emer_demand}")
    if reorder_point is not None:
        print(f"Inventory Policy -> ROP: {reorder_point}, OQ: {order_quantity}")
    print("Simulating...\n")

    for day in range(1, days + 1):
        # --- 1. Emergency Blood Drive Logic (ROP / OQ) ---
        if reorder_point is not None and bank.get_total_inventory() < reorder_point:
            # We hit the reorder point, trigger an emergency delivery/drive
            # We assume it arrives immediately or same-day (Lead Time = 0 for simplicity)
            bank.receive_blood(order_quantity)
            total_donations_received += order_quantity

        # --- 2. Random Supply Generation ---
        # "Walk-in" donations fluctuate around an average following a Poisson distribution
        daily_donations = generate_poisson(avg_donations)
        bank.receive_blood(daily_donations)
        total_donations_received += daily_donations
        
        # --- 3. Random Demand Generation ---
        sched_demand = generate_poisson(avg_sched_demand)
        emer_demand = generate_poisson(avg_emer_demand)
        
        total_sched_demand += sched_demand
        total_emer_demand += emer_demand
        
        # --- 4. Fulfill Demand (Priority Logic) ---
        # Priority 1: Emergency Demand
        pre_emer_shortage = bank.total_shortage
        bank.fulfill_demand(emer_demand)
        # If the bank's total shortage increased, it means we couldn't meet the emergency demand
        daily_emer_short = bank.total_shortage - pre_emer_shortage
        total_emer_shortage += daily_emer_short
        
        # Priority 2: Scheduled Demand
        pre_sched_shortage = bank.total_shortage
        bank.fulfill_demand(sched_demand)
        daily_sched_short = bank.total_shortage - pre_sched_shortage
        total_sched_shortage += daily_sched_short
        
        # --- 5. End of Day: Age blood and calculate spoilage ---
        pre_spoilage = bank.total_spoilage
        bank.end_of_day_aging()
        total_spoilage += (bank.total_spoilage - pre_spoilage)
        
    print("--- Final Results (Over 1 Year) ---")
    print(f"Total Blood Donated: {total_donations_received} units")
    print(f"Total Scheduled Demand: {total_sched_demand} units")
    print(f"Total Emergency Demand: {total_emer_demand} units")
    print("------------- METRICS -------------")
    print(f"Emergency Shortages (Critical!): {total_emer_shortage} units")
    print(f"Scheduled Shortages (Delayed Ops): {total_sched_shortage} units")
    print(f"Total Spoilage (Expired Blood): {total_spoilage} units")
    
    # Calculate Service Levels
    total_demand = total_emer_demand + total_sched_demand
    total_shortages = total_emer_shortage + total_sched_shortage
    if total_demand > 0:
        service_level = ((total_demand - total_shortages) / total_demand) * 100
        print(f"Overall Service Level: {service_level:.2f}% of demand met immediately.")
    
    ratio = (total_spoilage / total_donations_received) * 100 if total_donations_received > 0 else 0
    if not hasattr(simulate_stochastic, 'quiet') or not simulate_stochastic.quiet:
        print(f"Spoilage Ratio: {ratio:.2f}% of all received blood expired.")
        print("-----------------------------------\n")
        
    return {
        "emergency_shortages": total_emer_shortage,
        "scheduled_shortages": total_sched_shortage,
        "total_shortages": total_shortages,
        "total_spoilage": total_spoilage,
        "service_level": service_level if total_demand > 0 else 100,
        "spoilage_ratio": ratio
    }

if __name__ == "__main__":
    # Ensure reproducibility for testing
    random.seed(42)
    
    # Scenario A: No Inventory Policy (Just rely on daily walk-ins)
    # Average daily walk-ins (10) exactly equals average daily demand (7+3)
    print("SCENARIO A: No extra orders, perfect average match")
    simulate_stochastic(
        days=365, 
        max_shelf_life=35, 
        avg_donations=10, 
        avg_sched_demand=7, 
        avg_emer_demand=3
    )

    # Scenario B: Utilizing an Inventory Policy (ROP/OQ)
    # We maintain a buffer. If inventory drops below 15 (ROP), we order/drive an extra 10 units (OQ).
    print("SCENARIO B: Utilizing a Reorder Point (ROP: 15, OQ: 10)")
    simulate_stochastic(
        days=365, 
        max_shelf_life=35, 
        avg_donations=10, 
        avg_sched_demand=7, 
        avg_emer_demand=3,
        reorder_point=15,
        order_quantity=10
    )
