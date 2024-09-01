import random

class Common:

    @staticmethod
    def generate_prompt():
        subjects = ['A cat', 'The sun', 'A dog',
                    'The ocean', 'The moon', 'The Earth', 'A robot']
        verbs = ['jumps', 'shines', 'laughs', 'reflects', 'dances', 'sleeps']
        adjectives = ['happy', 'bright', 'playful',
                    'mysterious', 'colorful', 'beautiful']
        objects = ['on the roof', 'on galaxy', 'in the sky',
                'at the party', 'under the moon', 'in the forest']

        sentence = f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(adjectives)} {random.choice(objects)}"
        return sentence