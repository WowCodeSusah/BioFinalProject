# Food Web Simulator
## Overview

The Food Web Simulator is a Python-based graphical tool that allows users to simulate and interact with ecological food webs. Users can create nodes representing species, add relationships between them, and simulate population changes over time. The project is built using pygame and modular components for flexibility and scalability.

## Features

1. **Node Interaction** : Add, edit, delete nodes representing species in the ecosystem.

2. **Relationship Visualization**: Draw connections between nodes to represent predator-prey relationships.

3. **Simulation** : Step through days to observe changes in population values.

4. **Graphical User Interface** : Intuitive interface built using pygame for easy interaction.

5. **Animations** : Smooth transitions and menu animations.

## Requirements
Make sure the following dependencies are installed:
- Python 3.8+
- pygame

To install pygame, run:
```bash 
pip install pygame 
```

## How to Use
### Main Menu

1. **Add Node** : Create a new node with species name, population, and connections.

2. **Edit Node** : Modify existing nodes' attributes.

3. **Delete Node** : Remove a node and its relationships.

4. **Start Simulation** : Observe population changes and manage day progression.

### Simulation Controls
- Day Progression
- **+** : Advanced to the next day
- **-** : Go back to the previous day
- Nove Movement: Drag nodes within the screen to adjust layout.

### Modal Inputs
Input validation is performed for:
- **Node Name** : Ensures no duplicate names.

- **Population** : Accepts only numeric values.

- **Connections** : Validates existence of connected nodes.

## File Structure
food-web-simulator/
├── main.py                # Main entry point of the application
├── node.py                # Node class for species representation
├── button.py              # Button class for interactive UI elements
├── input_box.py           # InputBox class for user inputs
├── helper.py              # Helper functions for image imports and utilities
├── states/
│   ├── adding.py          # Logic for adding nodes
│   ├── edit.py            # Logic for editing nodes
│   ├── delete.py          # Logic for deleting nodes
└── resources/             # Assets (images, buttons, backgrounds)

## Contact
For any questions or suggestions, feel free to reach out:

Name: [Michael Bengawan, Ostein Vittorio Vellim, Tirza Gabriella]

Email: [ michael.bengawan@binus.ac.id, ostein.vellim@binus.ac.id, tirza.gabriella001@binus.ac.id ]


