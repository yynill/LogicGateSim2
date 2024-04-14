# Logic Gate Simulator in Python (Pygame)

This project is a logic gate simulator developed using Python and the Pygame library. It allows users to experiment with basic and complex logic gate configurations and visually understand how different gates operate in a circuit.
![Uploading Screen Shot 2024-04-14 at 16.12.22 PM.png…]()

## Features

The simulator includes the following components:

### Logic Gates

- **AND Gate**: Outputs true only if all inputs are true.
- **OR Gate**: Outputs true if at least one input is true.
- **NOT Gate**: Outputs the opposite of the input.
- **NAND Gate**: Outputs false only if all inputs are true.
- **NOR Gate**: Outputs true only if all inputs are false.
- **XOR Gate**: Outputs true if the inputs are different.

### Additional Components

- **Switch**: A switch that can be toggled with right click.
- **Light**: Indicates the output of the circuit, lights up based on the result.
- **LED (Multicolour)**: Shows different colors depending on the input combinations.
- **Counter Display**: Shows a numeric representation of the input in binary form.
- **Box**: does nothing.

### Multiselect and Drag

- **Drag**: Middle mouse click and hold to drag all items.
- **Multiselect**: Left-click on the background and drag a box to multi-select items.
- **Delete**: Press the `Delete` key to remove selected items.
- **Duplicate**: Use `Control + D` to duplicate selected items. Note: This currently has a bug where it also appends the state of the duplicate's parent, even if no inputs are connected.

Have fun!
