celsius = [39.2, 36.5, 37.3, 37.8]
fahrenheit = map(lambda f: f * 1.8 + 32, celsius)
print (list(fahrenheit))