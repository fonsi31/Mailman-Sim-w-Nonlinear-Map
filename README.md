# Mailmain Delivery Optimal Route Simulator

A Python script that simulates a mailman traversing the shortest route possible given a nonlinear map

## Features

- Plans the shortest route for a mailman given a list of mail drop-off locations
- Animates a moving motorcycle through a straight path in CLI
- Intercity Route Planning

## Algorithms and Data Structures

- Djikstra's Algorithm for calculating the shortest path between 2 locations
- Adjacency Linked List modeled using a hash map (dictionary) to store map infos


# Requirements

- Python 3.10 or later

## How to Run

1. Open a terminal.

2. Navigate to the project folder:

```bash
cd DSALG_MC02
```

3. Run the program:

```bash
python main.py
```

## Notes

- Ensure that `NonlinearMap.csv` and `PostOffices.csv` are located in the same directory as `main.py`.
