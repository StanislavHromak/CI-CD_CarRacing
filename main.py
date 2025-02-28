import game as g
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Racing Game with difficulty levels")
    parser.add_argument(
        "--difficulty",
        type=str,
        choices=["easy", "medium", "hard"],
        default="easy",
    )
    args = parser.parse_args()

    game = g.Game()
    difficulty_mapping = {
        "easy": "простий",
        "medium": "середній",
        "hard": "складний"
    }
    game.settings.set_difficulty(difficulty_mapping.get(args.difficulty, "складний"))
    game.run()