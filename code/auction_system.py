import pandas as pd
import matplotlib.pyplot as plt
from strategy import FollowerStrategy

class AuctionSystem:
    def __init__(self, auctioneer, bidders, num_rounds):
        self.auctioneer = auctioneer
        self.bidders = bidders
        self.num_rounds = num_rounds
        self.history = []

    def conduct_auction(self):
        for round_num in range(1, self.num_rounds + 1):
            bids = []

            for bidder in self.bidders:
                bid = bidder.place_bid(self.history)
                if bid is not None:
                    bids.append((bid, bidder))

            valid_bids = [(bid, bidder) for bid, bidder in bids if self.auctioneer.is_bid_acceptable(bid)]
            if valid_bids:
                valid_bids.sort(reverse=True, key=lambda x: x[0])
                highest_bid, winner = valid_bids[0]
                winner.won_units += 1
                self.history.append({"round": round_num, "winner": winner.id, "bid": highest_bid})

                # Notify all followers of the winning bid
                for bidder in self.bidders:
                    if isinstance(bidder.strategy, FollowerStrategy):
                        bidder.strategy.update_last_winner_bid(highest_bid)

            else:
                self.history.append({"round": round_num, "winner": None, "bid": None})

    def analyze_revenue(self):
        if not hasattr(self, 'history') or not self.history:
            print("No auction history available. Run the auction first.")
            return

        revenue_per_round = pd.DataFrame(self.history)

        if revenue_per_round.empty:
            print("No revenue data to analyze.")
            return

        round_revenues = revenue_per_round["bid"]

        print("\nRevenue per Round:")
        print(round_revenues.describe())

        plt.figure(figsize=(10, 6))
        plt.plot(revenue_per_round["round"], round_revenues, marker='o', linestyle='-')
        plt.title("Revenue per Round")
        plt.xlabel("Auction Round")
        plt.ylabel("Revenue")
        plt.grid(True)
        plt.show()