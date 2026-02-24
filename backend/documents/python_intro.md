# Introduction to Python

## What is Python?

Python is a high-level, interpreted, general-purpose programming language. Its design philosophy emphasizes code readability, and its syntax allows programmers to express concepts in fewer lines of code than would be possible in languages such as C++ or Java.

Python supports multiple programming paradigms, including structured, object-oriented, and functional programming. It was created by Guido van Rossum and first released in 1991.

## Key Features of Python

- **Easy to Learn**: Python has a simple and clean syntax that is easy for beginners to understand.
- **Interpreted**: Python code is executed line by line, which makes debugging easier.
- **Dynamically Typed**: Variable types are determined at runtime.
- **Cross-Platform**: Python runs on Windows, macOS, Linux, and other platforms.
- **Extensive Standard Library**: Python comes with a large collection of modules and packages.
- **Open Source**: Python is freely available and its source code is open.

## Python Data Types

Python has several built-in data types:
- **int**: Integer numbers (e.g., `42`, `-7`)
- **float**: Floating-point numbers (e.g., `3.14`, `-2.5`)
- **str**: Strings (e.g., `"Hello, World!"`)
- **bool**: Boolean values (`True` or `False`)
- **list**: Ordered, mutable collections (e.g., `[1, 2, 3]`)
- **tuple**: Ordered, immutable collections (e.g., `(1, 2, 3)`)
- **dict**: Key-value pairs (e.g., `{"name": "Alice", "age": 30}`)
- **set**: Unordered collections of unique elements (e.g., `{1, 2, 3}`)

## Python Control Flow

### if-elif-else statements
```python
x = 10
if x > 0:
    print("Positive")
elif x < 0:
    print("Negative")
else:
    print("Zero")
```

### for loops
```python
for i in range(5):
    print(i)
```

### while loops
```python
count = 0
while count < 5:
    print(count)
    count += 1
```

## Functions in Python

Functions are defined using the `def` keyword:
```python
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))  # Output: Hello, Alice!
```

## Python Object-Oriented Programming

Python supports OOP with classes and objects:
```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound."

class Dog(Animal):
    def speak(self):
        return f"{self.name} barks."

dog = Dog("Rex")
print(dog.speak())  # Output: Rex barks.
```

## Popular Python Libraries

- **NumPy**: Numerical computing
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **Scikit-learn**: Machine learning
- **TensorFlow / PyTorch**: Deep learning
- **Flask / FastAPI / Django**: Web development
- **Requests**: HTTP requests
- **SQLAlchemy**: Database ORM
