# Dice Game with HMAC-based Proof of Fairness

## Overview

This Python-based dice game introduces an innovative mechanism to ensure **proof of fairness** using **HMAC (Hash-based Message Authentication Code)** and **SHA3-256 encryption**. Players can enjoy a competitive game against the computer with complete confidence in the integrity of the results.

## Features

- **Secure and Transparent Fairness Mechanism**: HMAC and SHA3-256 ensure that random choices are tamper-proof, with the key revealed after user interaction for verification.
- **Customizable Dice Configurations**: Players can use dice of varying sides and configurations.
- **Probability Display**: Calculate and display probabilities of winning based on selected dice configurations.
- **Interactive Gameplay**: The user and computer take turns selecting dice, rolling them, and determining the winner.

## How It Works

1. **Dice Configuration**:
    
    - Users pass custom dice configurations via command-line arguments.
    - Each die must have at least 4 sides, and all dice must have the same number of sides.
2. **Proof of Fairness**:
    
    - A secret key is generated using `secrets.token_bytes()`.
    - The computer makes its move, generating a random number and its corresponding HMAC.
    - The HMAC is shared with the user before their guess, ensuring no changes can be made post-decision.
    - Once the user makes their move, the secret key is revealed, allowing them to verify the fairness.
3. **Gameplay**:
    
    - The first player is determined through an HMAC-based protocol.
    - Each player selects their dice, either manually or with assistance (e.g., probability display).
    - Dice are rolled, results are calculated, and the winner is declared.
4. **Verification**:
    
    - At every step involving randomness, HMAC values and keys are provided for verification.

## Usage

Run the script with custom dice configurations as command-line arguments. For example:

```bash
python3 game.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3
```

Each argument represents a die, with its sides separated by commas. Ensure:

- Each die has at least 4 sides.
- All dice have the same number of sides.

## Example Gameplay

1. **Start the Game**:
    
    ```bash
    python3 game.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3
    ```
    
2. **First Move**:
    
    - The computer generates a random number and its HMAC.
    - You guess if the random number is `0` or `1`.
3. **Dice Selection**:
    
    - The first player selects their dice from the provided configurations.
    - Probability information can be displayed to aid decision-making.
4. **Dice Rolls**:
    
    - Both players roll their dice, and results are compared.
    - The HMAC and secret key for rolls are revealed for verification.
1. **Result**:
    
    - The winner is determined based on the dice values rolled.

## Example Walkthrough

### Input

```bash
python3 game.py 2,2,4,4,9,9 6,8,1,1,8,6 6,8,1,1,8,6
```

### Output

```text
Dice configurations: [Dice(2, 2, 4, 4, 9, 9), Dice(6, 8, 1, 1, 8, 6), Dice(6, 8, 1, 1, 8, 6)]
Determining who makes the first move...
HMAC=ec0665a0a3fbf8dd1cf3ac7c2b07bfba2b8a1a5858899d252cf195f58ad5ed73
Guess 0 or 1 (X to exit): 1
My choice: 1 (KEY=c2e6fca641d2e56db001e93712d0e58198c4f9c81d697321e59684fd71a4fd9c)

You go first!
Choose your dice or type 'help' for probabilities:
0: 2, 2, 4, 4, 9, 9
1: 6, 8, 1, 1, 8, 6
2: 6, 8, 1, 1, 8, 6
Your choice: help

Probabilities of winning for each dice pair:
User Dice \ Computer Dice | Probability of Winning
---------------------------------------------
[2, 2, 4, 4, 9, 9] vs [6, 8, 1, 1, 8, 6] | 0.56
[2, 2, 4, 4, 9, 9] vs [6, 8, 1, 1, 8, 6] | 0.56
[6, 8, 1, 1, 8, 6] vs [2, 2, 4, 4, 9, 9] | 0.44
[6, 8, 1, 1, 8, 6] vs [6, 8, 1, 1, 8, 6] | 0.33
[6, 8, 1, 1, 8, 6] vs [2, 2, 4, 4, 9, 9] | 0.44
[6, 8, 1, 1, 8, 6] vs [6, 8, 1, 1, 8, 6] | 0.33

Choose your dice or type 'help' for probabilities:
0: 2, 2, 4, 4, 9, 9
1: 6, 8, 1, 1, 8, 6
2: 6, 8, 1, 1, 8, 6
Your choice: 2
You chose: Dice(6, 8, 1, 1, 8, 6)
Computer chose: Dice(2, 2, 4, 4, 9, 9)

Lets generate my throw:
Choosing a number between 0-5 (HMAC: a45d0e7c02c30d23143c54a57f5b3f26cfa45a958b6cee82493874b5aa80580e)
Pick a number (0-5): 3
The result is 3 + 3 = 0 (mod 6)
KEY: 5505cba14d391e1084c3aa0da758abef0bd2cb2be2a240c4e1c7175e63b939c5
My throw: 2

Now lets generate your throw:
Choosing a number between 0-5 (HMAC: fc5efa352323d8fe27e0e8ebc24247ccb0b3d8bce109dff33ab85bba0cc22650)
Pick a number (0-5): 5
The result is 1 + 5 = 0 (mod 6)
KEY: 0721dc9c65de6e86898214d9760b556123aca1e08cfb6a1d35f41b039a9ac74a
Your throw: 6

2 < 6: You win!
```

## Proof of Fairness

- Every random decision is accompanied by:
    1. **HMAC**: A hash value created using the random decision and a secret key.
    2. **Key Reveal**: The secret key is revealed post-user action, allowing the HMAC to be verified.

## License

This project is licensed under the MIT License.

---

Enjoy a secure and fair dice game with confidence! 🐍🎲
