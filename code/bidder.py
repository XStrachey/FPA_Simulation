import random

class Bidder:
    def __init__(self, id, base_valuation, strategy, strategy_name):
        """
        Initialize the bidder with their unique ID, base valuation, and strategy.
        
        :param id: The bidder's unique identifier.
        :param base_valuation: The bidder's base valuation of the item.
        :param strategy: An instance of a BiddingStrategy subclass.
        """
        self.id = id
        self.base_valuation = base_valuation
        self.strategy = strategy
        self.strategy_name = strategy_name
        self.won_units = 0  # Units won so far

    def get_dynamic_valuation(self, std_dev=50):
        """Apply random perturbation to base valuation."""
        return max(0, random.gauss(self.base_valuation, std_dev))  # Ensure valuation is non-negative

    def place_bid(self, history=None):
        """
        Place a bid using the bidder's strategy and valuation.
        """
        dynamic_valuation = self.get_dynamic_valuation()
        return self.strategy.generate_bid(dynamic_valuation, history)
