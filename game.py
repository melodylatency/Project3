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
    def generate_fair_number(lower: int, upper: int, key: bytes, seed: bytes = None) -> int:
        """Generates a fair number within the given range using a secure random key."""
        if seed:
            hmac_value = hmac.new(key, seed, hashlib.sha3_256).digest()
        else:
            hmac_value = hmac.new(key, secrets.token_bytes(32), hashlib.sha3_256).digest()
        return int.from_bytes(hmac_value[:2], 'big') % (upper - lower + 1) + lower


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
            
            # Check if the die has at least 4 sides.
            if len(values) < 4:
                raise ValueError(f"Invalid dice configuration: {arg}. Each die must have at least 4 sides.")
            
            # Check if all dice have the same number of sides.
            if dice_sides is None:
                dice_sides = len(values)  # Set the expected number of sides.
            elif len(values) != dice_sides:
                raise ValueError(f"Inconsistent number of sides: {arg}. All dice must have {dice_sides} sides.")
            
            # Add the valid dice to the list.
            self.dice_list.append(Dice(values))
        
        print(f"Dice configurations: {self.dice_list}")


    def determine_first_move(self):
        """Determine who makes the first move using provable fair random generation."""
        print("Let's determine who makes the first move.")

        # Step 1: Generate a secure random number (0 or 1)
        random_number = secrets.randbelow(2)  # Fair random integer in the range [0, 1]
        
        # Step 2: Generate a cryptographic key
        self.secret_key = RandomFairGenerator.generate_secure_key()
        
        # Step 3: Calculate HMAC for the random number
        hmac_value = hmac.new(self.secret_key, str(random_number).encode(), hashlib.sha3_256).hexdigest()
        print(f"HMAC={hmac_value.upper()}")
        
        print("Try to guess my selection.")
        print("0 - 0")
        print("1 - 1")
        print("X - exit")
        print("? - help")
        
        while True:
            choice = input("Your selection: ").strip()
            
            if choice == '0' or choice == '1':
                user_guess = int(choice)
                
                # Reveal the computer's choice and key
                print(f"My selection: {random_number} (KEY={self.secret_key.hex()})")
                
                # Determine who goes first
                if user_guess == random_number:
                    self.first_player = 'user'
                    print("You guessed correctly! You make the first move.")
                else:
                    self.first_player = 'computer'
                    print("You guessed incorrectly. I make the first move.")
                break
            
            elif choice.lower() == 'x':
                sys.exit(0)
            
            elif choice.lower() == '?':
                self.display_help()
            
            else:
                print("Invalid choice. Please try again.")


    def play_turn(self, player: str, available_dice: List[Dice]):
        """Allow a player to select a dice and generate a throw."""
        print(f"{player.capitalize()}'s turn!")
        print("Choose your dice:")
        for idx, dice in enumerate(available_dice):
            print(f"{idx} - {', '.join(map(str, dice.values))}")

        while True:
            choice = input("Your selection: ").strip()
            if choice.lower() == 'x':
                sys.exit(0)
            elif choice.isdigit() and int(choice) < len(available_dice):
                if player == 'user':
                    self.user_dice = available_dice[int(choice)]
                else:
                    self.computer_dice = available_dice[int(choice)]
                break
            else:
                print("Invalid choice. Please try again.")

    def play_game(self):
        """Play the dice game."""
        self.determine_first_move()

        # Determine dice selection
        available_dice = self.dice_list.copy()
        if self.first_player == 'computer':
            self.play_turn('computer', available_dice)
            available_dice.remove(self.computer_dice)  # Remove selected dice from the list for user
            self.play_turn('user', available_dice)
        else:
            self.play_turn('user', available_dice)
            available_dice.remove(self.user_dice)  # Remove selected dice from the list for computer
            self.play_turn('computer', available_dice)

        # Computer selects its throw
        print(f"My selection: {self.computer_dice.values}")
        computer_throw = self.generate_throw(self.computer_dice)

        # User selects their throw
        print(f"Your selection: {self.user_dice.values}")
        user_throw = self.generate_throw(self.user_dice)

        # Display throws and keys
        print(f"My throw: {computer_throw} (KEY={self.secret_key.hex()})")
        print(f"Your throw: {user_throw} (KEY={self.secret_key.hex()})")

        if computer_throw == user_throw:
            print("It's a tie!")
        elif user_throw > computer_throw:
            print(f"{user_throw} > {computer_throw}: You win!")
        else:
            print(f"{user_throw} < {computer_throw}: I win!")

    def generate_throw(self, dice: Dice):
        """Generate a throw using the dice and the shared key."""
        seed = secrets.token_bytes(16)  # Unique seed for each roll
        fair_number = RandomFairGenerator.generate_fair_number(0, len(dice.values) - 1, self.secret_key, seed)
        return dice.values[fair_number]

    def display_help(self):
        """Display help information."""
        print("Help: The game is fair because both the computer and user participate in the random number generation process.")
        print("Here is the probability table for each dice pair:\n")
        print(TableGenerator.generate_probability_table(self.dice_list))


# --- TableGenerator Class (for help table generation) ---
class TableGenerator:
    @staticmethod
    def generate_probability_table(dice_list: List[Dice]):
        """Generate a table showing probabilities of winning for each dice pair."""
        table = []
        for i, dice1 in enumerate(dice_list):
            for j, dice2 in enumerate(dice_list):
                if i != j:
                    prob = TableGenerator.simulate_game(dice1, dice2)  # Simulate to get the winning probability
                    table.append(f"Dice {i} vs Dice {j} -> Win Probability: {prob:.2f}")
        return "\n".join(table)

    @staticmethod
    def simulate_game(dice1: Dice, dice2: Dice) -> float:
        """Simulate many games to estimate win probabilities."""
        wins = 0
        draws = 0
        total = 10000  # Simulate 10,000 games for approximation
        for _ in range(total):
            roll1 = secrets.choice(dice1.values)
            roll2 = secrets.choice(dice2.values)
            if roll1 > roll2:
                wins += 1
            elif roll1 == roll2:
                draws += 1
        return wins / (total - draws)


# Main Program Execution
if __name__ == "__main__":
    dice_game = DiceGame(dice_list=[])
    
    try:
        dice_game.validate_arguments()
        dice_game.play_game()
    except ValueError as e:
        print(f"Error: {e}")
        print("Example usage: python3 game.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3")
        sys.exit(1)
