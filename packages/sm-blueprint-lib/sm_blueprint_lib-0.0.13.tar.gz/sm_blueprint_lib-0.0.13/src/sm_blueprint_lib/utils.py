"""
Utility functions for basic uses.
"""

from dataclasses import asdict
from json import load, dump, loads, dumps
from math import ceil, log2
from typing import Sequence
import PIL

from numpy import ndarray

from .bases.parts.baseinteractablepart import BaseInteractablePart
from .blueprint import Blueprint
from .parts.barrierblock import BarrierBlock
from .parts.logicgate import LogicGate
from .parts.timer import Timer


def load_blueprint(path: str):
    """Load a blueprint from a path file (normally a blueprint.json).

    Args:
        path (str): The path to the json file.

    Returns:
        Blueprint: The loaded blueprint.
    """
    with open(path) as fp:
        return Blueprint(**load(fp))


def save_blueprint(bp: Blueprint, path: str):
    """Save a blueprint to a file (normally a blueprint.json).

    Args:
        path (str): The path to save the json file.
        bp (Blueprint): The blueprint to be saved.
    """
    with open(path, mode="w") as fp:
        return dump(asdict(bp), fp, sort_keys=True, separators=(',', ':'))


def load_blueprint_from_string(str: str):
    """Load a blueprint from a json string.

    Args:
        str (str): The string to be loaded.

    Returns:
        Blueprint: The loaded blueprint.
    """
    return Blueprint(**loads(str))


def dump_string_from_blueprint(bp: Blueprint):
    """Dump a blueprint into a json-formatted string.

    Args:
        bp (Blueprint): The blueprint to be dumped.

    Returns:
        str: The json-formatted string.
    """
    return dumps(asdict(bp), sort_keys=True, separators=(',', ':'))


def connect(_from, _to, *, parallel=True):
    """Connect interactable parts together, recursively.

    Args:
        _from (Any): Must be an instance of BaseInteractablePart or a subclass.
        Also it can be any nested iterable of instances (list of parts, list of lists of parts, etc).
        _to (Any): Must be an instance of BaseInteractablePart or a subclass.
        Also it can be any nested iterable of instances (list of parts, list of lists of parts, etc).
        parallel (bool, optional): Defines the behaviour of the connections in the following way:

        With parallel=False, everything connects to everything:
            from1 🔀 to1

            from2 🔀 to2

        With parallel=True, every row is connected respectively:
            from1 → to1

            from2 → to2

        Also, if the dimensions does not match it tries to adapt (many to one, one to many, etc)

        Defaults to True.
    """
    if isinstance(_from, BaseInteractablePart) and isinstance(_to, BaseInteractablePart):
        _from.connect(_to)
        return
    # Try connect things row-by-row if possible (one to one, one to many, many to many)
    if parallel:
        # Assume both are sequence of parts
        if not isinstance(_from, BaseInteractablePart) and not isinstance(_to, BaseInteractablePart):
            for subfrom, subto in zip(_from, _to):
                connect(subfrom, subto, parallel=parallel)
        # Assume _from is a sequence of parts
        elif not isinstance(_from, BaseInteractablePart):
            for subfrom in _from:
                connect(subfrom, _to, parallel=parallel)
        else:                                               # Assume _to is a sequence of parts
            for subto in _to:
                connect(_from, subto, parallel=parallel)
    else:           # Just connect everything to everything lol
        # Assume both are sequence of parts
        if not isinstance(_from, BaseInteractablePart) and not isinstance(_to, BaseInteractablePart):
            for subfrom in _from:
                for subto in _to:
                    connect(subfrom, subto, parallel=parallel)
        # Assume _from is a sequence of parts
        elif not isinstance(_from, BaseInteractablePart):
            for subfrom in _from:
                connect(subfrom, _to, parallel=parallel)
        else:                                               # Assume _to is a sequence of parts
            for subto in _to:
                connect(_from, subto, parallel=parallel)


def get_bits_required(number: int | float):
    """Calculates how many bits are required to store this number.

    Args:
        number (int | float): The target number.
    """
    return ceil(log2(number))


def num_to_bit_list(number: int, bit_length: int):
    """Converts a number to a numpy array of its bits.

    Args:
        number (int): The number to convert.
        bit_length (int): The number of bits the list will have.
    """
    output = ndarray(bit_length, dtype=bool)
    for b in range(bit_length):
        output[b] = bool((number >> b) & 1)
    return output


"""

def fill_void(object,x,y,z,block, color = "000000" ,offSet = None):
    def show_fill_block():
        def logic_gate(image,pos,size, color):
            for x in range(16):
                for y in range(16):
                    if x <= 1 or y <= 1 or x >= 14 or y >= 14 :
                        image.putpixel((pos[0]+x, pos[1]+y), color)
                    if 1 < y < 14 and 1 < x < 14 :
                        image.putpixel((pos[0]+x, pos[1]+y), (128,128,128))

            image.putpixel((pos[0]+4, pos[1]+4), (32, 32, 32))            # I dont even know why this is the way it its -steve
            image.putpixel((pos[0]+4, pos[1]+5), (32, 32, 32))
            image.putpixel((pos[0]+4, pos[1]+6), (32, 32, 32))
            image.putpixel((pos[0]+4, pos[1]+7), (32, 32, 32))
            image.putpixel((pos[0]+4, pos[1]+8), (32, 32, 32))
            image.putpixel((pos[0]+4, pos[1]+9), (32, 32, 32))
            image.putpixel((pos[0]+4, pos[1]+10), (32, 32, 32))
            image.putpixel((pos[0]+4, pos[1]+11), (32, 32, 32))
            image.putpixel((pos[0]+5, pos[1]+4), (32, 32, 32))
            image.putpixel((pos[0]+5, pos[1]+5), (32, 32, 32))
            image.putpixel((pos[0]+5, pos[1]+6), (32, 32, 32))
            image.putpixel((pos[0]+5, pos[1]+7), (32, 32, 32))
            image.putpixel((pos[0]+5, pos[1]+8), (32, 32, 32))
            image.putpixel((pos[0]+5, pos[1]+9), (32, 32, 32))
            image.putpixel((pos[0]+5, pos[1]+10), (32, 32, 32))
            image.putpixel((pos[0]+5, pos[1]+11), (32, 32, 32))

            image.putpixel((pos[0]+6, pos[1]+10), (32, 32, 32))
            image.putpixel((pos[0]+6, pos[1]+11), (32, 32, 32))
            image.putpixel((pos[0]+7, pos[1]+10), (32, 32, 32))
            image.putpixel((pos[0]+7, pos[1]+11), (32, 32, 32))
            image.putpixel((pos[0]+8, pos[1]+10), (32, 32, 32))
            image.putpixel((pos[0]+8, pos[1]+11), (32, 32, 32))
            image.putpixel((pos[0]+9, pos[1]+9), (32, 32, 32))
            image.putpixel((pos[0]+9, pos[1]+10), (32, 32, 32))
            image.putpixel((pos[0]+9, pos[1]+11), (32, 32, 32))
            image.putpixel((pos[0]+10, pos[1]+10), (32, 32, 32))

            image.putpixel((pos[0]+6, pos[1]+4), (32, 32, 32))
            image.putpixel((pos[0]+6, pos[1]+5), (32, 32, 32))
            image.putpixel((pos[0]+7, pos[1]+4), (32, 32, 32))
            image.putpixel((pos[0]+7, pos[1]+5), (32, 32, 32))
            image.putpixel((pos[0]+8, pos[1]+4), (32, 32, 32))
            image.putpixel((pos[0]+8, pos[1]+5), (32, 32, 32))
            image.putpixel((pos[0]+9, pos[1]+4), (32, 32, 32))
            image.putpixel((pos[0]+9, pos[1]+5), (32, 32, 32))
            image.putpixel((pos[0]+9, pos[1]+6), (32, 32, 32))
            image.putpixel((pos[0]+10, pos[1]+5), (32, 32, 32))

            image.putpixel((pos[0]+10, pos[1]+6), (32, 32, 32))
            image.putpixel((pos[0]+10, pos[1]+7), (32, 32, 32))
            image.putpixel((pos[0]+10, pos[1]+8), (32, 32, 32))
            image.putpixel((pos[0]+10, pos[1]+9), (32, 32, 32))
            image.putpixel((pos[0]+11, pos[1]+6), (32, 32, 32))
            image.putpixel((pos[0]+11, pos[1]+7), (32, 32, 32))
            image.putpixel((pos[0]+11, pos[1]+8), (32, 32, 32))
            image.putpixel((pos[0]+11, pos[1]+9), (32, 32, 32))

        def Noblock(image,pos,size):
            for x in range(size[0]):
                for y in range(size[1]):
                    if x == y or x+1 == y or x == size[1]-y or x+1 == size[1]-y or x == 0 or y == 0 or x == size[0]-1 or y == size[1]-1 :
                        image.putpixel((pos[0]+x, pos[1]+y), (255,0,0))
                    else:
                        image.putpixel((pos[0] + x, pos[1] + y), (0, 0, 0))

        size = 16
        new_image = Image.new("RGB", (int(len(filled_blocks)*size), int(len(filled_blocks[0])*size)), color=0)
        for z in range(len(filled_blocks[0][0])):
            for x in range(len(filled_blocks)):
                for y in range(len(filled_blocks[x])):
                    if filled_blocks[x][y][z] is not None:
                        logic_gate(new_image,(x*size,-y*size),(size,size),hex_rgb(filled_blocks[x][y][z]))

                    else:
                        Noblock(new_image,(x*size,-y*size),(size,size))
            new_image.show()

    def fill_block(member):
        if hasattr(member, "timer_pos"):
            posx, posy, posz = member.timer_pos
            posx -= offx
            posy -= offy
            posz -= offz
            filled_blocks[posx][posy][posz] = member

        posx, posy, posz = member.pos
        posx -= offx
        posy -= offy
        posz -= offz
        filled_blocks[posx][posy][posz] = member

    def fill():
        isblock = False
        blocks_members = [attr for attr in dir(blocks) if not callable(getattr(blocks, attr)) and not attr.startswith("__")]
        for each in blocks_members:
            if block["uuid"] == blocks.__getattribute__(each)["uuid"]:
                isblock = True
                break


        for x in range(len(filled_blocks)):
            for y in range(len(filled_blocks[x])):
                if filled_blocks[x][y][0] is None:
                    if isblock:
                        object.fill_block(block, (x+offx,y+offy-1,offz), (1,1,1), color)
                    else:
                        object.place_object(block,(x+offx,y+offy-1,offz),"up","up", color)

    filled_blocks = [[[None for _ in range(z)] for _ in range(y)] for _ in range(x)]

    if offSet is not None:
        offx, offy, offz = offSet
    elif hasattr(object, "pos"):
        offx,offy,offz = object.pos
    else:
        offx, offy, offz = 0,0,0

    members = [attr for attr in dir(object) if not callable(getattr(object, attr)) and not attr.startswith("__")]

    for each in members:
        member = object.__getattribute__(each)
        if type(member) == type([]):
            for each in member:
                if hasattr(each, "pos"):
                    fill_block(each)

        elif hasattr(member,"pos"):
            fill_block(member)

    #show_fill_block()
    fill()

def border(blueprint,posx,posy,offx,offy):
    offx-=1
    offy-=1
    posx+=1

    for y in range(posy):
        blueprint.place_object(objects.Small_Pipe_Tee,(offx,y + offy,0),"up","up","000000")
        blueprint.place_object(objects.Duct_End,(offx,y + offy,0),"south","right","000000")
        blueprint.place_object(objects.Duct_End,(offx,y + offy,0),"north","left","000000")
        blueprint.place_object(objects.Duct_End,(offx,y + offy,0),"south","left","000000")

        blueprint.place_object(objects.Small_Pipe_Tee,(offx+posx,y + offy,0),"up","down","000000")
        blueprint.place_object(objects.Duct_End,(offx+posx,y + offy,0),"west","down","000000")
        blueprint.place_object(objects.Duct_End,(offx+posx,y + offy,0),"south","right","000000")
        blueprint.place_object(objects.Duct_End,(offx+posx,y + offy,0),"south","left","000000")

    for x in range(posx-1):
        blueprint.place_object(objects.Small_Pipe_Tee,(1+x+offx,offy-1,0),"up","left","000000")
        blueprint.place_object(objects.Duct_End,(1+x+offx,offy-1,0),"west","down","000000")
        blueprint.place_object(objects.Duct_End,(1+x+offx,offy-1,0),"east","left","000000")
        blueprint.place_object(objects.Duct_End,(1+x+offx,offy-1,0),"west","left","000000")

        blueprint.place_object(objects.Small_Pipe_Tee,(1+x+offx,offy+posy,0),"up","right","000000")
        blueprint.place_object(objects.Duct_End,(1+x+offx,offy+posy,0),"west","up","000000")
        blueprint.place_object(objects.Duct_End,(1+x+offx,offy+posy,0),"east","left","000000")
        blueprint.place_object(objects.Duct_End,(1+x+offx,offy+posy,0),"west","left","000000")
    offy-=1
    blueprint.place_object(objects.Small_Pipe_Bend, (offx, offy, 0), "west", "left", "000000")
    blueprint.place_object(objects.Duct_End, (offx, offy, 0), "west", "right", "000000")
    blueprint.place_object(objects.Duct_End, (offx, offy, 0), "south", "left", "000000")
    blueprint.place_object(objects.Duct_End, (offx, offy, 0), "west", "down", "000000")
    blueprint.place_object(objects.Duct_End, (offx, offy, 0), "south", "up", "000000")
    blueprint.place_object(objects.Small_Pipe_Bend, (offx, posy+offy+1, 0), "west", "right", "000000")
    blueprint.place_object(objects.Duct_End, (offx, posy+offy+1, 0), "west", "right", "000000")
    blueprint.place_object(objects.Duct_End, (offx, posy+offy+1, 0), "north", "left", "000000")
    blueprint.place_object(objects.Duct_End, (offx, posy+offy+1, 0), "west", "up", "000000")
    blueprint.place_object(objects.Duct_End, (offx, posy+offy+1, 0), "north", "right", "000000")
    blueprint.place_object(objects.Small_Pipe_Bend, (posx+offx, offy, 0), "east", "left", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, offy, 0), "south", "left", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, offy, 0), "east", "left", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, offy, 0), "south", "down", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, offy, 0), "east", "up", "000000")
    blueprint.place_object(objects.Small_Pipe_Bend, (posx+offx, posy+offy+1, 0), "east", "right", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, posy+offy+1, 0), "east", "down", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, posy+offy+1, 0), "north", "up", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, posy+offy+1, 0), "east", "left", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, posy+offy+1, 0), "north", "right", "000000")

"""

