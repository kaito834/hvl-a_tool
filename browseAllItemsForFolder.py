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

def main(id):
    """
    Retrive all items on specified folder from HVL-A2.0
    Output item ID/title/date/profile/url as CSV format

    Arguments:
        id: Item ID(string) Ex. FS-4
    Return:
        None
    """
    hvla = myhvlalib.myHvlA()
    # 3rd argument, '0', requires all items by browse API
    jsonDic = hvla.browse(id, '0', '0')

    results = jsonDic['results']
    result_keys = [
        'id', 'title', 'date', 'profile', 'url'
    ]
    print('no,' + ','.join(result_keys))
    for i, result in enumerate(results, 1):
        output = str(i)
        for result_key in result_keys:
            output = output + ',' + result[result_key]
        print(output)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: {0} _ID_".format(sys.argv[0]))
