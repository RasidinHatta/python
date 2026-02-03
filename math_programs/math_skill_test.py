import random

def powerof5():
    """
    Generate two random decimal digits (0-9) for a and b,
    then calculate (ab)^5 where ab is the two-digit number.
    For example: a=0, b=2 gives 02^5 = 2^5 = 32
    """
    # Generate two random decimal digits
    a = random.randint(0, 9)
    b = random.randint(0, 9)
    
    # Form the two-digit number
    number = a * 10 + b
    
    # Calculate the power of 5
    result = number ** 5
    
    return a, b, number, result

def main():
    print("=" * 50)
    print("Welcome to the Math Skill Test - Power of 5!")
    print("=" * 50)
    print()
    
    score = 0
    total_questions = 0
    
    while True:
        print("\n" + "-" * 50)
        print("New Question!")
        print("-" * 50)
        
        # Generate the problem
        a, b, number, result = powerof5()
        
        # Display the result
        print(f"\nThe result is: ab^5 = {result}")
        print()
        
        # Get user's guess
        try:
            guess_a = int(input("What is the value of 'a'? "))
            guess_b = int(input("What is the value of 'b'? "))
            
            # Check if the guess is correct
            total_questions += 1
            
            if guess_a == a and guess_b == b:
                print("\n✓ Correct! Well done!")
                score += 1
            else:
                print(f"\n✗ Wrong! The correct answer was: a = {a}, b = {b}")
                print(f"   ({a}{b})^5 = {number}^5 = {result}")
            
            # Show current score
            print(f"\nYour score: {score}/{total_questions}")
            
        except ValueError:
            print("\n⚠ Invalid input! Please enter numbers only.")
            continue
        
        # Ask if user wants to continue
        print()
        continue_game = input("Do you want another question? (yes/no): ").lower()
        
        if continue_game not in ['yes', 'y']:
            break
    
    # Final score
    print("\n" + "=" * 50)
    print("Game Over!")
    print("=" * 50)
    print(f"Final Score: {score}/{total_questions}")
    
    if total_questions > 0:
        percentage = (score / total_questions) * 100
        print(f"Accuracy: {percentage:.1f}%")
        
        if percentage == 100:
            print("🏆 Perfect score! You're a math genius!")
        elif percentage >= 80:
            print("🌟 Great job! Keep it up!")
        elif percentage >= 60:
            print("👍 Good effort! Practice makes perfect!")
        else:
            print("💪 Keep practicing! You'll get better!")
    
    print("\nThank you for playing!")

if __name__ == "__main__":
    main()
