import sys
sys.version


library = {"tom": 10, "tony": 2, "sam": 20}
library_a = ["a", "A", "b", "c"]
library_b = []

for name in library_a:

    if "a" in name or "A" in name:
        library_b.append(name.upper())
    else:
        pass

print(library_b)