"""Tooling to allow for cli argument overrides with argparse."""

import argparse
import logging
import typing


T = typing.TypeVar("T")
SingleArgValue = int | float | str
ArgValue = SingleArgValue | list[SingleArgValue]


def _infer_numeric_or_str(value: str) -> int | float | str:
    """Parse a cli argument into an int, float, or leave as a string."""
    for func in (int, float):
        try:
            # int(float) wouldn't throw a ValueError but int(str(float)) will
            # so we can use this to check if the parse was successful.
            return func(value)
        except ValueError:
            continue
    return value


def _delistify_single(l: list[T]) -> list[T] | T:
    """Unpack single element lists into a scalar."""
    return l[0] if len(l) == 1 else l


def parse_extra_args(
    argv,
    prefix: str = "x",
    strict: bool = False,
    infer: bool = True,
    delistify: bool = True,
) -> dict[str, ArgValue]:
    """Parse the extra args from the cli to allow for overrides.

    This allows users to pass arbitrary arguments in the format
    --x:${name}=${value}. It supports passing a list via the cli using repeated
    flags.

    Args:
      argv: The list of cli arguments, from ArgumentParser.parse_known_args()[1]
      prefix: The signal that this flag is an override.
      strict: Should we raise an error when a non-override flag is found.
      infer: Should we try to convert int/float flags to actual numbers.
      delistify: Should we try to unpack single value lists into a scalar.

    Note:
      If you have a typo on one of the main flags, it will get skipped during
      this parsing or cause an error if strict=True

    Returns:
      A dict of override flags to values parsed from the command line.
    """
    # Remove a trailing ":" or leading "--" if they include it.
    prefix = prefix.rstrip(":").lstrip("--")
    if ":" in prefix:
        raise ValueError(f'prefix cannot contain ":", got {prefix}')
    logger = logging.getLogger(__name__)
    prefix = f"--{prefix}:"
    logger.debug("Using '%s' as the override cli prefix.", prefix)
    parser = argparse.ArgumentParser()
    # Build a set of all argv flags that start with the prefix.
    prefix_args = set(filter(lambda x: prefix in x, argv))
    if infer:
        logger.debug("Trying to convert override args to int/floats.")
        type_func = _infer_numeric_or_str
    else:
        logger.debug("Leaving all override args as strings.")
        type_func = str
    for flag in prefix_args:
        flag = flag.split("=")[0]
        logger.debug("Adding '%s' as a cli override flag.", flag)
        parser.add_argument(flag, action="append", type=type_func)
    if strict:
        args = parser.parse_args(argv)
    else:
        for a in argv:
            if a not in prefix_args and a.startswith("--"):
                logger.warning("Unexpected argument: '%s', Skipping...", a)
        args = parser.parse_known_args(argv)[0]
    if delistify:
        logger.debug("Unpacking single arguments into scalars.")
        maybe_delistify = _delistify_single
    else:
        logger.debug("Leaving all arguments as lists.")
        maybe_delistify = lambda x: x
    # Remove the --${prefix}: part of the flag, maybe delisify single element
    # lists, and convert to dict.
    return {k.split(":")[1]: maybe_delistify(v) for k, v in vars(args).items()}
