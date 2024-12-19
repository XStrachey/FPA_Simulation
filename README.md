# First price sealed auction simulation

## Project Description
This project simulates first-price sealed-bid auctions for homogeneous items, where bidders compete for a single item per round. Each bidder employs a specific bidding strategy, and the auction system calculates results, tracks the history, and analyzes revenue. The project supports various bidding strategies, including:

1. **Nash Equilibrium Strategy** (for uniformly distributed valuations on [a, b]).
2. **Simple Proportional Strategy** (risk-based bidding).
3. **Follower Strategy** (learning from past winning bids).

The simulation is modular and extensible, allowing for easy integration of new strategies.

---

## Features
- **Multi-round Auctions**: Supports multiple auction rounds with history tracking.
- **Dynamic Valuations**: Bidder valuations are perturbed to reflect real-world randomness.
- **Bidding Strategies**: Implements a unified strategy interface for flexibility.
- **Revenue Analysis**: Provides detailed analysis and visualization of auction revenue per round.
- **Extensibility**: New bidding strategies can be added seamlessly.

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/XStrachey/FPA_Simulation.git
   cd FPA_Simulation
   ```

2. Run the script:
   ```bash
   python code/main.py
   ```

---

## Usage

### Running the Simulation
1. Define auction parameters:
   - **Reserve Price**: Minimum acceptable price.
   - **Number of Bidders**: Total participants.
   - **Valuation Range**: [a, b] range of bidder valuations.
   - **Number of Rounds**: Total rounds of auction.

2. Configure strategies:
   ```python
   nash_strategy = NashEquilibriumStrategy(num_bidders=20, lower_bound=500, upper_bound=1500)
   simple_strategy = SimpleProportionalStrategy(risk_factor=0.85)
   follower_strategy = FollowerStrategy(fallback_strategy=simple_strategy)
   ```

3. Assign strategies to bidders:
   ```python
   strategies = [
       (nash_strategy, "Nash Equilibrium"),
       (simple_strategy, "Simple Proportional"),
       (follower_strategy, "Follower Strategy")
   ]

   bidders = generate_bidders(num_bidders=20, strategies=strategies, valuation_range=(500, 1500))
   ```

4. Run the auction:
   ```python
   auction = AuctionSystem(auctioneer, bidders, num_rounds=5)
   auction.conduct_auction()
   auction.analyze_revenue()
   ```

### Results
- **Auction History**: Displays each round's winner and winning bid.
- **Revenue Analysis**: Summarizes and visualizes revenue per round.

---

## Adding New Strategies

1. Create a new class inheriting from `BiddingStrategy`:
   ```python
   class NewStrategy(BiddingStrategy):
       def generate_bid(self, valuation, history=None):
           # Define custom bidding logic
           pass
   ```

2. Add the strategy to the simulation:
   ```python
   new_strategy = NewStrategy(...)
   strategies.append((new_strategy, "New Strategy"))
   ```

3. Run the auction to test the new strategy.

---

## Example Output
### Console
```
Reserve Price: 750
# Bidders: 20
Valuation Range: (500, 1500)

Bidder 1: Valuation = 1200.50, Strategy = Nash Equilibrium
Bidder 2: Valuation = 900.75, Strategy = Simple Proportional
...

Round 1:
  Winner: Bidder 5 with bid: 1100.00
Round 2:
  Winner: Bidder 3 with bid: 1050.00
...

Revenue per Round:
count       5.000000
mean     1250.000000
std       200.000000
min      1000.000000
max      1500.000000
```