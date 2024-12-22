import json
import random
import hashlib

__all__ = ["Fingerprint"]

class Fingerprint:
    """
    A utility class for generating browser fingerprints.
    """

    RESOLUTIONS = [
        (1920, 1080), (1366, 768), (1440, 900), (1536, 864),
        (1280, 720), (1600, 900), (2560, 1440)
    ]
    LANGUAGES = [
        "en-US,en;q=0.9",
        "en-GB,en;q=0.8",
        "fr-FR,fr;q=0.9",
        "es-ES,es;q=0.8"
    ]
    TIMEZONES = [
        "UTC-12:00", "UTC-11:00", "UTC-10:00", "UTC-09:00", "UTC-08:00",
        "UTC-07:00", "UTC-06:00", "UTC-05:00", "UTC-04:00", "UTC-03:00",
        "UTC-02:00", "UTC-01:00", "UTC+00:00", "UTC+01:00", "UTC+02:00",
        "UTC+03:00", "UTC+04:00", "UTC+05:00", "UTC+06:00", "UTC+07:00",
        "UTC+08:00", "UTC+09:00", "UTC+10:00", "UTC+11:00", "UTC+12:00"
    ]

    @staticmethod
    def generate_canvas_fingerprint() -> str:
        random_data = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=100))
        return hashlib.sha256(random_data.encode()).hexdigest()

    @staticmethod
    def generate_webgl_fingerprint() -> str:
        random_data = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=100))
        return hashlib.md5(random_data.encode()).hexdigest()

    @staticmethod
    def generate_audio_fingerprint() -> str:
        random_data = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=100))
        return hashlib.sha1(random_data.encode()).hexdigest()

    @staticmethod
    def generate_fonts() -> list:
        available_fonts = [
            "Arial", "Verdana", "Helvetica", "Times New Roman", "Courier New",
            "Georgia", "Palatino", "Garamond", "Bookman", "Comic Sans MS",
            "Trebuchet MS", "Arial Black", "Impact"
        ]
        num_fonts = random.randint(5, len(available_fonts))
        return random.sample(available_fonts, num_fonts)

    @staticmethod
    def generate_plugins() -> list:
        available_plugins = [
            "Chrome PDF Viewer", "Shockwave Flash", "Widevine Content Decryption Module",
            "Native Client", "QuickTime", "Silverlight", "Java", "Unity Web Player"
        ]
        num_plugins = random.randint(0, len(available_plugins))
        return random.sample(available_plugins, num_plugins)

    @staticmethod
    def generate_cpu_class() -> str:
        cpu_classes = ["x86", "x64", "ARM", "ARM64"]
        return random.choice(cpu_classes)

    @staticmethod
    def generate_screen_orientation(width: int, height: int) -> str:
        if width > height:
            return "landscape-primary"
        else:
            return "portrait-primary"

    @classmethod
    def browser_fingerprint(cls, browser_type: str = "Chrome", user_agent: str  = None) -> dict:
        platform = {}
        platform["Chrome"] = "Win32"
        platform["Edge"] = "Win32"
        platform["Firefox"] = "Win32"
        platform["Safari"] = "MacIntel"

        inner_width = random.randint(1024, 1920)
        inner_height = random.randint(768, 1080)
        outer_width = inner_width + random.randint(24, 32)
        outer_height = inner_height + random.randint(75, 90)
        screen_x = 0
        screen_y = random.choice([0, 30])
        avail_width = random.randint(1280, 1920)
        avail_height = random.randint(800, 1080)

        fingerprint = {}
        fingerprint["language"] = random.choice(cls.LANGUAGES)
        fingerprint["colorDepth"] = 24
        fingerprint["pixelDepth"] = 24
        fingerprint["screenResolution"] = f"{inner_width}x{inner_height}"
        fingerprint["availableScreenResolution"] = f"{avail_width}x{avail_height}"
        fingerprint["timezone"] = random.choice(cls.TIMEZONES)
        fingerprint["platform"] = platform.get(browser_type, "Win32")
        fingerprint["userAgent"] = user_agent or f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        fingerprint["doNotTrack"] = random.choice(["1", "0"])
        fingerprint["canvasFingerprint"] = cls.generate_canvas_fingerprint()
        fingerprint["webGLFingerprint"] = cls.generate_webgl_fingerprint()
        fingerprint["audioFingerprint"] = cls.generate_audio_fingerprint()
        fingerprint["fonts"] = cls.generate_fonts()
        fingerprint["plugins"] = cls.generate_plugins()
        fingerprint["hardwareConcurrency"] = random.randint(2, 16)
        fingerprint["deviceMemory"] = random.choice([2, 4, 8, 16, 32])
        fingerprint["cpuClass"] = cls.generate_cpu_class()
        fingerprint["navigatorPluginsLength"] = random.randint(0, 10)
        fingerprint["screenOrientation"] = cls.generate_screen_orientation(inner_width, inner_height)
        fingerprint["availHeight"] = avail_height
        fingerprint["availWidth"] = avail_width
        fingerprint["colorDepth"] = 24
        fingerprint["pixelDepth"] = 24
        fingerprint["height"] = inner_height
        fingerprint["width"] = inner_width
        fingerprint["availTop"] = screen_y
        fingerprint["availLeft"] = screen_x
        fingerprint["outerWidth"] = outer_width
        fingerprint["outerHeight"] = outer_height
        return fingerprint

if __name__ == "__main__":
    fingerprint = Fingerprint.browser_fingerprint()
    print(json.dumps(fingerprint, indent=4))