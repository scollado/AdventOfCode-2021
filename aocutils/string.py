from io import StringIO


def hex2bin(hex_value: str) -> str:
    """
    Convert a hexadecimal string into its binary string representation
    :param hex_value: Hexadecimal string
    :type hex_value: str

    :return: 0-left-padded binary string
    :rtype: str
    """
    return bin(int(hex_value, 16))[2:].zfill(len(hex_value) * 4)


def hex2bin_stream(hex_value: str) -> StringIO:
    return StringIO(hex2bin(hex_value))


def bin2int(bin_value: str) -> int:
    return int(bin_value, 2)
