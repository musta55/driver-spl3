def divide_by_zero():
    try:
        x = 1 / 0  # Attempting to divide by zero, which raises a ZeroDivisionError
    except ZeroDivisionError as e:
        print(f"An exception occurred: {e}")
        # You can add your custom exception handling code here

if __name__ == "__main__":
    divide_by_zero()
