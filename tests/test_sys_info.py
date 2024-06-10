import unittest
from downedit.utils import SystemInfo

class TestSystemInfo(unittest.TestCase):
    def setUp(self):
        self.sys_info1 = SystemInfo()
        self.sys_info2 = SystemInfo()

    def test_singleton_instance(self):
        print("ID of sys_info1:", id(self.sys_info1))
        print("ID of sys_info2:", id(self.sys_info2))
        self.assertIs(self.sys_info1, self.sys_info2, "Both instances are not the same")

    def test_multiple_calls(self):
        print("ID of sys_info1:", id(self.sys_info1))
        print("ID of sys_info2:", id(self.sys_info2))
        print("CPU info for sys_info1:", self.sys_info1.get_cpu_info())
        print("CPU info for sys_info2:", self.sys_info2.get_cpu_info())
        print("RAM info for sys_info1:", self.sys_info1.get_ram_info())
        print("RAM info for sys_info2:", self.sys_info2.get_ram_info())
        print("GPU info for sys_info1:", self.sys_info1.get_gpu_info())
        print("GPU info for sys_info2:", self.sys_info2.get_gpu_info())

if __name__ == '__main__':
    unittest.main()