
# Numeral System Converter and Expression Evaluator

A Python module for converting numbers between numeral systems (2-36) and evaluating cross-base mathematical expressions.  
**Key Features**:  
- Integer/fractional conversions  
- Mixed-base calculations (`+`, `-`, `*`, `/`, `^`, parentheses)  
- Minimum base detection  
- Custom error handling  



## Quick Start

### 1. **Convert Numbers**

```python
from BaseKit import rebase

# Integer conversions
print(rebase("1011_2", to_base=10))  # "11_10" (binary -> decimal)
print(rebase("FF_16", to_base=2))  # "11111111_2" (hex -> binary)

# Fractional conversions
print(rebase("3.14_10", to_base=16))  # "3.23D7_16" (rounded to 4 digits)
print(rebase("A.8_16", to_base=10))  # "10.5_10" (hex -> decimal)

# Custom precision
print(rebase("0.1_2", to_base=10, rounding=6))  # "0.5_10"
```

### 2. **Evaluate Cross-Base Expressions**

```python
from BaseKit import eval2dec, rebase

# Mixed-base arithmetic
print(eval2dec("10_2 + A_16"))  # "12_10" (2 + 10 = 12)
print(eval2dec("FF_16 - 10_10"))  # "245_10" (255 - 10 = 245)

# Advanced operations
print(eval2dec("(10_8 + 20_16) / 2_10"))  # "20.0_10" (8 + 32 = 40; 40 / 2 = 20)
print(eval2dec("2_10 ^ 4_10"))  # "16_10" (2⁴ = 16)

print(rebase("f_30*10010_2", to_base=5))  # "2040_5" 30 + 33 = 270

```

### 3. **Find Minimum Valid Base**

```python
from BaseKit import minBase

print(minBase("Z"))  # 36 (max symbol in base-36)
print(minBase("1A"))  # 11 (symbol 'A' requires base ≥11)
```

---

## Error Handling

### Common Errors and Exceptions

| Error Class (Custom)               | Standard Exception | Trigger Example                | Error Message                          |
|------------------------------------|--------------------|--------------------------------|----------------------------------------|
| `Error.DigitInvalidForBase`        | `ValueError`       | `rebase("G_16")`               | "Invalid digit 'G' for base 16"        |
| `Error.BelongingAlphabet`          | `ValueError`       | `rebase("?@_16")`              | "The symbol ? is not supported..."     |
| `Error.BelongingFromBase/ToBase`   | `ValueError`       | `rebase("3.14_10", to_base=37)`| "to_base must be in (2:36). to_base=37"|
| `Error.NoBaseGiven`                | `SyntaxError`      | `rebase("1011")`               | "Missing base specification"           |
| `Error.BaseIntError`               | `ValueError`       | `rebase("10_2", from_base="hex")`| "Invalid from_base: hex"              |

**Example Tests from `tests.py`**:

```python
# tests.py
from BaseKit import rebase


def test_error_handling(self):
    with self.assertRaises(ValueError):  # Error.DigitInvalidForBase
        rebase("G_16")
    with self.assertRaises(SyntaxError):  # Error.NoBaseGiven
        rebase("1011")
    with self.assertRaises(ValueError):  # Error.BelongingToBase
        rebase("3.14_10", to_base=37)
```

---

## Testing
Run unit tests to verify functionality:
```bash
python -m unittest tests.py -v
```

**Test Coverage**:  
- **Conversions**: Integers, fractions, edge cases (e.g., `0_10 -> 0_2`).  
- **Expressions**: Mixed-base operations, parentheses, error propagation.  
- **Errors**: Invalid digits, missing bases, out-of-range bases.  

---

## Notes
- **Precision**: Fractional results are truncated to 10 decimal places.  
- **Security**: Uses `eval()` internally. Avoid untrusted input.  
- **Alphabet**: Default: `0-9, A-Z` (case-insensitive). Extend via `abc` parameter.  

---

**Author**: Fedor Tyulpin  
**Version**: 1.0  
```
