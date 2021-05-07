#!/usr/bin/env python3

import sys
import hashlib
import binascii

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print('Usage: %s "My Game.sav" "save.sram" 32' % sys.argv[0])

    common_file = open(sys.argv[1], 'rb')

    common_sram_data = common_file.read()

    common_sram_len = len(common_sram_data)

    classic_sram_len = int(sys.argv[3])*1024

    # Sanity check
    assert (common_sram_len > 0)
    assert (common_sram_len <= classic_sram_len)
    
    # pad the sram with zeroes
    classic_sram_data = common_sram_data + (b'\x00' * (classic_sram_len - common_sram_len))

    calculated_sha1 = binascii.hexlify(hashlib.sha1(classic_sram_data).digest())

    classic_file = open(sys.argv[2], 'wb')

    classic_file.write(calculated_sha1)
    classic_file.write(classic_sram_data)

    print("Done!")
