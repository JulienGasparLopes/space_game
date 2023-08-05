# space_game

Playground/reflection for a graphical base lib in python
Parts of the code will be splitted into differents libs later

## Future libs divison

- Mathematics (Vertices, Matrices, operations)
- Game logic abstraction (Context, Window, Inputs, Map, Update ...)
- Graphical abstraction (same lib as game logic ?)
- Graphical implementation using tkinter

## Features implemented

- Main game logic (tkinter)
- Map and Entity update
- Vertex2f (2dim), Rectangle and basic operations
- Input (mouse, keyboard)
- Basic graphical abstraction

## FactorIO like game :

Focused on factory management/optimisation with money, energy, production default systems

- Belt and Material transportation - OK
- Factory processing + input/output - OK
- Entity collisions (overlapping) - OK
- Menu abstraction + Editor - OK
- Editor (+ multi-placement + deletion + object rotation) - OK
- Material configuration and Crafting recipes - OK
- Front: Edit factory current recipe - WIP
- Money system - Next
- Factory occupation % (idle, runing, blocked) - Todo + fix blocked state

- Front/Back total division - Todo

## Others game relative subjects:

- room detection (see the_space/space_map.py::\_update_rooms)
