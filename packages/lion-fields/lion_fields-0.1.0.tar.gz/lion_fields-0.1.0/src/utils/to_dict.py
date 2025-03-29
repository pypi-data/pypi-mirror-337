from __future__ import annotations

import json
import logging
from typing import Any, Mapping

from .fuzzy_parse_json import fuzzy_parse_json

logger = logging.getLogger(__name__)


def to_dict(
    input_: Any,
    *,
    fuzzy_parse: bool = False,
    suppress: bool = False,
    recursive: bool = False,
    max_recursive_depth: int = 5,
    use_model_dump: bool = True,
) -> dict[str, Any]:
    """
    Convert various Python objects into a dictionary.

    Features:
      - If string, parse as JSON (with optional fuzzy parse).
      - If dict, return as-is.
      - If pydantic model, optionally call model_dump().
      - If recursion is True, then nested strings/dicts/lists are processed.

    Args:
        input_ (Any): The input to convert to a dict.
        fuzzy_parse (bool): If True, tries single-quote => double-quote fix on JSON strings.
        suppress (bool): If True, returns {} on any error instead of raising.
        recursive (bool): If True, also recursively process nested items.
        max_recursive_depth (int): Limit recursion depth (default=5).
        use_model_dump (bool): If True and `input_` is a pydantic model, call model_dump().

    Returns:
        A dictionary representation of `input_`.

    Raises:
        ValueError: If parsing fails (unless suppress=True).
        TypeError: If input_ is a type we cannot handle safely.
    """
    try:
        if recursive:
            return _recur_to_dict(
                input_,
                fuzzy_parse=fuzzy_parse,
                depth=0,
                max_depth=max_recursive_depth,
                use_model_dump=use_model_dump,
            )
        else:
            return _to_dict(
                input_,
                fuzzy_parse=fuzzy_parse,
                use_model_dump=use_model_dump,
            )
    except Exception as e:
        if suppress:
            logger.warning(f"to_dict suppressed error: {e}")
            return {}
        raise e


def _to_dict(
    obj: Any,
    *,
    fuzzy_parse: bool,
    use_model_dump: bool,
) -> dict[str, Any]:
    """
    Non-recursive version.
    If obj is a dict, returns as is.
    If string, parse as JSON.
    If pydantic model, optionally model_dump.
    Otherwise attempt dict(obj).
    """
    # 1) If it’s already a dict
    if isinstance(obj, dict):
        return obj

    # 2) If it’s a string => parse JSON
    if isinstance(obj, str):
        if fuzzy_parse:
            parsed = fuzzy_parse_json(obj)
        else:
            parsed = json.loads(obj)
        if isinstance(parsed, dict):
            return parsed
        # If it’s a list or something else, we forcibly convert to {0: item...}?
        # Or raise. Let's be consistent. We'll treat it as a type error:
        raise TypeError("Parsed JSON is not an object (dict).")

    # 3) If it’s a pydantic model
    # Checking by attribute is typical if we can’t import pydantic classes
    if use_model_dump and hasattr(obj, "model_dump") and callable(obj.model_dump):
        return obj.model_dump()

    # 4) If it’s a Mapping
    if isinstance(obj, Mapping):
        return dict(obj)

    # 5) Attempt direct dict(...) if it’s convertible
    try:
        return dict(obj)
    except Exception:
        # If we can’t, fallback to e.g. an empty dict or raise
        raise TypeError(f"Cannot convert {type(obj).__name__} to dict.")


def _recur_to_dict(
    obj: Any,
    *,
    fuzzy_parse: bool,
    depth: int,
    max_depth: int,
    use_model_dump: bool,
) -> Any:
    """
    Recursively process the object to convert nested strings/dicts/lists into dict form,
    up to max_depth.
    """
    if depth >= max_depth:
        return obj

    # 1) If string => parse once
    if isinstance(obj, str):
        try:
            val = _to_dict(obj, fuzzy_parse=fuzzy_parse, use_model_dump=use_model_dump)
            # Then continue recursion on the result
            return _recur_to_dict(
                val,
                fuzzy_parse=fuzzy_parse,
                depth=depth + 1,
                max_depth=max_depth,
                use_model_dump=use_model_dump,
            )
        except Exception:
            # If fails, just return the original string
            return obj

    # 2) If dict => parse children
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            new_val = _recur_to_dict(
                v,
                fuzzy_parse=fuzzy_parse,
                depth=depth + 1,
                max_depth=max_depth,
                use_model_dump=use_model_dump,
            )
            new_dict[k] = new_val
        return new_dict

    # 3) If list/tuple => parse each item
    if isinstance(obj, (list, tuple, set)):
        new_list = []
        for item in obj:
            new_item = _recur_to_dict(
                item,
                fuzzy_parse=fuzzy_parse,
                depth=depth + 1,
                max_depth=max_depth,
                use_model_dump=use_model_dump,
            )
            new_list.append(new_item)
        # Return same container type as original
        return type(obj)(new_list)

    # 4) If pydantic model
    if use_model_dump and hasattr(obj, "model_dump") and callable(obj.model_dump):
        raw = obj.model_dump()
        # Recurse on the raw dict
        return _recur_to_dict(
            raw,
            fuzzy_parse=fuzzy_parse,
            depth=depth + 1,
            max_depth=max_depth,
            use_model_dump=use_model_dump,
        )

    # 5) If mapping => turn into dict
    if isinstance(obj, Mapping):
        # convert to dict => then recurse
        d = dict(obj)
        return _recur_to_dict(
            d,
            fuzzy_parse=fuzzy_parse,
            depth=depth + 1,
            max_depth=max_depth,
            use_model_dump=use_model_dump,
        )

    # 6) If can do dict(obj)
    try:
        d = dict(obj)
        return _recur_to_dict(
            d,
            fuzzy_parse=fuzzy_parse,
            depth=depth + 1,
            max_depth=max_depth,
            use_model_dump=use_model_dump,
        )
    except Exception:
        pass

    # 7) Otherwise just return
    return obj
