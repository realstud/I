import itertools

def solve_cryptarithmetic(puzzle):
    # Parsing
    parts = puzzle.replace("=", "+").split("+")
    parts = [part.strip() for part in parts]
    words = parts[:-1]
    result = parts[-1]
    
    # Extracting unique letters
    all_letters = set()
    for word in parts:
        for letter in word:
            if letter.isalpha():
                all_letters.add(letter)
    all_letters = sorted(list(all_letters))
    
    # Find first letters (can't be zero)
    first_letters = set()
    for word in parts:
        for letter in word:
            if letter.isalpha():
                first_letters.add(letter)
                break
    
    for perm in itertools.permutations(range(10), len(all_letters)):
        letter_to_digit = {letter: digit for letter, digit in zip(all_letters, perm)}
        
        # Check first letter constraints (no leading zero)
        valid_first_letters = True
        for letter in first_letters:
            if letter_to_digit[letter] == 0:
                valid_first_letters = False
                break
        if not valid_first_letters:
            continue
        
        # Convert words to numbers
        nums = []
        for word in words:
            num = 0
            for letter in word:
                if letter.isalpha():
                    num = num * 10 + letter_to_digit[letter]
            nums.append(num)
        
        # Convert result to number
        res = 0
        for letter in result:
            if letter.isalpha():
                res = res * 10 + letter_to_digit[letter]
        
        # Check if the sum matches
        if sum(nums) == res:
            return letter_to_digit
    
    return None

def print_cryptarithmetic_solution(puzzle, solution):
    if solution is None:
        print("No solution found.")
        return
    
    parts = puzzle.replace("=", "+").split("+")
    parts = [part.strip() for part in parts]
    
    print("Original puzzle:", puzzle)
    print("\nSolution:")
    
    for word in parts:
        word = word.strip()
        if "=" in word:
            word = word.replace("=", "").strip()
    
        num = 0
        for letter in word:
            if letter.isalpha():
                num = num * 10 + solution[letter]
        
        
        print(f"{word} = {num} ({' '.join(str(solution[l]) for l in word if l.isalpha())})")
    
    
    equation = puzzle
    for letter, digit in solution.items():
        equation = equation.replace(letter, str(digit))
    print("\nVerified equation:", equation)

if __name__ == "__main__":
    print("Cryptarithmetic Puzzle Solver")
    print("-" * 30)
    print("Enter a puzzle in the form: SEND + MORE = MONEY")
    
    while True:
        puzzle = input("Enter puzzle (or 'q' to quit): ")
        
        if puzzle.lower() == 'q':
            break
        
        if "=" not in puzzle:
            print("Invalid puzzle format. Must include '='.")
            continue
        
        print("\nSolving puzzle, please wait...")
        solution = solve_cryptarithmetic(puzzle)
        print_cryptarithmetic_solution(puzzle, solution)
        print("-" * 50)