import random

def change_tone(text,tone):
    inserts = [
        "amid growing political controversies,",
        "as media outlets speculate on his next move,",
        "raising eyebrows among both critics and supporters,",
        "fueling debates about his priorities,",
        "while analysts question his long-term strategy,",
        "as his approval ratings fluctuate,",
        "in a move that left journalists scrambling for explanations,"
    ]

    words = text.split()
    if len(words) < 5:
        return text  # If too short, return as is

    num_insertions = random.choice([1, 2])  # Randomly decide to insert 1 or 2 phrases

    for _ in range(num_insertions):
        insert_position = random.randint(1, len(words) - 2)  # Pick a random spot
        words.insert(insert_position, random.choice(inserts))

    return " ".join(words)

