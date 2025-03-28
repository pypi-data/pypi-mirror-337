# FlameTracker Library

## Overview

The `FlameTracker` library provides a way to track and visualize function calls and execution times within Python programs. It includes features like:

- Hierarchical action tracking
- Timing of function calls
- JSON and string representation of call structures
- Flamegraph generation for performance visualization

## Installation

To use the `FlameTracker` library, install it in your Python environment:

```sh
pip install flametracker
```

## Usage

### Basic Tracking

```python
import flametracker

with flametracker.Tracker() as tracker:
    with tracker.action("example_action"):
        # Some computation here
        pass

print(tracker.to_str())
```

### Nested Actions

```python
import flametracker

with flametracker.Tracker() as tracker:
    with tracker.action("parent_action") as parent:
        with tracker.action("child_action") as child:
            child.set_result("Hello for child !")
```

### Function Wrapping

```python
import flametracker

@flametracker.wrap
def my_function(x):
    return x * 2

with flametracker.Tracker() as tracker:
    result = my_function(5)
```

### Generating a Flamegraph

```python
html_output = tracker.to_flamegraph()
with open("flamegraph.html", "w", encoding="utf-8") as f:
    f.write(html_output)
```

## Running Tests

To run the test suite using `pytest`, execute:

```sh
pytest
```

## License

This project is licensed under the MIT License.
