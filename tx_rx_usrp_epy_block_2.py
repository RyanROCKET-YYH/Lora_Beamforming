"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, vectorSize=512):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='FFT Max',   # will show up in GRC
            in_sig=[(np.float32,vectorSize)],
            out_sig=[np.float32]
        )

    def general_work(self, input_items, output_items):
        """example: multiply with constant"""
        max_val = np.max(input_items[0])
        print("max value is " + str(max_val))
        output_items[0] = max_val
        return len(output_items)
