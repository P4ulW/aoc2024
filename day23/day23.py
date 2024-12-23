from rich import print
from collections import defaultdict
from collections import deque


def main():
    filename = './in.txt'
    with open(filename) as file:
        connections = [tuple(line.strip().split('-'))
                       for line in file.readlines()]

    conns = {}
    for pc1, pc2 in connections:
        if pc1 not in conns:
            conns[pc1] = set([pc2])
        conns[pc1].add(pc2)

        if pc2 not in conns:
            conns[pc2] = set([pc1])
        conns[pc2].add(pc1)

    # part 1
    loop_of_threes = set()
    for node in conns.keys():
        if not node.startswith('t'):
            continue
        paths = follow_connection(node, conns, 3)
        for path in paths:
            path = sorted(path.split('->')[:3])
            loop_of_threes.add(tuple(path))
            # print(path)
    # print(loop_of_threes)
    print("sol part 1:", len(loop_of_threes), "\n")

    # part 2
    cliques = loop_of_threes
    for i in range(10):
        cliques = get_extended_cliques(cliques, conns)
    for c in cliques:
        out = ''
        for i in c:
            out += f'{i},'

        print(f'sol part 2: {out.removesuffix(',')}')
    # max_clique = max(cliques, key=len)
    # # print(f'{cliques}')


def get_extended_cliques(cliques, conns):
    extended_cliques = set()
    for clique in cliques:
        e_clique = extend_clique(clique, conns)
        # print(f'{clique}, {tuple(sorted(e_clique))}')
        if e_clique:
            extended_cliques.add(tuple(sorted(e_clique)))
    return extended_cliques


def extend_clique(clique, conns) -> list:
    possible_next_nodes = []
    for member in clique:
        possible_next_nodes.append(set(n for n in conns[member]))
    # print(possible_next_nodes)
    possible_next_node = set.intersection(*possible_next_nodes)
    # print(possible_next_node)
    if possible_next_node:
        return list([*clique, list(possible_next_node)[0]])
    return []


def follow_connection(
        start_node: str,
        connections: dict[str, set],
        max_depth=3):
    to_follow = deque()
    followed = set()
    paths = []

    to_follow.append((start_node, start_node, 0))
    while to_follow:
        node, path, depth = to_follow.popleft()
        followed.add(node)
        # print(f'node: \'{node}\', path: \'{path}\', depth: {depth}')

        if depth == max_depth and node == start_node:
            paths.append(path)

        for next_node in connections[node]:
            # print(f'next node: {next_node}')
            if depth > max_depth:
                # print('died from too depth')
                continue

            if depth == max_depth and next_node in path:
                # print('die from visited')
                continue

            to_follow.append((next_node, path+'->'+next_node, depth+1))
    return paths


if __name__ == "__main__":
    main()
    pass
