import tiktoken


def num_tokens_from_string(string: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens


if __name__ == "__main__":
    print(num_tokens_from_string("tiktoken is great!"))
