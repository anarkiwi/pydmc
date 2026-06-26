"""Exceptions for pydmcsid."""


class DmcError(Exception):
    """Base error for all pydmcsid failures."""


class SidParseError(DmcError):
    """A SID/PRG image could not be parsed as a DMC tune."""
