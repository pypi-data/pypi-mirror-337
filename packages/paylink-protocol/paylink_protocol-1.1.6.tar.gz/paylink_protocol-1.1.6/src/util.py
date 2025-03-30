def encodePayLinkData(appId: int, userId: int = 0) -> str:
    def to_b36(n: int) -> str:
        return ''.join("0123456789abcdefghijklmnopqrstuvwxyz"[r] for r in _divmod36(n)) or "0"

    def _divmod36(n: int):
        if n == 0: return [0]
        digits = []
        while n:
            n, r = divmod(n, 36)
            digits.insert(0, r)
        return digits

    a = to_b36(appId)
    u = to_b36(userId)
    l = f"{len(a):02}"
    return l + a + u

def decodePayLinkData(data: str) -> tuple[int, int]:
    la = int(data[:2])
    a = int(data[2:2+la], 36)
    u = int(data[2+la:], 36)
    return a, u

def encryptUserId(value: int, key: int) -> int:
    return value ^ key

def decryptUserId(encrypted: int, key: int) -> int:
    return encrypted ^ key