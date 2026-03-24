# Lakano's Medical Center Blood Bank Inventory Management Simulation

## Project Overview
This project simulates the inventory management of the Lakano's Medical Center blood bank. Blood is a critical, perishable resource. The goal is to find an optimal inventory policy that minimizes both blood spoilage (due to expiration) and blood shortages (which put patients at risk) in the face of stochastic demand (emergencies, scheduled surgeries) and supply (donations).

## Development Phases

### Phase 1: Conceptual Design & System Definition (Report Sections 1 & 2)
**Goal:** Define the model mathematically and logically before writing code.
*   **System Classification:** Stochastic, Dynamic, Discrete-Time (daily time steps).
*   **State Variables:** Current inventory of each blood type (A, B, AB, O, positive/negative), remaining shelf life of each unit in stock.
*   **Input Parameters:** 
    *   Maximum shelf life of blood (e.g., 35-42 days).
    *   Target inventory levels (Reorder Point, Order Quantity).
    *   Cost of spoilage vs. cost/penalty of shortage.
*   **Stochastic Variables:**
    *   Daily demand for blood (separated by scheduled operations vs. emergencies).
    *   Daily blood supply (donations received).
*   **Output Metrics:** Total units expired (spoilage), total number of unmet demands (shortages), service level %.
*   **Deliverable:** Conceptual flowchart of a single simulated day.

### Phase 2: Deterministic Core Engine (Coding begins)
**Goal:** Build the daily simulation loop using fixed, non-random numbers to verify logic.
*   **Implementation:** Python script simulating day-by-day operations.
*   **Logic:**
    1.  *Start of Day:* Receive new blood shipments/donations. Add to inventory with max shelf life.
    2.  *During Day:* Fulfill demand. **Crucial rule (FIFO):** Use the oldest blood first to minimize spoilage.
    3.  *End of Day:* Decrease the remaining shelf life of all stored blood by 1 day. Discard any blood that has reached 0 days.
*   **Validation:** Run with predictable inputs (e.g., 10 units donated per day, 8 used) to confirm inventory accurately tracks age and discards work correctly.

### Phase 3: Stochastic Elements & Probabilistic Modeling
**Goal:** Introduce randomness using Pseudorandom Number Generation (PRNG).
*   **Demand Generation:** Use probability distributions (e.g., Poisson distribution) to simulate the number of patients needing blood each day. Include occasional "spikes" simulating mass casualty events.
*   **Supply Generation:** Model unpredictable donation rates.
*   **Queuing (Optional but good):** Differentiate patient types. If a shortage occurs, "emergencies" get priority over "scheduled surgeries" (which might get delayed instead of failed).
*   **Outcome:** The model now reflects real-world unpredictability.

### Phase 4: Monte Carlo Experiments & Data Collection
**Goal:** Run thousands of scenarios to gather statistically significant data.
*   **Experiment Design:** Create an "Experiment Controller" function.
*   **Replications:** Run the 365-day simulation 1,000 times for a given inventory policy.
*   **Sensitivity Analysis:** Test different policies:
    *   *Scenario A:* Keep a bare minimum stock (low spoilage, high shortage risk).
    *   *Scenario B:* Keep a massive stockpile (zero shortages, massive spoilage).
    *   *Scenario C:* Finding the "sweet spot" (e.g., what if we aggressively run blood drives when stock dips below X?).
*   **Data Aggregation:** Collect averages and standard deviations of our Output Metrics across all runs.

### Phase 5: Results Analysis, Visualization, and Polish
**Goal:** Translate raw data into insights for the final presentation and report.
*   **Visualization:** Use Python (`matplotlib`/`seaborn`) to graph:
    *   Inventory levels over time (showing peaks and dips).
    *   Trade-off curve between Spoilage Rate vs. Shortage Rate.
*   **Conclusion:** Formulate practical recommendations based on the data (e.g., "The hospital should maintain a base stock of X units of Type O- blood and trigger emergency procurement if it drops below Y").
*   **Documentation:** Finalize comments in code and create a `README.md` with instructions on how to run the simulation (Rubric Requirement B).

### Phase 6: Interactive Web UI (Presentation / Rubric Component C)
**Goal:** Build a clean, modern, interactive web application to showcase the simulation live for the final presentation.
*   **Architecture:** We will wrap our Python simulation logic in a lightweight API (like FastAPI or Flask) and build a beautiful front-end (using HTML/CSS/Vanilla JS or React/Vite if you prefer).
*   **Key Features:**
    *   **Control Panel:** Sliders/inputs to adjust parameters dynamically (e.g., "Max Shelf Life", "Daily Emergency Rate").
    *   **Live Dashboard:** Displaying the key metrics (Spoilage vs. Shortage) updating as the Monte Carlo simulation runs in the background.
    *   **Data Visualization:** Interactive charts reflecting the output metrics, making the live demonstration incredibly polished and engaging for the professor.
    *   **Aesthetics:** A responsive design with modern colors (e.g., medical white, alert red, reassuring blue), smooth gradients, and clear typography so it looks professional on a projector screen.
