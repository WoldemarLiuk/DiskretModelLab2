import numpy as np

graph = np.loadtxt('D:\l2-1.txt', dtype='i', delimiter=' ', skiprows=1)
print('Матриця графа:')
print(graph)

def sum_edg(graph):
    w_sum = 0
    l = len(graph)
    for i in range(l):
        for j in range(i, l):
            w_sum += graph[i][j]
    return w_sum

def alg(graph, source, dest):
    shortest = [0 for i in range(len(graph))]
    selected = [source]
    l = len(graph)
    inf = 10000000
    min_sel = inf
    for i in range(l):
        if (i == source):
            shortest[source] = 0
        else:
            if (graph[source][i] == 0):
                shortest[i] = inf
            else:
                shortest[i] = graph[source][i]
                if (shortest[i] < min_sel):
                    min_sel = shortest[i]
                    ind = i

    if (source == dest):
        return 0
    selected.append(ind)
    while (ind != dest):
        for i in range(l):
            if i not in selected:
                if (graph[ind][i] != 0):
                    # Перевіряємо, чи потрібно оновити значення мінімальної відстані
                    if ((graph[ind][i] + min_sel) < shortest[i]):
                        shortest[i] = graph[ind][i] + min_sel
        temp_min = 1000000

        for j in range(l):
            if j not in selected:
                if (shortest[j] < temp_min):
                    temp_min = shortest[j]
                    ind = j
        min_sel = temp_min
        selected.append(ind)

    return shortest[dest]

# Пошук вершин з непарною к-стю ребер
def get_odd(graph):
    degrees = [0 for i in range(len(graph))]
    for i in range(len(graph)):
        for j in range(len(graph)):
            if (graph[i][j] != 0):
                degrees[i] += 1

    odds = [i for i in range(len(degrees)) if degrees[i] % 2 != 0]
    print('\nВершини з непарною к-стю ребер:', odds)
    return odds

# Функція генерування унікальних пар вершин з непарною к-стю ребер
def gen_pairs(odds):
    pairs = []
    for i in range(len(odds) - 1):
        pairs.append([])
        for j in range(i + 1, len(odds)):
            pairs[i].append([odds[i], odds[j]])
    return pairs

def Postman(graph):
    odds = get_odd(graph)
    if (len(odds) == 0):
        return sum_edg(graph)
    pairs = gen_pairs(odds)
    l = (len(pairs) + 1) // 2

    pairings_sum = []

    def get_pairs(pairs, done=[], final=[]):

        if (pairs[0][0][0] not in done):
            done.append(pairs[0][0][0])

            for i in pairs[0]:
                f = final[:]
                val = done[:]
                if (i[1] not in val):
                    f.append(i)
                else:
                    continue

                if (len(f) == l):
                    pairings_sum.append(f)
                    return
                else:
                    val.append(i[1])
                    get_pairs(pairs[1:], val, f)

        else:
            get_pairs(pairs[1:], done, final)

    get_pairs(pairs)
    min_sums = []

    for i in pairings_sum:
        s = 0
        for j in range(len(i)):
            s += alg(graph, i[j][0], i[j][1])
        min_sums.append(s)

    added_dis = min(min_sums)
    print('\nСума ваг ребер графа:', sum_edg(graph))
    print('Мінімальний шлях між вершинами з непарною к-стю ребер:', added_dis)
    postman_dis = added_dis + sum_edg(graph)
    return postman_dis

print('Мінімальний маршрут листоноші: ', Postman(graph))
