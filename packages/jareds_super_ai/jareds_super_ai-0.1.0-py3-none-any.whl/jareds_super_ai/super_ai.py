import numpy as np

class SillyPrinter:
    def __init__(self):
        # Lists of silly words and phrases
        self.silly_animals = [
            "penguin", "narwhal", "platypus", "quokka", "axolotl", 
            "blobfish", "flumpy dog", "dizzy cat", "wobbling duck"
        ]
        
        self.silly_actions = [
            "dancing", "singing opera", "writing poetry", "doing calculus", 
            "knitting a sweater", "playing the kazoo", "juggling marshmallows",
            "riding a unicycle", "solving quantum physics equations"
        ]
        
        self.silly_places = [
            "on the moon", "in a bowl of jelly", "under a giant mushroom",
            "inside a snow globe", "at the bottom of a teacup", 
            "on top of Mount Absurd", "in a bubble bath", "in a sock drawer"
        ]
        
        self.silly_adjectives = [
            "whimsical", "discombobulated", "preposterous", "bamboozled",
            "flabbergasted", "gobsmacked", "topsy-turvy", "higgledy-piggledy"
        ]

    def generate_silly_sentence(self):
        """Generate a random silly sentence using numpy's random functions"""
        # Use numpy's random choice function to select elements
        animal = np.random.choice(self.silly_animals)
        action = np.random.choice(self.silly_actions)
        place = np.random.choice(self.silly_places)
        adjective = np.random.choice(self.silly_adjectives)
        
        # Generate random numbers for extra silliness
        num_exclamations = np.random.randint(1, 5)
        random_number = np.random.randint(3, 42)
        
        # Construct a silly sentence
        templates = [
            f"A {adjective} {animal} is {action} {place}{'!' * num_exclamations}",
            f"Would you believe that {random_number} {animal}s started {action} {place}?",
            f"Breaking news: {adjective} scientist discovers {animal} {action} {place}!",
            f"In a world where {animal}s are {adjective}, one brave {animal} is {action} {place}.",
            f"The {random_number}th rule of {animal} club: always be {action} {place}."
        ]
        
        return np.random.choice(templates)
    
    def generate_silly_fact(self):
        """Generate a completely made-up silly 'fact'"""
        animal1 = np.random.choice(self.silly_animals)
        animal2 = np.random.choice(self.silly_animals)
        adjective = np.random.choice(self.silly_adjectives)
        
        random_percent = np.random.randint(1, 101)
        random_year = np.random.randint(1700, 2023)
        random_number = np.random.randint(2, 500)
        
        templates = [
            f"Did you know? {random_percent}% of {animal1}s are secretly {adjective}.",
            f"Fun fact: Until {random_year}, people believed {animal1}s and {animal2}s were the same creature.",
            f"Scientists have discovered that {animal1}s have {random_number} teeth, but only use 3 of them.",
            f"A group of {animal1}s is called a '{adjective}ness'.",
            f"In {random_year}, a {animal1} was elected mayor of a small town in Norway."
        ]
        
        return np.random.choice(templates)
    
    def print_random_silliness(self, count=1):
        """Print a random selection of silly outputs"""
        for _ in range(count):
            # Choose which type of silly output to generate
            generator_funcs = [
                self.generate_silly_sentence,
                self.generate_silly_fact,
                # self.silly_random_numbers
            ]
            
            generator = np.random.choice(generator_funcs)
            print(generator())

def main():
    silly = SillyPrinter()
    silly.print_random_silliness(3)  # Print 3 random silly things
