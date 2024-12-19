import random

class BiddingStrategy:
    def generate_bid(self, valuation, history=None):
        """
        Generate a bid based on the given valuation and optional auction history.

        :param valuation: The bidder's valuation of the item.
        :param history: (Optional) Auction history or other contextual information.
        :return: The bid amount.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

class NashEquilibriumStrategy(BiddingStrategy):
    def __init__(self, reserved_price, num_bidders):
        self.reserved_price = reserved_price
        self.num_bidders = num_bidders

    def generate_bid(self, valuation, history=None):
        if self.num_bidders <= 1:
            return self.reserved_price  # If there's only one bidder, bid on reserved price
        return valuation * (self.num_bidders - 1) / self.num_bidders

class SimpleProportionalStrategy(BiddingStrategy):
    def __init__(self, risk_factor):
        self.risk_factor = risk_factor

    def generate_bid(self, valuation, history=None):
        return valuation * self.risk_factor

class FollowerStrategy(BiddingStrategy):
    def __init__(self, fallback_strategy, max_deviation=10):
        self.fallback_strategy = fallback_strategy
        self.last_winner_bid = None
        self.max_deviation = max_deviation

    def update_last_winner_bid(self, last_winner_bid):
        self.last_winner_bid = last_winner_bid

    def generate_bid(self, valuation, history=None):
        if history and len(history) > 0:
            self.last_winner_bid = history[-1]['bid']
        if self.last_winner_bid and self.last_winner_bid <= valuation:
            adjustment = random.uniform(-self.max_deviation, self.max_deviation)
            return max(0, min(valuation, self.last_winner_bid + adjustment))
        return self.fallback_strategy.generate_bid(valuation, history)
