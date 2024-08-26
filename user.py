class User:
    def __init__(self, name, age, weight, height, bodyfat):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.bodyfat = bodyfat

    def __str__(self):
        return (f"Name: {self.name}, Age: {self.age}, Weight: {self.weight} kg, "
                f"Height: {self.height} cm, Body Fat: {self.bodyfat}%")