import random
from functools import partial
from auctioneer import Auctioneer
from bidder import Bidder
from auction_system import AuctionSystem
from strategy import NashEquilibriumStrategy, SimpleProportionalStrategy, FollowerStrategy

def generate_bidders(num_bidders, strategies, valuation_range):
    """
    Generate a list of bidders with random valuations and assigned strategies.

    :param num_bidders: Total number of bidders to generate.
    :param strategies: List of tuples (strategy_function, strategy_name).
    :param valuation_range: Range of valuations to randomly assign.
    :return: A list of Bidder objects.
    """
    bidders = []
    for i in range(num_bidders):
        valuation = random.uniform(*valuation_range)
        strategy, strategy_name = random.choice(strategies)  # Randomly select a strategy and its name
        bidders.append(Bidder(id=i + 1, base_valuation=valuation, strategy=strategy, strategy_name=strategy_name))
    return bidders

if __name__ == "__main__":
    reserve_price = 750
    num_bidders = 20
    valuation_range = (500, 1500)

    print(f"Reserve Price: {reserve_price}\n# Bidders: {num_bidders}\nValuation Range: {valuation_range}\n")

    # Initialize strategy instances
    nash_strategy = NashEquilibriumStrategy(reserved_price=reserve_price, num_bidders=num_bidders)
    simple_strategy = SimpleProportionalStrategy(risk_factor=0.85)
    follower_strategy = FollowerStrategy(fallback_strategy=simple_strategy)

    strategies = [
        (nash_strategy, "Nash Equilibrium"),
        (simple_strategy, "Simple Proportional"),
        (follower_strategy, "Follower Strategy")
    ]

    auctioneer = Auctioneer(valuation=1000, reserve_price=reserve_price)
    bidders = generate_bidders(num_bidders, strategies, valuation_range)

    for bidder in bidders:
        print(f"Bidder {bidder.id}: Valuation = {bidder.base_valuation:.2f}, Strategy = {bidder.strategy_name}")

    auction = AuctionSystem(auctioneer, bidders, num_rounds=5)
    auction.conduct_auction()
    auction.analyze_revenue()
