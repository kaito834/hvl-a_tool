#!/usr/bin/env python
"""
## Requirement
- myHvlAlib library
## Tested Environments
- Python 3.4.3 on Windows 8.1
- HVL-A2.0 (Firmware 2.03)
  - http://www.iodata.jp/product/hdd/rokuga/hvl-a/

Copyright (c) 2016 @kaito834

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""

__author__  = '@kaito834'
__version__ = '0.1'

import myhvlalib
import sys
import time

def main(itemfile):
    """
    Delete specified items on HVL-A2.0 by myHvlAlib library
    Read the items from the file.

    Arguments:
        itemfile: The path of file that contains item IDs(string)
    Return:
        None
    """
    hvla = myhvlalib.myHvlA()

    with open(itemfile, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            line = line.rstrip("\r\n")
            # Ref. https://docs.python.org/3/library/functions.html#print
            print("({0:>3}/{1:>3}) Deleting {2} ... ".format(i, len(lines), line), end='', flush=True)

            removeResultCode = hvla.remove(line)
            if removeResultCode == 0:
                print('SUCCESS')
            elif removeResultCode == 1:
                print('UNKNOWN (timeout)')
            elif removeResultCode == 2:
                print('FAILED (HTTPError)')
            elif removeResultCode == 3:
                print('FAILED (URLError)')

            print('Sleeping in 10 seconds ... ', end='', flush=True)
            time.sleep(10)
            print('Done')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: {0} _filename_".format(sys.argv[0]))
