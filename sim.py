#!/usr/bin/env python3
"""
Iterated Game Theory Tournament
-------------------------------
- Define strategies as Python functions.
- Run them against each other in repeated games.
- Tally scores and see which strategy performs best.

Default: Iterated Prisoner's Dilemma.
"""

import itertools
import random

# ------------------ Payoff Matrix ------------------
# (Player1 move, Player2 move) -> (P1 payoff, P2 payoff)
PD_PAYOFFS = {
    ("C", "C"): (3, 3),
    ("C", "D"): (0, 5),
    ("D", "C"): (5, 0),
    ("D", "D"): (1, 1),
}

# ------------------ Strategy Functions ------------------
# Each strategy takes (my_history, opp_history) and returns "C" or "D".

def always_cooperate(my_hist, opp_hist):
    return "C"

def always_defect(my_hist, opp_hist):
    return "D"

def tit_for_tat(my_hist, opp_hist):
    if not opp_hist:
        return "C"  # cooperate first
    return opp_hist[-1]  # copy opponent’s last move

def random_strategy(my_hist, opp_hist):
    return random.choice(["C", "D"])

# You can add new strategies here!


# ------------------ Tournament Simulator ------------------

def play_rounds(strat1, strat2, rounds=10, payoff_matrix=PD_PAYOFFS):
    """Play repeated game between two strategies for given rounds."""
    history1, history2 = [], []
    score1, score2 = 0, 0

    for _ in range(rounds):
        move1 = strat1(history1, history2)
        move2 = strat2(history2, history1)
        payoff = payoff_matrix[(move1, move2)]
        score1 += payoff[0]
        score2 += payoff[1]
        history1.append(move1)
        history2.append(move2)

    return score1, score2


def tournament(strategies, rounds_per_game=10):
    """Run round-robin tournament among all strategies."""
    totals = {name: 0 for name in strategies}

    for (name1, strat1), (name2, strat2) in itertools.combinations(strategies.items(), 2):
        s1, s2 = play_rounds(strat1, strat2, rounds=rounds_per_game)
        totals[name1] += s1
        totals[name2] += s2
        # also let them play against themselves
    for name, strat in strategies.items():
        s1, s2 = play_rounds(strat, strat, rounds=rounds_per_game)
        totals[name] += s1  # self-play counts too

    return totals


# ------------------ Main ------------------

def main():
    # Define the set of strategies in the tournament
    strategies = {
        "Always Cooperate": always_cooperate,
        "Always Defect": always_defect,
        "Tit for Tat": tit_for_tat,
        "Random": random_strategy,
    }

    rounds_per_game = int(input("Enter number of rounds per matchup: "))
    results = tournament(strategies, rounds_per_game)

    print("\n=== Tournament Results ===")
    for name, score in sorted(results.items(), key=lambda x: -x[1]):
        print(f"{name}: {score} points")


if __name__ == "__main__":
    main()
