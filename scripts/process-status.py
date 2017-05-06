#!/usr/bin/env python3

import psutil
import sys

pid = sys.argv[1]
print(psutil.Process(int(pid)).status())
