from random import choices, uniform
import string

def generate_data(num_rows):
    data = []
    for _ in range(num_rows):
        chemical = ''.join(choices(string.ascii_uppercase, k=1) + choices(string.ascii_lowercase, k=1))
        quantity = round(uniform(0, 100), 2)
        data.append((chemical, quantity))
    return data

# Generate 10 rows of data
data = generate_data(10)
print(data)