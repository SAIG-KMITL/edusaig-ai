from pydantic import BaseModel, Field
from typing import List, Optional

class EvaluateTestRequest(BaseModel):
    question: List[str] = [
    "What is the output of the following Python code: x = 5; y = 3; print(x + y)?",
    "What is the purpose of the 'if' statement in Python?",
    "What is the difference between '==' and '=' in Python?",
    "What will happen if you use a variable before declaring it in Python?",
    "What is the output of the following Python code: name = 'John'; print(name)?",
    "What is the purpose of the 'print()' function in Python?",
    "What is the output of the following Python code: x = 10; x += 5; print(x)?",
    "What are the basic data types in Python?",
    "What is the purpose of the 'input()' function in Python?",
    "What is the output of the following Python code: fruits = ['apple', 'banana', 'cherry']; print(fruits[0])?",
    "What is the primary function of a CPU (Central Processing Unit)?",
    "What is the main purpose of RAM (Random Access Memory) in a computer?",
    "Which component is responsible for storing the operating system and installed programs?",
    "What is the difference between a USB 2.0 and USB 3.0 port?",
    "What is the main purpose of a power supply unit (PSU) in a computer?",
    "Which type of storage device uses spinning disks to store data?",
    "What is the function of a motherboard in a computer?",
    "What is the main difference between a hard drive and a solid-state drive (SSD)?",
    "What is the purpose of a graphics card in a computer?",
    "What is the main purpose of a cooling fan in a computer?"
    ]
    correct_answer: List[str] = [
    "8",
    "To check if a condition is true or false and execute code accordingly",
    "Comparison operator",
    "Python will throw a syntax error.",
    "It will print John",
    "It is used for output operations",
    "15",
    "Floats, Integers, Strings, Booleans",
    "To take user input from the keyboard",
    "apple",
    "To execute instructions and perform calculations",
    "To store programs and data temporarily",
    "Hard Drive",
    "USB 2.0 ports have a speed of 480 Mbps, while USB 3.0 ports have a speed of 5 Gbps.",
    "To convert AC power to DC power for the computer's components",
    "Hard Disk Drive",
    "To connect hardware components together",
    "A hard drive uses magnetic disks while an SSD uses flash memory.",
    "To render images and video on the screen",
    "To cool down the computer's components"
    ]
    user_answer: List[str] = [
    "7",
    "To create a loop that will continue until a certain condition is met",
    "Assignment operator",
    "Python will throw a runtime error.",
    "It will throw an error",
    "It is used for error handling",
    "20",
    "Integers, Floats",
    "To sort a list of items in ascending order",
    "banana",
    "To control the flow of data between components",
    "To process data quickly",
    "RAM",
    "USB 2.0 ports can charge devices faster than USB 3.0 ports.",
    "To store data on the computer's hard drive",
    "Solid State Drive",
    "Solid State Drive",
    "To display images",
    "To increase the computer's memory"
    ]