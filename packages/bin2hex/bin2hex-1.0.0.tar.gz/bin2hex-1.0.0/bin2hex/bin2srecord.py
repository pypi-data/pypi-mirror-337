# 
# Copyright 2025 Yitao Zhang
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#

from typing import Optional, BinaryIO

srecord_mark = b"S"
srecord_type_data = srecord_mark + b"\x00"
srecord_type_end_of_file = b"\x01"
srecord_type_extended_segment_address = b"\x02"
srecord_type_start_segment_address = b"\x03"
srecord_type_extended_linear_address = b"\x04"
srecord_type_start_linear_address = b"\x05"
srecord_max_data_bytes = 255
srecord_offset_bits = 16

def __generate_len__(data:bytes) -> bytes:
    # Length = Address + Data + Checksum
    return (len(data) & 0xFFFF + 1).to_bytes(2, byteorder="big")

def __generate_checksum__(data:bytes) -> bytes:
    # Checksum = Length + Address + Data
    return (sum(data) & 0xFF).to_bytes(1, byteorder="big")

def __generate_record__(record_type:bytes, address:int, data:bytes) -> str:
    # Fill record mark
    record_address_to_data = address.to_bytes(2, byteorder="big") + data
    record_len_to_data = __generate_len__(record_address_to_data) + record_address_to_data
    return record_type.decode("ascii") + (record_len_to_data + __generate_checksum__(record_len_to_data)).hex().upper()

def generate_data_record(load_offset:int, data:bytes) -> str:
    return __generate_record__(record_type_data, load_offset, data)

def generate_end_of_file_record() -> str:
    return __generate_record__(record_type_end_of_file, 0, b"")

def generate_extended_segment_address_record(upper_segment_base_address:bytes) -> str:
    return __generate_record__(record_type_extended_segment_address, 0, upper_segment_base_address)

def generate_start_segment_address_record(segment_address:bytes) -> str:
    return __generate_record__(record_type_start_segment_address, 0, segment_address)

def generate_extended_linear_address_record(upper_linear_base_address:bytes) -> str:
    return __generate_record__(record_type_extended_linear_address, 0, upper_linear_base_address)

def generate_start_linear_address_record(linear_address:bytes) -> str:
    return __generate_record__(record_type_start_linear_address, 0, linear_address)

def bin_to_ihex(input_file: Optional[BinaryIO], output_file: Optional[BinaryIO], start_address:int = 0, align_width:int = 16, start_entry:int = None) -> bool:
    if align_width > record_max_data_bytes:
        print(f"Error: The alignment is too large. The maximum alignment is {record_max_data_bytes}")
        return False

    address = start_address
    while True:
        if address % (1 << record_offset_bits) == 0 or address == start_address:
            # Generate and write extended linear address record
            upper_linear_base_address = (address >> record_offset_bits).to_bytes(2, byteorder="big")
            output_file.write(generate_extended_linear_address_record(upper_linear_base_address) + '\n')

        # Read data
        data = input_file.read(align_width)
        # Break if no more data(the file ending is reached)
        if not data:
            break
        # Generate and write the data record
        output_file.write(generate_data_record(address & (1 << record_offset_bits - 1), data) + '\n')
        # Alignment control
        address = address + align_width

    if start_entry is not None:
        output_file.write(generate_start_linear_address_record(start_entry) + '\n')

    return True

bin2ihex_dict = {
    "ihex": {
        "function": bin_to_ihex,
        "description": [
            "Convert to the Intel hexadecimal format file",
            "The option \"address\" is accepted as optional. Default is 0x0",
            "The option \"alignment\" is accepted as optional. Default is 16 which means 16 bytes per line. Must be smaller than 256",
        ],
    },
}