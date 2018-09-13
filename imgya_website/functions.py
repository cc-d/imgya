def base58_encode(n):
    # Lowercase L, Uppercase O, Uppercase I, Number 0 are excluded for easy-to-type name reasons
    base58_chars = '123456789' + 'ABCDEFGHJKLMNPQRSTUVWXYZ' + 'abcdefghijkmnopqrstuvwxyz'
    s = ''
    if n == 0:
        s = base58_chars[0]
    else:
        while n > 0:
            n, r = divmod(n, 58)
            s = base58_chars[r] + s
    return s

def base58_decode(s):
    # Lowercase L, Uppercase O, Uppercase I, Number 0 are excluded for easy-to-type name reasons
    n = 0
    base58_chars = '123456789' + 'ABCDEFGHJKLMNPQRSTUVWXYZ' + 'abcdefghijkmnopqrstuvwxyz'
    e = len(s)
    for c in s:
        i = base58_chars.index(c)
        n += (i * (58 ** (e-1)))
        e -= 1
    return n