# Import the main function from the compiled .so file (bhp)
from .bhp import main  # This assumes main is exposed by the compiled .so file

if __name__ == "__main__":
    main()  # Call the main function
