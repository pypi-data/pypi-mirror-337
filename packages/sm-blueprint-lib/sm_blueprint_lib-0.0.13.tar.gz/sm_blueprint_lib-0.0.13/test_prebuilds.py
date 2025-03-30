import os
from random import randint
from math import sin
from typing import Sequence

from numpy import array
from src.sm_blueprint_lib import Blueprint, connect, num_to_bit_list, save_blueprint
from src.sm_blueprint_lib.parts.logicgate import LogicGate
from src.sm_blueprint_lib.pos import Pos
from src.sm_blueprint_lib.prebuilds.adder import simple_adder_subtractor
from src.sm_blueprint_lib.prebuilds.barrel_shifter import barrel_shifter
from src.sm_blueprint_lib.prebuilds.clock40hz import clock40hz
from src.sm_blueprint_lib.prebuilds.comparator import comparator
from src.sm_blueprint_lib.prebuilds.counter import counter
from src.sm_blueprint_lib.prebuilds.distance_sensor import distance_sensor, distance_sensor_raycast
from src.sm_blueprint_lib.prebuilds.ram import ram
from src.sm_blueprint_lib.prebuilds.decoder import decoder
from src.sm_blueprint_lib.prebuilds.register import counter_register, register
from src.sm_blueprint_lib.prebuilds.rom import rom
from src.sm_blueprint_lib.prebuilds.timer_ram_multiclient import timer_ram_multiclient
from src.sm_blueprint_lib.prebuilds.timer_ram_cached import timer_ram_cached


bp = Blueprint()

timer_ram_cached(bp,
                 bit_length=8,
                 num_address_per_cache=8,
                 num_caches=4,
                 num_timer_banks=4,
                 num_caches_per_bank=128)

# comparator(bp, bit_length=32)

# simple_adder_subtractor(bp, bit_length=32)

# counter_register(bp,
#                  bit_length=6,
#                  OE=True,
#                  with_increment=True,
#                  with_decrement=True)


# clock40hz(bp, 10)

# timer_ram_multiclient(bp, bit_length=32, num_address=16, num_clients=1)

# timer_ram_cached(bp,
#                  bit_length=32,
#                  num_address_per_cache=4,
#                  num_caches=4,
#                  num_timer_banks=4,
#                  num_caches_per_bank=1024)


# barrel_shifter(bp,
#                bit_length=32,
#                num_bit_shift=6)

# distance_sensor(bp,
#                 range(1, 9, 1))

# distance_sensor_raycast(bp,
#                         range(1, 21, 2))


# # Initial instructions rom
# micro_ins = [100,101,102,103,104,105,106,107,108]
# rom1 = rom(bp, pos=(-30, -30, 0),
#            page_size=(32, 8),
#            data=micro_ins)


# register(bp, pos=(15,-5,0), bit_length=24, OE=False)

# decoder(bp, pos=(30, 5, 0), num_address=16)

# ram(bp, pos=(20,5,0),
#     bit_length=8,
#     num_address=8)

# reg = register(bp, pos=(0, -10, 0), bit_length=32)
# c = counter(bp, pos=(0, -9, 1), bit_length=32,
#             precreated_swxors=reg[0][:, 1])


print(f"Prebuild size: {len(bp.bodies[0].childs)} parts")
path = r"C:\Users\mauri\AppData\Roaming\Axolot Games\Scrap Mechanic\User\User_76561198400983548\Blueprints\c35f6e4e-52cb-4b00-8afa-f0ffd3fbb012\blueprint.json"
save_blueprint(bp, path)
