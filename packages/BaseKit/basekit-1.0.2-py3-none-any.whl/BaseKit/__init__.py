f"""
Numeral System Conversion and Expression Evaluation Module
 Version: 1.0\n
 Author: Fedor Tyulpin\n
 \n
 Key Features:\n
 1. Cross-Base Calculations\n
 - Evaluate expressions with numbers in different bases (2-36)\n
 - Supported operations: +, -, *, /, ^, **, (, )\n
 - Parentheses support\n
 \n
 2. Flexible Conversion\n
 - Convert between any bases (2-36)\n
 - Handle integers and fractions\n
 - Configurable precision\n
 \n
 3. Syntax Support:\n
 - Format: [sign][value][.fraction]_[base]\n
 - Case-insensitive letters (A-Z)\n
 \n
 Limitations:\n
 - Uses eval() - avoid untrusted input\n
 - Max base: 36 (0-9 + A-Z)\n
 - For extended base use abc= in rebase\n
 - Precision limited to 10 decimal places\n

"""

from .BaseBridge import *

