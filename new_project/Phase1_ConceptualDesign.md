# Phase 1: Conceptual Design & System Definition
This document outlines the mathematical model and system parameters for the Lakano's Medical Center Blood Bank Inventory Simulation.

## 1. System Classification
*   **System Type:** Inventory Management System (Specifically, a perishable goods inventory model)
*   **Time Model:** Discrete-time (simulated in single complete days, $\Delta t = 1 \text{ day}$).
*   **Behavioral Model:** Stochastic (contains randomness in demand and supply) and Dynamic (state changes over time).

## 2. State Variables
These are variables that completely define the state of the system at any time step $t$.
*   $I_t$: The total inventory on hand at the start of day $t$.
*   $A_{x, t}$: The amount of blood in inventory that has a remaining shelf life of exactly $x$ days.
    *   Therefore, $I_t = \sum_{x=1}^{M} A_{x, t}$ (where $M$ is the max shelf life).

## 3. Input Parameters (Constants & Constraints)
These are policy decisions or facts of reality that we can adjust between experiments.
*   $M$: Maximum shelf life of a blood unit (e.g., $M = 35$ days). Blood older than $M$ is discarded.
*   $S$: Base daily scheduled demand (e.g., $S = 5$ units). Operations booked in advance. 
*   $E_{base}$: Base expected daily emergency demand (e.g., $E_{base} = 2$ units).
*   $D_{base}$: Base expected daily donations (e.g., $D_{base} = 10$ units).
*   $ROP$: Reorder Point. If $I_t < ROP$, trigger an emergency blood drive or external order.
*   $OQ$: Order Quantity. The amount to order when $I_t$ falls below the $ROP$.

## 4. Stochastic Elements (Randomness)
These variables attempt to simulate the unpredictability of the real world using Pseudorandom Number Generators (PRNGs), specifically drawing from a Poisson distribution. Let $P(\lambda)$ denote a random draw from a Poisson distribution with mean $\lambda$.
*   **Scheduled Demand ($D_{sched, t}$):** Usually predictable, but occasionally varies. $D_{sched, t} \sim P(S)$
*   **Emergency Demand ($D_{emer, t}$):** Highly unpredictable. $D_{emer, t} \sim P(E_{base})$
    *   *Note:* Emergencies get priority. If there is a shortage, $D_{sched}$ is delayed before $D_{emer}$ is denied.
*   **Total Demand ($D_{total, t}$):** $D_{sched, t} + D_{emer, t}$
*   **Donations Received ($Supply_t$):** Daily "walk-in" donors. $Supply_t \sim P(D_{base})$

## 5. Output Metrics (Performance Variables)
These are the metrics we measure to evaluate how good the inventory policy ($ROP$, $OQ$) is.
*   **Spoilage ($W_t$):** Number of units discarded due to expiration on day $t$. (Units where remaining life $x = 0$).
*   **Shortage ($K_t$):** Number of units of demand that could not be met. $K_t = \max(0, D_{total, t} - I_t)$.
*   **Shortage Ratio:** $\frac{\sum K_t}{\sum D_{total, t}}$
*   **Spoilage Ratio:** $\frac{\sum W_t}{\sum (\text{Total Blood Received})}$

## 6. Daily Logic Flow (Algorithm)
Each simulated day follows this sequence of events:
1.  **Receive Blood:** Generate $Supply_t$. Add to inventory with a remaining life of exactly $M$ days.
2.  **Generate Demand:** Generate $D_{sched}$ and $D_{emer}$. Total is $D_{total}$.
3.  **Fulfill Demand (FIFO approach):**
    *   Find the oldest available blood (lowest remaining shelf life $x > 0$).
    *   Subtract demand from this aged blood first to minimize future spoilage.
    *   Keep fulfilling until $D_{total}$ is $0$ or $I_t$ is $0$.
4.  **Calculate Shortages:** If $I_t$ hit $0$ while $D_{total}$ was still $>0$, record the shortage $K_t$.
5.  **Calculate Spoilage:** Identify any remaining inventory with shelf life $x = 1$. This blood expires at the end of the day. Record as Spoilage $W_t$.
6.  **Age Blood:** Decrease the remaining shelf life ($x$) of all remaining blood by $1$ day.

---
*This document outlines the foundation for building the simulation engine in Phase 2. It satisfies the "Conceptual Model", "Classification", and "Identification of Variables" rubric requirements.*
