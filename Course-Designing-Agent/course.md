# Python for Beginners: Write Working Programs from Day One
_Learn to write Python programs that solve real problems, automate tasks, and launch your programming journey with confidence._

**Audience:** Complete programming beginners with no prior coding experience, career changers looking to enter tech fields, students preparing for computer science studies, professionals seeking to automate tasks in their current roles, and hobbyists interested in building personal projects. Assumes basic computer literacy but no technical background.  
**Duration:** ~14.5 hours  
**Prerequisites:** Basic computer skills: creating/saving files, navigating folders, using a text editor, Ability to install software on their computer (Python interpreter and a code editor), Comfort with basic arithmetic and logical thinking, No prior programming experience required

## Learning Outcomes
- Write and execute Python programs using variables, data types, and operators to process information and produce output
- Build programs that make decisions using conditional statements and automate repetitive tasks with for and while loops
- Define reusable functions with parameters and return values to organize code and solve modular problems
- Store and manipulate structured data using lists and dictionaries to model real-world information
- Process text files by reading data, transforming it with string methods, and writing results to disk
- Debug programs systematically by interpreting error messages and applying troubleshooting techniques
- Import and use standard library modules to leverage Python's built-in capabilities without reinventing solutions
- Build a complete multi-feature application that integrates variables, control flow, functions, data structures, and file I/O

## Module 1: Getting Started: Your First Python Program (75m)
_Install Python, run code in the interactive shell, and write your first script that produces visible output._

**Objectives:**
- Install Python and a code editor on your computer
- Execute Python code in the REPL (interactive shell) and run saved script files
- Write programs using print statements, basic arithmetic, and comments
- Identify and fix simple syntax errors by reading error messages

**Lessons:**
1. Installing Python and Setting Up Your Environment (20m)
2. The Python REPL: Your Interactive Playground (25m)
3. Writing and Running Your First Script (30m)

**Activity:** Build a 'Personal Introduction' program that prints your name, hometown, and three favorite hobbies using multiple print statements. Run it from the terminal and modify it to include calculated information (like your age in days by multiplying years by 365).

**Takeaways:**
- The REPL provides instant feedback for trying Python expressions; scripts save code for repeated execution
- Python files end in .py and run from the terminal using 'python filename.py'
- Error messages point to the line and type of problem—they're helpful guides, not failures
- Comments (starting with #) explain code to humans and are ignored by Python

## Module 2: Variables and Data Types: Storing Information (110m)
_Store values in named variables and work with Python's core data types: integers, floats, strings, and booleans._

**Objectives:**
- Create variables with meaningful names and assign values using the = operator
- Distinguish between integers, floats, strings, and booleans and when to use each
- Perform operations appropriate to each data type (arithmetic, concatenation, comparison)
- Convert between data types using int(), float(), str(), and understand when conversion is necessary

**Lessons:**
1. Variables: Naming and Storing Values (30m)
2. Numbers: Integers and Floats (25m)
3. Strings: Working with Text (25m)
4. Booleans, Type Conversion, and Input (30m)

**Activity:** Create a 'Personal Calculator' that prompts the user for two numbers using input(), converts them to floats, performs all arithmetic operations (+, -, *, /, //, %, **), and displays the results with descriptive labels. Test with whole numbers and decimals to see the difference between / and //.

**Takeaways:**
- Variables store references to values; assignment with = creates or updates these references
- Python has four core types: int (whole numbers), float (decimals), str (text), bool (True/False)
- input() always returns a string—use int() or float() to convert before math operations
- = assigns values; == tests equality; don't confuse them in your code

## Module 3: Making Decisions with Conditional Statements (80m)
_Write programs that make decisions and execute different code paths based on conditions using if, elif, and else._

**Objectives:**
- Write if statements that execute code only when a condition is True
- Chain multiple conditions using elif to test alternatives in order
- Provide fallback behavior with else when no conditions match
- Combine conditions using logical operators (and, or, not) to express complex logic

**Lessons:**
1. The if Statement: Conditional Execution (30m)
2. elif and else: Multiple Branches (25m)
3. Logical Operators and Complex Conditions (25m)

**Activity:** Build a 'Grade Calculator' that asks for a numerical score (0-100), then uses if/elif/else to display the letter grade (A: 90-100, B: 80-89, C: 70-79, D: 60-69, F: below 60) with appropriate messages. Add validation that checks if the score is outside 0-100 and displays an error message.

**Takeaways:**
- Indentation is syntax in Python—it defines which code belongs to which block
- if/elif/else chains test conditions in order; the first True condition executes, then the chain exits
- Use == for comparison, = for assignment; mixing them is a common beginner error
- Logical operators (and, or, not) combine simple conditions into complex decision logic

## Module 4: Automating Repetition with Loops (85m)
_Use for and while loops to automate repetitive tasks, iterate over sequences, and process collections of data._

**Objectives:**
- Write for loops that iterate over ranges and sequences to repeat actions
- Use while loops to repeat code until a condition becomes False
- Accumulate results using variables that update inside loops
- Control loop execution with break (exit early) and continue (skip to next iteration)

**Lessons:**
1. for Loops: Iterating Over Sequences (30m)
2. while Loops: Repeating Until a Condition Changes (25m)
3. Loop Patterns: Accumulation and Control (30m)

**Activity:** Create a 'Number Guessing Game' where the program picks a random number (1-100) using import random and random.randint(). Use a while loop to let the user guess repeatedly. After each guess, tell them if they're too high or too low. When they guess correctly, display how many attempts it took and break out of the loop.

**Takeaways:**
- for loops iterate over known sequences; while loops continue until a condition changes
- range(n) produces 0 through n-1, not 1 through n—watch for off-by-one errors
- Accumulator pattern (initialize before loop, update inside) builds up results across iterations
- break exits the loop entirely; continue skips to the next iteration

## Module 5: Organizing Code with Functions (90m)
_Define reusable functions that take inputs, perform operations, and return results to eliminate repetition and organize code._

**Objectives:**
- Define functions using def with parameters and return values
- Call functions by name with arguments and capture returned values
- Explain the difference between defining a function (creating it) and calling it (using it)
- Use functions to eliminate code duplication and break problems into smaller pieces

**Lessons:**
1. Defining and Calling Functions (35m)
2. Parameters, Arguments, and Return Values (30m)
3. Scope and Function Design (25m)

**Activity:** Build a 'Temperature Converter' with three functions: celsius_to_fahrenheit(), fahrenheit_to_celsius(), and a main menu function that asks the user which conversion they want, gets the temperature, calls the appropriate function, and displays the result. Test all functions with known values (0°C = 32°F, 100°C = 212°F).

**Takeaways:**
- def defines a function (the recipe); calling it by name runs the code (follows the recipe)
- return sends values back to caller; print() displays to screen—they serve different purposes
- Parameters are placeholders in the definition; arguments are actual values when calling
- Functions eliminate repetition, make code testable, and break complex problems into manageable pieces

## Module 6: Working with Lists: Ordered Collections (85m)
_Create and manipulate lists to store sequences of items, iterate over them, and transform collections of data._

**Objectives:**
- Create lists with square brackets and access items by index (including negative indices)
- Add items with append() and extend(), remove items with remove() and pop()
- Iterate over lists with for loops and build new lists from existing ones
- Slice lists to extract portions and understand list mutability

**Lessons:**
1. Creating Lists and Accessing Items (30m)
2. Modifying Lists: Adding and Removing Items (25m)
3. Iterating and Slicing Lists (30m)

**Activity:** Create a 'To-Do List Manager' that starts with an empty list. Build a menu that lets users: (1) add a task, (2) view all tasks with numbers, (3) mark a task complete by removing it by index, (4) quit. Use a while loop for the menu and demonstrate append(), list iteration, and pop().

**Takeaways:**
- Lists are mutable ordered sequences accessed by zero-based index; negative indices count from the end
- append() adds to end; remove() deletes by value; pop() removes by index and returns the item
- Slicing [start:stop] extracts portions; stop index is exclusive (not included in result)
- List methods like append() and sort() modify in-place and return None, not a new list

## Module 7: Dictionaries: Storing Key-Value Relationships (80m)
_Use dictionaries to model real-world entities and relationships by storing data as key-value pairs._

**Objectives:**
- Create dictionaries with curly braces and access values by key
- Add, modify, and remove key-value pairs dynamically
- Iterate over keys, values, and key-value pairs with dictionary methods
- Choose between lists and dictionaries based on whether you need order/indexing or named access

**Lessons:**
1. Creating and Accessing Dictionaries (30m)
2. Modifying Dictionaries and Checking Membership (25m)
3. Iterating Over Dictionaries (25m)

**Activity:** Build a 'Contact Book' that stores names as keys and phone numbers as values in a dictionary. Create functions to: add a contact, search for a contact by name (using .get() to handle missing names gracefully), display all contacts, and remove a contact. Use a menu loop to call these functions.

**Takeaways:**
- Dictionaries map keys to values like a real dictionary maps words to definitions
- Access by key with dict[key]; use .get(key, default) to avoid KeyError when key might not exist
- Use .items() with for key, value in dict.items() to iterate over both keys and values
- Choose dictionaries when you need named access to values; choose lists when order and numeric indexing matter

## Module 8: String Manipulation and Text Processing (80m)
_Process and transform text using string methods, slicing, formatting, and common text patterns._

**Objectives:**
- Extract parts of strings using slicing and indexing
- Transform strings with methods like .lower(), .upper(), .strip(), .replace(), and .split()
- Format output using f-strings to embed variables in text
- Process text data line-by-line and word-by-word for analysis

**Lessons:**
1. String Slicing and Indexing (25m)
2. Essential String Methods (30m)
3. String Formatting with f-strings (25m)

**Activity:** Create a 'Text Analyzer' that asks the user for a sentence, then displays: total characters (with and without spaces), word count (using .split()), frequency of a user-specified word (using .lower() and .count()), and the sentence in all caps, all lowercase, and title case. Use f-strings for all output.

**Takeaways:**
- Strings are immutable—methods return new strings rather than modifying the original
- .split() breaks strings into lists of words; .join() combines lists back into strings
- f-strings embed variables and expressions in text: f'Result: {variable}' is clean and readable
- .strip(), .lower(), and .replace() are workhorses for cleaning and normalizing text data

## Module 9: Reading and Writing Files (80m)
_Make programs persist data beyond execution by reading from and writing to text files on disk._

**Objectives:**
- Open files for reading and writing using open() with appropriate modes
- Read entire files, read line-by-line, and write content to files
- Use the with statement to ensure files close properly even if errors occur
- Process file data using loops, string methods, and data structures

**Lessons:**
1. Reading Files (30m)
2. Writing Files (25m)
3. Processing File Data (25m)

**Activity:** Build an 'Expense Tracker' that reads transactions from a text file (one per line: 'Category: Amount'). Parse each line using .split(':'), store expenses in a dictionary where keys are categories and values are lists of amounts. Calculate total spending per category and overall total, then write a summary report to a new file.

**Takeaways:**
- with open(filename, mode) as file ensures files close properly—always use this pattern
- 'r' reads, 'w' writes (erasing existing content), 'a' appends; default is 'r' if mode omitted
- Iterate over file object directly (for line in file) for memory-efficient line-by-line processing
- Combining file I/O with data structures (lists, dictionaries) enables powerful data processing

## Module 10: Error Handling and Debugging (75m)
_Write robust programs that handle errors gracefully and develop systematic debugging skills._

**Objectives:**
- Distinguish between syntax errors (caught before running) and runtime errors (exceptions during execution)
- Use try/except blocks to catch exceptions and prevent crashes
- Read and interpret error messages to identify problem location and type
- Apply systematic debugging techniques including print statements and step-through analysis

**Lessons:**
1. Understanding Errors and Reading Tracebacks (25m)
2. Handling Errors with try/except (30m)
3. Debugging Strategies (20m)

**Activity:** Enhance an existing program (like the number guessing game or calculator) with comprehensive error handling. Use try/except to catch ValueError when converting user input to numbers, handle FileNotFoundError when opening files, and validate that numbers are in expected ranges. Test with intentionally bad input to verify error handling works.

**Takeaways:**
- Tracebacks show error type, message, and line number—read from bottom to top
- try/except catches runtime errors so programs can respond gracefully instead of crashing
- Catch specific exceptions (ValueError, FileNotFoundError) rather than using bare except
- Print debugging is simple but effective—display variable values to see what's actually happening

## Module 11: Modules and the Standard Library (80m)
_Leverage Python's standard library by importing modules and learn to explore available functionality._

**Objectives:**
- Import modules using import and use their functions with dot notation
- Use key standard library modules: random, datetime, math, os
- Read module documentation to discover available functions and their usage
- Understand when to import specific functions with from module import function

**Lessons:**
1. Importing and Using Modules (25m)
2. Essential Standard Library Modules (35m)
3. Exploring Documentation and help() (20m)

**Activity:** Build a 'Password Generator' that uses the random module to create secure passwords. Let users specify length and whether to include uppercase, lowercase, numbers, and symbols. Use random.choice() to select characters from appropriate strings. Add a feature using datetime to timestamp when passwords were generated and save the log to a file.

**Takeaways:**
- import module loads a module; use functions with module.function() syntax
- Python's standard library provides tools for common tasks—don't reinvent the wheel
- help() and dir() let you explore modules interactively; docs.python.org has comprehensive reference
- from module import function imports specific items for use without the module prefix

## Module 12: Capstone Project: Building a Complete Application (135m)
_Integrate everything you've learned to build a multi-feature program that solves a real-world problem._

**Objectives:**
- Design a program structure that uses functions to organize different features
- Combine variables, control flow, loops, data structures, and file I/O in a single application
- Implement error handling to make the program robust against invalid input
- Test the program systematically and debug issues that arise

**Lessons:**
1. Planning Your Application (30m)
2. Building Core Features (45m)
3. Adding Persistence and Polish (35m)
4. Testing, Debugging, and Refinement (25m)

**Activity:** Build a complete 'Personal Library Manager' that stores books (title, author, year, read status) in a list of dictionaries and saves to a JSON file. Features: add book, view all books, search by title or author, mark book as read, delete book, show statistics (total books, books read, average publication year). Use functions for each feature, a while loop for the menu, error handling for file operations and user input, and provide formatted output.

**Takeaways:**
- Complex programs are built incrementally—one working feature at a time, tested before moving on
- Functions organize code by purpose; each function should do one clear thing
- File I/O makes programs practical—data persists and programs become tools, not toys
- Planning before coding (what features? what data structures? what file format?) prevents getting stuck

## Assessment
**Capstone:** Build a 'Personal Finance Tracker' application that helps users manage their budget. The program stores income and expense transactions (date, category, amount, description) in a list of dictionaries and persists data to a JSON file. Core features include: add transaction (with input validation), view all transactions sorted by date, calculate total income vs. expenses and show balance, display spending by category using a dictionary to aggregate amounts, search transactions by category or date range, and generate a summary report saved to a text file. The application must use functions to organize each feature, implement error handling for file operations and invalid input, provide a clear menu-driven interface with a while loop, and demonstrate proficiency with variables, conditionals, loops, functions, lists, dictionaries, string formatting, and file I/O. Students deliver working code and a brief text file explaining their design choices.

**Grading:**
- Functionality: Program runs without crashes and all required features work correctly with valid input (40%)
- Code organization: Effective use of functions to separate concerns; each function has a clear single purpose (20%)
- Data structures: Appropriate use of lists and dictionaries to model and manipulate transaction data (15%)
- Error handling: Try/except blocks prevent crashes from invalid input and file errors; validation provides helpful messages (10%)
- File persistence: Data correctly saves to and loads from file; program state persists between sessions (10%)
- Code quality: Meaningful variable names, appropriate comments, consistent style, and readable formatting (5%)

## Next Steps
- Intermediate Python course covering list comprehensions, decorators, generators, object-oriented programming, and advanced data structures
- Web development with Flask or Django to build web applications with Python
- Data analysis with pandas and NumPy to process and visualize datasets
- Automation scripting: use Python to automate file management, web scraping, and system administration tasks
- Problem-solving practice on HackerRank, LeetCode (Easy problems), or Exercism Python track to solidify fundamentals
- Automate the Boring Stuff with Python by Al Sweigart - free book focused on practical automation projects
- Build personal projects: task manager, weather app using APIs, simple games, or tools for your hobbies/work
- Join Python communities: r/learnpython subreddit, Python Discord servers, local meetups or study groups