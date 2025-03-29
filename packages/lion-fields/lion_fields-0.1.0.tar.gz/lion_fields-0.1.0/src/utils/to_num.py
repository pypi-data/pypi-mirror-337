import re
from typing import Any, Literal

NumericTypeLiteral = Literal["int", "float"]
PATTERN_DECIMAL = r"[-+]?\d+(\.\d+)?"
PATTERN_SPECIAL = r"[-+]?inf|[-+]?infinity|nan"
ALLOWED_PATTERN = f"(?:{PATTERN_DECIMAL}|{PATTERN_SPECIAL})"


def to_num(
    input_: Any,
    /,
    *,
    upper_bound: float | None = None,
    lower_bound: float | None = None,
    num_type: NumericTypeLiteral = "float",
    precision: int | None = None,
) -> int | float:
    """
    Convert input to int or float, with optional bounds and precision.
    - No multi-value parsing
    - No scientific, fractions, percentages, or complex numbers
    - Accepts 'inf', '-inf', 'nan' if present in the string (remove if not desired)

    Args:
        input_ (Any): Input value to parse. Could be numeric or string.
        upper_bound (float | None): Maximum allowed numeric value (inclusive).
        lower_bound (float | None): Minimum allowed numeric value (inclusive).
        num_type (Literal["int", "float"]): Whether to return an int or float. Default is "float".
        precision (int | None): If float, apply rounding to given decimal places.

    Returns:
        int | float: The parsed and validated number.

    Raises:
        ValueError: If parsing fails, or value is out of bounds.
        TypeError: If an incompatible type is encountered, or conversion to int fails when decimals exist.
    """

    # 1. If already numeric, handle directly
    if isinstance(input_, (int, float)):
        return _finalize_number(
            float(input_), num_type, upper_bound, lower_bound, precision
        )

    # 2. Convert to string and attempt parsing
    input_str = str(input_).strip().lower()

    # Simple decimal or special pattern check
    match = re.fullmatch(ALLOWED_PATTERN, input_str)
    if not match:
        raise ValueError(f"Invalid numeric input: '{input_str}'")

    # 3. Convert to float
    if "inf" in input_str or "nan" in input_str:
        value = float(input_str)  # e.g., float('inf'), float('-inf'), float('nan')
    else:
        value = float(input_str)  # parse normal decimal

    return _finalize_number(value, num_type, upper_bound, lower_bound, precision)


def _finalize_number(
    value: float,
    num_type: Literal["int", "float"],
    upper_bound: float | None,
    lower_bound: float | None,
    precision: int | None,
) -> int | float:
    """
    Apply bounds, rounding (if float), and convert to the requested num_type.
    """
    # A) Bounds check
    if not (value == value):  # Check for nan
        pass  # If nan, can't do a numeric comparison, skip
    else:
        if upper_bound is not None and value > upper_bound:
            raise ValueError(f"Value {value} exceeds upper bound {upper_bound}")
        if lower_bound is not None and value < lower_bound:
            raise ValueError(f"Value {value} below lower bound {lower_bound}")

    # B) If float is requested, optionally apply precision
    if num_type == "float":
        if precision is not None and not (value != value):  # not nan
            value = round(value, precision)
        return value

    # C) If int is requested, ensure it's effectively an integer
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError("Cannot convert 'inf' or 'nan' to int")

    if value.is_integer():
        return int(value)
    else:
        # If there's a decimal part, that's invalid for an int
        raise TypeError(f"Cannot safely convert non-integer value {value} to int.")
