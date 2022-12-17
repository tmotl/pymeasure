#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2022 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import (
    truncated_range, truncated_discrete_set,
    strict_discrete_set, strict_range
)


class DM3058(Instrument):
    function = Instrument.control(
        ":FUNC?", ":FUNC:%s",
        """ A string property that controls function of the multimeter,
        which can take the values: :code:'current' (DC), :code:'current ac',
        :code:'voltage' (DC),  :code:'voltage ac', :code:'resistance' (2-wire),
        :code:'resistance 4W' (4-wire), :code:'capacitance', :code:'period', 
        :code:'frequency', and :code:'diode'. """,
        validator=strict_discrete_set,
        values=['voltage',
               'voltage ac',
               'current',
               'current ac',
               'resistance',
               'resistance 4W',
               'capacitance',
               'continuity',
               'diode',
               'frequency',
               'period'],
        map_values=False,
        get_process=lambda v: {
            'DCV': 'voltage',
            'ACV': 'voltage ac',
            'DCI': 'current',
            'ACI': 'current ac',
            '2WR': 'resistance',
            '4WR': 'resistance 4W',
            'CAP': 'capacitance',
            'CONT': 'continuity',
            'DIODE': 'diode',
            'FREQ': 'frequency',
            'PERI': 'period'
        }[v],
        set_process=lambda v: {
            'voltage': 'VOLT:DC',
            'voltage ac': 'VOLT:AC',
            'current': 'CURR:DC',
            'current ac': 'CURR:AC',
            'resistance': 'RES',
            'resistance 4W': 'FRES',
            'capacitance': 'CAP',
            'continuity': 'CONT',
            'diode': 'DIOD',
            'frequency': 'FREQ',
            'period': 'PER'
        }[v]
    )

    ######################### General Measurement #############################

    measurement_available = Instrument.measurement(
        ":MEAS?",
        """Check if new data is available""",
        get_process=lambda v: bool(v.lower())
    )

    measurement_auto_range = Instrument.control(
        None,
        ":MEAS %s",
        """Enable auto range for the measurement""",
        set_process=lambda v: "AUTO" if v else "MANU"
    )

    ######################### Voltage DC #############################

    voltage = Instrument.measurement(
        ":MEAS:VOLT:DC?",
        """Measure DC voltage in V."""
    )

    voltage_range = Instrument.control(
        ":MEAS:VOLT:DC:RANG?",
        ":MEAS:VOLT:DC %s",
        """Set or get the DC voltage range. A suitable range is automatically selected.""",
        validator=truncated_discrete_set,
        values={0.2: 0, 2.0: 1, 20.0: 2, 200.0: 3, 1000.0: 4},
        map_values=True,
    )

    voltage_impedance = Instrument.control(
        ":MEAS:VOLT:DC:IMPE?",
        ":MEAS:VOLT:DC:IMPE %s",
        """Set the input impedance. Can be 10M or 10G. 10G is only possible if range is 200 mV or 2 V.""",
        validator=strict_discrete_set,
        values=["10M", "10G"]
    )

    voltage_filter = Instrument.control(
        ":MEAS:VOLT:DC:FILT?",
        ":MEAS:VOLT:DC:FILT %s",
        """Enable the filter for DC voltage measurement.""",
        set_process=lambda v: "ON" if v else "OFF",
        get_process=lambda v: v == "ON"
    )

    ######################### Voltage AC #############################

    voltage_ac = Instrument.measurement(
        ":MEAS:VOLT:AC?",
        """Measure AC voltage in Vrms""",
    )

    voltage_ac_range = Instrument.control(
        ":MEAS:VOLT:AC:RANG?",
        ":MEAS:VOLT:AC %s",
        """Set or get the DC voltage range. A suitable range is automatically selected.""",
        validator=truncated_discrete_set,
        values={0.2: 0, 2.0: 1, 20.0: 2, 200.0: 3, 750.0: 4},
        map_values=True,
    )

    ######################### Current DC #############################

    current = Instrument.measurement(
        ":MEAS:CURR:DC?",
        """Measure DC current in A."""
    )

    current_range = Instrument.control(
        ":MEAS:CURR:DC:RANG?",
        ":MEAS:CURR:DC %s",
        """Set or get the DC current range. A suitable range is automatically selected.""",
        validator=truncated_discrete_set,
        values={200e-6: 0, 2e-3: 1, 20e-3: 2, 200.0e-3: 3, 2.0: 4, 10.0: 5},
        map_values=True,
    )

    current_filter = Instrument.control(
        ":MEAS:CURR:DC:FILT?",
        ":MEAS:CURR:DC:FILT %s",
        """Enable the filter for DC current measurement.""",
        set_process=lambda v: "ON" if v else "OFF",
        get_process=lambda v: v == "ON"
    )

    ######################### Current AC #############################

    current_ac = Instrument.measurement(
        ":MEAS:CURR:AC?",
        """Measure AC current""",
    )

    current_ac_range = Instrument.control(
        ":MEAS:CURR:AC:RANG?",
        ":MEAS:CURR:AC %s",
        """Set or query the AC voltage range""",
        validator=truncated_discrete_set,
        values={20e-3: 0, 200e-3: 1, 2.0: 2, 10.0: 3},
        map_values=True,
    )

    ######################### Resistance #############################

    resistance = Instrument.measurement(
        ":MEAS:RES?",
        """Read the resistance"""
    )

    resistance_range = Instrument.control(
        ":MEAS:RES:RANG?",
        ":MEAS:RES %s",
        """Set or query the resistance range""",
        validator=truncated_discrete_set,
        values={200.0: 0, 2e3: 1, 20e3: 2, 200e3: 3, 1e6: 4, 10e6: 5, 100e6: 6},
        map_values=True,
    )

    resistance_4w = Instrument.measurement(
        ":MEAS:FRES?",
        """Read the resistance in 4 wire mode"""
    )

    resistance_4w_range = Instrument.control(
        ":MEAS:FRES:RANG?",
        ":MEAS:FRES %s",
        """Set or query the resistance range in 4 wire mode""",
        validator=truncated_discrete_set,
        values={200.0: 0, 2e3: 1, 20e3: 2, 200e3: 3, 1e6: 4, 10e6: 5, 100e6: 6},
        map_values=True,
    )

    ######################### Frequency #############################

    frequency = Instrument.measurement(
        ":MEAS:FREQ?",
        """Read the frequency"""
    )

    frequency_voltage_range = Instrument.control(
        ":MEAS:FREQ:RANG?",
        ":MEAS:FREQ %s",
        """Set or query the voltage range for frequency measurement""",
        validator=truncated_discrete_set,
        values={0.2: 0, 2.0: 1, 20.0: 2, 200.0: 3, 750.0: 4},
        map_values=True,
    )

    ######################### Period #############################

    period = Instrument.measurement(
        ":MEAS:PER?",
        """Read the frequency"""
    )

    period_voltage_range = Instrument.control(
        ":MEAS:PER:RANG?",
        ":MEAS:PER %s",
        """Set or query the voltage range for period measurement""",
        validator=truncated_discrete_set,
        values={0.2: 0, 2.0: 1, 20.0: 2, 200.0: 3, 750.0: 4},
        map_values=True,
    )

    ######################### Continuity #############################

    continuity = Instrument.measurement(
        ":MEAS:CONT?",
        """Measure Continuity"""
    )

    continuity_limit = Instrument.control(
        None,
        ":MEAS:CONT %s",
        """Set limit for continuity measurement from 10 Ohm to 2000 Ohm""",
        validator=strict_range,
        values=[10, 2000]
    )

    ######################### Diode #############################

    diode = Instrument.measurement(
        ":MEAS:DIOD?",
        """Measure diode"""
    )

    ######################### Capacitance #############################

    capacitance = Instrument.measurement(
        ":MEAS:CAP?",
        """Read the capacitance"""
    )

    capacitance_range = Instrument.control(
        ":MEAS:CAP:RANG?",
        ":MEAS:CAP %s",
        """Set or query the capacitance range""",
        validator=truncated_discrete_set,
        values={2e-9: 0, 20e-9: 1, 200e-9: 2, 2e-6: 3, 200e-6: 4, 10e-3: 5},
        map_values=True,
    )

    def __init__(self, adapter, name="Rigol DM3058", **kwargs):
        super().__init__(
            adapter,
            name,
            **kwargs
        )
