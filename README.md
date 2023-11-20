# Structure Visualizer
An application for easily visualizing OOP structures, with attributes and inheritance support.

## Quick Start
```console
> git clone https://github.com/Magicspell/StructureVisualizer
> cd ./StructureVisualizer
> ./Start.ps1
```
## About
StructureVisualizer is entirely made with python, using [pygame](https://github.com/pygame/pygame) for graphics. It consists of a two widgets, an editable text box and a graphics widow, both created from scratch for this project.

The program parses the input text and converts it to graphics, which are updated live and displayed.

## Syntax
The syntax for the text box is as follows:

### Class Definition:
```
MyClass
```
A string with no spaces, periods, or equal signs will be interpreted as a class with no parent.
### Child Class Definition:
```
MyClass ChildClass
```
A previously defined class followed by a new class name will create a new class with the defined as parent.
### Attributes
```
MyClass.age = int
```
A defined class (order does not matter) followed by a dot and the name for the attribute will create a new attribute, the type of which will be a defined class after the equals sign. In this example, we would have to also define `int` as a class.