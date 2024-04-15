# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19UbJtDzLYpLIFZh3X9y7DumxOYy9J3uw
"""

import ast
import hashlib
# import graphviz
import math
# from IPython.display import Image


test = ""
def syntactical_analysis(code):
    global test

    res=''
    try:
        # Parse the code into an abstract syntax tree (AST)
        tree = ast.parse(code)

        # Walk through the AST and check for syntax errors
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for function definitions
                if not node.name.isidentifier():
                    res += f"Error: Invalid function name '{node.name}'<br/>"
            elif isinstance(node, ast.Assign):
                # Check for assignments
                for target in node.targets:
                    if not isinstance(target, ast.Name) or not target.id.isidentifier():
                        res+="Error: Invalid assignment target<br/>"
            elif isinstance(node, ast.Expr):
                # Check for expressions
                if not isinstance(node.value, ast.Call) or not isinstance(node.value.func, ast.Name):
                    res+="Error: Invalid expression<br/>"
            # Add more checks for other types of nodes as needed

        res+=f"Syntactical analysis completed. No syntax errors found.<br/>"
        return res

    except SyntaxError as e:
        # If there's a syntax error in the code, print the error message
        return (f"SyntaxError: {e} <br/>")

def check_pep8(code):
    global test

    tree = ast.parse(code)
    violations = []

    # Check maximum line length
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            lines = node.value.s.split('<br/>')
            for i, line in enumerate(lines):
                if len(line) > 79:
                    violations.append(f"Line {node.lineno + i}: Exceeds maximum line length (PEP 8 guideline 2)")

    # Check indentation
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if node.body:
                first_statement = node.body[0]
                if hasattr(first_statement, 'col_offset') and first_statement.col_offset != 4:
                    violations.append(f"Line {first_statement.lineno}: Incorrect indentation (PEP 8 guideline 1)")

    # Check line breaks before or after binary operators
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp):
            if hasattr(node, 'left') and hasattr(node, 'right'):
                if node.left.lineno != node.right.lineno:
                    violations.append(f"Line {node.lineno}: Inconsistent line breaks around binary operator (PEP 8 guideline)")

    # Check blank lines
    last_blank_line = None
    for i, line in enumerate(code.split('<br/>')):
        if line.strip() == '':
            if last_blank_line is not None and i - last_blank_line == 1:
                violations.append(f"Line {i}: Unnecessary blank line (PEP 8 guideline)")
            last_blank_line = i

    # Check source file encoding
    if "encoding" in code.lower() or "utf-8" not in code.lower():
        violations.append("Source file does not use UTF-8 encoding or has an explicit encoding declaration (PEP 8 guideline)")

    # Check imports
    found_import = False
    found_from_import = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found_import = True
        if isinstance(node, ast.ImportFrom):
            found_from_import = True

    if found_import and found_from_import:
        violations.append("Imports should be either all import statements or all from import statements, not a mix (PEP 8 guideline)")

    # Check for whitespace in expressions and statements
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
                if not (node.left.lineno == node.right.lineno and node.lineno == node.left.lineno):
                    violations.append(f"Line {node.lineno}: Whitespace issue in expression/statement (PEP 8 guideline)")

        if isinstance(node, (ast.Assign, ast.AugAssign)):
            if len(node.targets) > 1:
                violations.append(f"Line {node.lineno}: More than one assignment target (PEP 8 guideline)")

    # Check for trailing commas
    for node in ast.walk(tree):
        if isinstance(node, ast.List) or isinstance(node, ast.Tuple):
            if node.elts:
                last_element = node.elts[-1]
                if isinstance(last_element, ast.Tuple):
                    if last_element.elts:
                        last_tuple_element = last_element.elts[-1]
                        if isinstance(last_tuple_element, ast.Str):
                            if last_tuple_element.s.endswith(","):
                                violations.append(f"Line {last_tuple_element.lineno}: Trailing comma found (PEP 8 guideline)")
                elif isinstance(last_element, ast.Str):
                    if last_element.s.endswith(","):
                        violations.append(f"Line {last_element.lineno}: Trailing comma found (PEP 8 guideline)")

    # Check for block comments
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            comment_lines = node.value.s.split('<br/>')
            if len(comment_lines) > 1:
                if comment_lines[0].strip().startswith('#'):
                    for line in comment_lines[1:]:
                        if not line.strip().startswith('#'):
                            violations.append(f"Line {node.lineno}: Malformed block comment (PEP 8 guideline)")
                            break

    # Check for inline comments
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if node.lineno == node.value.lineno and node.col_offset == node.value.col_offset:
                for comment in ast.walk(node):
                    if isinstance(comment, ast.Expr) and isinstance(comment.value, ast.Str):
                        if comment.lineno == node.lineno:
                            if not comment.value.s.strip().startswith('# '):
                                violations.append(f"Line {comment.lineno}: Inline comment should start with '# ' (PEP 8 guideline)")



    # Check function annotations
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.returns is not None:
                if not isinstance(node.returns, ast.Name):
                    violations.append(f"Line {node.returns.lineno}: Function return annotation not using PEP 484 syntax")
            for arg in node.args.args:
                if arg.annotation is not None:
                    if not isinstance(arg.annotation, ast.Name):
                        violations.append(f"Line {arg.annotation.lineno}: Function argument annotation not using PEP 484 syntax")

    # Check variable annotations
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            if hasattr(node, 'annotation') and node.annotation is not None:
                if not isinstance(node.annotation, ast.Name):
                    violations.append(f"Line {node.lineno}: Variable annotation not using PEP 526 syntax")

    return violations



# Example Python code to analyze
example_code = """
def add_numbers(a, b):
   return a + b

result = add_numbers(5, 10)
print(result)
"""

def validation_1(code):
  global test
  violations = check_pep8(code)
  if not violations:
      test+=f"The code follows PEP 8 conventions.<br/>"
  else:
      test+=f"<b>PEP 8 violations found:</b>"
      for violation in violations:
          test+=f"{violation} <br/>"

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.errors = []
        self.space_complexity = 1
        self.time_complexity = 1

    def visit_FunctionDef(self, node):
        # Reset space and time complexity for each function
        self.space_complexity += len(node.targets) 
        self.time_complexity = 0

        self.generic_visit(node)

    def visit_For(self, node):
        # Increment space complexity for loop variables
        self.space_complexity += 1

        # Increment time complexity for loop iterations
        self.time_complexity += 1

        self.generic_visit(node)

    def visit_While(self, node):
        # Increment space complexity for loop variables
        self.space_complexity += 1

        # Increment time complexity for loop iterations
        self.time_complexity += 1

        self.generic_visit(node)

    def visit_Call(self, node):
        # Increment time complexity for function calls
        self.time_complexity += 1

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Increment time complexity for function definition
        self.time_complexity += 1

        self.generic_visit(node)

    def analyze_code(self, code):
        res=""

        try:
            # Parse the code into an abstract syntax tree (AST)
            tree = ast.parse(code)

            # Analyze the AST for space and time complexity
            self.visit(tree)

            # Provide feedback on space and time complexity
            res+=f"Space Complexity: {self.space_complexity}<br/>"
            res+=f"Time Complexity: {self.time_complexity}<br/>"

            if self.space_complexity > 5:
                res+="High space complexity detected. Consider optimizing your code for memory usage.<br/>"
            else:
                res+="Space complexity is within acceptable limits.<br/>"
            if self.time_complexity > 5:
                res+="High time complexity detected. Consider optimizing your code for performance.<br/>"
            else:
                res+="Time complexity is within acceptable limits.<br/>"

        except SyntaxError as e:
            # If there's a syntax error in the code, add it to the list of errors
            self.errors.append(f"SyntaxError: {e} <br/>")

        return res

def validation_2(code):
  # Create an instance of CodeAnalyzer and analyze the code
  global test
  analyzer = CodeAnalyzer()
  test+=analyzer.analyze_code(code)

# Print any syntactical errors detected
  if analyzer.errors:
      test+=f"Syntactical errors detected:<br/>"
      for error in analyzer.errors:
          test+=f"{error}<br/>"
  else:
      test+=f"No syntactical errors detected.<br/>"

def calculate_maintainability_index(halstead_volume, cyclomatic_complexity, lines_of_code):
    """
    Calculate Maintainability Index (MI) based on Halstead Volume, Cyclomatic Complexity, and Lines of Code.
    """
    mi = 171 - 5.2 * math.log(halstead_volume) - 0.23 * cyclomatic_complexity - 16.2 * math.log(lines_of_code)
    return mi

def provide_maintainability_feedback(halstead_volume, cyclomatic_complexity, lines_of_code):
    mi = calculate_maintainability_index(halstead_volume, cyclomatic_complexity, lines_of_code)

    if mi >= 100:
        return "High maintainability: The code is well-structured and easy to maintain.<br/>"
    elif 80 <= mi < 100:
        return "Medium maintainability:  Some improvements can be made to enhance maintainability.<br/>"
    else:
        return " Low maintainability: The code may be difficult to maintain. Consider refactoring.<br/>"

def caclm1():
  global test
  halstead_volume = 1000
  cyclomatic_complexity = 20
  lines_of_code = 200
  test += provide_maintainability_feedback(halstead_volume, cyclomatic_complexity, lines_of_code)

def count_lines(code):
    return len(code.split('\n'))

def count_loops(node):
    loops = 0
    for child in ast.walk(node):
        if isinstance(child, (ast.For, ast.While)):
            loops += 1
    return loops

def count_modules(node):
    modules = 0
    for child in ast.walk(node):
        if isinstance(child, ast.FunctionDef):
            modules += 1
    return modules

def analyze_code(code):
    res=""
    try:
        parsed_code = ast.parse(code)
        lines = count_lines(code)
        loops = count_loops(parsed_code)
        modules = count_modules(parsed_code)

        res+=f"Number of lines: {lines}<br/>"
        res+=f"Number of loops: {loops}<br/>"
        res+=f"Number of modules: {modules}<br/>"

        # Suggestions based on analysis results
        if lines > 100:
            res+="Suggestion: Consider breaking down your code into smaller functions or modules for better readability and maintainability.<br/>"
        if loops > 5:
            res+="Suggestion: Having a large number of loops may indicate a need for optimization. Consider optimizing loop operations or refactoring code.<br/>"


    except SyntaxError as e:
        res+=f"Syntax Error: {e}<br/>"
    return res

# Example usage:
input_code = """
def example_function():
    for i in range(5):
        res+=fi)

def another_function():
    while True:
        res+=f"Infinite loop")
"""

def calculate_halstead_volume(tree):
    # Initialize counts for operators and operands
    operator_count = 0
    operand_count = 0
    unique_operators = set()
    unique_operands = set()

    # Traverse the AST to count operators and operands
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp):
            # Handle binary operators
            operator_count += 1
            unique_operators.add(type(node.op).__name__)
        elif isinstance(node, ast.UnaryOp):
            # Handle unary operators
            operator_count += 1
            unique_operators.add(type(node.op).__name__)
        elif isinstance(node, ast.Name):
            # Handle variable names as operands
            operand_count += 1
            unique_operands.add(node.id)
        elif isinstance(node, ast.Constant):
            # Handle constant values as operands
            operand_count += 1
            unique_operands.add(node.value)

    # Calculate Halstead Length and Vocabulary
    halstead_length = operator_count + operand_count
    halstead_vocabulary = len(unique_operators) + len(unique_operands)

    # Calculate Halstead Volume
    halstead_volume = halstead_length * math.log(halstead_vocabulary, 2)

    return halstead_volume



class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1  # Start with 1 for the base path

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Assert(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_comprehension(self, node):
        self.complexity += 1
        self.generic_visit(node)

def calculate_cyclomatic_complexity(code):
    tree = ast.parse(code)
    visitor = ComplexityVisitor()
    visitor.visit(tree)
    return visitor.complexity

def calculate_maintainability_index_1(code):
    """
    Calculate Maintainability Index (MI) based on the given code.
    """
    # Parse the code into an abstract syntax tree (AST)
    tree = ast.parse(code)

    # Calculate Halstead Volume, Cyclomatic Complexity, and Lines of Code from the AST
    halstead_volume = calculate_halstead_volume(tree)
    cyclomatic_complexity = calculate_cyclomatic_complexity(tree)
    lines_of_code = code.count('<br/>') + 1

    # Calculate Maintainability Index (MI) using the obtained metrics
    mi = 171 - 5.2 * math.log(halstead_volume) - 0.23 * cyclomatic_complexity - 16.2 * math.log(lines_of_code)

    return mi


def provide_maintainability_feedback_1(code):
    mi = calculate_maintainability_index_1(code)

    if mi >= 100:
        return "High maintainability: The code is well-structured and easy to maintain.<br/>"
    elif 80 <= mi < 100:
        return "Medium maintainability: Some improvements can be made to enhance maintainability.<br/>" \
               #+ "Consider the following suggestions:<br/>" \
               #+ "1. Break down complex functions into smaller, more modular functions.<br/>" \
               #+ "2. Improve code documentation and add meaningful comments to clarify the logic.<br/>" \
               #+ "3. Refactor repetitive code into reusable functions or classes.<br/>" \
               #+ "4. Simplify control flow and reduce nested conditionals or loops.<br/>" \
               #+ "5. Use descriptive variable and function names to improve code readability.<br/>"
    else:
        return "Low maintainability: The code may be difficult to maintain. Consider refactoring.<br/>" \
               #+ "Here are some suggestions to improve maintainability:<br/>" \
               #+ "1. Break down monolithic functions into smaller, more focused units.<br/>" \
               #+ "2. Identify and remove dead code or unused variables to reduce complexity.<br/>" \
               #+ "3. Reduce code duplication by extracting common functionality into separate functions or modules.<br/>" \
               #+ "4. Eliminate global variables and minimize mutable state to improve code predictability.<br/>" \
               #+ "5. Use consistent coding conventions and adhere to best practices to make the codebase more cohesive.<br/>"


def calculate_overall_score(code):
    # Perform syntax analysis
    try:
        ast.parse(code)
        syntax_score = 1  # Full points for no syntax errors
    except SyntaxError:
        syntax_score = 0  # No points for syntax errors

    # Perform semantic analysis (for simplicity, not implemented here)
    semantic_score = 1  # Assuming semantic analysis always passes

    # Calculate Halstead volume
    halstead_volume = calculate_halstead_volume(ast.parse(code))

    # Calculate cyclomatic complexity
    cyclomatic_complexity = calculate_cyclomatic_complexity(ast.parse(code))

    # Calculate maintainability index
    maintainability_index = calculate_maintainability_index_1(code)





    # Combine scores with weights (adjust weights as needed)
    overall_score = (syntax_score * 0.2 +
                     semantic_score * 0.2 +
                     halstead_volume * 0.2 +
                     cyclomatic_complexity * 0.2 +
                     maintainability_index * 0.4)

    return overall_score


def categorize_code(score):
    if score > 90:
        return "High standard code<br/>"
    elif 60 <= score <= 90:
        return "Medium standard code<br/>"
    elif 40 <= score < 60:
        return "Low standard code<br/>"
    else:
        return "Very low standard code<br/>"


# Example usage:
example_code = """
def fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        next_term = fib_sequence[-1] + fib_sequence[-2]
        fib_sequence.append(next_term)
    return fib_sequence

result = fibonacci(10)
print(result)
"""

def extract_functions(code):
    """
    Extract function definitions from the given code.
    """
    tree = ast.parse(code)
    return [node for node in tree.body if isinstance(node, ast.FunctionDef)]

def hash_function(node):
    """
    Hash a function node for comparison.
    """
    return hashlib.md5(ast.dump(node).encode()).hexdigest()

def hash_statement(node):
    """
    Hash an individual statement node for comparison.
    """
    hash_object = hashlib.md5()
    hash_object.update(ast.dump(node).encode())
    return hash_object.hexdigest()

def find_duplicate_functions(functions):
    """
    Find duplicate function definitions using hashing.
    """
    function_hash_map = {}
    duplicate_functions = []

    for function in functions:
        function_hash = hash_function(function)
        if function_hash in function_hash_map:
            if function.name not in duplicate_functions:
                duplicate_functions.append(function.name)
        else:
            function_hash_map[function_hash] = function.name  # Store both hash and function name

    return duplicate_functions

def find_repeated_statements(functions):
    """
    Find repeated statements within functions.
    """
    repeated_statements = []

    for function in functions:
        code_lines = set()
        for node in function.body:
            if isinstance(node, ast.stmt):
                statement_hash = hash_statement(node)
                if statement_hash in code_lines:
                    repeated_statements.append((function.name, node.lineno))
                else:
                    code_lines.add(statement_hash)

    return repeated_statements

def detect_code_duplication(code):
    """
    Detect code duplication in the given code.
    """
    res=""
    functions = extract_functions(code)
    duplicate_functions = find_duplicate_functions(functions)
    repeated_statements = find_repeated_statements(functions)

    if duplicate_functions:
        res+= "Function Duplication Detected:<br/>"
        for function_name in duplicate_functions:
            res+= "Duplicate Function: {function_name}<br/>"
            res+= "Suggestion: Refactor the duplicate code into a reusable function or module.<br/>"
    else:
        res+= "No Function Duplication Detected.<br/>"

    if repeated_statements:
        res+= "<br/>Repeated Statements Detected:<br/>"
        for function_name, line_number in repeated_statements:
            res+= f"In function '{function_name}', line {line_number}:<br/>"
            res+= "Repeated Statement Found<br/>"
            res+= "Suggestion: Extract the repeated code into a separate function or optimize for better readability.<br/>"
    else:
        res+= "No Repeated Statements Detected.<br/>"
    return res

def analyze_error_handling(code):
    res=""
    try:
        # Attempt to parse the code into an abstract syntax tree (AST)
        tree = ast.parse(code)

        # Analyze error handling
        if lacks_error_handling(tree):
            res+="Error Handling Issues Detected:<br/>"
            res+="Suggestion: Implement proper error handling mechanisms.<br/>"
        else:
            res+="Error Handling is Adequate.<br/>"

    except SyntaxError as e:
        res+= f"Syntax Error: {e}<br/>"
        res+= "Unable to analyze error handling due to syntax errors in the code.<br/>"
    return res

def lacks_error_handling(tree):
    # Flag to indicate if error handling is missing
    missing_error_handling = False

    # Walk through the AST to find error-prone constructs
    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            # If 'try' block exists but 'except' block is missing
            if not node.handlers:
                missing_error_handling = True
                break
        elif isinstance(node, ast.Raise):
            # If 'raise' statement is used without handling the exception
            missing_error_handling = True
            break

    return missing_error_handling


# Example usage:
example_code = """
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        res+="Error: Division by zero")
    return result

# Call the function
divide(10, 0)
"""

def analyze_code_organization(code):
    res=""
    try:
        parsed_code = ast.parse(code)
        module_names = extract_module_names(parsed_code)
        if len(module_names) > 1:
            res+="Code Organization Issues Detected:<br/>"
            res+="Multiple modules found in the code.<br/>"
            res+="Suggestion: Consider organizing the code into separate files or consolidating related functionality into fewer modules.<br/>"
        else:
            res+="Code Organization is Good.<br/>"
    except SyntaxError as e:
        res+=f"Syntax Error: {e}<br/>"
    return res

def extract_module_names(parsed_code):
    module_names = set()
    for node in ast.walk(parsed_code):
        if isinstance(node, ast.FunctionDef):
            module_names.add(node.name)
    return module_names

# Example usage:
example_code = """
def add(a, b):
    return a + b
    return a - b
"""
#import sample.txt file and init with code

def result(code):
#   code =""
#   with open('sample.txt', 'r') as file:
#       code = file.read()
  global test
  # Call the function   
  syntactical_analysis(code)
  check_pep8(code)
  validation_1(code)
  #validation_2(code)
  caclm1()
  test+=analyze_code(code)
  test+=f"Cyclomatic Complexity: {calculate_cyclomatic_complexity(code)}<br/>"
  overall_score = calculate_overall_score(code)
  test+=f"<b>Overall score: {overall_score}</b><br/>"
  test+=f"Code Level: {categorize_code(overall_score)}"
  feedback = provide_maintainability_feedback_1(code)
  test+=f"Maintainability feedback:{feedback}"
  test+=detect_code_duplication(code)
  test+=analyze_error_handling(code)
  test+=analyze_code_organization(code)
  temp = test
  test = ""
  return temp

