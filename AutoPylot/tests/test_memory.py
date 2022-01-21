"""Test the memory class."""
from ..utils import memory


def test_memory_dict():
    mem = memory.Memory()
    mem["test"] = "this is a test"
    assert mem == {"test": "this is a test"}


def test_memory_add_dict():
    mem = memory.Memory()
    mem["test"] = "this is a test"
    mem + {"test2": "this is an other test"}
    assert mem == {"test": "this is a test", "test2": "this is an other test"}


def test_memory_add():
    mem = memory.Memory()
    mem["test"] = "this is a test"
    other_mem = memory.Memory()
    other_mem["test2"] = "this is an other test"
    mem + other_mem
    assert mem == {"test": "this is a test", "test2": "this is an other test"}


def test_memory_last_modified():
    mem = memory.Memory()
    mem["test"] = "this is a test"
    assert mem.last_modified != 0
