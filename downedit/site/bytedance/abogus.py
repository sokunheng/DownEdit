from random import choice, randint, random
from re import compile
from time import time
from urllib.parse import quote, urlencode

from downedit.site.bytedance.hash import Hash


class ABogus:
    """
    Generates obfuscated parameters for ByteDance services.
    """

    _PARAMETER_REGEX = compile(r'%([0-9A-F]{2})')
    _DEFAULT_ARGUMENTS = [0, 1, 14]
    _USER_AGENT_KEY = "\u0000\u0001\u000e"
    _DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    _END_STRING = "cus"
    _DEFAULT_VERSION = [1, 0, 1, 5]
    _DEFAULT_BROWSER_INFO = "1536|742|1536|864|0|0|0|0|1536|864|1536|864|1536|742|24|24|Win32"
    _DEFAULT_REGISTERS = [
        1937774191,
        1226093241,
        388252375,
        3666478592,
        2842636476,
        372324522,
        3817729613,
        2969243214,
    ]
    _STRING_TABLES = {
        "s0": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
        "s1": "Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=",
        "s2": "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=",
        "s3": "ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe",
        "s4": "Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe",
    }

    def __init__(
        self,
        user_agent: str = _DEFAULT_USER_AGENT,
        platform: str = None,
    ):
        self._chunk = []
        self._size = 0
        self._registers = self._DEFAULT_REGISTERS[:]
        self._user_agent_code = self._generate_user_agent_code(user_agent)
        self._browser_info = self._generate_browser_info(platform) if platform else self._DEFAULT_BROWSER_INFO
        self._browser_info_length = len(self._browser_info)
        self._browser_code = self._get_char_codes(self._browser_info)

    @classmethod
    def _generate_random_list_1(cls, random_num=None, a=170, b=85, c=45) -> list:
        return cls._generate_random_list(random_num, a, b, 1, 2, 5, c & a)

    @classmethod
    def _generate_random_list_2(cls, random_num=None, a=170, b=85) -> list:
        return cls._generate_random_list(random_num, a, b, 1, 0, 0, 0)

    @classmethod
    def _generate_random_list_3(cls, random_num=None, a=170, b=85) -> list:
        return cls._generate_random_list(random_num, a, b, 1, 0, 5, 0)

    @staticmethod
    def _generate_random_list(
        a: float = None,
        b: int = 170,
        c: int = 85,
        d: int = 0,
        e: int = 0,
        f: int = 0,
        g: int = 0,
    ) -> list:
        r = a or (random() * 10000)
        v = [r, int(r) & 255, int(r) >> 8]
        v.append((int(v[1]) & b) | d)
        v.append((int(v[1]) & c) | e)
        v.append((int(v[2]) & b) | f)
        v.append((int(v[2]) & c) | g)
        return v[-4:]

    @staticmethod
    def _get_string_from_char_codes(*args) -> str:
        return "".join(chr(code) for code in args)

    @classmethod
    def _generate_string_1(cls, random_num_1=None, random_num_2=None, random_num_3=None) -> str:
        return (
            cls._get_string_from_char_codes(*cls._generate_random_list_1(random_num_1))
            + cls._get_string_from_char_codes(*cls._generate_random_list_2(random_num_2))
            + cls._get_string_from_char_codes(*cls._generate_random_list_3(random_num_3))
        )

    def _generate_string_2(self, url_params: str, method: str = "GET", start_time: int = 0, end_time: int = 0) -> str:
        intermediate_list = self._generate_string_2_list(url_params, method, start_time, end_time)
        end_check_value = self._calculate_end_check_number(intermediate_list)
        intermediate_list.extend(self._browser_code)
        intermediate_list.append(end_check_value)
        return self._rc4_encrypt(self._get_string_from_char_codes(*intermediate_list), "y")

    def _generate_user_agent_code(self, user_agent: str) -> list[int]:
        encrypted_ua = self._rc4_encrypt(user_agent, self._USER_AGENT_KEY)
        processed_ua = self._generate_result(encrypted_ua, "s3")
        return self._sum_array(processed_ua)


    def _generate_string_2_list(self, url_params: str, method: str = "GET", start_time: int = 0, end_time: int = 0) -> list:
        start_time = start_time or int(time() * 1000)
        end_time = end_time or (start_time + randint(4, 8))
        params_array = self._generate_params_code(url_params)
        method_array = self._generate_method_code(method)
        return self._generate_list_4(
            (end_time >> 24) & 255,
            params_array[21],
            self._user_agent_code[23],
            (end_time >> 16) & 255,
            params_array[22],
            self._user_agent_code[24],
            (end_time >> 8) & 255,
            (end_time >> 0) & 255,
            (start_time >> 24) & 255,
            (start_time >> 16) & 255,
            (start_time >> 8) & 255,
            (start_time >> 0) & 255,
            method_array[21],
            method_array[22],
            int(end_time / 256 / 256 / 256 / 256) >> 0,
            int(start_time / 256 / 256 / 256 / 256) >> 0,
            self._browser_info_length,
        )

    @staticmethod
    def _convert_registers_to_array(registers: list[int]) -> list[int]:
        output_array = [0] * 32
        for i in range(8):
            c = registers[i]
            output_array[4 * i + 3] = c & 255
            c >>= 8
            output_array[4 * i + 2] = c & 255
            c >>= 8
            output_array[4 * i + 1] = c & 255
            c >>= 8
            output_array[4 * i] = c & 255
        return output_array

    def _compress_data(self, data_block: list[int]):
        f_array = self._generate_f_array(data_block)
        registers = self._registers[:]
        for o in range(64):
            c = self._left_rotate(registers[0], 12) + registers[4] + self._left_rotate(self._pseudo_random_value(o), o)
            c &= 0xFFFFFFFF
            c = self._left_rotate(c, 7)
            s = (c ^ self._left_rotate(registers[0], 12)) & 0xFFFFFFFF

            u = self._helper_function_h(o, registers[0], registers[1], registers[2])
            u = (u + registers[3] + s + f_array[o + 68]) & 0xFFFFFFFF

            b = self._helper_function_v(o, registers[4], registers[5], registers[6])
            b = (b + registers[7] + c + f_array[o]) & 0xFFFFFFFF

            registers[3] = registers[2]
            registers[2] = self._left_rotate(registers[1], 9)
            registers[1] = registers[0]
            registers[0] = u

            registers[7] = registers[6]
            registers[6] = self._left_rotate(registers[5], 19)
            registers[5] = registers[4]
            registers[4] = (b ^ self._left_rotate(b, 9) ^ self._left_rotate(b, 17)) & 0xFFFFFFFF

        for l in range(8):
            self._registers[l] = (self._registers[l] ^ registers[l]) & 0xFFFFFFFF

    @classmethod
    def _generate_f_array(cls, e: list[int]) -> list[int]:
        r = [0] * 132
        for t in range(16):
            r[t] = (e[4 * t] << 24) | (e[4 * t + 1] << 16) | (e[4 * t + 2] << 8) | e[4 * t + 3]
            r[t] &= 0xFFFFFFFF

        for n in range(16, 68):
            a = r[n - 16] ^ r[n - 9] ^ cls._left_rotate(r[n - 3], 15)
            a ^= cls._left_rotate(a, 15) ^ cls._left_rotate(a, 23)
            r[n] = (a ^ cls._left_rotate(r[n - 13], 7) ^ r[n - 6]) & 0xFFFFFFFF

        for n in range(68, 132):
            r[n] = r[n - 68] ^ r[n - 64]

        return r

    @staticmethod
    def _pad_array(arr: list, length: int = 60) -> list:
        while len(arr) < length:
            arr.append(0)
        return arr

    def _fill_chunk(self, length: int = 60):
        size = 8 * self._size
        self._chunk.append(128)
        self._chunk = self._pad_array(self._chunk, length)
        for i in range(4):
            self._chunk.append((size >> (8 * (3 - i))) & 255)

    @staticmethod
    def _generate_list_4(
        a: int,
        b: int,
        c: int,
        d: int,
        e: int,
        f: int,
        g: int,
        h: int,
        i: int,
        j: int,
        k: int,
        m: int,
        n: int,
        o: int,
        p: int,
        q: int,
        r: int,
    ) -> list:
        return [
            44,
            a,
            0,
            0,
            0,
            0,
            24,
            b,
            n,
            0,
            c,
            d,
            0,
            0,
            0,
            1,
            0,
            239,
            e,
            o,
            f,
            g,
            0,
            0,
            0,
            0,
            h,
            0,
            0,
            14,
            i,
            j,
            0,
            k,
            m,
            3,
            p,
            1,
            q,
            1,
            r,
            0,
            0,
            0,
        ]

    @staticmethod
    def _calculate_end_check_number(data_list: list) -> int:
        result = 0
        for value in data_list:
            result ^= value
        return result

    @classmethod
    def _decode_url_string(cls, url_string: str) -> str:
        return cls._PARAMETER_REGEX.sub(cls._replace_url_encoded_character, url_string)

    @staticmethod
    def _replace_url_encoded_character(match: re.Match) -> str:
        return chr(int(match.group(1), 16))

    @staticmethod
    def _left_rotate(value: int, shift: int) -> int:
        return ((value << shift) & 0xFFFFFFFF) | (value >> (32 - shift))

    @staticmethod
    def _pseudo_random_value(value: int) -> int:
        return 2043430169 if 0 <= value < 16 else 2055708042

    @staticmethod
    def _helper_function_h(e: int, r: int, t: int, n: int) -> int:
        if 0 <= e < 16:
            return (r ^ t ^ n) & 0xFFFFFFFF
        elif 16 <= e < 64:
            return (r & t | r & n | t & n) & 0xFFFFFFFF
        raise ValueError("e must be between 0 and 63")

    @staticmethod
    def _helper_function_v(e: int, r: int, t: int, n: int) -> int:
        if 0 <= e < 16:
            return (r ^ t ^ n) & 0xFFFFFFFF
        elif 16 <= e < 64:
            return (r & t | (~r) & n) & 0xFFFFFFFF
        raise ValueError("e must be between 0 and 63")

    @staticmethod
    def _get_char_codes(input_string: str) -> list[int]:
        return [ord(char) for char in input_string]

    @staticmethod
    def _split_array(arr: list, chunk_size: int = 64) -> list[list]:
        return [arr[i : i + chunk_size] for i in range(0, len(arr), chunk_size)]

    def _write_data(self, data: list[int]):
        self._size = len(data)
        if len(data) <= 64:
            self._chunk = data
        else:
            chunks = self._split_array(data, 64)
            for chunk in chunks[:-1]:
                self._compress_data(chunk)
            self._chunk = chunks[-1]

    def _reset_state(self):
        self._chunk = []
        self._size = 0
        self._registers = self._DEFAULT_REGISTERS[:]

    def _sum_array(self, data: str, length: int = 60) -> list[int]:
        self._reset_state()
        self._write_data(self._get_char_codes(data))
        self._fill_chunk(length)
        self._compress_data(self._chunk)
        return self._convert_registers_to_array(self._registers)

    @classmethod
    def _generate_result_unit(cls, value: int, table_name: str) -> str:
        result = ""
        for i, j in zip(range(18, -1, -6), (16515072, 258048, 4032, 63)):
            result += cls._STRING_TABLES[table_name][(value & j) >> i]
        return result

    @classmethod
    def _generate_result_end(cls, input_string: str, table_name: str = "s4") -> str:
        result = ""
        byte_value = ord(input_string[120]) << 16
        result += cls._STRING_TABLES[table_name][(byte_value & 16515072) >> 18]
        result += cls._STRING_TABLES[table_name][(byte_value & 258048) >> 12]
        result += "=="
        return result

    @classmethod
    def _generate_result(cls, input_string: str, table_name: str = "s4") -> str:
        result_list = []
        for i in range(0, len(input_string), 3):
            if i + 2 < len(input_string):
                value = (ord(input_string[i]) << 16) | (ord(input_string[i + 1]) << 8) | ord(input_string[i + 2])
            elif i + 1 < len(input_string):
                value = (ord(input_string[i]) << 16) | (ord(input_string[i + 1]) << 8)
            else:
                value = ord(input_string[i]) << 16

            for j, k in zip(range(18, -1, -6), (0xFC0000, 0x03F000, 0x0FC0, 0x3F)):
                if j == 6 and i + 1 >= len(input_string):
                    break
                if j == 0 and i + 2 >= len(input_string):
                    break
                result_list.append(cls._STRING_TABLES[table_name][(value & k) >> j])

        result_list.append("=" * ((4 - len(result_list) % 4) % 4))
        return "".join(result_list)

    @classmethod
    def _generate_arguments_code(cls) -> list[int]:
        a = []
        for j in range(24, -1, -8):
            a.append(cls._DEFAULT_ARGUMENTS[0] >> j)
        a.append(cls._DEFAULT_ARGUMENTS[1] / 256)
        a.append(cls._DEFAULT_ARGUMENTS[1] % 256)
        a.append(cls._DEFAULT_ARGUMENTS[1] >> 24)
        a.append(cls._DEFAULT_ARGUMENTS[1] >> 16)
        for j in range(24, -1, -8):
            a.append(cls._DEFAULT_ARGUMENTS[2] >> j)
        return [int(i) & 255 for i in a]

    def _generate_method_code(self, method: str = "GET") -> list[int]:
        return Hash.sm3_to_array(Hash.sm3_to_array(method + self._END_STRING))

    def _generate_params_code(self, params: str) -> list[int]:
        return Hash.sm3_to_array(Hash.sm3_to_array(params + self._END_STRING))

    @classmethod
    def _generate_browser_info(cls, platform: str = "Win32") -> str:
        inner_width = randint(1280, 1920)
        inner_height = randint(720, 1080)
        outer_width = randint(inner_width, 1920)
        outer_height = randint(inner_height, 1080)
        screen_x = 0
        screen_y = choice((0, 30))
        value_list = [
            inner_width,
            inner_height,
            outer_width,
            outer_height,
            screen_x,
            screen_y,
            0,
            0,
            outer_width,
            outer_height,
            outer_width,
            outer_height,
            inner_width,
            inner_height,
            24,
            24,
            platform,
        ]
        return "|".join(map(str, value_list))

    @staticmethod
    def _rc4_encrypt(plaintext: str, key: str) -> str:
        s = list(range(256))
        j = 0
        for i in range(256):
            j = (j + s[i] + ord(key[i % len(key)])) % 256
            s[i], s[j] = s[j], s[i]

        i = 0
        j = 0
        cipher = []
        for k in range(len(plaintext)):
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            s[i], s[j] = s[j], s[i]
            t = (s[i] + s[j]) % 256
            cipher.append(chr(s[t] ^ ord(plaintext[k])))
        return "".join(cipher)

    def _get_abogus_value(
        self,
        url_params: dict | str,
        method: str = "GET",
        start_time: int = 0,
        end_time: int = 0,
        random_num_1=None,
        random_num_2=None,
        random_num_3=None,
    ) -> str:
        string_1 = self._generate_string_1(random_num_1, random_num_2, random_num_3)
        string_2 = self._generate_string_2(
            urlencode(
                url_params,
                quote_via=quote
            )
            if isinstance(url_params, dict)
            else url_params, method, start_time, end_time
        )
        return self._generate_result(string_1 + string_2, "s4")

    def get_value(
        self,
        url_params: dict | str,
        method: str = "GET",
        start_time: int = 0,
        end_time: int = 0,
        random_num_1=None,
        random_num_2=None,
        random_num_3=None,
    ) -> str:
        """
        Generates an obfuscated value for ByteDance services.

        Args:
            url_params (dict | str): The URL parameters to obfuscate.
            method (str, optional): The HTTP method. Defaults to "GET".
            start_time (int, optional): The start time. Defaults to 0.
            end_time (int, optional): The end time. Defaults to 0.
            random_num_1 (float, optional): A random number. Defaults to None.
            random_num_2 (int, optional): A random number. Defaults to None.
            random_num_3 (int, optional): A random number. Defaults to None.

        Returns:
            str: The obfuscated value.
        """
        return self._get_abogus_value(
            url_params,
            method,
            start_time,
            end_time,
            random_num_1,
            random_num_2,
            random_num_3
        )