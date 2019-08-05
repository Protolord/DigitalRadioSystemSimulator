class RadioConfig():

    def __init__(self):
        self.tx_carrier_freq = 1000    # Unit: Hz
        self.tx_modulation = 'BPSK'    # Values: BPSK, QPSK, 16QAM
        self.tx_symbol_duration = 0.1  # Unit: second
        self.tx_timestart = 0          # Unit: second
        self.tx_timestop = 1           # Unit: second
        self.rx_carrier_freq = 1000    # Unit: Hz
        self.rx_modulation = 'BPSK'    # Values: BPSK, QPSK, 16QAM
        self.rx_symbol_duration = 0.1  # Unit: second
        self.rx_timestart = 0          # Unit: second
        self.rx_timestop = 1           # Unit: second
        self.radio_index = 0
