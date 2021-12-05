from refueling import Refueling
from car import Car
import copy


def read_file(file):
    f = open(file, 'r', encoding='utf-8')
    km_to_city_b = int(f.readline())
    tank_capacity, kilometers_per_liter, spent_money, count_refuels = f.readline().split(' ')
    car_start = Car(float(tank_capacity), float(kilometers_per_liter), float(spent_money))
    refuels_list = [Refueling(0, 0)]
    for i in range(int(count_refuels)):
        distance_from_start_city, cost_in_liter = f.readline().split(' ')
        refueling = Refueling(cost_in_liter, distance_from_start_city)
        refuels_list.append(refueling)
    refuels_list.append(Refueling(0, km_to_city_b))
    f.close()
    return car_start, refuels_list, count_refuels


def create_graph(refuels_list, count_refuels):
    graph_refuels = []
    weights_nodes_refuels = {}
    for i in range(int(count_refuels) + 1):
        graph_refuels.append([])
        for j in range(i + 1, int(count_refuels) + 2):
            weights_nodes_refuels[(i, j)] = [refuels_list[j], abs(int(refuels_list[j].distance_from_start_city)
                                                                  - int(refuels_list[i].distance_from_start_city))]
    for i in range(int(count_refuels) + 1):
        for j in range(int(count_refuels) - i):
            graph_refuels[i].append(j + i + 1)
        graph_refuels[i].append(len(graph_refuels))
    return graph_refuels, weights_nodes_refuels


def create_path(graph_refuels, weights_nodes_refuels, car_start):
    d = [car_start]
    used = []
    for i in range(len(graph_refuels)):
        d.append(Car(car_start.tank_capacity, car_start.kilometers_per_liter, 999999))
        used.append(False)

    for i in range(len(graph_refuels)):
        v = None
        for j in range(len(graph_refuels)):
            if not used[j] and (v is None or d[j].spent_money < d[v].spent_money):
                v = j
        if d[v].spent_money == 999999:
            break
        used[v] = True
        for e in graph_refuels[v]:
            if d[v].spent_money + d[v].check_cost_fuel(weights_nodes_refuels[(v, e)][0],
                                                       weights_nodes_refuels[(v, e)][1]) < d[e].spent_money and \
                    d[v].check_drive_kilometres(weights_nodes_refuels[(v, e)][1]):
                if d[v].check_liters_per_tank_capacity(weights_nodes_refuels[(v, e)][1]) > d[v].tank_capacity / 2 and \
                        e != len(graph_refuels):
                    flag = False
                    for r in graph_refuels[e]:
                        if d[v].check_opportunity_to_get_there(weights_nodes_refuels[(v, e)][1]
                                                               + weights_nodes_refuels[(e, r)][1]):
                            d[e] = copy.deepcopy(d[v])
                            d[e].drive_kilometres(weights_nodes_refuels[(v, e)][1])
                            flag = True
                            break
                    if not flag:
                        d[e] = copy.deepcopy(d[v])
                        d[e].drive_kilometres(weights_nodes_refuels[(v, e)][1])
                        d[e].fuel(weights_nodes_refuels[(v, e)][0])
                else:
                    d[e] = copy.deepcopy(d[v])
                    d[e].drive_kilometres(weights_nodes_refuels[(v, e)][1])
                    if e != len(graph_refuels):
                        d[e].fuel(weights_nodes_refuels[(v, e)][0])

    return d[len(graph_refuels)].spent_money


def write_file(file, min_cost):
    f = open(file, 'w', encoding='utf-8')
    f.write(str(min_cost))
    f.close()


if __name__ == '__main__':
    car, refuels, n = read_file('in.txt')
    graph, weights = create_graph(refuels, n)
    answer = create_path(graph, weights, car)
    write_file('out.txt', round(answer, 1))
