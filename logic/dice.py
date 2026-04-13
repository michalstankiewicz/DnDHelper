import random


def roll_dice(sides):
    """Basic dice roll"""
    return random.randint(1, sides)


def roll_multiple_dice(num_dice, sides):
    """Roll more then 1 dice """
    if num_dice <= 0:
        raise ValueError("Number of dice must be greater than 0")
    if sides <= 0:
        raise ValueError("Dice must have more than 0 sides")
    rolls = [roll_dice(sides) for _ in range(num_dice)]
    return rolls, sum(rolls)  # returns individual rolls and their total


def roll_from_string(dice_string):
    """Allow roll from str user input"""
    try:
        num_dice, sides = map(int, dice_string.lower().split('d'))
        return roll_multiple_dice(num_dice, sides)
    except Exception as e:
        raise ValueError("Invalid dice format. Use NdM (e.g., 2d6)") from e
