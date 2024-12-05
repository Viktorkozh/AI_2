#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import heapq
import math
from collections import deque


class Problem:
    def __init__(self, initial=None, goal=None, **kwds):
        self.__dict__.update(initial=initial, goal=goal, **kwds)

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def is_goal(self, state):
        return state == self.goal

    def action_cost(self, s, a, s1):
        return 1

    def h(self, node):
        return 0

    def __str__(self):
        return "{}({!r}, {!r})".format(type(self).__name__, self.initial, self.goal)


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(
            state=state, parent=parent, action=action, path_cost=path_cost
        )

    def __repr__(self):
        return "<{}>".format(self.state)

    def __len__(self):
        return 0 if self.parent is None else (1 + len(self.parent))

    def __lt__(self, other):
        return self.path_cost < other.path_cost

    # Алгоритм не смог найти решение.
    failure = None  # Placeholder for failure node
    # Указывает на то, что поиск с итеративным углублением был прерван.
    cutoff = None  # Placeholder for cutoff node

    def expand(self, problem):
        s = self.state
        for action in problem.actions(s):
            s1 = problem.result(s, action)
            cost = self.path_cost + problem.action_cost(s, action, s1)
            yield Node(s1, self, action, cost)

    def path_actions(self):
        if self.parent is None:
            return []
        return self.parent.path_actions() + [self.action]

    def path_states(self):
        if self in (Node.cutoff, Node.failure, None):
            return []
        if self.parent is None:
            return [self.state]
        return self.parent.path_states() + [self.state]


# Initialize the failure and cutoff nodes
Node.failure = Node("failure", path_cost=math.inf)
Node.cutoff = Node("cutoff", path_cost=math.inf)


FIFOQueue = deque
LIFOQueue = list


class PriorityQueue:
    def __init__(self, items=(), key=lambda x: x):
        self.key = key
        self.items = []  # a heap of (score, item) pairs
        for item in items:
            self.add(item)

    def add(self, item):
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        return heapq.heappop(self.items)[1]

    def top(self):
        return self.items[0][1]

    def __len__(self):
        return len(self.items)


class PourProblem(Problem):
    def __init__(self, initial, goal, sizes):
        super().__init__(initial=initial, goal=goal, sizes=sizes)
        self.sizes = sizes

    def actions(self, state):
        actions = []
        for i in range(len(state)):
            # Fill action
            actions.append(("Fill", i))
            # Dump action
            actions.append(("Dump", i))
            for j in range(len(state)):
                if i != j:
                    # Pour action
                    actions.append(("Pour", i, j))
        return actions

    def result(self, state, action):
        new_state = list(state)
        if action[0] == "Fill":
            new_state[action[1]] = self.sizes[action[1]]
        elif action[0] == "Dump":
            new_state[action[1]] = 0
        elif action[0] == "Pour":
            i, j = action[1], action[2]
            amount_to_pour = min(new_state[i], self.sizes[j] - new_state[j])
            new_state[i] -= amount_to_pour
            new_state[j] += amount_to_pour
        return tuple(new_state)

    def is_goal(self, state):
        return any(x == self.goal for x in state)


def breadth_first_search(problem):
    node = Node(problem.initial)
    if problem.is_goal(problem.initial):
        return node

    frontier = FIFOQueue([node])
    reached = {problem.initial}

    while frontier:
        node = frontier.pop()

        for child in node.expand(problem):
            s = child.state

            if problem.is_goal(s):
                return child

            if s not in reached:
                reached.add(s)
                frontier.appendleft(child)

    return Node.failure


if __name__ == "__main__":
    initial_state = (1, 1, 1)  # начальные уровни воды в кувшинах
    goal_volume = 13  # целевой объем воды
    sizes = (2, 16, 32)  # размеры кувшинов

    problem = PourProblem(initial_state, goal_volume, sizes)
    solution = breadth_first_search(problem)

    if solution is Node.failure:
        print("Решение не найдено.")
    else:
        print("Решение найдено:")
        print("Действия:", solution.path_actions())
        print("Состояния:", solution.path_states())
