# src/lap_doer/example.py


def greet(name):
    greeting = f"Hello, {name}!"  # unused variable, missing type hints

    return greeting


def unused_function():
    pass


def main():
    print(greet("World"))


if __name__ == "__main__":
    main()
