import re


def is_valid_serial(serial: str) -> bool:
    """
    Check if the serial matches the asset number tag pattern.
    """
    serial_pattern = re.compile("^[0-9]{6}$")
    match = serial_pattern.match(serial)
    if match is None:
        return False
    return True


def is_valid_hid_serial(serial: str) -> bool:
    """
    Check if the serial matches the serial pattern given to the Human Interface
    Device (HID) USB port on the TIAB IO board.
    """
    serial_pattern = re.compile("^[0-9A-F]{16}$")
    match = serial_pattern.match(serial)
    if match is None:
        return False
    return True


def is_mpsse_channel(channel: str) -> bool:
    """
    Check if the channel provided is an MPSSE channel
    """
    mpsse_channel_pattern = re.compile("^[aAbB]{1}$")
    match = mpsse_channel_pattern.match(channel)
    if match is None:
        return False
    return True


def channel_letter_to_number(channel: str) -> int:
    letter = channel.lower()
    match letter:
        case "a":
            return 1
        case "b":
            return 2
        case "c":
            return 3
        case "d":
            return 4
    raise ValueError("Invalid channel letter provided")


def set_bit(byte: int, bit: int):
    return byte | (1 << bit)


def clear_bit(byte: int, bit: int):
    return byte & ~(1 << bit)


def check_bit(byte: int, bit: int) -> bool:
    return bool(byte & (1 << bit))


def construct_ftdi_url(vid: int, pid: int, serial: str, channel: int) -> str:
    return f"ftdi://0x{vid:04x}:0x{pid:04x}:{serial}/{channel}"
