import inspect
from sys import settrace
import copy
import sys
import re
from py2cfg import CFGBuilder
import pydot
# Stores the current local variables
current_variables = {}

# Uniquely identifies a function
tab = 0

# Used to determine if a loop is being executed or not
inWhileLoop = False
inForLoop = False

# Uniquely identifies a while loop
whileloopID = []

# Uniquely identifies a for loop
forloopID = []

# Stores the indentation of the current line being executed, used to uniquely identify a loop
indentWhile = 0

# Uniquely identifies a slideshow (used to display loops)
slideShowId = 0

# Stores the complete history of the program stack
stack_history = []

# Used to determine whether the explanation of the current line of code should be printed or not
print_details = True

# Stores the name of the file
fileName = ""
def print_executed_code(code):
    lines = code.split('\n')
    for line in lines:
         print('<pre><div class="code-line">%s</div></pre>' % line)

# local trace function which returns itself
def my_tracer(frame, event, arg=None):

    global tab
    global current_variables
    global inWhileLoop
    global whileloopID
    global inForLoop
    global forloopID
    global indentWhile
    global slideShowId
    global indentFor
    global print_details
    global fileName

    # extracts frame code
    code = frame.f_code

    # extracts file name
    fileName = code.co_filename
    # extracts calling function name
    func_name = code.co_name
    # extracts the line number
    line_no = frame.f_lineno
    # print(code)
    tracer_function_code = inspect.getsource(code)
    # Print the entire code executed by the tracer function only once
    if not hasattr(my_tracer, '_code_printed'):
        print('The source code is:\n')
        print_executed_code(tracer_function_code)


        cfg = CFGBuilder().build_from_file("dot", "rod_cutting.py")
        cfg.build_visual('dot', 'pdf')

        # Modify the print statement to include a styled button and an initially hidden PDF
        print('''
        <button onclick="showPDF()" style="margin: 20px; padding: 10px; background-color: #4caf50; color: white; border: none; cursor: pointer;">Static Analysis</button>
        <embed id="pdf" src="dot.pdf" type="application/pdf" style="display: none; margin: 20px; padding: 10px width: 100%; height: 800px;">
        ''')

        # Add JavaScript function to show/hide the PDF
        print('''
        <script>
        function showPDF() {
            var pdf = document.getElementById('pdf');
            if (pdf.style.display === 'none') {
                pdf.style.display = 'block';
            } else {
                pdf.style.display = 'none';
            }
        }
        </script>
        ''')


        setattr(my_tracer, '_code_printed', True)
    # Local trace function is not executed for the following functions
    if func_name == 'encode' or func_name[0] == "<":
        return

    """
    Trace functions should have three arguments: frame, event, and arg:
    Frame is the current stack frame.
    Event is a string: 'call', 'line', 'return', 'exception' or 'opcode'.
    Arg depends on the event type.
    """


    # event call means a function has been called

    if event == 'call':
        # Stores the name of the previous function which called the current function.
        # If no such function exists then it stores empty string
        prev_function = getattr(inspect.stack()[2],"function")

        # Stores the string which describes the function to be executed and is shown on the accordian(HTML element) in the webpage
        call_entry = prev_function + " " + "Call" + "ed (function) " + func_name + " with arguments"

        # This loop adds the argument names and values(passed to the function called) to call_entry
        for j, k in frame.f_locals.items():
            call_entry += "<br>" + "&nbsp;&nbsp;&nbsp;&nbsp;" + str(j) + " &rarr; " + str(k)

        # This generates the accordian on the webpage
        print('''
		<button onclick="myFunction('Demo%s')" class="w3-btn w3-block w3-green w3-left-align" style = "font-size:20px">%s</button>
    	<div id="Demo%s" class="w3-container w3-hide div_func_button">
		''' % (tab, call_entry, tab))

        tab += 1
    
    if event == 'exception':
        # Handle exception event
        exc_type, exc_value, exc_traceback = arg
        print(f'Exception: {exc_type.__name__} - {exc_value}')
    
    if event == 'opcode':
        # Handle opcode event
        opcode = frame.f_code.co_code[frame.f_lasti]
        print(f'Executing opcode: {opcode}')

    # event return means the function has returned
    if event == 'return':

        # Stores the string which describes what the function returned
        call_exit = "function " + func_name + " " + event + "ed " + str(arg)

        # Displays call_exit on the webpage
        print('''
		</div>
		<div class = " w3-green div_return_text" style = "font-size:20px">%s</div>
		''' % (call_exit))

    # event line means the next line of code is about to be executed
    if event == 'line':
        # Extracts current line of code
        curr_code = getattr(inspect.stack()[1],"code_context")[0]

        # Stores the local variables after the current line has been executed
        new_variables = inspect.stack()[1][0].f_locals

        # stack_history is updated to include new_variables
        stack_history.append(copy.deepcopy(new_variables))

        # Regular expressions
        regexWhile = r"(\s*)while.*"
        matchWhile = re.search(regexWhile, curr_code)

        regexFor = r"(\s*)for.*"
        matchFor = re.search(regexFor, curr_code)

        regex_if = r"(\s*)(if )(.*)"
        match_if = re.search(regex_if, curr_code)

        # This for loop shows in the webpage if a variable is introduced or updated
        for var in new_variables:
            # New variable introduced
            if var not in current_variables:
                if print_details:
                    print("<div class = \"div_var_intro\">%s</div>" % (var + " = " + str(new_variables[var]) + " is introduced."),"<br>")
            # Old variable updated


            else:
                # Generates the complete history of how a variable has changed as the program was executed using stack_history
                if new_variables[var] != current_variables[var]:
                    # Stores the history of variable
                    var_history = []
                    for stack in stack_history:
                        if var in stack:
                            if (len(var_history)==0) or (len(var_history)>0 and var_history[-1] != stack[var]):
                                var_history.append(copy.deepcopy(stack[var]))
                    var_history_str =  [str(v) for v in var_history]
                    # Displays the history of a variable in a popup in the webpage
                    tooltip_text = "<div class=\"tooltip\">"+ var +"\n<span class=\"tooltiptext\">" + " &rarr; ".join(var_history_str) + "</span>\n</div>"
                    print("<div class = \"div_var_mod\">%s</div>" % (tooltip_text + " = " + str(current_variables[var]) + " &rarr; " + str(new_variables[var])),"<br>")

        print_details = True
        # Regex to identify simple assignment statements, explanation will not be generated for them
        regex_simple_assignment = r"(\s*)([a-zA-Z][a-zA-Z0-9_]*)(\s*)(=)(\s*)((\d+)|\[\])"
        match_simple_assignment = re.search(regex_simple_assignment,curr_code)

        # If the statement is a simple assignment then print_details is set to false.
        if match_simple_assignment != None:
            print_details = False
            pass

        # Find and store the current indent of the program for the evaluation of loops
        curr_indent = 0
        for c in curr_code:
            if c == " ":
                curr_indent+=1
            else:
                break

        """
        SlideShow for loops:
        Structure:
        <SlideShow> [When a loop is entered]
            <Slide1>   \
            </Slide1>   |
            <Slide2>    |
            </Slide2>   |   For each iteration of the loop
            .           |
            .           |
            .           /
        </SlideShow> [When a loop is exited]
        """

        # Ends the slideshow HTML element if a loop is exited
        if len(whileloopID)>0 and curr_indent < whileloopID[-1][1]+4:
            print("</div class = \"temp\">")
        if len(forloopID)>0 and curr_indent < forloopID[-1][1]+4:
            print("</div class = \"temp\">")

        # Ends a SINGLE slide of the slideshow HTML element if the while loop ends
        if inWhileLoop and curr_indent < whileloopID[-1][1]+4 and whileloopID[-1][:2]!=[line_no,indentWhile]:
            inWhileLoop = False
            print("""<a class="prev" onclick="plusSlides(-1,%s)">&#10094;</a>
            <a class="next" onclick="plusSlides(1,%s)">&#10095;</a>
            </div>""" % (whileloopID[-1][2], whileloopID[-1][2]))
            whileloopID.pop()

        # Ends a SINGLE slide of the slideshow HTML element if the for loop ends
        if inForLoop and curr_indent < forloopID[-1][1]+4 and forloopID[-1][:2]!=[line_no,indentFor]:
            inForLoop = False
            print("""<a class="prev" onclick="plusSlides(-1,%s)">&#10094;</a>
            <a class="next" onclick="plusSlides(1,%s)">&#10095;</a>
            </div>""" % (forloopID[-1][2], forloopID[-1][2]))
            forloopID.pop()

        # Creates a new slide when entering a new iteration of a while loop and
        # Creates a new slideshow when entering a new while loop
        if matchWhile != None:
            inWhileLoop = True
            indentWhile = 0
            for c in curr_code:
                if c == " ":
                    indentWhile+=1
                else:
                    break
            # New SlideShow if needed
            if len(whileloopID)==0 or whileloopID[-1][:2]!=[line_no,indentWhile]:
                whileloopID.append([line_no,indentWhile,slideShowId])
                print("<div id = \"ss%s\" class=\"slideshow-container\">" % (slideShowId))
                slideShowId+=1
            # New slide
            print("<div id=\"ms%s\" class=\"mySlides\">" % (whileloopID[-1][2]))

        # Creates a new slide when entering a new iteration of a for loop and
        # Creates a new slideshow when entering a new for loop
        if matchFor != None:
            inForLoop = True
            indentFor = 0
            for c in curr_code:
                if c == " ":
                    indentFor+=1
                else:
                    break
            # New SlideShow if needed
            if len(forloopID)==0 or forloopID[-1][:2]!=[line_no,indentFor]:
                forloopID.append([line_no,indentFor,slideShowId])
                print("<div id = \"ss%s\" class=\"slideshow-container\">" % (slideShowId))
                slideShowId+=1
            # New slide
            print("<div id=\"ms%s\" class=\"mySlides\">" % (forloopID[-1][2]))

        # Stores whether the current line of code is an if statement
        is_if = False
        # Stores the result of evaluation of the condition in the if statement
        if_result = ""

        # Finds whether the condtion in the if statement is true or false
        if match_if != None:
            # Evaluates and stores a copy of condition of if statement with the variable names replaced with the corresponding value
            mod_code = copy.deepcopy(match_if.group(3))
            mod_code = mod_code[:-1]
            sorted_list_of_variables = sorted([var for var in new_variables], key = len, reverse = True)
            for var in sorted_list_of_variables:
                mod_code = mod_code.replace(var, str(new_variables[var]))
            is_if = True
            # Evaluation of the condition
            try:
                if_result = str(eval(mod_code))
            except:
                is_if = False

        # Stores the current line of code in form of html code with the popups added
        curr_code_html = curr_code

        # Regex to identify a function
        regex_function = r"(\s+)([a-zA-Z][a-zA-Z0-9_]*)\(.*\)"
        match_function = re.search(regex_function, curr_code)

        # Regex to identify Object1.Object2.---.ObjectN.function(), type of functions
        regex_object_function = r"([a-zA-Z][a-zA-Z0-9_]*)(\.[a-zA-Z][a-zA-Z0-9_]*)+\(.*\)"
        match_object_function = re.search(regex_object_function, curr_code)

        # Generates a tooltip which displays some information about the object or the function
        function_name = ""
        if match_object_function != None:
            curr_code_html = curr_code[:match_object_function.start()]
            matched_var = match_object_function.group(1)
            # If the object is defined by the user then it is replaced by its value
            if matched_var in current_variables:
                function_name = str(current_variables[matched_var])
            # This loop generated the tooltip for each object and function. Ex: object1.object2.function()
            for k in range(len(match_object_function.groups())):
                if matched_var not in current_variables or k != 0:
                    function_name += curr_code[match_object_function.start(k+1):match_object_function.end(k+1)]
                tooltip_text = eval(str(function_name) + ".__doc__")
                curr_code_html += "<div class=\"tooltip\">"+ curr_code[match_object_function.start(k+1):match_object_function.end(k+1)] +"\n<span class=\"tooltiptext\">" + tooltip_text + "</span>\n</div>"
            curr_code_html += curr_code[match_object_function.end(len(match_object_function.groups())):]
            pass

        # Generates a tooltip which displays some information about the function
        elif match_function != None:
            curr_code_html = curr_code[:match_function.start(2)]
            function_name += curr_code[match_function.start(2):match_function.end(2)]
            tooltip_text = eval(str(function_name) + ".__doc__")
            if tooltip_text is not None:
                curr_code_html += "<div class=\"tooltip\">"+ curr_code[match_function.start(2):match_function.end(2)] +"\n<span class=\"tooltiptext\">" + tooltip_text + "</span>\n</div>"
            else:
                pass

            # curr_code_html += "<div class=\"tooltip\">"+ curr_code[match_function.start(2):match_function.end(2)] +"\n<span class=\"tooltiptext\">" + tooltip_text + "</span>\n</div>"
            curr_code_html += curr_code[match_function.end(2):]
            pass

        # Prints the line number and code in the webpage
        print("<div class = \"div_line_num\">%s</div>" % (str(line_no-550)), "<div class = \"div_code_text\">%s</div>" % (curr_code_html),"<br>")

        # If the line of code is and if statement then the result of the evaluation of the condition is printed after it.
        if is_if:
            print("<div class = \"div_var_intro\">%s</div><br>" % (if_result))

        # Current variables are replaced by the new variables
        current_variables = copy.deepcopy(new_variables)

    return my_tracer


def htmlInit():
    f = open("pytracex.html", 'w')

    # std output is set to the webpage so the output of the program can be displayed
    sys.stdout = f

    # Initializes the webpage along with the CSS
    # NOTE: rod_cutting.py is replaced with the name of the file by my-second-page.js
    print('''
		<!DOCTYPE html>
		<html>
    <head>
    		<title>PyTraceX</title>
    		<meta name="viewport" content="width=device-width, initial-scale=1">
    		<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <script src="prism/w3code.js"></script>
    </head>
        <style>
        .code-line {
        margin-left: 57px;
        color:#007BA7;
        font-family: monospace;
        font-size: 14px;
        margin: 2px 0;
        }
        body {
            margin-left: 50px;
            background: rgb(245, 255, 245);
        }
        .div_var_intro {
            display:inline-block;
            margin-left: 57px;
            line-height: 2;
        }
        .div_line_num {
            display:inline-block;
            width:50px;
            color:teal;
            line-height: 3;
        }
        .div_code_text {
            display:inline-block;
            color:#007BA7;
            font-size:18px;
            font-style:monolisa;
            line-height: 1.5;
        }
        .div_var_mod {
            display:inline-block;
            margin-left: 57px;
            line-height: 2;
        }
        .div_func_button {
            margin-left:10px;
            border-left-style:solid;
            border-left-width:10px;
            border-left-color: rgba(0, 128, 0, 0.3);
        }
        .div_return_text {
            border-top-style: solid;
            border-width: 2px;
            border-color: rgb(245, 255, 245);
            margin-bottom: 10px;
            padding: 5px;
        }
        .slideshow-container {
            position: relative;
            background: rgba(0, 128, 0, 0.1);;
            }

            /* Slides */
            .mySlides {
            display: none;
            margin:5px;
            padding: 30px;
            padding-top: 10px;
            padding-bottom: 10px;
            }

            /* Next & previous buttons */
            .prev, .next {
            cursor: pointer;
            position: absolute;
            top: 50%;
            width: auto;
            margin-top: -20px;
            padding: 5px;
            color: rgba(0, 128, 0, 0.8);
            font-weight: bold;
            font-size: 20px;
            border-radius: 0 3px 3px 0;
            user-select: none;
            }

            /* Position the "next button" to the right */
            .next {
            position: absolute;
            right: 0;
            border-radius: 3px 0 0 3px;
            }

            /* On hover, add a black background color with a little bit see-through */
            .prev:hover, .next:hover {
            color: white;
            }

            /* The dot/bullet/indicator container */
            .dot-container {
            text-align: center;
            padding: 20px;
            background: #ddd;
            }

            /* The dots/bullets/indicators */
            .dot {
            cursor: pointer;
            height: 15px;
            width: 15px;
            margin: 0 2px;
            background-color: #bbb;
            border-radius: 50%;
            display: inline-block;
            transition: background-color 0.6s ease;
            }

            /* Add a background color to the active dot/circle */
            .active, .dot:hover {
            background-color: #717171;
            }

            /* Add an italic font style to all quotes */
            q {font-style: italic;}

            /* Add a blue color to the author */
            .author {color: cornflowerblue;}
            .tooltip {
            color: blue;
            position: relative;
            display: inline-block;
            border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
          }

          /* Tooltip text */
          .tooltip .tooltiptext {
          bottom: 100%;
          left: 50%;
          margin-left: -125px;
          visibility: hidden;
          width: 250px;
          background-color: black;
          color: #fff;
          text-align: center;
          padding: 5px 0;
          border-radius: 6px;

            /* Position the tooltip text - see examples below! */
            position: absolute;
            z-index: 1;
          }

          /* Show the tooltip text when you mouse over the tooltip container */
          .tooltip:hover .tooltiptext {
            visibility: visible;
          }
          .tooltip .tooltiptext::after {
          content: " ";
          position: absolute;
          top: 100%; /* At the bottom of the tooltip */
          left: 50%;
          margin-left: -5px;
          border-width: 5px;
          border-style: solid;
          border-color: black transparent transparent transparent;
        }
        </style>
		<body>
		<div class="w3-container">
        <h2 style="text-align: center; color: rgba(0, 128, 0, 0.8); font-weight: bold; font-size: 48px; font-style: italic;">PyCompreX</h2>

		<h2>Filename : rod_cutting.py</h2>
    <hr>
		<p>Open and collapse the accordian to see the summary</p>
	''')


htmlInit()

# Tracer function is set to the function my_tracer
settrace(my_tracer)

# <__b_s__> is replaced with the code selected by the user by my-second-page.js
"""
This module provides two implementations for the rod-cutting problem:
1. A naive recursive implementation which has an exponential runtime
2. Two dynamic programming implementations which have quadratic runtime
The rod-cutting problem is the problem of finding the maximum possible revenue
obtainable from a rod of length ``n`` given a list of prices for each integral piece
of the rod. The maximum revenue can thus be obtained by cutting the rod and selling the
pieces separately or not cutting it at all if the price of it is the maximum obtainable.
"""


def naive_cut_rod_recursive(n: int, prices: list):
    """
    Solves the rod-cutting problem via naively without using the benefit of dynamic
    programming. The results is the same sub-problems are solved several times
    leading to an exponential runtime
    Runtime: O(2^n)
    Arguments
    -------
    n: int, the length of the rod
    prices: list, the prices for each piece of rod. ``p[i-i]`` is the
    price for a rod of length ``i``
    Returns
    -------
    The maximum revenue obtainable for a rod of length n given the list of prices
    for each piece.
    Examples
    --------
    >>> naive_cut_rod_recursive(4, [1, 5, 8, 9])
    10
    >>> naive_cut_rod_recursive(10, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30])
    30
    """

    _enforce_args(n, prices)
    if n == 0:
        return 0
    max_revue = float("-inf")
    for i in range(1, n + 1):
        max_revue = max(
            max_revue, prices[i - 1] + naive_cut_rod_recursive(n - i, prices)
        )

    return max_revue


def top_down_cut_rod(n: int, prices: list):
    """
    Constructs a top-down dynamic programming solution for the rod-cutting
    problem via memoization. This function serves as a wrapper for
    _top_down_cut_rod_recursive
    Runtime: O(n^2)
    Arguments
    --------
    n: int, the length of the rod
    prices: list, the prices for each piece of rod. ``p[i-i]`` is the
    price for a rod of length ``i``
    Note
    ----
    For convenience and because Python's lists using 0-indexing, length(max_rev) =
    n + 1, to accommodate for the revenue obtainable from a rod of length 0.
    Returns
    -------
    The maximum revenue obtainable for a rod of length n given the list of prices
    for each piece.
    Examples
    -------
    >>> top_down_cut_rod(4, [1, 5, 8, 9])
    10
    >>> top_down_cut_rod(10, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30])
    30
    """
    _enforce_args(n, prices)
    max_rev = [float("-inf") for _ in range(n + 1)]
    return _top_down_cut_rod_recursive(n, prices, max_rev)


def _top_down_cut_rod_recursive(n: int, prices: list, max_rev: list):
    """
    Constructs a top-down dynamic programming solution for the rod-cutting problem
    via memoization.
    Runtime: O(n^2)
    Arguments
    --------
    n: int, the length of the rod
    prices: list, the prices for each piece of rod. ``p[i-i]`` is the
    price for a rod of length ``i``
    max_rev: list, the computed maximum revenue for a piece of rod.
    ``max_rev[i]`` is the maximum revenue obtainable for a rod of length ``i``
    Returns
    -------
    The maximum revenue obtainable for a rod of length n given the list of prices
    for each piece.
    """
    if max_rev[n] >= 0:
        return max_rev[n]
    elif n == 0:
        return 0
    else:
        max_revenue = float("-inf")
        for i in range(1, n + 1):
            max_revenue = max(
                max_revenue,
                prices[i - 1] + _top_down_cut_rod_recursive(n - i, prices, max_rev),
            )

        max_rev[n] = max_revenue

    return max_rev[n]


def bottom_up_cut_rod(n: int, prices: list):
    """
    Constructs a bottom-up dynamic programming solution for the rod-cutting problem
    Runtime: O(n^2)
    Arguments
    ----------
    n: int, the maximum length of the rod.
    prices: list, the prices for each piece of rod. ``p[i-i]`` is the
    price for a rod of length ``i``
    Returns
    -------
    The maximum revenue obtainable from cutting a rod of length n given
    the prices for each piece of rod p.
    Examples
    -------
    >>> bottom_up_cut_rod(4, [1, 5, 8, 9])
    10
    >>> bottom_up_cut_rod(10, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30])
    30
    """
    _enforce_args(n, prices)

    # length(max_rev) = n + 1, to accommodate for the revenue obtainable from a rod of
    # length 0.
    max_rev = [float("-inf") for _ in range(n + 1)]
    max_rev[0] = 0

    for i in range(1, n + 1):
        max_revenue_i = max_rev[i]
        for j in range(1, i + 1):
            max_revenue_i = max(max_revenue_i, prices[j - 1] + max_rev[i - j])

        max_rev[i] = max_revenue_i

    return max_rev[n]


def _enforce_args(n: int, prices: list):
    """
    Basic checks on the arguments to the rod-cutting algorithms
    n: int, the length of the rod
    prices: list, the price list for each piece of rod.
    Throws ValueError:
    if n is negative or there are fewer items in the price list than the length of
    the rod
    """
    if n < 0:
        raise ValueError(f"n must be greater than or equal to 0. Got n = {n}")

    if n > len(prices):
        raise ValueError(
            f"Each integral piece of rod must have a corresponding "
            f"price. Got n = {n} but length of prices = {len(prices)}"
        )


def main():
    prices = [6, 10, 12, 15, 20, 23]
    n = len(prices)

    # the best revenue comes from cutting the rod into 6 pieces, each
    # of length 1 resulting in a revenue of 6 * 6 = 36.
    expected_max_revenue = 36

    max_rev_top_down = top_down_cut_rod(n, prices)
    max_rev_bottom_up = bottom_up_cut_rod(n, prices)
    max_rev_naive = naive_cut_rod_recursive(n, prices)

    assert expected_max_revenue == max_rev_top_down
    assert max_rev_top_down == max_rev_bottom_up
    assert max_rev_bottom_up == max_rev_naive


if __name__ == "__main__":
    main()

# source: https://github.com/TheAlgorithms/Python


# Tracer function is set to None
settrace(None)

# It contains the script for the accordian and the slideshows
print('''<script>
var ss_count = %s;
function myFunction(id) {
  var x = document.getElementById(id);
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
  } else {
    x.className = x.className.replace(" w3-show", "");
  }
}
var slideIndex = new Array(ss_count).fill(1);
var ind = 1;
for(ind = 0; ind < ss_count; ind++){
    showSlides(slideIndex[ind],ind);
}


function plusSlides(n,i) {
  showSlides(slideIndex[i] += n,i);
}

function currentSlide(n,i) {
  showSlides(slideIndex[i] = n,i);
}

function showSlides(n,i) {
  var k;
  var slides = document.getElementById("ss"+i).querySelectorAll('#ms'+i);
  console.log(slides)
  if (n > slides.length) {slideIndex[i] = 1}
    if (n < 1) {slideIndex[i] = slides.length}
    for (k = 0; k < slides.length; k++) {
      slides[k].style.display = "none";
    }
  slides[slideIndex[i]-1].style.display = "block";
}
</script>
</body>
</html>''' % (slideShowId))
