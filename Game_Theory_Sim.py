#!/usr/bin/env python3
"""
Terminal-based Game Theory Simulator with Menu
----------------------------------------------

Features:
- Menu to load predefined games or create a custom game.
- User chooses number of repetitions for simulation.
- Finds pure Nash equilibria.
- Simulates repeated play with random strategies.

"""

import itertools
import random

# ---------- Predefined Games ----------

def prisoners_dilemma():
    players = ["Player 1", "Player 2"]
    strategies = {p: ["Cooperate", "Defect"] for p in players}
    payoffs = {
        ("Cooperate", "Cooperate"): (3, 3),
        ("Cooperate", "Defect"): (0, 5),
        ("Defect", "Cooperate"): (5, 0),
        ("Defect", "Defect"): (1, 1),
    }
    return players, strategies, payoffs

def stag_hunt():
    players = ["Player 1", "Player 2"]
    strategies = {p: ["Stag", "Hare"] for p in players}
    payoffs = {
        ("Stag", "Stag"): (4, 4),
        ("Stag", "Hare"): (0, 3),
        ("Hare", "Stag"): (3, 0),
        ("Hare", "Hare"): (3, 3),
    }
    return players, strategies, payoffs

def matching_pennies():
    players = ["Player 1", "Player 2"]
    strategies = {p: ["Heads", "Tails"] for p in players}
    payoffs = {
        ("Heads", "Heads"): (1, -1),
        ("Heads", "Tails"): (-1, 1),
        ("Tails", "Heads"): (-1, 1),
        ("Tails", "Tails"): (1, -1),
    }
    return players, strategies, payoffs


# ---------- Custom Game Input ----------

DEFAULT_STRATEGIES = ["Cooperate", "Defect"]

def input_game():
    num_players = int(input("Enter number of players: "))
    players = [f"Player {i+1}" for i in range(num_players)]
    strategies = {p: DEFAULT_STRATEGIES[:] for p in players}

    print("\nDefined strategies for each player:")
    for p in players:
        print(f"{p}: {strategies[p]}")

    payoffs = {}
    print("\nNow enter payoffs for each profile.")
    print("Format: payoff for each player, separated by spaces (e.g., '3 2')\n")

    for profile in itertools.product(*[strategies[p] for p in players]):
        print(f"Profile {profile}: ", end="")
        vals = list(map(float, input().split()))
        if len(vals) != num_players:
            raise ValueError("Number of payoffs must match number of players")
        payoffs[profile] = tuple(vals)

    return players, strategies, payoffs


# ---------- Solvers ----------

def pure_nash_equilibria(players, strategies, payoffs):
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
    history = []
    total_scores = {p: 0 for p in players}

    for r in range(repetitions):
        profile = tuple(random.choice(strategies[p]) for p in players)
        payoff = payoffs[profile]
        history.append((profile, payoff))
        for i, p in enumerate(players):
            total_scores[p] += payoff[i]

    return history, total_scores


# ---------- Menu System ----------

def choose_game():
    print("\n=== Game Theory Simulator Menu ===")
    print("1. Prisoner's Dilemma")
    print("2. Stag Hunt")
    print("3. Matching Pennies")
    print("4. Custom Game")
    choice = input("Choose a game (1-4): ")

    if choice == "1":
        return prisoners_dilemma()
    elif choice == "2":
        return stag_hunt()
    elif choice == "3":
        return matching_pennies()
    elif choice == "4":
        return input_game()
    else:
        print("Invalid choice, defaulting to Prisoner's Dilemma.")
        return prisoners_dilemma()


# ---------- Main ----------

def main():
    players, strategies, payoffs = choose_game()
    repetitions = int(input("\nEnter number of repetitions for simulation: "))

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
