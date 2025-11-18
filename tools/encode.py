import urllib


def quote(s: str) -> str:
    return urllib.parse.quote(s)

if __name__ == '__main__':
    word = "你好"
    print(quote(word))
