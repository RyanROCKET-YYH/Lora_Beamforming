#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Tx Rx Usrp
# Author: Tapparel Joachim@EPFL,TCL
# GNU Radio version: 3.10.3.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio import zeromq
import gnuradio.lora_sdr as lora_sdr
import tx_rx_usrp_epy_block_0 as epy_block_0  # embedded python block
import tx_rx_usrp_epy_block_1 as epy_block_1  # embedded python block



from gnuradio import qtgui

class tx_rx_usrp(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Tx Rx Usrp", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Tx Rx Usrp")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "tx_rx_usrp")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.soft_decoding = soft_decoding = True
        self.sf = sf = 7
        self.samp_rate_rx = samp_rate_rx = 250000
        self.pay_len = pay_len = 255
        self.impl_head = impl_head = False
        self.has_crc = has_crc = True
        self.frame_period = frame_period = 1000
        self.cr = cr = 2
        self.center_freq = center_freq = 915e6
        self.bw = bw = 125000
        self.Att_dB = Att_dB = 0

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_push_msg_sink_0 = zeromq.push_msg_sink('tcp://127.0.0.1:50124', 100, True)
        self.zeromq_pull_msg_source_0_0 = zeromq.pull_msg_source('tcp://127.0.0.1:50123', 100, False)
        self.zeromq_pull_msg_source_0 = zeromq.pull_msg_source('tcp://127.0.0.1:50122', 100, False)
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join(('', '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
        )
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate_rx)
        # No synchronization enforced.

        self.uhd_usrp_source_0_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0_0.set_bandwidth(bw, 0)
        self.uhd_usrp_source_0_0.set_gain(10, 0)

        self.uhd_usrp_source_0_0.set_center_freq(center_freq, 1)
        self.uhd_usrp_source_0_0.set_antenna('RX2', 1)
        self.uhd_usrp_source_0_0.set_bandwidth(bw, 1)
        self.uhd_usrp_source_0_0.set_gain(10, 1)
        self.uhd_usrp_source_0_0.set_min_output_buffer((2**sf<<2))
        self.qtgui_sink_x_0 = qtgui.sink_c(
            2048, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate_rx, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/60)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.lora_rx_0 = lora_sdr.lora_sdr_lora_rx( bw=bw, cr=1, has_crc=True, impl_head=False, pay_len=255, samp_rate=samp_rate_rx, sf=sf, soft_decoding=True, ldro_mode=2, print_rx=[False,False])
        self.epy_block_1 = epy_block_1.blk()
        self.epy_block_0 = epy_block_0.blk()
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(1000, 0.001, 4000, 1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_1, 'message_out'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.zeromq_pull_msg_source_0, 'out'), (self.epy_block_0, 'msg_in'))
        self.msg_connect((self.zeromq_pull_msg_source_0_0, 'out'), (self.epy_block_1, 'msg_in'))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.epy_block_1, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.epy_block_0, 0), (self.lora_rx_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.epy_block_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 1), (self.epy_block_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "tx_rx_usrp")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_soft_decoding(self):
        return self.soft_decoding

    def set_soft_decoding(self, soft_decoding):
        self.soft_decoding = soft_decoding

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf

    def get_samp_rate_rx(self):
        return self.samp_rate_rx

    def set_samp_rate_rx(self, samp_rate_rx):
        self.samp_rate_rx = samp_rate_rx
        self.qtgui_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate_rx)
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate_rx)

    def get_pay_len(self):
        return self.pay_len

    def set_pay_len(self, pay_len):
        self.pay_len = pay_len

    def get_impl_head(self):
        return self.impl_head

    def set_impl_head(self, impl_head):
        self.impl_head = impl_head

    def get_has_crc(self):
        return self.has_crc

    def set_has_crc(self, has_crc):
        self.has_crc = has_crc

    def get_frame_period(self):
        return self.frame_period

    def set_frame_period(self, frame_period):
        self.frame_period = frame_period

    def get_cr(self):
        return self.cr

    def set_cr(self, cr):
        self.cr = cr

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.qtgui_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate_rx)
        self.uhd_usrp_source_0_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_source_0_0.set_center_freq(self.center_freq, 1)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.uhd_usrp_source_0_0.set_bandwidth(self.bw, 0)
        self.uhd_usrp_source_0_0.set_bandwidth(self.bw, 1)

    def get_Att_dB(self):
        return self.Att_dB

    def set_Att_dB(self, Att_dB):
        self.Att_dB = Att_dB




def main(top_block_cls=tx_rx_usrp, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
