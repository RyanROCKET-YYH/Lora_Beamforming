"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Beamformer',   # will show up in GRC
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.complex64]
        )
        self.message_port_register_in(pmt.intern('msg_in'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
        self.phase_shift = 0
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        
    def handle_msg(self, msg):
        #print("Receive phase adjustment: " + str(pmt.to_long(msg)))
        self.phase_shift = pmt.to_long(msg)

    def work(self, input_items, output_items):
        output_items[0][:] = input_items[0][:] + (input_items[1][:] * np.exp(1j * np.deg2rad(self.phase_shift)))
        return len(output_items[0])
