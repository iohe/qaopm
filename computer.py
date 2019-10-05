
import utime
from memory import Memory, load_memory
from display_adapter import DisplayAdapter
from snapshot import load_sna_snapshot, load_z80_v1_snapshot
from interrupt_operations import OpRetn
from io import IO
from processor import Processor, InterruptRequest
import image
import lcd
import gc
from machine import UART

class DummyIO(IO):
    def read(self, port, high_byte):
        print("read {} {}".format(hex(port), hex(high_byte)))
        ke = UART.repl_uart().any()
        #naive implementation to declare that 0 was read.
        if ke > 0:
            if port == 0xfe: 
                if high_byte == 0xef:
                    mychar = UART.repl_uart().readchar()
                    if mychar == 48:
                        print("returning254")
                        return 254
        return 191

    def write(self, port, high_byte, value):
        pass
        # print 'write {}, {}'.format(hex(port), hex(value))

def start(rom_file, snapshot_file):
    img = image.Image("image.jpg")
    gc.collect()
    memory = bytearray(0x10000) 
    lcd.init(freq=15000000)
    display_r = DisplayAdapter(memory)
    gc.collect()
    processor = Processor(memory, DummyIO())
    gc.collect()
    load_memory(memory, rom_file, 0x0000)
    load_z80_v1_snapshot(snapshot_file, processor, memory)
    
    #run_loop(processor, PixelArray(screen), display_adapter)
    run_loop(processor, img, display_r)

#def run_loop(processor, screen, display_adapter):
def run_loop(processor, img, display_r):
    processor_clock_hz = 4000000
    seconds_per_refresh = 0.02
    time_per_t_state = 1.0 / processor_clock_hz
    t_states_per_refresh = seconds_per_refresh / time_per_t_state

    i = 0
    while i < 10000:
        i += 1
        update_display(img, display_r) + seconds_per_refresh
        t_states = 0
        processor.interrupt(InterruptRequest(irq_ack))
        while t_states < t_states_per_refresh:
            t_states += processor.execute()


def irq_ack():
    pass


def current_time_ms():
    return utime.time()


def update_display(img, display_adapter):
    display_adapter.update_display(img)
    lcd.display(img)
#    pygame.display.flip()
    return current_time_ms()
