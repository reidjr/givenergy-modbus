from pydantic import BaseConfig, create_model

from givenergy_modbus.model.register import IR
from givenergy_modbus.model.register import DataType as DT
from givenergy_modbus.model.register import RegisterDefinition as Def
from givenergy_modbus.model.register import RegisterGetter


class BatteryRegisterGetter(RegisterGetter):
    """Structured format for all battery attributes."""

    REGISTER_LUT = {
        # Input Registers, block 60-119
        'v_cell_01': Def(DT.milli, None, IR(60)),
        'v_cell_02': Def(DT.milli, None, IR(61)),
        'v_cell_03': Def(DT.milli, None, IR(62)),
        'v_cell_04': Def(DT.milli, None, IR(63)),
        'v_cell_05': Def(DT.milli, None, IR(64)),
        'v_cell_06': Def(DT.milli, None, IR(65)),
        'v_cell_07': Def(DT.milli, None, IR(66)),
        'v_cell_08': Def(DT.milli, None, IR(67)),
        'v_cell_09': Def(DT.milli, None, IR(68)),
        'v_cell_10': Def(DT.milli, None, IR(69)),
        'v_cell_11': Def(DT.milli, None, IR(70)),
        'v_cell_12': Def(DT.milli, None, IR(71)),
        'v_cell_13': Def(DT.milli, None, IR(72)),
        'v_cell_14': Def(DT.milli, None, IR(73)),
        'v_cell_15': Def(DT.milli, None, IR(74)),
        'v_cell_16': Def(DT.milli, None, IR(75)),
        'serial_number': Def(DT.string, None, IR(110), IR(111), IR(112), IR(113), IR(114)),
    }


class BatteryConfig(BaseConfig):
    """Pydantic configuration for the Battery class."""

    orm_mode = True
    getter_dict = BatteryRegisterGetter


_Battery = create_model(
    'Battery', __config__=BatteryConfig, **BatteryRegisterGetter.to_fields()
)  # type: ignore[call-overload]


class Battery(_Battery):  # type: ignore[misc,valid-type]
    """Add some utility methods to the base pydantic class."""

    def is_valid(self) -> bool:
        """Try to detect if a battery exists based on its attributes."""
        return self.serial_number not in (
            '',
            '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            '          ',
        )


# class Battery(GivEnergyBaseModel):
#     """Structured format for BMS attributes."""
#
#     temp_cells_1_4: float
#     temp_cells_5_8: float
#     temp_cells_9_12: float
#     temp_cells_13_16: float
#     v_cells_sum: float
#     temp_bms_mosfet: float
#     v_out: float
#     full_capacity: float
#     design_capacity: float
#     remaining_capacity: float
#     status: tuple[int, ...]
#     warning: tuple[int, ...]
#     num_cycles: int
#     num_cells: int
#     bms_firmware_version: int
#     state_of_charge: int
#     design_capacity_2: float
#     temp_max: float
#     temp_min: float
#     e_discharge_total: float
#     e_charge_total: float
#     serial_number: str
#     usb_inserted: bool
#
#     @classmethod
#     def from_registers(cls, rc: RegisterCache) -> 'Battery':
#         """Constructor parsing registers directly."""
#         return Battery(
#             v_cell_01=rc[IR(60)] / 1000,
#             v_cell_02=rc[IR(61)] / 1000,
#             v_cell_03=rc[IR(62)] / 1000,
#             v_cell_04=rc[IR(63)] / 1000,
#             v_cell_05=rc[IR(64)] / 1000,
#             v_cell_06=rc[IR(65)] / 1000,
#             v_cell_07=rc[IR(66)] / 1000,
#             v_cell_08=rc[IR(67)] / 1000,
#             v_cell_09=rc[IR(68)] / 1000,
#             v_cell_10=rc[IR(69)] / 1000,
#             v_cell_11=rc[IR(70)] / 1000,
#             v_cell_12=rc[IR(71)] / 1000,
#             v_cell_13=rc[IR(72)] / 1000,
#             v_cell_14=rc[IR(73)] / 1000,
#             v_cell_15=rc[IR(74)] / 1000,
#             v_cell_16=rc[IR(75)] / 1000,
#             temp_cells_1_4=rc[IR(76)] / 10,
#             temp_cells_5_8=rc[IR(77)] / 10,
#             temp_cells_9_12=rc[IR(78)] / 10,
#             temp_cells_13_16=rc[IR(79)] / 10,
#             v_cells_sum=rc[IR(80)] / 1000,
#             temp_bms_mosfet=rc[IR(81)] / 10,
#             v_out=rc.to_uint32(IR(82), IR(83)) / 1000,
#             full_capacity=rc.to_uint32(IR(84), IR(85)) / 100,
#             design_capacity=rc.to_uint32(IR(86), IR(87)) / 100,
#             remaining_capacity=rc.to_uint32(IR(88), IR(89)) / 100,
#             status=rc.to_duint8(IR(90), IR(91), IR(92), IR(93)),
#             warning=rc.to_duint8(IR(94)),
#             num_cycles=rc[IR(96)],
#             num_cells=rc[IR(97)],
#             bms_firmware_version=rc[IR(98)],
#             state_of_charge=rc[IR(100)],
#             design_capacity_2=rc.to_uint32(IR(101), IR(102)) / 100,
#             temp_max=rc[IR(103)] / 10,
#             temp_min=rc[IR(104)] / 10,
#             e_discharge_total=rc[IR(105)] / 10,
#             e_charge_total=rc[IR(106)] / 10,
#             serial_number=rc.to_string(IR(110), IR(111), IR(112), IR(113), IR(114)),
#             usb_inserted=bool(rc[IR(115)]),
#         )
#
#     def is_valid(self) -> bool:
#         """Try to detect if a battery exists based on its serial number."""
#         return self.serial_number not in (
#             '',
#             '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
#             '          ',
#         )
