import random


def roll_dice(sides):
    return random.randint(1, sides)

# todo: add more dice types (d4, d6, d8, d10, d12, d20) and a function to roll multiple dice at once (e.g., 2d6)


def roll_multiple_dice(num_dice, sides):

    if num_dice <= 0:
        raise ValueError("Number of dice must be greater than 0")
    if sides <= 0:
        raise ValueError("Dice must have more than 0 sides")
    rolls = [roll_dice(sides) for _ in range(num_dice)]
    return rolls, sum(rolls)  # returns individual rolls and their total


def roll_from_string(dice_string):
    try:
        num_dice, sides = map(int, dice_string.lower().split('d'))
        return roll_multiple_dice(num_dice, sides)
    except Exception as e:
        raise ValueError("Invalid dice format. Use NdM (e.g., 2d6)") from e
