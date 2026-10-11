# Tower of Hanoi Visual Simulator

A Python + Tkinter application that visually solves the classic Tower of Hanoi puzzle using recursion.

## Features
- Enter the number of disks (1 to 8)
- Three rods: Source, Auxiliary, Destination
- Disks of different sizes and colors
- Step-by-step animated disk movement
- Shows current move number and total moves (2^n - 1)
- Start, Pause/Resume and Reset buttons
- Adjustable animation speed
- Completion message when the puzzle is solved

## Requirements
- Python 3.8 or higher
- Tkinter (comes with Python on Windows)

No extra libraries need to be installed.

## Project Structure
TowerOfHanoiSimulator/
├── main.py # GUI and animation (Tkinter)
├── hanoi_logic.py # Recursive Tower of Hanoi logic
├── README.md
└── .gitignore


## How to Run
1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

4. Enter the number of disks and click **Start**.

## How It Works
The function `solve_hanoi(n, source, auxiliary, destination, moves)` is recursive:
1. Move n-1 disks from source to auxiliary.
2. Move the largest disk from source to destination.
3. Move n-1 disks from auxiliary to destination.

All moves are stored in a list and then animated one by one using Tkinter's `after()` method.

The minimum number of moves is calculated with the formula **2^n - 1**.

## Concepts Used
Recursion, Lists, Functions, Tkinter GUI, Exception Handling, Modular Programming

## Author 
Arpita Ikhankar