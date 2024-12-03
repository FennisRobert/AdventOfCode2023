from pathlib import Path


import argparse

def main(arg1, arg2):
    # Your script's main logic here
    day = int(arg1)
    year = int(arg2)
    
    filetext = f"""from aoc import *

######## PART 1 #######
data = load({day},{year},test=True)

print(data)

print(f'Solution to part 1: {{None}}')

######## PART 2 #######
data = load({day},{year},test=True)

print(data)

print(f'Solution to part 2: {{None}}')

    """
    
    with open(str(Path(str(year)) / f'day{day}.txt'), 'w') as file:
        file.write('')
    with open(str(Path(str(year)) / f'day{day}test.txt'), 'w') as file:
        file.write('')
    with open(f'{year}_{day}.py','w') as f:
        f.write(filetext)
    
    
if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Description of your script")

    # Add arguments to the parser
    parser.add_argument('arg1', type=str, help='Description of argument 1')
    parser.add_argument('arg2', type=int, help='Description of argument 2')

    # Parse the arguments from the command line
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args.arg1, args.arg2)