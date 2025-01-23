import sys
import secrets
import hmac
import hashlib
from typing import List


# --- Dice Class ---
class Dice:
    def __init__(self, values: List[int]):
        self.values = values

    def __repr__(self):
        return f"Dice({', '.join(map(str, self.values))})"


# --- RandomFairGenerator Class ---
class RandomFairGenerator:
    @staticmethod
    def generate_secure_key() -> bytes:
        """Generates a cryptographically secure random key."""
        return secrets.token_bytes(32)  # 256-bit key

    @staticmethod
    def generate_hmac(value: int, key: bytes) -> str:
        """Generates HMAC for a given value and key."""
        message = str(value).encode()
        return hmac.new(key, message, hashlib.sha3_256).hexdigest()


# --- DiceGame Class ---
class DiceGame:
    def __init__(self, dice_list: List[Dice]):
        self.dice_list = dice_list
        self.computer_dice = None
        self.user_dice = None
        self.first_player = None
        self.secret_key = RandomFairGenerator.generate_secure_key()

    def validate_arguments(self):
        if len(sys.argv) < 4:
            raise ValueError("Not enough dice provided. You need to provide 3 or more dice configurations.")

        dice_sides = None  # To track the number of sides for consistency check.
        self.dice_list = []  # Ensure dice_list is initialized.

        for arg in sys.argv[1:]:
            try:
                values = list(map(int, arg.split(',')))
            except ValueError:
                raise ValueError(f"Invalid dice configuration: {arg}. Ensure each value is an integer.")

            if len(values) < 4:
                raise ValueError(f"Invalid dice configuration: {arg}. Each die must have at least 4 sides.")

            if dice_sides is None:
                dice_sides = len(values)
            elif len(values) != dice_sides:
                raise ValueError(f"Inconsistent number of sides: {arg}. All dice must have {dice_sides} sides.")

            self.dice_list.append(Dice(values))

        print(f"Dice configurations: {self.dice_list}")

    def determine_first_move(self):
        print("Determining who makes the first move...")
        random_number = secrets.randbelow(2)  # 0 or 1
        self.secret_key = RandomFairGenerator.generate_secure_key()
        hmac_value = hmac.new(self.secret_key, str(random_number).encode(), hashlib.sha3_256).hexdigest()
        print(f"HMAC={hmac_value}")

        while True:
            choice = input("Guess 0 or 1 (X to exit): ").strip()
            if choice == '0' or choice == '1':
                user_guess = int(choice)
                print(f"My choice: {random_number} (KEY={self.secret_key.hex()})")
                print("")
                if user_guess == random_number:
                    self.first_player = 'user'
                    print("You go first!")
                else:
                    self.first_player = 'computer'
                    print("I go first!")
                break
            elif choice.lower() == 'x':
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")

    def play_turn(self, player: str, available_dice: List[Dice]):
        if player == 'computer':
            computer_choice_index = secrets.randbelow(len(available_dice))
            self.computer_dice = available_dice[computer_choice_index]
            print(f"Computer chose: {self.computer_dice}")
        else:
            while True:
                print("Choose your dice:")
                for idx, dice in enumerate(available_dice):
                    print(f"{idx}: {', '.join(map(str, dice.values))}")
                choice = input("Your choice: ").strip()
                if choice.isdigit() and 0 <= int(choice) < len(available_dice):
                    self.user_dice = available_dice[int(choice)]
                    print(f"You chose: {self.user_dice}")
                    break
                else:
                    print("Invalid choice. Try again.")

    def generate_throw(self):
        self.secret_key = RandomFairGenerator.generate_secure_key()
        computer_choice = secrets.randbelow(len(self.computer_dice.values))
        hmac_value = RandomFairGenerator.generate_hmac(computer_choice, self.secret_key)
        print(f"Choosing a number between 0-{len(self.computer_dice.values) - 1} (HMAC: {hmac_value})")
        user_choice = self.manual_pick(self.user_dice)

        total = computer_choice + user_choice
        index = total % len(self.computer_dice.values)
        print(f"The result is {computer_choice} + {user_choice} = {index} (mod {len(self.computer_dice.values)})")
        print(f"KEY: {self.secret_key.hex()}")

        return index

    def play_game(self):
        self.determine_first_move()

        available_dice = self.dice_list.copy()
        if self.first_player == 'computer':
            self.play_turn('computer', available_dice)
            available_dice.remove(self.computer_dice)
            self.play_turn('user', available_dice)
        else:
            self.play_turn('user', available_dice)
            available_dice.remove(self.user_dice)
            self.play_turn('computer', available_dice)
    
    def end_game(self):
        print("")
        print("Lets generate my throw:")
        computer_index = self.generate_throw()
        computer_throw = self.computer_dice.values[computer_index]
        print(f"My throw: {computer_throw}")
        print("")
        print("Now lets generate your throw:")
        user_index = self.generate_throw()
        user_throw = self.user_dice.values[user_index]
        print(f"Your throw: {user_throw}")
        
        print("")

        if computer_throw == user_throw:
            print(f"{computer_throw} = {user_throw}: It's a tie!")
        elif user_throw > computer_throw:
            print(f"{computer_throw} < {user_throw}: You win!")
        else:
            print(f"{computer_throw} > {user_throw}: Computer wins!")

    def manual_pick(self, dice: Dice):
        while True:
            choice = input(f"Pick a number (0-{len(dice.values) - 1}): ").strip()
            if choice.isdigit() and 0 <= int(choice) < len(dice.values):
                return int(choice)
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    dice_game = DiceGame(dice_list=[])
    try:
        dice_game.validate_arguments()
        dice_game.play_game()
        dice_game.end_game()
    except ValueError as e:
        print(f"Error: {e}")
        print("Example usage: python3 game.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3")
        sys.exit(1)
