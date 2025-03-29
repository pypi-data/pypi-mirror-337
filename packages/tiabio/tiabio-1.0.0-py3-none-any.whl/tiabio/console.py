import serial
import serial.tools.list_ports
import tiabio.keyboard as keyboard
import tiabio.mouse as mouse
import re


def _constants(object):
    constant_style = re.compile("^[A-Z0-9_]+$")
    return [
        attribute
        for attribute in dir(object)
        if not attribute.startswith("__") and constant_style.match(attribute)
    ]


def _value_in_object(value, object):
    consts = _constants(object)
    for const in consts:
        const_value = getattr(object, const)
        if const_value == value:
            return True
    return False


def buttons_list_to_byte(buttons_list: list[int] | None = None) -> int:
    buttons: int = 0
    if buttons_list:
        for button in buttons_list:
            if not _value_in_object(button, mouse.buttons):
                raise ValueError("Use the predefined values in tiabio.mouse.buttons")
            buttons |= 1 << button
    return buttons


console_port_exception = """\
No port matches VID '{vid:04x}', PID '{pid:04x}', and serial number \
'{serial_number}'. If the serial numbers are correct then please ensure that\
the device is connected correctly.\
"""

_prompt: str = "> \x1b[4h"


_VALID_POWER_OUTPUTS = {"none", "dc", "usbpd", "manual-usb"}
_VALID_VOLTAGE_LEVELS = {0, 5, 9, 12, 15, 20}


class ReadTimeoutError(Exception):
    pass


class Console:
    def __init__(self, vid: int, pid: int, serial_number: str):
        console_port_name = None
        for port in serial.tools.list_ports.comports():
            interface_number: str = "3"
            if (
                port.vid == vid
                and port.pid == pid
                and port.serial_number == serial_number
                and port.location
                and port.location.endswith(interface_number)
            ):
                console_port_name = port.device
                break
        if not console_port_name:
            raise FileNotFoundError(
                console_port_exception.format(
                    vid=vid, pid=pid, serial_number=serial_number
                )
            )
        self.serial = serial.Serial(console_port_name, baudrate=115200)

    def close(self):
        self.serial.close()

    def write(self, text: str):
        self.serial.write(text.encode())

    def get_response(self) -> str:
        read: str = self.serial.read_until(_prompt.encode()).decode()
        if not read.endswith(_prompt):
            raise ReadTimeoutError
        lines: list[str] = read.splitlines()
        response_lines: list[str] = lines[1:-1]
        response: str = "\n".join(response_lines)
        return response

    def cancel(self):
        self.write("\x03")

    def hit_enter(self):
        self.write("\r\n")

    def find_input_prompt(self):
        self.serial.reset_input_buffer()
        self.cancel()
        self.get_response()

    def send_cmd(self, cmd: str):
        self.find_input_prompt()
        self.write(cmd)
        self.hit_enter()

    def mouse_cmd(
        self,
        buttons_list: list[int] | None = None,
        x: int = 0,
        y: int = 0,
        wheel: int = 0,
        pan: int = 0,
    ) -> str:
        buttons: int = buttons_list_to_byte(buttons_list)
        args = locals()
        check_args = {key: args[key] for key in ["x", "y", "wheel", "pan"]}
        for key, value in check_args.items():
            if not (value >= -128 and value <= 127):
                raise ValueError(
                    f"Invalid value '{value}', '{key}' should be a value from -128 to 127"
                )
        cmd: str = f"mouse {buttons} {x} {y} {wheel} {pan}"
        self.send_cmd(cmd)
        return self.get_response()

    def keyboard_cmd(
        self, keycodes: list[int] | None = None, modifiers_list: list[int] | None = None
    ):
        if keycodes and len(keycodes):
            if len(keycodes) > 6:
                raise ValueError(
                    "The maximum number of keys that can be pressed at once is 6"
                )
        else:
            keycodes = [keyboard.keycodes.NONE]
        modifiers: int = 0
        if modifiers_list:
            for modifier in modifiers_list:
                if not _value_in_object(modifier, keyboard.modifiers):
                    raise ValueError(
                        "Use the predefined values in tiabio.keyboard.modifiers"
                    )
                modifiers |= 1 << modifier
        cmd = f"keyboard {modifiers}"
        for keycode in keycodes:
            if not _value_in_object(keycode, keyboard.keycodes):
                raise ValueError(
                    "Use the predefined values in tiabio.keyboard.keycodes"
                )
            cmd = f"{cmd} {keycode}"
        self.send_cmd(cmd)

    def help_cmd(self) -> str:
        self.send_cmd("help")
        return self.get_response()

    def hello_cmd(self) -> str:
        self.send_cmd("hello")
        return self.get_response()

    def led_steady_cmd(self):
        self.send_cmd("led steady")

    def led_flash_cmd(self):
        self.send_cmd("led flash")

    def led_rainbow_cmd(self):
        self.send_cmd("led rainbow")

    def eeprom_start_cmd(self) -> str:
        self.send_cmd("eeprom start")
        return self.get_response()

    def eeprom_status_cmd(self) -> str:
        self.send_cmd("eeprom status")
        return self.get_response()

    def eeprom_finish_cmd(self) -> str:
        self.send_cmd("eeprom finish")
        return self.get_response()

    def eeprom_read_cmd(self) -> str:
        self.send_cmd("eeprom read")
        return self.get_response()

    def set_power_output_cmd(self, output: str):
        if output not in _VALID_POWER_OUTPUTS:
            raise ValueError("'output' must be one of: %r" % _VALID_POWER_OUTPUTS)
        self.send_cmd(f"set-power-output {output}")

    def set_dc_voltage_cmd(self, voltage: int):
        if voltage not in _VALID_VOLTAGE_LEVELS:
            raise ValueError("'voltage' must be one of: %r" % _VALID_VOLTAGE_LEVELS)
        self.send_cmd(f"set-dc-voltage {voltage}")

    def set_manual_usb_voltage_cmd(self, voltage: int):
        if voltage not in _VALID_VOLTAGE_LEVELS:
            raise ValueError("'voltage' must be one of: %r" % _VALID_VOLTAGE_LEVELS)
        self.send_cmd(f"set-manual-usb-voltage {voltage}")

    def power_output_cmd(self) -> str:
        self.send_cmd("power-output")
        return self.get_response()

    def dc_voltage_cmd(self) -> str:
        self.send_cmd("dc-voltage")
        return self.get_response()

    def usbpd_voltage_cmd(self) -> str:
        self.send_cmd("usbpd-voltage")
        return self.get_response()

    def manual_usbpd_voltage_cmd(self) -> str:
        self.send_cmd("manual-usbpd-voltage")
        return self.get_response()

    def get_temperature_cmd(self) -> str:
        self.send_cmd("get-temperature")
        return self.get_response()

    def custom_cmd(self, cmd: str) -> str:
        self.send_cmd(cmd)
        return self.get_response()
