import os
import wmi
import platform
import psutil

from .singleton import Singleton

class SystemInfo(metaclass=Singleton):
    """
    This class provides methods to retrieve system information like CPU, OS, RAM, GPU, and username.
    """
    
    def get_cpu_info(self):
        cpu_info = wmi.WMI().Win32_Processor()[0]
        cpu_name = cpu_info.Name
        cpu_cores = os.cpu_count()
        return f"{cpu_name} ({cpu_cores} cores)"

    def get_os_info(self):
        pc_os = platform.system() + " " + platform.release() + f" ({platform.architecture()[0]})"
        return pc_os

    def get_user_name(self):
        return platform.node()

    def get_ram_info(self):
        pc_ram = psutil.virtual_memory().total / (1024**3)
        return pc_ram

    def get_gpu_info(self):
        gpu_info = wmi.WMI().Win32_VideoController()[0]
        pc_gpu = gpu_info.Description if gpu_info.Description else "No GPU found"
        return pc_gpu

    def get_pc_info(self):
        return {
            "OS": self.get_os_info(),
            "USER": self.get_user_name(),
            "CPU": self.get_cpu_info(),
            "RAM": self.get_ram_info(),
            "GPU": self.get_gpu_info(),
        }