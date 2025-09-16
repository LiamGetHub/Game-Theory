#!/usr/bin/env python3
"""
Terminal-based Game Theory Simulator
------------------------------------

Features:
- User chooses number of players.
- User chooses number of repetitions (repeated play).
- Strategies are defined in code (can be extended easily).
- Payoffs must be filled in for every profile.
- Finds pure Nash equilibria.
"""

import itertools

# ---------- Setup ----------

# Example strategies (edit this list to add your own)
DEFAULT_STRATEGIES = ["Cooperate", "Defect"]

def input_game():
    """Create a game from user input."""
    num_players = int(input("Enter number of players: "))
    repetitions = int(input("Enter number of repetitions: "))

    players = [f"Player {i+1}" for i in range(num_players)]
    strategies = {p: DEFAULT_STRATEGIES[:] for p in players}

    print("\nDefined strategies for each player:")
    for p in players:
        print(f"{p}: {strategies[p]}")

    # Get payoffs
    payoffs = {}
    print("\nNow enter payoffs for each profile.")
    print("Format: payoff for each player, separated by spaces (e.g., '3 2')\n")

    for profile in itertools.product(*[strategies[p] for p in players]):
        print(f"Profile {profile}: ", end="")
        vals = list(map(float, input().split()))
        if len(vals) != num_players:
            raise ValueError("Number of payoffs must match number of players")
        payoffs[profile] = tuple(vals)

    return players, strategies, payoffs, repetitions


# ---------- Solvers ----------

def pure_nash_equilibria(players, strategies, payoffs):
    """Return list of pure-strategy Nash equilibria."""
    equilibria = []
    for prof in itertools.product(*[strategies[p] for p in players]):
        current = payoffs[prof]
        is_eq = True
        for i, p in enumerate(players):
            best = current[i]
            for alt in strategies[p]:
                if alt == prof[i]:
                    continue
                alt_prof = list(prof)
                alt_prof[i] = alt
                alt_prof = tuple(alt_prof)
                if payoffs[alt_prof][i] > best:
                    is_eq = False
                    break
            if not is_eq:
                break
        if is_eq:
            equilibria.append(prof)
    return equilibria


# ---------- Simulation ----------

def simulate(players, strategies, payoffs, repetitions):
    """Play the game repeatedly (players pick random strategies each round)."""
    import random
    history = []
    total_scores = {p: 0 for p in players}

    for r in range(repetitions):
        profile = tuple(random.choice(strategies[p]) for p in players)
        payoff = payoffs[profile]
        history.append((profile, payoff))
        for i, p in enumerate(players):
            total_scores[p] += payoff[i]

    return history, total_scores


# ---------- Main ----------

def main():
    players, strategies, payoffs, repetitions = input_game()

    print("\n=== Pure Nash Equilibria ===")
    equilibria = pure_nash_equilibria(players, strategies, payoffs)
    if equilibria:
        for eq in equilibria:
            print("NE:", eq, "->", payoffs[eq])
    else:
        print("No pure strategy NE found.")

    print("\n=== Simulation of repeated play ===")
    history, totals = simulate(players, strategies, payoffs, repetitions)
    for round_num, (prof, payoff) in enumerate(history, start=1):
        print(f"Round {round_num}: {prof} -> {payoff}")

    print("\nTotal scores after", repetitions, "rounds:")
    for p in players:
        print(f"{p}: {totals[p]}")


if __name__ == "__main__":
    main()
