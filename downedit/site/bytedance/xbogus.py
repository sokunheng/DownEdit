from base64 import b64encode
from hashlib import md5
from time import time
from urllib.parse import quote, urlencode


class XBogus:
    """
    Generates the x-bogus parameter for ByteDance services.
    """

    _DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    _STRING_TABLE = "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe="
    _ARRAY_MAP = [None] * 48 + list(range(10)) + [None] * 39 + list(range(10, 16))
    _CANVAS_VALUE = 3873194319

    def _create_array_from_values(self, *args) -> list[int]:
        """
        Creates a 19-element array from input values.
        """
        array = [0] * 19
        array[0], array[10], array[1],
        array[11], array[2], array[12],
        array[3], array[13], array[4],
        array[14], array[5], array[15],
        array[6], array[16], array[7],
        array[17], array[8], array[18],
        array[9] = args
        return array

    def _generate_obfuscated_string_1(self, *args) -> str:
        """
        Generates an obfuscated string using a specific permutation.
        """
        array = [0] * 19
        array[0], array[1], array[2],
        array[3], array[4], array[5],
        array[6], array[7], array[8],
        array[9], array[10], array[11],
        array[12], array[13], array[14],
        array[15], array[16], array[17],
        array[18] = args
        return "".join(map(chr, map(int, array)))

    @staticmethod
    def _generate_numbers_from_text(text: str) -> list[int]:
        """
        Generates a list of numbers from a text string.
        """
        return [
            (ord(text[i]) << 16) | (ord(text[i + 1]) << 8) | ord(text[i + 2])
            for i in range(0, 21, 3)
        ]

    @staticmethod
    def _generate_obfuscated_string_2(a: int, b: int, c: str) -> str:
        """
        Generates a short obfuscated string.
        """
        return chr(a) + chr(b) + c

    def _generate_obfuscated_string_3(self, a: str, b: str) -> str:
        """
        Generates an obfuscated string using RC4.
        """
        d = list(range(256))
        c = 0
        f = ""
        for i in range(256):
            d[i] = i
        for j in range(256):
            c = (c + d[j] + ord(a[j % len(a)])) % 256
            d[j], d[c] = d[c], d[j]
        t = 0
        c = 0
        for k in range(len(b)):
            t = (t + 1) % 256
            c = (c + d[t]) % 256
            d[t], d[c] = d[c], d[t]
            f += chr(ord(b[k]) ^ d[(d[t] + d[c]) % 256])
        return f

    def _calculate_md5_hash(self, input_data) -> str:
        """
        Calculates the MD5 hash of input data.
        """
        if isinstance(input_data, str):
            array = self._convert_md5_to_array(input_data)
        elif isinstance(input_data, list):
            array = input_data
        else:
            raise TypeError("Input data must be a string or a list.")

        md5_hash = md5()
        md5_hash.update(bytes(array))
        return md5_hash.hexdigest()

    def _convert_md5_to_array(self, md5_string: str) -> list[int]:
        """
        Converts an MD5 string to an array of integers.
        """
        if isinstance(md5_string, str) and len(md5_string) > 32:
            return [ord(char) for char in md5_string]
        else:
            return [
                (self._ARRAY_MAP[ord(md5_string[index])] << 4)
                | self._ARRAY_MAP[ord(md5_string[index + 1])]
                for index in range(0, len(md5_string), 2)
            ]


    def _process_url_path(self, url_path: str) -> list[int]:
        """
        Processes the URL path to generate an array.
        """
        return self._convert_md5_to_array(
            self._calculate_md5_hash(self._convert_md5_to_array(self._calculate_md5_hash(url_path)))
        )

    def _generate_string_from_number(self, number: int) -> str:
        """
        Generates a string from a number using a lookup table.
        """
        string_representation = [number & 16515072, number & 258048, number & 4032, number & 63]
        string_representation = [i >> j for i, j in zip(string_representation, range(18, -1, -6))]
        return "".join([self._STRING_TABLE[i] for i in string_representation])

    @staticmethod
    def _handle_user_agent(key: str, user_agent: bytes) -> bytes:
        """
        Handles user agent using RC4.
        """
        d = list(range(256))
        c = 0
        result = bytearray(len(user_agent))

        for i in range(256):
            c = (c + d[i] + ord(key[i % len(key)])) % 256
            d[i], d[c] = d[c], d[i]

        t = 0
        c = 0

        for i in range(len(user_agent)):
            t = (t + 1) % 256
            c = (c + d[t]) % 256
            d[t], d[c] = d[c], d[t]
            result[i] = user_agent[i] ^ d[(d[t] + d[c]) % 256]
        return result

    def _generate_user_agent_array(self, user_agent: str, params: int) -> list[int]:
        """
        Generates a user agent array.
        """
        ua_key = ["\u0000", "\u0001", chr(params)]
        value = self._handle_user_agent("".join(ua_key), user_agent.encode("utf-8"))
        value = b64encode(value)
        return list(md5(value).digest())

    def _generate_x_bogus(self, query: list[int], params: int, user_agent: str, timestamp: int) -> str:
        """
        Generates the x-bogus value.
        """
        user_agent_array = self._generate_user_agent_array(user_agent, params)
        array = [
            64,
            int(0.00390625 * (2**32)),
            1,
            params,
            query[-2],
            query[-1],
            69,
            63,
            user_agent_array[-2],
            user_agent_array[-1],
            timestamp >> 24 & 255,
            timestamp >> 16 & 255,
            timestamp >> 8 & 255,
            timestamp & 255,
            self._CANVAS_VALUE >> 24 & 255,
            self._CANVAS_VALUE >> 16 & 255,
            self._CANVAS_VALUE >> 8 & 255,
            self._CANVAS_VALUE & 255,
            0,
        ]

        for i in array[:-1]:
            array[-1] ^= i

        obfuscated_string_1 = self._generate_obfuscated_string_1(*self._create_array_from_values(*array))
        obfuscated_string_2 = self._generate_obfuscated_string_2(2, 255, self._generate_obfuscated_string_3("ÿ", obfuscated_string_1))
        return "".join(self._generate_string_from_number(i) for i in self._generate_numbers_from_text(obfuscated_string_2))

    def get_x_bogus(
        self,
        query: dict,
        params: int = 8,
        user_agent: str = _DEFAULT_USER_AGENT,
        timestamp: int = None
    ) -> str:
        """
        Generates the x-bogus parameter.
        """
        timestamp = int(timestamp or time())
        processed_query = self._process_url_path(urlencode(query, quote_via=quote))
        return self._generate_x_bogus(processed_query, params, user_agent, timestamp)

if __name__ == "__main__":
    # bogus = XBogus()
    # print(bogus.get_x_bogus({
    #     "Accept": "*/*",
    #     "Accept-Encoding": "*/*",
    #     "Accept-Language": "zh-SG,zh-CN;q=0.9,zh;q=0.8",
    #     "Content-Type": "text/plain;charset=UTF-8",
    #     "Referer": "https://www.douyin.com/",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    # }))
    ...