#!/usr/bin/env python3

import sys
import hashlib
import binascii

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print('Usage: %s "save.sram" "My Game.sav" 8' % sys.argv[0])

    classic_file = open(sys.argv[1], 'rb')

    classic_all_data = classic_file.read()

    classic_all_data_len = len(classic_all_data)

    sha1_len = 0x28

    # Sanity check: the file length should be length of SHA-1 hash + size of sram. size of sram is probably always a multiple of 1024?
    assert (((classic_all_data_len - sha1_len) % 1024) == 0)
    assert (classic_all_data_len > sha1_len)
    
    classic_stored_sha1 = binascii.unhexlify(classic_all_data[0:sha1_len])

    classic_sram_data = classic_all_data[sha1_len:classic_all_data_len]
    classic_sram_data_len = len(classic_sram_data)

    classic_calculated_sha1 = hashlib.sha1(classic_sram_data).digest()

    # Sanity check: does the stored SHA1 match the actual SHA1 of the save data?
    assert classic_calculated_sha1 == classic_stored_sha1


    common_sram_data_len = int(sys.argv[3])*1024

    assert classic_sram_data_len >= common_sram_data_len

    common_sram = open(sys.argv[2], 'wb')

    # We slice away what we assume is padding. We could assert this maybe
    common_sram.write(classic_sram_data[0:common_sram_data_len])

    print("Done!")
