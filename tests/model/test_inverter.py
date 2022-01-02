import datetime

from givenergy_modbus.model.inverter import Inverter

# fmt: off
INPUT_REGISTERS = [
    0, 14, 10, 70, 0, 2367, 0, 1832, 0, 0, 0, 0, 159, 4990, 0, 12, 4790, 4, 0, 5, 0, 0, 6, 0, 0, 0, 209, 0, 946, 0,
    65194, 0, 0, 3653, 0, 85, 84, 84, 30, 0, 0, 222, 342, 680, 81, 0, 930, 0, 213, 1, 4991, 0, 0, 2356, 4986, 223, 170,
    0, 292, 4, 3117, 3124, 3129, 3129, 3125, 3130, 3122, 3116, 3111, 3105, 3119, 3134, 3146, 3116, 3135, 3119, 175, 167,
    171, 161, 49970, 172, 0, 50029, 0, 19097, 0, 16000, 0, 1804, 0, 1552, 256, 0, 0, 0, 12, 16, 3005, 0, 9, 0, 16000,
    174, 167, 0, 0, 0, 0, 0, 16967, 12594, 13108, 18229, 13879, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 906, 926,
]
HOLDING_REGISTERS = [
    8193, 3, 2098, 513, 0, 50000, 3600, 1, 16967, 12594, 13108, 18229, 13879, 21313, 12594, 13108, 18229, 13879, 3005,
    449, 1, 449, 2, 0, 32768, 30235, 6000, 1, 0, 0, 17, 0, 4, 7, 140, 22, 1, 1, 23, 57, 19, 1, 2, 0, 0, 0, 101, 1, 0, 0,
    100, 0, 0, 1, 1, 160, 0, 0, 1, 0, 1500, 30, 30, 1840, 2740, 4700, 5198, 126, 27, 24, 28, 1840, 2620, 4745, 5200,
    126, 52, 1, 28, 1755, 2837, 4700, 5200, 2740, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 430, 1, 4320, 5850, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 6, 1, 4, 50, 50, 0, 4, 0, 100, 0, 0, 0, 0,
]
# fmt: on


def test_inverter():
    """Ensure we can instantiate an Inverter with register banks and derive correct attributes from it."""
    i = Inverter(holding_registers=HOLDING_REGISTERS, input_registers=INPUT_REGISTERS)
    assert i.holding_registers == HOLDING_REGISTERS
    assert i.input_registers == INPUT_REGISTERS

    assert i.serial_number == 'SA1234G567'
    assert i.model == 'Hybrid'
    assert i.battery_serial_number == 'BG1234G567'
    assert i.battery_firmware_version == 3005
    assert i.dsp_firmware_version == 449
    assert i.arm_firmware_version == 449
    assert i.winter_mode
    assert i.system_time == datetime.datetime(2022, 1, 1, 23, 57, 19)

    # time slots are BCD-encoded: 30 == 00:30, 430 == 04:30
    assert i.charge_slot_1_start == 30
    assert i.charge_slot_1_end == 430
    assert i.charge_slot_1 == (datetime.time(0, 30), datetime.time(4, 30))
    assert i.charge_slot_2_start == 0
    assert i.charge_slot_2_end == 4
    assert i.charge_slot_2 == (datetime.time(0, 0), datetime.time(0, 4))
    assert i.discharge_slot_1_start == 0
    assert i.discharge_slot_1_end == 0
    assert i.discharge_slot_1 == (datetime.time(0, 0), datetime.time(0, 0))
    assert i.discharge_slot_2_start == 0
    assert i.discharge_slot_2_end == 0
    assert i.discharge_slot_2 == (datetime.time(0, 0), datetime.time(0, 0))

    assert i.v_pv1 == 1.4000000000000001
    assert i.v_pv2 == 1.0
    assert i.p_bus_inside_voltage == 7.0
    assert i.n_bus_inside_voltage == 0.0
    assert i.v_single_phase_grid == 236.70000000000002

    assert i.battery_throughput_h == 0
    assert i.battery_throughput_l == 183.20000000000002
    assert i.battery_throughput == 183.20000000000002

    assert i.e_pv1_day == 0.4
    assert i.e_pv2_day == 0.5
    assert i.e_grid_out_total == 0.6000000000000001

    assert i.battery_percent == 4
    assert i.e_battery_discharge_total == 90.60000000000001
    assert i.e_battery_charge_total == 92.60000000000001