from rich import print

ITER = 2_000


def mix(x, y):
    return x ^ y


def prune(x):
    return x % 16777216


def get_secret_number(x):
    x = prune(mix(x, x*64))
    x = prune(mix(x, x//32))
    x = prune(mix(x, x*2048))
    return x


def n_secret_num(x: int, n: int):
    for _ in range(n):
        x = get_secret_number(x)
    return x


def get_prices(num: int):
    s_nums = [num % 10,]
    for _ in range(ITER):
        num = get_secret_number(num)
        s_nums.append(num % 10)

    return s_nums


def get_changes(prices: list[int]):
    changes = [prices[i+1]-prices[i] for i in range(len(prices)-1)]
    return changes


def get_bananas_for_pattern(
        prices: list[int],
        changes: list[int]):
    bananas = {}
    for i in range(len(changes)-3):
        pattern = (changes[i], changes[i+1], changes[i+2], changes[i+3])
        if not pattern in bananas:
            # i plus 4 because len(prices) = len(changes) - 1
            bananas[pattern] = prices[i+4]

    return bananas


def main():
    filename = './inputs.txt'
    with open(filename) as file:
        data = [line.strip() for line in file.readlines()]
    print(data)

    res = sum(n_secret_num(int(num), ITER) for num in data)
    print(f'part 1: {res}')

    total_bananas = {}
    for num in data:
        prices = get_prices(int(num))
        changes = get_changes(prices)
        bananas_for_pattern = get_bananas_for_pattern(prices, changes)
        for pattern, bananas in bananas_for_pattern.items():
            if pattern not in total_bananas:
                total_bananas[pattern] = bananas
            else:
                total_bananas[pattern] += bananas

    print(max(total_bananas.values()))

    return


if __name__ == "__main__":
    main()
    pass
