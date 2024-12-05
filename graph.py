#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from itertools import permutations

with open("elem.json", "r", encoding="utf-8") as file:
    data = json.load(file)

selected_ids = {
    "8",
    "9",
    "2",
    "15",
    "6",
    "1",
    "3",
    "7",
    "13",
    "18",
}  # Выбор 10-ти городов из 20-ти

cities = {}
distances = {}

for item in data:
    if "label" in item["data"]:
        if item["data"]["id"] in selected_ids:
            cities[item["data"]["id"]] = item["data"]["label"]
    elif "source" in item["data"]:
        source = item["data"]["source"]
        target = item["data"]["target"]
        if source in selected_ids and target in selected_ids:
            weight = item["data"]["weight"]
            distances[(source, target)] = weight
            distances[(target, source)] = weight


def route_length(route):
    return sum(
        distances.get((route[i], route[i + 1]), float("inf"))
        for i in range(len(route) - 1)
    )


if __name__ == "__main__":
    all_routes = permutations(cities.keys())

    shortest_route = min(all_routes, key=route_length)
    shortest_distance = route_length(shortest_route)

    print("Выбранные города:")
    for city_id, city_name in cities.items():
        print(f"{city_id}: {city_name}")

    print("\nКратчайший маршрут:")
    print(" -> ".join(cities[city] for city in shortest_route))
    print(f"Общая длина маршрута: {shortest_distance} км")

    print("Расстояния:")
    for city1 in cities:
        for city2 in cities:
            if city1 != city2:
                distance = distances.get((city1, city2), "Нет.")
                print(f"{city1} -> {city2}: {distance}")
