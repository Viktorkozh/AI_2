#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from collections import deque


class CityProblem:
    def __init__(self, cities, distances, initial, goal):
        self.cities = cities
        self.distances = distances
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        return [target for target in self.cities if (state, target) in self.distances]

    def result(self, state, action):
        return action

    def is_goal(self, state):
        return state == self.goal


def breadth_first_search(problem):
    node = problem.initial
    if problem.is_goal(node):
        return [node]

    frontier = deque([node])
    came_from = {node: None}

    while frontier:
        current = frontier.popleft()

        for action in problem.actions(current):
            if action not in came_from:
                came_from[action] = current
                if problem.is_goal(action):
                    return reconstruct_path(came_from, action)
                frontier.append(action)

    return None


def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


if __name__ == "__main__":
    with open("elem.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    selected_ids = {"8", "9", "2", "15", "6", "1", "3", "7", "13", "18"}

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

    start_city = "8"
    goal_city = "15"

    problem = CityProblem(cities, distances, start_city, goal_city)
    solution = breadth_first_search(problem)

    if solution is None:
        print("Решение не найдено.")
    else:
        print("Кратчайший путь:")
        print(" -> ".join(cities[city] for city in solution))
