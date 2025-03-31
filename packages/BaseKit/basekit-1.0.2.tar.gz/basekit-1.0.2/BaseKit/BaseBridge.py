class Error():
    class BelongingFromBase(Exception):
        pass

    class BelongingToBase(Exception):
        pass

    class BelongingAlphabet(Exception):
        pass

    class NoBaseGiven(Exception):
        pass

    class BaseIntError(Exception):
        pass

    class DigitInvalidForBase(Exception):
        pass


def eval2dec( num : str, from_base : int = None, abc : list[str, str, ...] | None= None):
    f"""
    Evaluate mathematical expressions with numbers in different bases

    Args:
        num (str): Expression with numbers in [value]_[base] format

    Returns:
        str: Result in decimal system (_10 format)
        
    Raises:
        Most raises are the same as the raises of the 'rebase' function

    Example:
        >>> eval2dec("(10_2 + A_16) * 3_10")
        '36_10'

    """
    num = num.replace("**", "^").replace(" ", "")
    ex_symbol = "^/*-+"
    c_n = {}

    nums = num
    for sim in ex_symbol:
        nums = nums.replace(sim, '|').replace("(", "").replace(")", "")
    nums = nums.split("|")


    for numx in nums:
        if numx != "":
            key = numx
            c_n[key] = rebase(numx,from_base = from_base, abc=abc)[:-3]

    for x in c_n:
        num = num.replace(x, c_n[x])

    return f"{eval(num.replace('^', '**'))}_10"


def rebase(num: str, to_base : int = 10, from_base: int | str = None, rounding: int = 4, abc=None) -> str:
    f"""
    Convert numbers or expression between numeral systems

    Args:
        
        num (str): Input number or expression with numbers in format: [value]_[base] 
        
        to_base (int): Trgaet base (2-36, default=10)
                
        from_base (int | str): Optional source base instead of the format _[base] (If used with an expression, it is the 
        number system of each number in the expression.)
                
        rounding (int): Max fractional digits of answer (default=4) (does not round the number, but simply cuts off 
        the end) 
        
        abc (list[str,str,...]): Alphabet (initially contains 0-9, A-Z) Can be expanded if needed to count in systems 
        greater than 36. All values  will be added to the original alphabet
    
    Raises:
        - BaseIntError: The number specified as a number system cannot be represented as a decimal number.
        - BelongingFromBase: from_base or to_base is not in valid range (unchanged [2:36])
        - NoBaseGiven: The from_base value is not specified in any way
        - BelongingAlphabet: The number contains an invalid character that cannot be represented as a number. 
        Perhaps the alphabet needs to be expanded?
        - DigitInvalidForBase: The number contains a digit that is impossible in the given number system
        
        
    Returns:
        str: Converted number in format: [value]_[to_base]

    Example:
        >>> rebase("1A.3F_16 + 12.3_10",to_base=10)
        '38.5459_10'
        
        >>> rebase("1A.3F_16",to_base=10)
        '26.2460_10'
        
        >>> rebase("1A.3F",to_base=10,from_base=16)
        '26.2460_10'
    
   """
    if abc is None:
        abc = []
    abc = [f"{x}" for x in range(10)] + [chr(i).upper() for i in range(97, 123)] + abc if abc is not [] else []


    if any([char in "()^/*-+" for char in num]):
        num = eval2dec(num, from_base)

    if num[0]=="-":
        ad_par = "-"
    else:
        ad_par = ""


    if isinstance(from_base, str) and from_base != "":
        try:
            from_base = int(f"{from_base}", 10)
        except:
            raise Error.BaseIntError(f"Invalid from_base: {from_base}")

    if isinstance(to_base, str) or to_base != "":
        try:
            to_base = int(f"{to_base}", 10)
        except:
            raise Error.BaseIntError(f"Invalid to_base: {to_base}")

    if "_" not in num:
        if from_base is None or from_base == "":
            raise Error.NoBaseGiven("Missing base specification")
    elif from_base is None or from_base == "":

        try:
            from_base = int(num[num.index("_") + 1:],10)
        except:
            raise Error.BaseIntError(f"Invalid from_base: {from_base}")

        num = num[:num.index("_")].replace("-", "").replace(" ", "")
    else:
        num = num[:num.index("_")].replace("-", "").replace(" ", "")


    if not(2 <= int(from_base) <=len(abc)):
        raise Error.BelongingFromBase(f"from_base value must be in the range (2:{len(abc)} for the given alphabet (abc)). from_base = {from_base}")

    if not(2 <= to_base <=len(abc)):
        raise Error.BelongingToBase(f"to_base value must be in the range (2:{len(abc)} for the given alphabet (abc)). to_base = {to_base}")



    for let in num.replace(".", "").upper():

        if let not in abc:
            raise Error.BelongingAlphabet(f"The symbol {let} is not supported by this alphabet")

        if abc.index(let) >= from_base:
            raise Error.DigitInvalidForBase(f"Invalid digit '{let}' for base {from_base}")

    ans = []
    dot_id = num.index(".") if "." in num else len(num)
    len_bd = len(num[:dot_id])
    num = num.replace(".", "").upper()

    for i in range(len_bd, len_bd - len(num), -1):
        ans.append(abc.index(num[0]) * from_base ** (i - 1))
        num = num[1:]

    ans_10 = sum(ans)
    bd_10 = ans_10 // 1
    ad_10 = float(f"{ans_10 % 1}")

    a = []
    while bd_10 >= to_base:
        a.append(abc[int(bd_10 % to_base)])
        bd_10 //= to_base
    a.append(abc[int(bd_10 % to_base)])
    a.reverse()
    a = "".join(a)

    b = []
    while 0 < ad_10 < 1:
        b.append(abc[int(f"{(ad_10 * to_base) // 1}"[:-2])])
        ad_10 = (ad_10 * to_base) % 1
    b = "".join(b[:rounding])

    return f"{ad_par}{a}.{b}_{to_base}" if b else f"{ad_par}{a}_{to_base}"

def minBase(num : str, abc : list = None) -> int:
    f"""
    A function that returns the minimum number system in which a given number (num) can exist
    
    Args:
        num: A digit (0-9, A-Z) or number that is the maximum number for the desired number system (9 for decimal number system)
        abc: (list[str,str,...]): Alphabet (initially contains 0-9, A-Z) Can be expanded if needed to count in systems greater than 36. All values  will be added to the original alphabet
        
    Returns:
        int : A number that is the smallest number system in which a given number (num) can exist

    Raises:
        BelongingAlphabet: The entered number is not contained in the alphabet. Perhaps an alphabet expansion is needed?
        InvalidSymbol: 
    """

    if abc is None: abc = []
    num = max(num)
    abc = [f"{x}" for x in range(10)] + [chr(i).upper() for i in range(97, 123)] + abc if abc is not [] else []


    if num.upper() not in abc:
        raise Error.BelongingAlphabet(f"The digit {num.upper()} is not contained in the alphabet")

    return abc.index(num)+1


if __name__ == "__main__":

    print(f"\033[95mHi! There some examples about this program\033[0m")

    # Usage Examples
    print("\n\033[1mBasic Conversion:\033[0m")
    print(rebase("1011_2", to_base=10))  # → "11_10"
    print(rebase("FF_16", to_base=2))  # → "11111111_2"

    print("\n\033[1mFractional Conversion:")
    print(rebase("3.14_10", to_base=16))  # → "3.23D7_16"

    print("\n\033[1mExpression Evaluation:\033[0m")
    print(eval2dec("10_8 + 20_16 / 2_10"))  # → "24.0_10"

    # Original test case
    print("\n\033[1mOriginal Test:\033[0m")
    print(rebase("(10_10+10_10)*2_10", to_base=10, from_base=""))  # 40_10
