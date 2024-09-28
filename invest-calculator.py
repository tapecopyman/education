#https://chatgpt.com/share/66f79dce-6b5c-8006-9d4d-43ac64321cbb
#I want to create an investment calculator.  It will allow me to input an initial investment amount and the average annual return.  
#I will also be able to input the number of years for the investment.  
# Make a python program for this
# by ChatGPT o1-mini


def get_positive_float(prompt):
    """
    Prompt the user to enter a positive float value.
    Repeats until a valid positive float is entered.
    """
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def calculate_future_value(initial_investment, annual_return, years):
    """
    Calculate the future value of an investment based on compound interest.
    
    Parameters:
    - initial_investment (float): The initial amount invested.
    - annual_return (float): The annual return rate (as a percentage).
    - years (int): The number of years the money is invested.
    
    Returns:
    - float: The future value of the investment.
    """
    # Convert annual return percentage to a decimal
    r = annual_return / 100
    # Calculate future value using compound interest formula
    future_value = initial_investment * (1 + r) ** years
    return future_value

def main():
    print("=== Investment Calculator ===\n")
    
    # Get user inputs with validation
    initial_investment = get_positive_float("Enter the initial investment amount: $")
    annual_return = get_positive_float("Enter the average annual return (%): ")
    while True:
        try:
            years = int(input("Enter the number of years for the investment: "))
            if years < 0:
                print("Please enter a non-negative integer for years.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer value for years.")
    
    # Calculate future value
    future_value = calculate_future_value(initial_investment, annual_return, years)
    
    # Display the result formatted to two decimal places
    print(f"\nAfter {years} years, your investment will be worth: ${future_value:,.2f}")

if __name__ == "__main__":
    main()
