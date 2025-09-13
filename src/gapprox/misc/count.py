from typing import Iterable
def count(stuff:Iterable, something:any=None) -> int:
    'count how many things are in stuff, excluding something'
    return sum(thing!=something for thing in stuff)

