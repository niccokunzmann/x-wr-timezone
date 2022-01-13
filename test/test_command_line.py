"""Test the command line interfae explicitely"""
import subprocess


CMD = "x-wr-timezone"


def test_help():
    """Test that a help is being displayed."""
    help = subprocess.check_output([CMD, "--help"])
    assert b'x-wr-timezone' in help
