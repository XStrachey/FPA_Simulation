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
    def __init__(self, num_bidders, lower_bound, upper_bound):
        """
        Initialize the Nash Equilibrium strategy.

        :param num_bidders: Number of bidders in the auction.
        :param lower_bound: Lower bound (a) of the valuation distribution.
        :param upper_bound: Upper bound (b) of the valuation distribution.
        """
        self.num_bidders = num_bidders
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def generate_bid(self, valuation, history=None):
        """
        Generate the bid according to Nash Equilibrium strategy for U[a, b].

        :param valuation: The bidder's valuation of the item.
        :param history: (Optional) Auction history or other contextual information.
        :return: The bid amount.
        """
        a = self.lower_bound
        b = self.upper_bound
        n = self.num_bidders

        # Apply the Nash Equilibrium bidding formula for U[a, b]
        bid = valuation - (b - a) / n * (1 - ((valuation - a) / (b - a)) ** n)
        return max(0, bid)  # Ensure bid is non-negative

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
