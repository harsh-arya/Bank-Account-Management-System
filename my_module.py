# My Function Module

# Refactoring String for precise comparison
def refactor(str):
    return str.strip().lower()

# Universal Function which takes Title & Options (Dictionary) menu with title, options as attributes
def menu(title, options):
    print("\n" + "="*50)
    print(f'{title.upper()}'.center(50))
    print("="*50)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option.title()}")
    print("="*50 + "\n")

    try:
        choice = int(input(f"Enter your choice(1-{len(options)}) : "))
        if 1 <= choice <= len(options):
            return choice
        print(f"Enter numerical value within range (1-{len(options)}).")
        return False
    except ValueError:
        print("Error! Please enter numerical value.")
        return False