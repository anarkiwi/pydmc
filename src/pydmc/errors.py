"""Exceptions for pydmc."""


class DmcError(Exception):
    """Base error for all pydmc failures."""


class SidParseError(DmcError):
    """A SID/PRG image could not be parsed as a DMC tune."""
