symbols_radix_62 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

symbols_dozenal = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '↊', '↋']

symbols_RFC_4648 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']

symbols_ASCII = ['␀', '␁', '␂', '␃', '␄', '␅', '␆', '␇', '␈', '␉', '␊', '␋', '␌', '␍', '␎', '␏', '␐', '␑', '␒', '␓', '␔', '␕', '␖', '␗', '␘', '␙', '␚', '␛', '␜', '␝', '␞', '␟', '␠', '!', '\"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '␡']

def num_to_str(num:any, radix:int=10, symbols:list[str]=symbols_radix_62, little_endian:bool=True, prefix:str='', pad_modulus:int=None, pad_symbol:str=None, pad_direction:str="right"):
    output:str = prefix

    if len(symbols) < radix:
        raise ValueError(f"{len(symbols)} symbols not sufficient for base {radix}")

    if endianness == "little":
        while num >= radix:
            output = symbols[num%radix] + output
            num //= radix
        output = symbols[num] + output
    elif endianness == "big":
        while num >= radix:
            output += symbols[num%radix]
            num //= radix
        output += symbols[num]
    else:
        raise ValueError(f'{endianness} should be "little" or "big"')

    if pad_modulus is not None:
        pad_required = len(output)%pad_modulus
        if pad_direction == "left":
            for i in range(pad_required):
                output = pad_symbol + output
        elif pad_direction == "right":
            for i in range(pad_required):
                output += pad_symbol
        else:
            raise ValueError(f'{pad_direction} should be "left" or "right"')

    return output
