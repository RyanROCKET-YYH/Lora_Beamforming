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
            name='Angle messenger',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[]
        )
        self.message_port_register_in(pmt.intern('msg_in'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('message_out'))
        self.average_list = []
        self.average_list_size = 25
        
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
    
    def handle_msg(self, msg):
        #print(self.average_list)
        self.message_port_pub(pmt.intern("message_out"), pmt.from_float(max(self.average_list)))

    def work(self, input_items, output_items):
        if len(self.average_list) >= self.average_list_size:
            self.average_list.pop(0)
        self.average_list.append(input_items[0][-1])
        return len(input_items[0])
