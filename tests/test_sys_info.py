import os
import sys

import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from downedit.utils import pc_info

class TestSystemInfo(unittest.TestCase):
    def setUp(self):
        self.sys_info1 = pc_info
        self.sys_info2 = pc_info

    def test_singleton_instance(self):
        print("ID of sys_info1:", id(self.sys_info1))
        print("ID of sys_info2:", id(self.sys_info2))
        self.assertIs(self.sys_info1, self.sys_info2, "Both instances are not the same")

    def test_multiple_calls(self):
        print("ID of sys_info1:", id(self.sys_info1))
        print("ID of sys_info2:", id(self.sys_info2))
        print("CPU info for sys_info1:", self.sys_info1["CPU"])
        print("CPU info for sys_info2:", self.sys_info2["CPU"])
        print("RAM info for sys_info1:", self.sys_info1["RAM"])
        print("RAM info for sys_info2:", self.sys_info2["RAM"])
        print("GPU info for sys_info1:", self.sys_info1["GPU"])
        print("GPU info for sys_info2:", self.sys_info2["GPU"])

if __name__ == '__main__':
    unittest.main()