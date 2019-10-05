#!/usr/bin/python
from io import IO
from processor import Processor
from memory import Memory, load_memory
# import argparse
import lcd
from display_adapter import DisplayAdapter
import image
import gc

def run():
    img = image.Image("image.jpg")
   
    memory = bytearray(0x10000) 
    lcd.init(freq=15000000)
    gc.collect()
    display_r = DisplayAdapter(memory)
    io = IO()
    gc.collect()
    print(gc.mem_free())
    print("before processor")
    processor = Processor(memory, io)
    gc.collect()
    print("after processor")
    print(gc.mem_free())
    load_memory(memory, "48.rom", 0x0000)
    print(gc.mem_free())

    t_states = 0
    while True:
        executed = processor.execute()
        #if args.verbose:
        #    print(executed)
        print(executed)
        #else:
        #    print('.'),
        t_states += executed
        gc.mem_free()
        if str(executed) == 'nop':
            break
        display_r.update_display(img)

        lcd.display(img)

    print('\n')
    print('Completed program execution in {} t-states'.format(t_states))

if __name__ == '__main__':
    run()
