import sys
import os
import random
import statistics
from stochastic_engine import simulate_stochastic

def run_monte_carlo(replications, days, max_shelf_life, avg_donations, avg_sched_demand, avg_emer_demand,
                    reorder_point=None, order_quantity=None):
    """
    Runs many replications of the stochastic simulation to gather statistically significant average metrics.
    """
    print(f"--- Running Monte Carlo Simulation ({replications} Replications of {days} days) ---")
    if reorder_point:
        print(f"Testing Policy -> ROP: {reorder_point}, OQ: {order_quantity}")
    else:
        print("Testing Policy -> None")
        
    results = {
        "emergency_shortages": [],
        "scheduled_shortages": [],
        "total_shortages": [],
        "total_spoilage": [],
        "service_level": [],
        "spoilage_ratio": []
    }
    
    # Suppress output from individual stochastic runs
    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    
    for _ in range(replications):
        run_data = simulate_stochastic(
            days, max_shelf_life, avg_donations, avg_sched_demand, avg_emer_demand,
            reorder_point, order_quantity
        )
        for key in results:
            results[key].append(run_data[key])
            
    # Restore stdout
    sys.stdout = old_stdout
    
    # Aggregate data
    averages = {key: statistics.mean(val) for key, val in results.items()}
    std_devs = {key: statistics.stdev(val) if len(val) > 1 else 0 for key, val in results.items()}
    
    print("\n--- Monte Carlo Results (Averages) ---")
    print(f"Emergency Shortages : {averages['emergency_shortages']:.1f}  (StdDev: {std_devs['emergency_shortages']:.1f})")
    print(f"Scheduled Shortages : {averages['scheduled_shortages']:.1f}  (StdDev: {std_devs['scheduled_shortages']:.1f})")
    print(f"Total Shortages     : {averages['total_shortages']:.1f}  (StdDev: {std_devs['total_shortages']:.1f})")
    print(f"Total Spoilage      : {averages['total_spoilage']:.1f}  (StdDev: {std_devs['total_spoilage']:.1f})")
    print(f"Service Level       : {averages['service_level']:.2f}% (StdDev: {std_devs['service_level']:.2f}%)")
    print(f"Spoilage Ratio      : {averages['spoilage_ratio']:.2f}% (StdDev: {std_devs['spoilage_ratio']:.2f}%)")
    print("--------------------------------------\n")
    
    return averages

if __name__ == "__main__":
    # Ensure reproducibility
    random.seed(123)
    
    REPLICATIONS = 100
    DAYS_PER_RUN = 365
    MAX_SHELF_LIFE = 35
    AVG_DONATIONS = 10
    AVG_SCHED_DEMAND = 7
    AVG_EMER_DEMAND = 3
    
    print("Experiment: Testing Different Reorder Points (ROP) to find the optimal trade-off.")
    
    # Test Policy 1: No ROP
    run_monte_carlo(REPLICATIONS, DAYS_PER_RUN, MAX_SHELF_LIFE, AVG_DONATIONS, AVG_SCHED_DEMAND, AVG_EMER_DEMAND)
    
    # Test Policy 2: ROP 10
    run_monte_carlo(REPLICATIONS, DAYS_PER_RUN, MAX_SHELF_LIFE, AVG_DONATIONS, AVG_SCHED_DEMAND, AVG_EMER_DEMAND,
                    reorder_point=10, order_quantity=10)
    
    # Test Policy 3: ROP 20 (Higher buffer)
    run_monte_carlo(REPLICATIONS, DAYS_PER_RUN, MAX_SHELF_LIFE, AVG_DONATIONS, AVG_SCHED_DEMAND, AVG_EMER_DEMAND,
                    reorder_point=20, order_quantity=10)
    
    # Test Policy 4: ROP 40 (Massive buffer)
    run_monte_carlo(REPLICATIONS, DAYS_PER_RUN, MAX_SHELF_LIFE, AVG_DONATIONS, AVG_SCHED_DEMAND, AVG_EMER_DEMAND,
                    reorder_point=40, order_quantity=15)
