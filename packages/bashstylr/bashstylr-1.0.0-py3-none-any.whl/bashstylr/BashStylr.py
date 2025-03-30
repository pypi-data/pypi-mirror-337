"""Set and store the bashstylr configurations."""


class Bashstylr(object):
    __slots__ = ('cache', 'prompt')

    def __new__(cls: type['Bashstylr'], cache: dict = {}, /) -> 'Bashstylr':
        assert isinstance(cache, dict), f"'{cache}' must be a dictionary"
        assert len(cache) == 0, f"the dictionary must initially be empty"
        return super(Bashstylr, cls).__new__(cls)

    def __init__(self: 'Bashstylr', cache: dict = {}, /) -> None:
        self.cache = cache
        self.prompt = list()

    def __str__(self: 'Bashstylr', /) -> str:
        return f'Bashstylr({self.cache})'

    def __cache_find__(self: 'Bashstylr', name: str, /) -> bool:
        assert isinstance(name, str), f"'{name}' must be a string"
        return name in self.cache.keys()

    def __cache_fetch__(self: 'Bashstylr', name: str, /) -> str | None:
        if not self.__cache_find__(name):
            return None
        else:
            return self.cache[name]

    def __cache_put__(self: 'Bashstylr', name: str, value: str, /) -> None:
        assert isinstance(name, str), f"'{name}' must be a string"
        assert isinstance(value, str), f"'{value}' must be a string"

        if not self.__cache_fetch__(name):
            self.cache[name] = value
            return None
        else:
            raise NameError(f"'{name}' has already been cached")

    def __prompt_len__(self: 'Bashstylr', negative: bool, /) -> int:
        assert isinstance(negative, bool), f"'{negative}' must be an intege"
        if not negative:
            return len(self.prompt)
        else:
            return -len(self.prompt)

    def add_style(self: 'Bashstylr', style: str, /) -> None:
        assert isinstance(style, str), f"'{style}' must be a string"
        match style:
            case 'reset':
                self.__cache_put__('style_reset', "\x1b[0m")
                return None
            case 'bold':
                self.__cache_put__('style_bold', "\x1b[1m")
                return None
            case 'dim':
                self.__cache_put__('style_dim', "\x1b[2m")
                return None
            case 'italic':
                self.__cache_put__('style_italic', "\x1b[3m")
                return None
            case 'underline':
                self.__cache_put__('style_underline', "\x1b[4m")
                return None
            case 'inverse':
                self.__cache_put__('style_inverse', "\x1b[5m")
                return None
            case 'hidden':
                self.__cache_put__('style_hidden', "\x1b[6m")
                return None
            case 'strikethrough':
                self.__cache_put__('style_strikethrough', "\x1b[7m")
                return None
            case _:
                raise NameError(f"'{style}' is not a valid bash style")

    def add_foreground(self: 'Bashstylr', name: str, red: int, green: int, blue: int, /) -> None:
        assert isinstance(name, str), f"'{name}' must be a string"
        assert isinstance(red, int) and red in range(0, 256), f"'{red}' must be an integer in the range 0 to 256"
        assert isinstance(green, int) and green in range(0, 256), f"'{green}' must be an integer in the range 0 to 256"
        assert isinstance(blue, int) and blue in range(0, 256), f"'{blue}' must be an integer in the range 0 to 256"
        
        if not name.startswith('fg_'):
            raise NameError(f"'{name}' must start with the word 'fg_'")
        else:
            self.__cache_put__(name, "\x1b[38;2;{r};{g};{b}m".format(r=red, g=green, b=blue))
            return None

    def add_background(self: 'Bashstylr', name: str, red: int, green: int, blue: int, /) -> None:
        assert isinstance(name, str), f"'{name}' must be a string"
        assert isinstance(red, int) and red in range(0, 256), f"'{red}' must be an integer in the range 0 to 256"
        assert isinstance(green, int) and green in range(0, 256), f"'{green}' must be an integer in the range 0 to 256"
        assert isinstance(blue, int) and blue in range(0, 256), f"'{blue}' must be an integer in the range 0 to 256"
        
        if not name.startswith('bg_'):
            raise NameError(f"'{name}' must start with the word 'bg_'")
        else:
            self.__cache_put__(name, "\x1b[48;2;{r};{g};{b}m".format(r=red, g=green, b=blue))
            return None

    def add_text(self: 'Bashstylr', name: str, text: str, /) -> None:
        assert isinstance(name, str), f"'{name}' must be a string"
        assert isinstance(text, str), f"'{text}' must be a string"

        if not name.startswith('text_'):
            raise NameError(f"'{name}' must start with the word 'text_'")
        else:
            self.__cache_put__(name, text)
            return None

    def prompt_append(self: 'Bashstylr', name: str, /) -> None:
        assert isinstance(name, str), f"'{name}' must be a string"
        string = self.__cache_fetch__(name)
        if string is None:
            raise NameError(f"Failed to append to prompt, '{name}' not in cache")
        else:
            self.prompt.append(string)
            return None

    def pormpt_insert(self: 'Bashstylr', name: str, index: int, /) -> None:
        assert isinstance(name, str), f"'{name}' must be a string"
        assert isinstance(index, int), f"'{index}' must be an intege"
        string = self.__cache_fetch__(name)

        if string is None:
            raise NameError(f"Failed to insert into prompt, '{name}' not in cache")
        else:
            if abs(index) is index and index <= self.__prompt_len__(False) - 1:
                self.prompt.insert(index, string)
            elif -index is index and index <= self.__prompt_len__(True):
                self.prompt.insert(index, string)
            else:
                raise IndexError(f"The position '{index}' is out of range")

    def prompt_prepend(self: 'Bashstylr', name: str, /) -> None:
        assert isinstance(name, str), f"'{name}' must be a string"
        string = self.__cache_fetch__(name)
        if string is None:
            raise NameError(f"Failed to prepend to prompt, '{name}' not in cache")
        else:
            self.prompt.insert(0, string)
            return None

    def ps1_compatible(self: 'Bashstylr', /) -> str:
        ps1 = str()
        for string in self.prompt:
            ps1 += r"\[" + string + r"\]"
        return ps1

    def prompt_print(self: 'Bashstylr', /) -> None:
        print(''.join(self.prompt), end="\n")
        return None
