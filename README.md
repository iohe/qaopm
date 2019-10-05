Place all these .py files in MaixPy/components/micropython/port/builtin_py
MaixPy is @8279a1fe1
To build
 cd MaixPy/projects/maixpy_k210
 python3 project.py rebuild

Flash MaixPy/projects/maixpy_k210/build/maixpy.bin

import computer
#48.rom is original rom loaded at 0x0000
#nether.z80 is a z80 snapshot loaded at 0x4000
computer.start("48.rom", "nether.z80")

