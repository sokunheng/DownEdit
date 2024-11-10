import os
import platform
import psutil

from .singleton import Singleton

class SystemInfo(metaclass=Singleton):
    """
    This class provides methods to retrieve system information like CPU, OS, RAM, GPU, and username.
    """
    def __init__(self):
        self._cpu_info = None
        self._gpu_info = None

        if platform.system() == "Windows":
            import wmi
            self.wmi_obj = wmi.WMI()
        else:
            self.wmi_obj = None

    def get_cpu_info(self):
        if not self._cpu_info:
            if self.wmi_obj:
                cpu_info = self.wmi_obj.Win32_Processor()[0]
                cpu_name = cpu_info.Name
            else:
                cpu_name = "Unknown CPU"
            cpu_cores = os.cpu_count()
            self._cpu_info = f"{cpu_name} ({cpu_cores} cores)"
        return self._cpu_info

    def get_os_info(self):
        pc_os = platform.system() + " " + platform.release() + f" ({platform.architecture()[0]})"
        return pc_os

    def get_user_name(self):
        return platform.node()

    def get_ram_info(self):
        pc_ram = psutil.virtual_memory().total / (1024**3)
        return pc_ram

    def get_gpu_info(self):
        if not self._gpu_info and self.wmi_obj:
            gpu_info = self.wmi_obj.Win32_VideoController()[0]
            pc_gpu = gpu_info.Description if gpu_info.Description else "No GPU found"
            self._gpu_info = pc_gpu
        elif not self._gpu_info:
            self._gpu_info = "No GPU found"
        return self._gpu_info

    def get_pc_info(self):
        return {
            "OS": self.get_os_info(),
            "USER": self.get_user_name(),
            "CPU": self.get_cpu_info(),
            "RAM": self.get_ram_info(),
            "GPU": self.get_gpu_info(),
        }

system_info = SystemInfo()
pc_info = system_info.get_pc_info()
