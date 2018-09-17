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

def valid_name(s, ignore=[]):
    # Ensure album, image names are valid base58 names. The allowed parameter is a list of characters which are ignored.
    base58_chars = '123456789' + 'ABCDEFGHJKLMNPQRSTUVWXYZ' + 'abcdefghijkmnopqrstuvwxyz'
    if len(s) > 0 and len(s) < 20:
        for c in s:
            if c not in base58_chars and c not in ignore:
                return False
        return True
    return False

def valid_username(u):
    c = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'
    if len(u) < 1 or len(u) > 20:
        return False
    else:
        for a in u:
            if a not in c:
                return False
    return True

def valid_alphanumeric(s):
    # Ensure string is alphanumeric
    an = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'
    for c in s:
        if c not in an:
            return False
    return True

def valid_email(e):
    import re
    r = re.findall('[^@]+@[^@]+\.[^@]+', e)
    if len(r) == 1:
        if r[0] == e:
            return True
    return False
