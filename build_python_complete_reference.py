from __future__ import annotations

from collections import defaultdict
import builtins as py_builtins
import io
import keyword
import token as tokenmod
import tokenize
from html import escape
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent
OUTFILE = ROOT / "python_complete_reference.html"
STYLESHEET = ROOT / "styles.css"
LIGHT_STYLESHEET = ROOT / "styles-light.css"
DARK_STYLESHEET = ROOT / "styles-dark.css"

BUILTIN_NAMES = {name for name in dir(py_builtins) if not name.startswith('_')}

LAYER_NAMES = {
    0: "Runtime & Environment",
    1: "Primitive Building Blocks",
    2: "Data Structures",
    3: "Control Flow",
    4: "Functions",
    5: "Object-Oriented Programming",
    6: "Iterators & Generators",
    7: "Decorators & Metaprogramming",
    8: "Modules & Packages",
    9: "File I/O & Serialization",
    10: "Concurrency & Parallelism",
    11: "Type System & Tooling",
    12: "Testing",
    13: "Performance & Internals",
    14: "Ecosystem & Advanced Patterns",
}

NAV_LABELS = {
    0: "Layer 0: Environment",
    1: "Layer 1: Primitives",
    2: "Layer 2: Data Structures",
    3: "Layer 3: Control Flow",
    4: "Layer 4: Functions",
    5: "Layer 5: OOP",
    6: "Layer 6: Iterators",
    7: "Layer 7: Metaprogramming",
    8: "Layer 8: Modules",
    9: "Layer 9: I/O",
    10: "Layer 10: Concurrency",
    11: "Layer 11: Typing",
    12: "Layer 12: Testing",
    13: "Layer 13: Performance",
    14: "Layer 14: Patterns",
}


def b(text: str) -> str:
    lines = text.strip("\n").splitlines()
    first_content = next((line for line in lines if line.strip()), "")
    # Strip the example's outer margin without touching embedded multiline string contents.
    margin = first_content[: len(first_content) - len(first_content.lstrip())]
    if not margin:
        return "\n".join(lines)
    return "\n".join(line[len(margin):] if line.startswith(margin) else line for line in lines)


def ex(title: str, why: str, code: str, observe: str) -> dict[str, str]:
    return {"title": title, "why": why, "code": code, "observe": observe}


def c(cid: str, layer: int, title: str, prereqs: list[str], quick: str, learn: list[str], problem: str, mental: str, examples: list[dict[str, str]], why_not: str = "") -> dict[str, object]:
    return {
        "id": cid,
        "layer": layer,
        "title": title,
        "prereqs": prereqs,
        "quick": quick,
        "learn": learn,
        "problem": problem,
        "mental": mental,
        "examples": examples,
        "why_not": why_not or "Python usually keeps one simple runtime rule instead of inventing a second special case. Prefer the plainer construct when it communicates intent more clearly.",
    }


concepts: list[dict[str, object]] = []

concepts.extend([
    c(
        "PY01",
        0,
        "What is Python?",
        [],
        "Python is a high-level language whose reference runtime, CPython, compiles source code to bytecode and runs that bytecode on the Python Virtual Machine.",
        [
            "How the Python pipeline turns source into running code",
            "Why CPython is the baseline implementation",
            "What the GIL means at a high level before the threading deep-dive",
        ],
        "Python exists so humans can automate real work with readable code, a large standard library, and a runtime model that stays inspectable instead of hidden behind opaque tooling.",
        "source.py -> lexer tokens -> parser -> AST -> bytecode -> PVM -> objects and side effects",
        [
            ex(
                "Hello world, character by character",
                "This makes the smallest useful Python program explicit. Even the invisible newline matters because Python reads text, not mystical commands.",
                b('''
                source = 'print("Hello, world!")\\n'
                print(repr(source))
                print("p r i n t -> the function name")
                print("( and ) -> the call boundary")
                print('"Hello, world!" -> a string literal')
                print("\\n -> the newline character ending the line")
                '''),
                "The repr output shows the final newline as `\\n`. If you remove it, the source is still valid, but the string representation changes because the file text changed.",
            ),
            ex(
                "Inspect the AST and bytecode for a tiny program",
                "Python does not execute raw text directly. It parses structure first, then compiles the structure into bytecode.",
                b('''
                import ast
                import dis

                source = "total = 1 + 2\\nprint(total)\\n"
                tree = ast.parse(source)
                print(ast.dump(tree, indent=2))

                compiled = compile(source, "<demo>", "exec")
                dis.dis(compiled)
                '''),
                "You should see `Assign` and `Call` nodes in the AST, then bytecode instructions like `LOAD_CONST`, `STORE_NAME`, and `CALL` in the disassembly.",
            ),
            ex(
                "See which Python implementation is running",
                "The language is larger than CPython. Alternative implementations exist because different deployment targets care about different tradeoffs.",
                b('''
                import platform
                import sys

                print(platform.python_implementation())
                print(sys.implementation)
                print("CPython has the GIL; PyPy adds a JIT; Jython targets the JVM")
                '''),
                "On most machines this prints `CPython`. Choose PyPy when long-running pure-Python code benefits from a JIT, or Jython when JVM integration matters more than CPython extension compatibility.",
            ),
        ],
        "Python could have forced ahead-of-time compilation or manual memory management, but its design favors fast feedback. CPython wins by compatibility, PyPy by JIT speed on some workloads, and Jython by Java ecosystem access.",
    ),
    c(
        "PY02",
        0,
        "Python Installation & the REPL",
        [],
        "Installing Python gives you an interpreter, a launcher, and an interactive REPL where you can ask the runtime questions immediately.",
        [
            "How the OS finds the interpreter through PATH, the `py` launcher, and shebang lines",
            "Why the REPL is a learning tool, not just a toy",
            "How `_`, `help()`, `dir()`, and `type()` help you discover behavior",
        ],
        "A fast feedback loop matters because beginners and experts both need a safe place to test assumptions before committing code to a file or a larger application.",
        "shell lookup -> executable path -> interpreter process -> REPL prompt -> objects you can inspect live",
        [
            ex(
                "Find the interpreter you are actually using",
                "This matters because multiple Python installs can exist on one machine. PATH and the Windows launcher decide which one starts.",
                b('''
                import sys
                import os

                print(sys.executable)
                print(sys.version)
                print(os.environ.get("PATH", "")[:120] + "...")
                '''),
                "`sys.executable` tells you the exact interpreter path. If a different Python starts than you expected, PATH order or the launcher configuration is usually why.",
            ),
            ex(
                "Core REPL discovery tools",
                "The REPL becomes useful when you treat it like a microscope. You can inspect objects without creating a full project first.",
                b('''
                name = "python"
                print(type(name))
                print(dir(name)[:8])
                print(help(name.upper))
                '''),
                "`type()` shows the object's class, `dir()` shows accessible attributes, and `help()` opens built-in documentation. In a real REPL, `_` would also hold the last result.",
            ),
            ex(
                "Shebang text and the launcher concept",
                "Unix-like systems can read the first line of a script as an instruction for which interpreter should run it.",
                b('''
                script = "#!/usr/bin/env python3\\nprint('hello from a script')\\n"
                print(script.splitlines()[0])
                print("On Windows, `py script.py` plays a similar launcher role")
                '''),
                "The shebang is not Python syntax; it is metadata for the operating system. On Windows, the `py` launcher often gives a cleaner multi-version story.",
            ),
        ],
        "You can write everything in files, but skipping the REPL slows learning because every tiny experiment becomes a save-run-debug loop.",
    ),
    c(
        "PY03",
        0,
        "How Python Executes Code",
        [],
        "Python turns text into tokens, tokens into an abstract syntax tree, and that tree into bytecode that the virtual machine executes.",
        [
            "What the lexer, parser, AST, bytecode, and PVM each do",
            "How `ast.parse()` and `dis.dis()` expose the execution pipeline",
            "Why `.pyc` files and `__pycache__` exist",
        ],
        "Execution models matter because debugging is easier when you know whether a failure comes from parsing, compilation, name lookup, or runtime behavior.",
        "text -> tokens -> syntax tree -> compiled code object -> bytecode loop -> object operations",
        [
            ex(
                "Parse a five-line program into an AST",
                "This shows that Python tracks structure, not just lines of text.",
                b('''
                import ast

                source = """
                tax = 0.18
                subtotal = 20
                total = subtotal * (1 + tax)
                message = f"total={total:.2f}"
                print(message)
                """
                tree = ast.parse(source)
                print(ast.dump(tree, indent=2))
                '''),
                "Look for nodes like `Assign`, `BinOp`, `JoinedStr`, and `Call`. If the source were malformed, parsing would fail before any runtime work happened.",
            ),
            ex(
                "Disassemble the same program",
                "Bytecode is the instruction stream the CPython virtual machine actually executes.",
                b('''
                import dis

                source = "x = 10\\ny = x + 5\\nprint(y)\\n"
                code = compile(source, "<exec-model>", "exec")
                dis.dis(code)
                '''),
                "Instructions such as `LOAD_CONST`, `STORE_NAME`, `LOAD_NAME`, `BINARY_OP`, and `CALL` show how high-level code becomes a low-level sequence.",
            ),
            ex(
                "Compile a file and inspect `__pycache__`",
                "`.pyc` files speed startup by caching bytecode so the parser and compiler do not need to rerun every time.",
                b('''
                import pathlib
                import py_compile

                path = pathlib.Path("demo_exec_model.py")
                path.write_text("value = 42\\nprint(value)\\n", encoding="utf-8")
                py_compile.compile(str(path), doraise=True)
                print(sorted(str(p) for p in path.parent.glob("__pycache__/demo_exec_model*.pyc")))
                '''),
                "The cache file appears under `__pycache__`. Delete it and Python simply regenerates it when appropriate; it is an optimization, not your source of truth.",
            ),
        ],
        "Python could have hidden all of this behind a black box, but exposing ASTs, code objects, and disassembly makes tooling, debugging, and teaching much easier.",
    ),
    c(
        "PY04",
        0,
        "Python Versioning",
        [],
        "Python's version story explains why Python 3 broke compatibility with Python 2 and why modern features usually arrive through the PEP process.",
        [
            "How Python 1, 2, and 3 fit on a timeline",
            "What PEPs are and why they shape the language",
            "How to check language features against the running version",
        ],
        "Versions matter because examples that work in Python 3.12 may fail in Python 3.8, and many confusing tutorials on the internet still mix Python 2 syntax into Python 3 discussions.",
        "language evolution -> PEP proposal -> accepted feature -> release series -> your runtime version decides availability",
        [
            ex(
                "Check the running version and gate a feature",
                "Language features are tied to concrete releases. `match/case`, for example, requires Python 3.10 or later.",
                b('''
                import sys

                print(sys.version_info)
                if sys.version_info >= (3, 10):
                    print("pattern matching is available")
                else:
                    print("use if/elif instead")
                '''),
                "Version tuples let you write exact checks instead of guessing from documentation screenshots.",
            ),
            ex(
                "Read The Zen of Python",
                "PEP 20 is a compact summary of the language's values and is worth reading because many design choices trace back to it.",
                b('''
                import this
                print("PEP 20: The Zen of Python")
                '''),
                "`import this` prints aphorisms such as 'Explicit is better than implicit.' They are not laws, but they explain the language's bias toward clarity.",
            ),
            ex(
                "Print important version identifiers",
                "Semantic versioning is not the whole Python story, but release numbers still communicate feature availability and support windows.",
                b('''
                import platform
                print(platform.python_version())
                print(platform.python_implementation())
                print("Python 2 reached end of life on 2020-01-01")
                '''),
                "Python 3 won because the ecosystem migrated, tooling improved, and the cost of staying on Python 2 kept rising.",
            ),
        ],
        "Python could have kept every Python 2 behavior forever, but breaking compatibility in Python 3 fixed Unicode handling, cleaned up syntax, and removed long-term design debt.",
    ),
    c(
        "PY05",
        1,
        "Variables, Assignment, and Name Binding",
        ["PY01", "PY02", "PY03", "PY04"],
        "In Python, assignment binds a name to an object; it does not copy a value into a box called a variable.",
        [
            "Why names and objects are separate ideas",
            "How aliasing explains shared mutations",
            "Where multiple assignment and unpacking are useful and where they bite",
        ],
        "Python uses name binding so objects can be passed around cheaply, shared intentionally, and rebound without pretending that names physically contain values.",
        "names table -> object references -> heap objects\n`a` and `b` can point at the same object",
        [
            ex(
                "A name is a tag, not a storage box",
                "`id()` makes the object identity visible so you can see two names pointing at one object.",
                b('''
                data = [1, 2, 3]
                alias = data
                print(id(data), id(alias))
                alias.append(4)
                print(data)
                '''),
                "Both names have the same `id`, and mutating through `alias` changes what `data` sees because the list object is shared.",
            ),
            ex(
                "Augmented assignment differs for ints and lists",
                "Immutable objects usually create a new object on `+=`, while mutable containers often modify in place.",
                b('''
                number = 10
                before_number = id(number)
                number += 5

                items = [1, 2]
                before_items = id(items)
                items += [3]

                print(before_number, id(number))
                print(before_items, id(items))
                '''),
                "The integer gets a new identity after `+=`. The list usually keeps the same identity because the operation mutates it in place.",
            ),
            ex(
                "Tuple unpacking and the shared-list trap",
                "Unpacking is expressive, but chained assignment to a mutable object creates aliases.",
                b('''
                a, *rest, z = (1, 2, 3, 4, 5)
                print(a, rest, z)

                x = y = z = []
                y.append("boom")
                print(x, y, z)
                '''),
                "The unpacking example creates separate bindings. The chained assignment example makes three names refer to the same list, which is almost never what you want.",
            ),
        ],
        "Some languages model variables as typed storage slots. Python chooses flexible name binding because objects carry their own type and lifetime information.",
    ),
    c(
        "PY06",
        1,
        "Python's Type System",
        ["PY01", "PY02", "PY03", "PY04"],
        "Python is dynamically typed, strongly typed, and comfortable with duck typing: objects are judged by behavior more than declared ancestry.",
        [
            "What dynamic typing means at runtime",
            "Why duck typing values behavior over declarations",
            "How strong typing prevents silent coercion bugs",
        ],
        "The type system exists to let code stay flexible without silently gluing incompatible values together in ways that hide mistakes.",
        "name -> object -> type\noperations ask the object what behavior it supports at runtime",
        [
            ex(
                "Rebinding the same name to different types",
                "Dynamic typing means the name is not permanently declared as one type.",
                b('''
                value = 10
                print(value, type(value))
                value = "ten"
                print(value, type(value))
                value = [10]
                print(value, type(value))
                '''),
                "The same name points to different objects over time. The objects know their own type; the name does not.",
            ),
            ex(
                "Duck typing with unrelated classes",
                "If two objects respond to the same method, one function can often use both without caring about inheritance.",
                b('''
                class Dog:
                    def speak(self):
                        return "woof"

                class Robot:
                    def speak(self):
                        return "synthetic greeting"

                def announce(thing):
                    print(thing.speak())

                announce(Dog())
                announce(Robot())
                '''),
                "`announce` works because it needs a `speak()` method, not a specific class name. That is duck typing in practice.",
            ),
            ex(
                "Strong typing rejects unsafe mixing",
                "Python refuses to guess how to combine incompatible types because guesses often hide bugs.",
                b('''
                try:
                    print("1" + 1)
                except TypeError as exc:
                    print(type(exc).__name__, exc)

                print(int("1") + 1)
                '''),
                "`\"1\" + 1` fails with `TypeError`. That is a feature: Python makes you choose the conversion instead of silently producing a surprising result.",
            ),
        ],
        "Python could have required declarations everywhere or copied JavaScript-style coercion. It chooses dynamic behavior with strong runtime checks to keep code flexible without making bugs invisible.",
    ),
    c(
        "PY07",
        1,
        "Built-in Data Types Overview",
        ["PY01", "PY02", "PY03", "PY04"],
        "Python ships core numeric, text, binary, and singleton types because programs need stable building blocks before larger structures like lists and dictionaries make sense.",
        [
            "What `int`, `float`, `complex`, `bool`, `str`, `bytes`, and `NoneType` are for",
            "How to inspect size and type information",
            "Where floating-point surprises and singleton behavior come from",
        ],
        "These built-ins exist so common tasks have precise runtime meanings: whole numbers, approximate decimals, text, raw bytes, truth values, and the explicit absence of a value.",
        "small primitive object types -> combined later into larger structures",
        [
            ex(
                "Inspect several built-in types at once",
                "`type()`, `isinstance()`, and `sys.getsizeof()` reveal what kind of object you have and how much space the wrapper object itself consumes.",
                b('''
                import sys

                values = [42, 3.14, 2 + 3j, True, "text", b"text", None]
                for value in values:
                    print(repr(value), type(value), isinstance(value, object), sys.getsizeof(value))
                '''),
                "Every item is an object. Sizes vary, and `None` is still a real singleton object even though it means 'no useful value'.",
            ),
            ex(
                "Huge integers and floating-point surprise",
                "Python integers grow to arbitrary precision, while binary floating-point cannot represent many decimal fractions exactly.",
                b('''
                from decimal import Decimal
                import math

                giant = 10**100
                print(giant)
                print(0.1 + 0.2)
                print((0.1 + 0.2) == 0.3)
                print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
                print(math.isclose(0.1 + 0.2, 0.3))
                '''),
                "The huge integer works exactly. The float comparison fails because IEEE 754 stores an approximation. Use `Decimal` for decimal money rules or `math.isclose()` for tolerant comparisons.",
            ),
            ex(
                "`None` is a singleton",
                "There is exactly one `None` object, which is why identity tests are correct here.",
                b('''
                first = None
                second = None
                print(first is second)
                print(type(None))
                print(id(first), id(second))
                '''),
                "Both names point to the same singleton object, so `is` is the correct test for `None`.",
            ),
        ],
        "Python keeps these primitives distinct because pretending text, bytes, integers, and floats are interchangeable leads to subtle bugs, especially around encoding and numeric precision.",
    ),
    c(
        "PY08",
        1,
        "Operators",
        ["PY01", "PY02", "PY03", "PY04"],
        "Operators are compact syntax for common operations, but each operator still follows precise runtime rules about precedence, identity, membership, and short-circuit evaluation.",
        [
            "How arithmetic, comparison, logical, identity, membership, and assignment operators behave",
            "Why `is` and `==` are different questions",
            "Where short-circuiting and the walrus operator are useful",
        ],
        "Operators exist because some actions are so common that function-call syntax would be noisy, but compact syntax only works if you understand the exact question each operator asks.",
        "expression tree -> precedence decides grouping -> operands invoke object behavior -> result object returned",
        [
            ex(
                "Equality is not identity",
                "`==` asks whether values compare equal. `is` asks whether two names point to the same object.",
                b('''
                a = 256
                b = 256
                print(a == b, a is b)

                left = [1, 2]
                right = [1, 2]
                print(left == right, left is right)
                '''),
                "Small integers may be cached, so `a is b` can appear true. Lists with the same contents compare equal but are still different objects.",
            ),
            ex(
                "Short-circuit evaluation skips unnecessary work",
                "Logical operators stop as soon as the result is determined, which is useful for guards and dangerous if you forget about side effects.",
                b('''
                def trace(label, value):
                    print(label)
                    return value

                result = trace("left", False) and trace("right", True)
                print(result)
                result = trace("left again", True) or trace("right again", False)
                print(result)
                '''),
                "The second operand is skipped in both expressions once the result is already known.",
            ),
            ex(
                "Use the walrus operator for one-pass capture",
                "Added in Python 3.8, `:=` lets you bind and test a value in one expression when that genuinely improves clarity.",
                b('''
                data = ["", "alpha", "beta"]
                if (first_real := next((item for item in data if item), None)) is not None:
                    print(first_real)
                '''),
                "Use the walrus operator when it removes duplication, not when it makes a simple condition look cryptic.",
            ),
        ],
        "Python could have made operators perform more implicit coercion, but it keeps them explicit because operator-heavy bugs are hard to spot once the code gets dense.",
    ),
])

concepts.extend([
    c(
        "PY09",
        2,
        "Strings",
        ["PY05", "PY06", "PY07", "PY08"],
        "Strings model human-readable text, which is not the same thing as raw bytes. They are immutable sequences of Unicode code points.",
        [
            "How Unicode text differs from encoded bytes",
            "Why strings are immutable and how slicing and formatting work",
            "When to choose f-strings, `.format()`, `%`, raw strings, or multiline literals",
        ],
        "Text processing is everywhere, so Python separates text from bytes and makes string operations predictable instead of mixing encoding concerns into every line.",
        "Unicode text -> string object\nencode() -> bytes\ndecode() -> string again",
        [
            ex(
                "Encode and decode an emoji",
                "Unicode text is abstract; bytes are one possible encoded representation of that text.",
                b('''
                snake = "🐍"
                payload = snake.encode("utf-8")
                print(payload)
                print(payload.decode("utf-8"))
                '''),
                "UTF-8 turns the single character into multiple bytes. Decoding the same byte sequence returns the original string.",
            ),
            ex(
                "Formatting, slicing, and f-string debugging",
                "String operations stay readable because the type exposes common text tasks directly.",
                b('''
                name = "Ada"
                score = 91.234
                print(name[:2])
                print(f"{name:>8} | {score:.1f}")
                print(f"{score=}")
                print(r"c:\\new_folder\\notes.txt")
                '''),
                "Slicing returns a new string, f-strings can align and round values, and raw strings are handy when backslashes would otherwise be noisy.",
            ),
            ex(
                "Immutability and efficient joining",
                "Repeated concatenation inside a loop creates many temporary strings; joining a list is usually linear and clearer.",
                b('''
                parts = ["py", "thon", "-", "rocks"]
                joined = "".join(parts)
                print(joined)
                try:
                    joined[0] = "P"
                except TypeError as exc:
                    print(type(exc).__name__, exc)
                '''),
                "Strings cannot be mutated in place. Build pieces in a list and join them instead of repeatedly creating larger and larger temporary strings.",
            ),
        ],
        "Python could have blurred text and bytes into one type, but Python 3 deliberately separates them because encoding bugs are easier to fix when the distinction is explicit.",
    ),
    c(
        "PY10",
        2,
        "Lists",
        ["PY05", "PY06", "PY07", "PY08"],
        "Lists are mutable, ordered sequences that store references to objects rather than embedding the objects themselves.",
        [
            "How list mutability affects aliasing and slice assignment",
            "When comprehensions beat loops and when they do not",
            "Why copying nested lists requires more than `copy()`",
        ],
        "Programs need a resizable sequence for 'zero or more items'. Lists fill that role, trading memory overhead for flexible mutation and fast append behavior.",
        "list object -> array of references -> referenced objects elsewhere in memory",
        [
            ex(
                "Lists store references, not inline values",
                "This is why a list can hold mixed object types and why shallow copies still share nested objects.",
                b('''
                import sys
                from array import array

                values = [1, 2, 3, 4]
                packed = array('i', [1, 2, 3, 4])
                print(sys.getsizeof(values))
                print(sys.getsizeof(packed))
                '''),
                "The list usually has more overhead because it stores general-purpose object references. `array.array` is denser because it stores fixed-type machine values.",
            ),
            ex(
                "Comprehension, loop, and map can compute the same result",
                "All three forms work; choose the clearest one that matches the amount of logic involved.",
                b('''
                numbers = [1, 2, 3, 4]
                squares_loop = []
                for n in numbers:
                    squares_loop.append(n * n)
                squares_comp = [n * n for n in numbers]
                squares_map = list(map(lambda n: n * n, numbers))
                print(squares_loop, squares_comp, squares_map)
                '''),
                "The outputs match. Comprehensions are usually the sweet spot for simple transformations because they are both compact and readable.",
            ),
            ex(
                "Slice assignment can change length, and deep copy matters for nesting",
                "Lists are flexible enough that replacing a slice can grow or shrink the container.",
                b('''
                import copy

                values = [0, 1, 2, 3]
                values[1:3] = [10, 20, 30]
                print(values)

                nested = [[1], [2]]
                shallow = nested.copy()
                deep = copy.deepcopy(nested)
                shallow[0].append(99)
                print(nested, deep)
                '''),
                "After slice assignment the list has a new length. The shallow copy still shares inner lists, while the deep copy does not.",
            ),
        ],
        "If you need fixed-size homogeneous storage, a list is often the wrong tool. Python keeps lists general on purpose so everyday code stays simple.",
    ),
    c(
        "PY11",
        2,
        "Tuples",
        ["PY05", "PY06", "PY07", "PY08"],
        "Tuples are lightweight ordered sequences usually used for fixed-shape records, return values, and hashable grouping when their contents are immutable.",
        [
            "Why immutability makes tuples useful",
            "How packing and unpacking improve readability",
            "Why tuple contents can still reference mutable objects",
        ],
        "A fixed-shape container solves a different problem than a list: it communicates 'this set of positions belongs together and usually should not be resized'.",
        "tuple -> ordered references with fixed length\nmay still point at mutable inner objects",
        [
            ex(
                "Packing, unpacking, and starred capture",
                "Python uses tuples implicitly in many multiple-assignment situations.",
                b('''
                point = 10, 20
                x, y = point
                a, *middle, z = (1, 2, 3, 4, 5)
                print(point, x, y)
                print(a, middle, z)
                '''),
                "Commas create the tuple. Starred unpacking is useful when you care about the ends more than the exact middle length.",
            ),
            ex(
                "`namedtuple` gives field names to positions",
                "Plain tuples are compact but anonymous; `namedtuple` keeps the storage pattern while making the record self-describing.",
                b('''
                from collections import namedtuple

                User = namedtuple("User", ["name", "email"])
                user = User("Ada", "ada@example.com")
                print(user.name, user.email)
                '''),
                "Field names remove the 'what was index 1 again?' problem without needing a full custom class.",
            ),
            ex(
                "Tuple immutability does not freeze nested objects",
                "The tuple cannot be resized, but a mutable item stored inside it can still change.",
                b('''
                record = ("numbers", [1, 2, 3])
                record[1].append(4)
                print(record)

                cache = {(1, 2): "ok"}
                print(cache[(1, 2)])
                '''),
                "The tuple remains the same tuple, but the inner list mutates. Tuples can be dictionary keys only when all of their contents are hashable.",
            ),
        ],
        "Lists are better when shape changes frequently. Tuples are better when the positions have meaning and the record should stay structurally stable.",
    ),
    c(
        "PY12",
        2,
        "Dictionaries",
        ["PY05", "PY06", "PY07", "PY08"],
        "Dictionaries map hashable keys to values and preserve insertion order in modern Python.",
        [
            "How hashing lets key lookup stay fast on average",
            "When to use `dict[]`, `get()`, merging, and comprehensions",
            "Why `defaultdict` and JSON round-trips are common patterns",
        ],
        "Keyed lookup is fundamental because many real problems are not 'the third item in a list' but 'the setting named timeout' or 'the user with this email'.",
        "key -> hash -> slot lookup -> value reference\ncollisions handled internally by the dict implementation",
        [
            ex(
                "Basic lookups and insertion order",
                "Python 3.7+ guarantees that dictionaries remember insertion order, which makes many data-processing tasks more intuitive.",
                b('''
                settings = {"host": "db.local", "port": 5432, "ssl": True}
                print(settings["host"])
                print(list(settings.keys()))
                '''),
                "The key order prints in insertion order. That behavior started as an implementation detail and became a language guarantee in Python 3.7.",
            ),
            ex(
                "`get`, merge styles, and `defaultdict` grouping",
                "These tools remove noisy boilerplate around missing keys.",
                b('''
                from collections import defaultdict

                a = {"x": 1, "y": 2}
                b_map = {"y": 99, "z": 3}
                print(a.get("missing", 0))
                print(a | b_map)

                groups = defaultdict(list)
                for name, team in [("Ada", "blue"), ("Grace", "blue"), ("Linus", "green")]:
                    groups[team].append(name)
                print(dict(groups))
                '''),
                "`get` avoids `KeyError`, `a | b` returns a new merged dict in Python 3.9+, and `defaultdict` creates missing containers automatically.",
            ),
            ex(
                "JSON round-trip to and from a dictionary",
                "JSON maps neatly to Python dicts and lists, which is why dictionaries sit at the center of many APIs.",
                b('''
                import json

                payload = {"user": "Ada", "active": True, "roles": ["admin", "editor"]}
                raw = json.dumps(payload)
                print(raw)
                restored = json.loads(raw)
                print(restored["roles"])
                '''),
                "The dict becomes a JSON string and back again. Be careful with data types JSON does not support directly, such as datetime objects.",
            ),
        ],
        "Python could have offered only list-based lookups and forced manual searches, but hash maps are too central to everyday programming to omit.",
    ),
])

concepts.extend([
    c(
        "PY13",
        2,
        "Sets & Frozensets",
        ["PY05", "PY06", "PY07", "PY08"],
        "Sets store unique hashable items and make membership testing and set algebra concise and fast on average.",
        [
            "Why uniqueness and membership tests are the main set use cases",
            "How union, intersection, difference, and symmetric difference work",
            "When `frozenset` is useful because immutability makes it hashable",
        ],
        "Many problems are really about 'have I seen this before?' or 'what overlaps between these groups?' Sets express that directly instead of forcing linear scans through lists.",
        "set -> hash table of unique keys only\nno duplicates, no positional indexing",
        [
            ex(
                "Membership in a set versus a list",
                "Sets shine when existence checks matter more than order.",
                b('''
                names_list = ["ada", "grace", "guido", "linus"]
                names_set = {"ada", "grace", "guido", "linus"}
                print("guido" in names_list)
                print("guido" in names_set)
                '''),
                "Both tests return `True`, but the set is designed for fast membership lookup while the list checks item by item.",
            ),
            ex(
                "Set algebra reads like the problem statement",
                "Union, intersection, difference, and symmetric difference correspond directly to common reasoning patterns.",
                b('''
                backend = {"Ada", "Grace", "Linus"}
                devops = {"Grace", "Sam", "Linus"}
                print(backend | devops)
                print(backend & devops)
                print(backend - devops)
                print(backend ^ devops)
                '''),
                "`|` is union, `&` is intersection, `-` is difference, and `^` is symmetric difference: members in exactly one set.",
            ),
            ex(
                "`frozenset` can be a dictionary key",
                "A normal set is mutable and therefore unhashable. Freezing it makes it safe to use inside other hash-based structures.",
                b('''
                permissions = {
                    frozenset({"read", "write"}): "editor",
                    frozenset({"read"}): "viewer",
                }
                print(permissions[frozenset({"read"})])
                '''),
                "If you tried to use a normal set as the key, Python would raise `TypeError: unhashable type: 'set'`.",
            ),
        ],
        "Use a list when order and duplicates matter. Use a set when the core question is uniqueness or membership.",
    ),
    c(
        "PY14",
        2,
        "The Collections Module",
        ["PY05", "PY06", "PY07", "PY08"],
        "`collections` provides specialized containers for patterns that plain lists and dicts can represent but do not represent elegantly.",
        [
            "Why `deque`, `Counter`, `defaultdict`, `ChainMap`, and `OrderedDict` exist",
            "How specialized containers reduce boilerplate",
            "When named tuples are more expressive than raw tuples",
        ],
        "Specialized containers exist because general-purpose containers force you to re-implement the same patterns repeatedly: queues, counting, layered config, and stable reordering.",
        "general containers -> specialized wrappers tuned for common access patterns",
        [
            ex(
                "`deque` supports cheap appends at both ends",
                "A list is great for appending on the right but expensive for repeated inserts on the left.",
                b('''
                from collections import deque

                queue = deque(["b", "c"])
                queue.appendleft("a")
                queue.append("d")
                print(queue)
                '''),
                "`deque` is the right tool for queues, breadth-first search, and sliding windows.",
            ),
            ex(
                "`Counter` and `defaultdict` remove counting boilerplate",
                "These types map directly onto frequency analysis and grouped aggregation.",
                b('''
                from collections import Counter, defaultdict

                words = "to be or not to be".split()
                print(Counter(words).most_common(2))

                graph = defaultdict(list)
                graph["A"].append("B")
                graph["A"].append("C")
                print(dict(graph))
                '''),
                "`Counter` exposes counts as first-class data, and `defaultdict(list)` is the standard way to build adjacency lists.",
            ),
            ex(
                "`ChainMap` and `OrderedDict` for layered config and manual ordering",
                "Sometimes you need to search through several mappings as one logical view or move keys to represent recency.",
                b('''
                from collections import ChainMap, OrderedDict

                defaults = {"port": 8000, "debug": False}
                env = {"debug": True}
                cli = {"port": 9000}
                config = ChainMap(cli, env, defaults)
                print(config["port"], config["debug"])

                order = OrderedDict.fromkeys(["a", "b", "c"])
                order.move_to_end("a")
                print(list(order))
                '''),
                "`ChainMap` searches each mapping in order. `OrderedDict` is still handy when you need ordering operations such as `move_to_end`.",
            ),
        ],
        "You can always force these patterns into plain dicts and lists, but that usually produces more code and weaker intent.",
    ),
    c(
        "PY15",
        3,
        "Conditionals",
        ["PY05", "PY06", "PY07", "PY08"],
        "Conditionals choose between code paths based on truthy and falsy values, and modern Python also supports structural pattern matching with `match/case` (added in Python 3.10).",
        [
            "How `if/elif/else` and ternary expressions work",
            "When `match/case` is clearer than a long chain of comparisons",
            "Why nested ternaries become unreadable quickly",
        ],
        "Branching exists because programs react to state. The important question is not 'can I branch?' but 'what form makes the decision obvious to the next reader?'.",
        "condition -> truth test -> choose one branch\npattern matching -> compare shape and values -> bind pieces if matched",
        [
            ex(
                "Classic `if/elif/else` decision making",
                "Use this when you are evaluating unrelated conditions or simple thresholds.",
                b('''
                score = 87
                if score >= 90:
                    grade = "A"
                elif score >= 80:
                    grade = "B"
                else:
                    grade = "C or below"
                print(grade)
                '''),
                "Conditions are checked top to bottom until one succeeds. Order matters.",
            ),
            ex(
                "Pattern matching on structured input",
                "`match/case` shines when both the shape and the content of data matter.",
                b('''
                # Added in Python 3.10
                command = ("move", 3, 4)
                match command:
                    case ("move", x, y) if x >= 0 and y >= 0:
                        print(f"move to {x}, {y}")
                    case ("quit",):
                        print("stop")
                    case _:
                        print("unknown command")
                '''),
                "Pattern matching can unpack and validate in one place. Use `_` as the wildcard when nothing else matches.",
            ),
            ex(
                "A ternary is fine until it stops being readable",
                "The expression form is useful for short binary choices, not for dense nested business logic.",
                b('''
                age = 20
                status = "adult" if age >= 18 else "minor"
                print(status)
                '''),
                "Keep ternaries short. Once you feel tempted to nest them, switch back to a normal `if/elif/else` block.",
            ),
        ],
        "Pattern matching is powerful, but `if/elif` remains the best tool when the logic is just a few unrelated boolean checks.",
    ),
    c(
        "PY16",
        3,
        "Loops",
        ["PY05", "PY06", "PY07", "PY08"],
        "Python's `for` loop is really a foreach loop over an iterable, while `while` repeats until a condition becomes false.",
        [
            "Why Python's `for` loop is built on iteration rather than integer counters",
            "How `break`, `continue`, `pass`, and loop `else` behave",
            "Why `enumerate()` and `zip()` are more Pythonic than `range(len(...))`",
        ],
        "Loops exist because real work often means 'do this for every item' or 'keep trying until the state changes'. Python builds looping on the iterator protocol so one syntax can drive many container types.",
        "iterable -> iter() -> next() until StopIteration\nloop else runs only if no break happened",
        [
            ex(
                "`for` is a foreach loop",
                "You usually loop over values directly instead of managing indexes yourself.",
                b('''
                for name in ["Ada", "Grace", "Guido"]:
                    print(name)
                '''),
                "This reads like the problem statement: for each name, print it. No manual counter is needed.",
            ),
            ex(
                "The `else` clause means 'not broken out of'",
                "This is surprisingly useful in search patterns.",
                b('''
                target = 7
                for number in [1, 3, 5, 7, 9]:
                    if number == target:
                        print("found")
                        break
                else:
                    print("not found")
                '''),
                "Because the loop hits `break`, the `else` block is skipped. Remove the target and the `else` block runs.",
            ),
            ex(
                "Use `enumerate`, `zip`, and remember loop variables persist",
                "These helpers make coordinated iteration clearer than manual index math.",
                b('''
                names = ["Ada", "Grace"]
                scores = [98, 99]
                for index, (name, score) in enumerate(zip(names, scores), start=1):
                    print(index, name, score)
                print(name)
                '''),
                "After the loop, `name` still exists in Python. That surprises people coming from languages with tighter loop-variable scope.",
            ),
        ],
        "You can always force a counter-based loop, but Python prefers direct iteration because it matches the data model and eliminates many off-by-one bugs.",
    ),
])

concepts.extend([
    c(
        "PY17",
        3,
        "Comprehensions",
        ["PY05", "PY06", "PY07", "PY08"],
        "Comprehensions build lists, sets, and dicts from iterables with a compact transformation-and-filter syntax.",
        [
            "How list, dict, and set comprehensions map cleanly to simple loops",
            "When generator expressions save memory",
            "When a comprehension becomes too dense to be worth it",
        ],
        "Comprehensions exist because the pattern 'iterate, transform, maybe filter, append' is so common that spelling it with full loops adds noise when the logic is simple.",
        "input iterable -> expression applied per item -> optional filter -> new collection or lazy generator",
        [
            ex(
                "Equivalent loop and comprehension",
                "A comprehension is easiest to read when one expression and maybe one filter are enough.",
                b('''
                numbers = [1, 2, 3, 4, 5]
                odds_loop = []
                for n in numbers:
                    if n % 2:
                        odds_loop.append(n * 10)
                odds_comp = [n * 10 for n in numbers if n % 2]
                print(odds_loop, odds_comp)
                '''),
                "The outputs match. The comprehension removes boilerplate, but the logic is still simple enough to scan in one pass.",
            ),
            ex(
                "Set and dict comprehensions",
                "The pattern generalizes naturally beyond lists.",
                b('''
                words = ["Ada", "ada", "Grace"]
                lowered = {word.lower() for word in words}
                lengths = {word: len(word) for word in words}
                print(lowered)
                print(lengths)
                '''),
                "Set comprehensions automatically remove duplicates, and dict comprehensions let keys and values come from expressions.",
            ),
            ex(
                "Generator expressions are lazy",
                "Use a generator when you want to stream values instead of materializing them all immediately.",
                b('''
                numbers = (n * n for n in range(5))
                print(numbers)
                print(list(numbers))
                '''),
                "The generator prints as a generator object first because it has not computed all results yet. That saves memory for large pipelines.",
            ),
        ],
        "Once a comprehension contains deep nesting, side effects, or complicated branching, a normal loop is usually clearer and easier to debug.",
    ),
    c(
        "PY18",
        3,
        "Exception Handling",
        ["PY05", "PY06", "PY07", "PY08"],
        "Exceptions separate ordinary control flow from error paths so failures can travel up the call stack until code that understands the problem handles them.",
        [
            "How `try`, `except`, `else`, and `finally` fit together",
            "Why broad exception handling hides bugs",
            "How custom exceptions and chaining communicate causes clearly",
        ],
        "Programs fail in ways you cannot completely predict: missing files, bad input, network errors, logic mistakes. Exceptions let Python surface those failures without forcing every function to return error codes manually.",
        "normal path\ntry block -> exception? -> matching except -> optional else if none -> finally always runs",
        [
            ex(
                "`try/except/else/finally` in one place",
                "Each clause answers a different question: what might fail, what to do if it fails, what to do if it succeeds, and what must always happen.",
                b('''
                try:
                    value = int("42")
                except ValueError:
                    print("bad input")
                else:
                    print("parsed", value)
                finally:
                    print("cleanup happens")
                '''),
                "`else` runs only when no exception was raised. `finally` always runs, which is why it is useful for cleanup.",
            ),
            ex(
                "Exception chaining preserves the original cause",
                "`raise X from Y` keeps the debugging trail intact instead of discarding the lower-level failure.",
                b('''
                try:
                    int("not-a-number")
                except ValueError as exc:
                    raise RuntimeError("Could not parse user id") from exc
                '''),
                "The traceback will show both the original `ValueError` and the higher-level `RuntimeError`, which is much more informative than hiding the cause.",
            ),
            ex(
                "Custom hierarchy and the danger of broad catches",
                "Specific exceptions make error handling deliberate instead of vague.",
                b('''
                class DatabaseError(Exception):
                    pass

                class ConnectionError(DatabaseError):
                    pass

                class QueryError(DatabaseError):
                    pass

                try:
                    raise QueryError("bad SQL")
                except DatabaseError as exc:
                    print(type(exc).__name__, exc)
                '''),
                "Catching `DatabaseError` groups related application failures. Catching `Exception` everywhere would also swallow unrelated programming mistakes.",
            ),
        ],
        "Returning sentinel values for every failure quickly becomes noisy and easy to ignore. Exceptions keep the success path cleaner while preserving full error context.",
    ),
    c(
        "PY19",
        4,
        "Functions",
        ["PY03", "PY15", "PY16", "PY17", "PY18"],
        "Functions package behavior under a name, introduce a call stack frame, and return values explicitly or `None` implicitly.",
        [
            "How `def`, `return`, and the call stack fit together",
            "Why functions are first-class objects in Python",
            "Why mutable default arguments are evaluated once at definition time",
        ],
        "Functions exist so programs can name reusable behavior, test pieces independently, and compose larger systems without repeating the same steps line by line.",
        "call site -> new stack frame -> local names -> return value or None -> caller resumes",
        [
            ex(
                "A function returns `None` when you do not return explicitly",
                "Understanding the implicit default matters because `print(do_work())` often surprises beginners.",
                b('''
                def greet(name):
                    print(f"Hello, {name}")

                result = greet("Ada")
                print(result)
                '''),
                "The greeting prints first, then `None` prints because the function finished without an explicit `return`.",
            ),
            ex(
                "Functions are first-class objects",
                "You can store them, pass them around, and call them later because functions are objects too.",
                b('''
                def double(n):
                    return n * 2

                actions = [double]
                chosen = actions[0]
                print(chosen(21))
                '''),
                "The function lives in a list and is called through another name. That property underpins callbacks, decorators, and higher-order functions.",
            ),
            ex(
                "The mutable default argument trap",
                "Default arguments are evaluated once when the function is defined, not each time it is called.",
                b('''
                def append_item(item, bucket=[]):
                    bucket.append(item)
                    return bucket

                print(append_item("a"))
                print(append_item("b"))
                '''),
                "The second call reuses the same list. Fix this with a `None` default and create a new list inside the function.",
            ),
        ],
        "Functions do not replace every pattern. When behavior and state need to travel together, a class or closure can be the better abstraction.",
    ),
    c(
        "PY20",
        4,
        "Arguments Deep-Dive",
        ["PY03", "PY15", "PY16", "PY17", "PY18"],
        "Python supports positional, keyword, variadic, keyword-only, and positional-only parameters so APIs can control both flexibility and clarity.",
        [
            "The exact parameter-ordering rules in a function signature",
            "Why positional-only `/` and keyword-only `*` exist",
            "How call-site unpacking with `*` and `**` works",
        ],
        "Function signatures are contracts. Python gives you tools to make those contracts explicit so callers cannot accidentally rely on argument styles you never meant to support.",
        "call arguments -> matched left to right to parameters -> extra positional go to *args -> extra named go to **kwargs",
        [
            ex(
                "A signature using every major parameter kind",
                "This is the full grammar in one place: positional-only, regular positional-or-keyword, variadic positional, keyword-only, and variadic keyword.",
                b('''
                def api(version, /, resource, *parts, format="json", retries=3, **options):
                    return version, resource, parts, format, retries, options

                print(api("v1", "users", 10, 20, format="csv", timeout=5))
                '''),
                "Arguments before `/` must be positional. Arguments after `*parts` but before `**options` are keyword-only.",
            ),
            ex(
                "Positional-only parameters prevent fragile keyword usage",
                "Added in Python 3.8, `/` lets library authors reserve the freedom to rename parameters later.",
                b('''
                def divide(x, y, /):
                    return x / y

                print(divide(8, 2))
                try:
                    divide(x=8, y=2)
                except TypeError as exc:
                    print(type(exc).__name__, exc)
                '''),
                "The function works positionally and rejects keyword calls. That protects the API surface.",
            ),
            ex(
                "Unpack arguments at the call site",
                "`*` and `**` are useful on both sides of a function call.",
                b('''
                def greet(name, city, punctuation="!"):
                    print(f"Hello {name} from {city}{punctuation}")

                args = ["Ada", "London"]
                kwargs = {"punctuation": "?"}
                greet(*args, **kwargs)
                '''),
                "The sequence supplies positional arguments and the mapping supplies named arguments. This pattern is common in wrappers and adapters.",
            ),
        ],
        "More flexibility is not always better. Overusing `*args` and `**kwargs` can make APIs vague and hard for tools and humans to understand.",
    ),
])

concepts.extend([
    c(
        "PY21",
        4,
        "Scope & LEGB Rule",
        ["PY03", "PY15", "PY16", "PY17", "PY18"],
        "Python resolves names through the LEGB chain: Local, Enclosing, Global, Builtin.",
        [
            "How Python walks outward through scopes during name lookup",
            "Why closures capture names rather than snapshots of values",
            "When `global` and `nonlocal` are appropriate",
        ],
        "Scope rules exist so Python can decide which object a name should refer to without forcing every reference to be fully qualified.",
        "Local -> Enclosing -> Global -> Builtin\nfirst matching name wins",
        [
            ex(
                "Name lookup follows LEGB",
                "A nested function checks its own locals first, then outer function locals, then module globals, then builtins.",
                b('''
                label = "global"

                def outer():
                    label = "enclosing"
                    def inner():
                        print(label)
                    inner()

                outer()
                '''),
                "`inner` prints `enclosing` because it finds the name in the nearest enclosing scope before it ever considers the global name.",
            ),
            ex(
                "Loop-variable closure trap and the default-argument fix",
                "Closures capture the variable, not its value at each iteration.",
                b('''
                funcs = []
                for n in range(3):
                    funcs.append(lambda n=n: n)
                print([f() for f in funcs])
                '''),
                "Without `n=n`, every lambda would use the final loop value. Binding the current value into a default argument captures the value you intended.",
            ),
            ex(
                "Use `nonlocal` to update an enclosing name",
                "`nonlocal` is the closure-friendly tool for stateful function factories.",
                b('''
                def make_counter():
                    count = 0
                    def increment():
                        nonlocal count
                        count += 1
                        return count
                    return increment

                counter = make_counter()
                print(counter(), counter(), counter())
                '''),
                "The inner function updates the binding from the enclosing function instead of creating a new local variable.",
            ),
        ],
        "Global state is easy to reach but hard to reason about. Closures and explicit arguments are usually safer than reaching for `global` by default.",
    ),
    c(
        "PY22",
        4,
        "Lambda Functions",
        ["PY03", "PY15", "PY16", "PY17", "PY18"],
        "A `lambda` creates a small anonymous function expression with a single expression body.",
        [
            "What lambdas are good for and where they stop",
            "Why lambdas cannot contain statements",
            "Why named functions are better once behavior grows",
        ],
        "Lambdas exist so tiny functions can be written inline at the point of use, but Python keeps them intentionally limited so they do not turn into unreadable mini-programs.",
        "lambda parameters: expression -> function object\nno statements, only one expression result",
        [
            ex(
                "A lambda used as a sorting key",
                "This is the most common and idiomatic use case: a tiny transformation at the call site.",
                b('''
                people = [{"name": "Ada", "age": 36}, {"name": "Grace", "age": 85}]
                print(sorted(people, key=lambda person: person["age"]))
                '''),
                "The lambda is short, local, and obvious. A named helper would add indirection without adding clarity here.",
            ),
            ex(
                "Lambdas are still normal function objects",
                "They can be passed around like any other callable.",
                b('''
                operations = [lambda x: x + 1, lambda x: x * 2]
                print([op(10) for op in operations])
                '''),
                "Both lambdas behave like ordinary functions, but they do not carry helpful names in tracebacks or documentation.",
            ),
            ex(
                "Named functions win once logic gets interesting",
                "The limitation to expressions is deliberate. Branching, assertions, and richer documentation belong in a real `def`.",
                b('''
                def normalize(name):
                    name = name.strip().title()
                    if not name:
                        raise ValueError("empty name")
                    return name

                print(normalize("  ada  "))
                '''),
                "You could not express that validation cleanly in a lambda. A named function is easier to test, debug, and reuse.",
            ),
        ],
        "Use lambdas for tiny one-off callables. The moment you need comments, branching, or a meaningful name, switch to `def`.",
    ),
    c(
        "PY23",
        4,
        "Higher-Order Functions",
        ["PY03", "PY15", "PY16", "PY17", "PY18"],
        "Higher-order functions accept functions, return functions, or both. Python uses that idea throughout the standard library.",
        [
            "How `map`, `filter`, `reduce`, `sorted(key=...)`, and `partial` fit one model",
            "Why caching is also a higher-order function pattern",
            "When `operator` helpers beat tiny lambdas",
        ],
        "Once functions are first-class, you can parameterize behavior itself instead of hard-coding every decision into one giant function.",
        "callable in -> wrapper or transformed result out",
        [
            ex(
                "Re-implement a tiny `map`",
                "This proves that 'apply a function to each item' is just a pattern, not magic.",
                b('''
                def my_map(func, items):
                    result = []
                    for item in items:
                        result.append(func(item))
                    return result

                print(my_map(lambda x: x * 2, [1, 2, 3]))
                '''),
                "Understanding the loop underneath makes `map()` much less mysterious.",
            ),
            ex(
                "`partial` preconfigures a function",
                "This is useful when you want a specialized callable without subclassing or writing a wrapper by hand.",
                b('''
                from functools import partial

                def power(base, exponent):
                    return base ** exponent

                square = partial(power, exponent=2)
                print(square(9))
                '''),
                "`square` is a new callable with one argument already fixed.",
            ),
            ex(
                "Caching turns expensive pure calls into fast repeated lookups",
                "`lru_cache` wraps a function and remembers previous results based on arguments.",
                b('''
                from functools import lru_cache

                @lru_cache(maxsize=None)
                def fib(n):
                    return n if n < 2 else fib(n - 1) + fib(n - 2)

                print(fib(20))
                print(fib.cache_info())
                '''),
                "The first call computes many subproblems; later repeated calls reuse cached answers.",
            ),
        ],
        "Higher-order tools are powerful, but a straightforward loop is often clearer when the transformation or filtering logic is long.",
    ),
    c(
        "PY24",
        4,
        "Recursion",
        ["PY03", "PY15", "PY16", "PY17", "PY18"],
        "Recursion solves a problem by reducing it to smaller versions of the same problem until a base case stops the chain.",
        [
            "How recursive calls create a stack of frames",
            "Why a missing base case or too much depth fails in CPython",
            "How memoization and explicit stacks compare",
        ],
        "Some problems are naturally self-similar: tree traversal, directory walking, recursive descent parsing. Recursion mirrors that structure directly.",
        "call n -> call n-1 -> call n-2 ... until base case\nreturns unwind in reverse order",
        [
            ex(
                "Factorial with a base case",
                "This is the classic shape of a recursive function: base case plus smaller recursive call.",
                b('''
                def factorial(n):
                    if n == 0:
                        return 1
                    return n * factorial(n - 1)

                print(factorial(5))
                '''),
                "Picture the stack frames piling up until `n == 0`, then returning 1, 1*1, 2*1, 3*2, and so on back out.",
            ),
            ex(
                "Memoization avoids repeated work",
                "Naive recursion often recomputes the same subproblems many times.",
                b('''
                from functools import lru_cache

                @lru_cache(maxsize=None)
                def fib(n):
                    return n if n < 2 else fib(n - 1) + fib(n - 2)

                print(fib(30))
                '''),
                "Caching makes recursive Fibonacci practical by turning repeated overlapping calls into lookups.",
            ),
            ex(
                "An explicit stack can replace recursion",
                "CPython does not optimize tail recursion away, so an iterative version is sometimes safer for deep inputs.",
                b('''
                def factorial_iterative(n):
                    stack = list(range(1, n + 1))
                    result = 1
                    while stack:
                        result *= stack.pop()
                    return result

                print(factorial_iterative(5))
                '''),
                "The explicit stack lives in Python data rather than the call stack, which avoids recursion-limit problems for some patterns.",
            ),
        ],
        "Recursion is elegant when the structure is recursive. It is a poor fit when iterative code is flatter, clearer, or guaranteed to avoid deep call stacks.",
    ),
])

concepts.extend([
    c(
        "PY25",
        5,
        "Classes & Objects",
        ["PY19", "PY20", "PY21", "PY22", "PY23", "PY24"],
        "Classes define how new objects should be built, while each object stores its own state and can expose behavior through methods.",
        [
            "How class bodies execute and produce class objects",
            "Why `self` refers to the receiving instance",
            "How instance and class attributes participate in lookup",
        ],
        "Once functions alone stop being enough, you need a way to keep related state and behavior together. Classes are Python's built-in tool for that job.",
        "class statement runs -> class object created -> calling class makes instance -> method call passes instance as self",
        [
            ex(
                "A complete `BankAccount` class",
                "This is the common shape of a class: initializer, instance state, and methods that operate on that state.",
                b('''
                class BankAccount:
                    bank_name = "Python Credit Union"

                    def __init__(self, owner, balance=0):
                        self.owner = owner
                        self.balance = balance

                    def deposit(self, amount):
                        self.balance += amount
                        return self.balance

                account = BankAccount("Ada", 100)
                print(account.owner, account.deposit(25))
                '''),
                "Each instance gets its own `owner` and `balance`, while `bank_name` lives on the class and is shared unless an instance overrides it.",
            ),
            ex(
                "Class body execution is real code",
                "A class statement is not just metadata. Python executes the body to build the namespace for the new class.",
                b('''
                class Demo:
                    print("class body executing")
                    label = "ready"

                print(Demo.label)
                '''),
                "The print inside the class body runs immediately when Python defines the class, not later when you create an instance.",
            ),
            ex(
                "Attribute lookup checks the instance before the class",
                "That lookup chain explains why class attributes act like defaults.",
                b('''
                class Counter:
                    step = 1

                first = Counter()
                second = Counter()
                second.step = 5
                print(first.step, second.step, Counter.step)
                '''),
                "`first.step` falls back to the class attribute. `second.step` finds an instance attribute of the same name first.",
            ),
        ],
        "A plain function plus a dict can sometimes be enough. Reach for a class when the relationship between state and behavior is central, not incidental.",
    ),
    c(
        "PY26",
        5,
        "The Object Model",
        ["PY19", "PY20", "PY21", "PY22", "PY23", "PY24"],
        "In Python, everything is an object: numbers, strings, functions, classes, modules, and instances all have identity, type, and behavior.",
        [
            "Why `id()`, `type()`, and `is` belong together",
            "How reference counting and cyclic garbage collection interact in CPython",
            "Why object identity is separate from object equality",
        ],
        "The object model matters because Python exposes it directly. Many advanced features are just ordinary object operations once you see that everything participates in the same system.",
        "object -> identity + type + attributes\nCPython tracks references and runs cyclic GC for loops of references",
        [
            ex(
                "Numbers, functions, classes, and modules are all objects",
                "The model is uniform, which is why introspection feels natural in Python.",
                b('''
                import math

                def greet():
                    return "hi"

                for thing in [42, "text", greet, list, math]:
                    print(type(thing), getattr(thing, "__class__", None))
                '''),
                "Each item has a type because each item is an object. That includes the function and the module.",
            ),
            ex(
                "Reference counting is visible",
                "CPython keeps an immediate count of references to many objects.",
                b('''
                import sys

                value = []
                alias = value
                print(sys.getrefcount(value))
                '''),
                "The exact number is implementation-dependent because the function call itself adds a temporary reference, but the count changes when names start or stop pointing to the object.",
            ),
            ex(
                "Cycles require the garbage collector",
                "Reference counts alone cannot free objects that keep each other alive in a loop.",
                b('''
                import gc

                a = []
                b_ref = [a]
                a.append(b_ref)
                print(gc.isenabled())
                print(gc.collect())
                '''),
                "The cyclic GC complements reference counting by finding unreachable cycles that simple counters cannot break on their own.",
            ),
        ],
        "Identity questions (`is`) are narrower than equality questions (`==`). Use identity only when you truly care about sameness of object, such as with `None` or shared sentinels.",
    ),
    c(
        "PY27",
        5,
        "Inheritance",
        ["PY19", "PY20", "PY21", "PY22", "PY23", "PY24"],
        "Inheritance lets one class reuse and specialize behavior from another, and Python resolves multiple inheritance with the C3 method resolution order.",
        [
            "How single and multiple inheritance differ",
            "Why `super()` follows the MRO instead of 'just call my parent'",
            "When composition is simpler than inheritance",
        ],
        "Inheritance exists because some abstractions are genuine specializations of others, but Python gives you both inheritance and composition because reuse alone is not enough to justify an inheritance tree.",
        "class -> __mro__ tuple decides lookup order\nsuper() walks that order cooperatively",
        [
            ex(
                "Simple inheritance and override",
                "A subclass can reuse behavior and then extend or replace parts of it.",
                b('''
                class Animal:
                    def speak(self):
                        return "sound"

                class Dog(Animal):
                    def speak(self):
                        return "woof"

                print(Dog().speak())
                '''),
                "`Dog` inherits from `Animal` but overrides `speak` with more specific behavior.",
            ),
            ex(
                "Diamond inheritance and MRO",
                "Python uses C3 linearization so multiple inheritance still has one deterministic lookup order.",
                b('''
                class A: pass
                class B(A): pass
                class C(A): pass
                class D(B, C): pass
                print(D.__mro__)
                '''),
                "The MRO shows the order Python will follow when it looks for attributes. This is why `super()` is about the next class in MRO, not a hard-coded parent name.",
            ),
            ex(
                "Composition often wins",
                "If one object mainly needs another object to do its job, composition is usually simpler than subclassing.",
                b('''
                class Engine:
                    def start(self):
                        return "engine on"

                class Car:
                    def __init__(self):
                        self.engine = Engine()

                print(Car().engine.start())
                '''),
                "`Car` is not a kind of `Engine`; it has an `Engine`. That 'has-a' relationship is a strong sign that composition is the right tool.",
            ),
        ],
        "Use inheritance when the subtype relationship is real and cooperative method dispatch adds value. Use composition when you mainly want to assemble behavior.",
    ),
    c(
        "PY28",
        5,
        "Encapsulation",
        ["PY19", "PY20", "PY21", "PY22", "PY23", "PY24"],
        "Python prefers conventions and properties over hard privacy barriers, using naming conventions and descriptors to guide access.",
        [
            "What `_name` and `__name` really mean",
            "How `@property` provides computed access and validation",
            "Why `__slots__` can reduce per-instance memory",
        ],
        "Encapsulation exists to protect invariants and communicate intended use. Python chooses social and technical tools together instead of pretending enforcement is absolute.",
        "public name -> normal attribute\n_single -> internal convention\n__double -> name-mangled to reduce accidental clashes",
        [
            ex(
                "Name mangling is not true privacy",
                "Double-leading underscores mainly prevent accidental attribute collisions in subclasses.",
                b('''
                class SecretBox:
                    def __init__(self):
                        self.__token = "abc123"

                box = SecretBox()
                print(getattr(box, "_SecretBox__token"))
                '''),
                "The attribute is still reachable because name mangling changes the external attribute name; it does not create an impenetrable wall.",
            ),
            ex(
                "`@property` can validate writes",
                "Properties let an attribute-like API enforce rules without changing the call site into a method call.",
                b('''
                class Temperature:
                    def __init__(self, celsius):
                        self.celsius = celsius

                    @property
                    def celsius(self):
                        return self._celsius

                    @celsius.setter
                    def celsius(self, value):
                        if value < -273.15:
                            raise ValueError("below absolute zero")
                        self._celsius = value
                print(Temperature(20).celsius)
                '''),
                "Callers use attribute syntax, but the setter enforces the invariant.",
            ),
            ex(
                "`__slots__` removes the instance dictionary",
                "When you will create many tiny objects, slots can save memory by fixing the allowed attribute set.",
                b('''
                class Plain:
                    def __init__(self):
                        self.x = 1
                        self.y = 2

                class Slotted:
                    __slots__ = ("x", "y")
                    def __init__(self):
                        self.x = 1
                        self.y = 2

                print(hasattr(Plain(), "__dict__"), hasattr(Slotted(), "__dict__"))
                '''),
                "The slotted instance usually has no per-instance `__dict__`. That saves memory at the cost of flexibility.",
            ),
        ],
        "Python avoids rigid access modifiers because conventions plus properties are often enough, and strict barriers would clash with introspection-heavy workflows.",
    ),
])

concepts.extend([
    c(
        "PY29",
        5,
        "Dunder / Magic Methods",
        ["PY19", "PY20", "PY21", "PY22", "PY23", "PY24"],
        "Dunder methods let your classes participate in Python syntax and built-ins by implementing agreed-upon protocol hooks.",
        [
            "How operators and built-ins dispatch to special methods",
            "Which dunder methods control printing, iteration, comparison, arithmetic, and context management",
            "Why dunder methods should preserve user expectations",
        ],
        "These hooks exist so your objects can feel native in the language instead of forcing every interaction through ad hoc method names.",
        "built-in syntax -> Python looks for matching dunder method -> your object supplies behavior",
        [
            ex(
                "A `Vector` with arithmetic and representation hooks",
                "This one class can integrate with `print`, `repr`, `len`, iteration, containment, equality, hashing, calls, and operators.",
                b('''
                class Vector:
                    def __init__(self, *values):
                        self.values = tuple(values)
                    def __repr__(self):
                        return f"Vector{self.values!r}"
                    def __str__(self):
                        return f"<{', '.join(map(str, self.values))}>"
                    def __len__(self):
                        return len(self.values)
                    def __iter__(self):
                        return iter(self.values)
                    def __getitem__(self, index):
                        return self.values[index]
                    def __contains__(self, item):
                        return item in self.values
                    def __call__(self):
                        return sum(self.values)
                    def __add__(self, other):
                        return Vector(*(a + b for a, b in zip(self.values, other.values)))
                    def __mul__(self, scalar):
                        return Vector(*(scalar * v for v in self.values))
                    __rmul__ = __mul__
                    def __abs__(self):
                        return sum(v * v for v in self.values) ** 0.5
                    def __eq__(self, other):
                        return self.values == other.values
                    def __hash__(self):
                        return hash(self.values)

                v = Vector(1, 2)
                print(repr(v), str(v), len(v), abs(v), 2 * v, v())
                '''),
                "Each operation routes through a matching dunder. That is how your class plugs into core language syntax.",
            ),
            ex(
                "Iteration and indexing come from protocols, not special treatment",
                "Built-ins like `for` and `in` depend on these hooks.",
                b('''
                v = Vector(3, 4, 5)
                print(list(v))
                print(v[1])
                print(4 in v)
                '''),
                "Because the class implements iteration and item access, it behaves naturally in loops and membership checks.",
            ),
            ex(
                "Context management uses dunders too",
                "`with` dispatches to `__enter__` and `__exit__` exactly the same way operators dispatch to arithmetic dunders.",
                b('''
                class Session:
                    def __enter__(self):
                        print("open")
                        return self
                    def __exit__(self, exc_type, exc, tb):
                        print("close")
                        return False

                with Session() as session:
                    print("using session")
                '''),
                "The resource opens on entry and closes on exit, even though the `with` statement itself looks like special syntax.",
            ),
        ],
        "Only implement dunder methods that make semantic sense. A surprising `__len__` or `__eq__` is worse than omitting the hook.",
    ),
    c(
        "PY30",
        5,
        "Abstract Base Classes and Protocols",
        ["PY19", "PY20", "PY21", "PY22", "PY23", "PY24"],
        "Abstract base classes define nominal interfaces, while protocols describe structural expectations that any compatible object can satisfy.",
        [
            "How `ABC` and `@abstractmethod` enforce nominal contracts",
            "Why `Protocol` fits duck-typed code better",
            "What `@runtime_checkable` changes",
        ],
        "Interfaces matter because larger programs need shared expectations about behavior, but Python offers both explicit inheritance and structural compatibility depending on the style of code you want.",
        "ABC -> class must inherit and implement\nProtocol -> object only needs matching methods/attributes",
        [
            ex(
                "An abstract base class defines required methods",
                "ABCs are useful when you want explicit participation in a hierarchy.",
                b('''
                from abc import ABC, abstractmethod

                class Shape(ABC):
                    @abstractmethod
                    def area(self):
                        raise NotImplementedError

                class Square(Shape):
                    def __init__(self, side):
                        self.side = side
                    def area(self):
                        return self.side ** 2

                print(Square(4).area())
                '''),
                "Trying to instantiate `Shape` directly would fail because its abstract contract is incomplete.",
            ),
            ex(
                "A protocol checks for structure",
                "Protocols let unrelated classes cooperate if they provide the required methods.",
                b('''
                from typing import Protocol, runtime_checkable

                @runtime_checkable
                class Drawable(Protocol):
                    def draw(self) -> str: ...

                class Icon:
                    def draw(self) -> str:
                        return "icon"

                print(isinstance(Icon(), Drawable))
                '''),
                "`Icon` never inherited from `Drawable`, but it still satisfies the protocol because it has the expected method.",
            ),
            ex(
                "Protocols fit duck typing naturally",
                "They document expectations without forcing a central base class into every design.",
                b('''
                def render(item: Drawable) -> None:
                    print(item.draw())

                render(Icon())
                '''),
                "This style works well in Python because many APIs care about behavior, not family tree membership.",
            ),
        ],
        "Choose ABCs when explicit hierarchy membership matters. Choose protocols when you want interface documentation that still respects duck typing.",
    ),
    c(
        "PY31",
        5,
        "Dataclasses",
        ["PY19", "PY20", "PY21", "PY22", "PY23", "PY24"],
        "Dataclasses generate repetitive class machinery such as `__init__`, `__repr__`, and comparisons for classes that are mainly structured data.",
        [
            "When a dataclass is better than a plain class or named tuple",
            "How `field()` and `default_factory` handle defaults safely",
            "Why `frozen=True` and `slots=True` matter",
        ],
        "A lot of classes are mostly data containers with validation. Dataclasses remove the boilerplate so you can focus on the fields and invariants instead of hand-writing the same methods every time.",
        "field declarations -> generated methods -> optional post-init validation and transforms",
        [
            ex(
                "A basic dataclass",
                "The decorator generates initializer and representation methods automatically.",
                b('''
                from dataclasses import dataclass

                @dataclass
                class User:
                    name: str
                    active: bool = True

                print(User("Ada"))
                '''),
                "This is ideal when the class is mostly state with little custom behavior.",
            ),
            ex(
                "Use `default_factory` instead of a mutable default",
                "Dataclasses share the same 'evaluate once' default rule as normal functions, so mutable defaults still need special handling.",
                b('''
                from dataclasses import dataclass, field

                @dataclass
                class Team:
                    members: list[str] = field(default_factory=list)

                team = Team()
                team.members.append("Ada")
                print(team)
                '''),
                "`default_factory` creates a fresh list per instance, avoiding the classic shared-mutable-default bug.",
            ),
            ex(
                "`__post_init__`, `frozen`, and `slots`",
                "Dataclasses still let you validate and derive fields after automatic initialization.",
                b('''
                from dataclasses import dataclass, field

                @dataclass(frozen=True, slots=True)
                class Product:
                    name: str
                    price: float
                    label: str = field(init=False)
                    def __post_init__(self):
                        object.__setattr__(self, "label", f"{self.name}:{self.price:.2f}")

                print(Product("Book", 9.99).label)
                '''),
                "`frozen=True` makes the instance hash-friendly and immutable in spirit, while `slots=True` can reduce memory overhead.",
            ),
        ],
        "Dataclasses are not mandatory. If behavior dominates over stored fields, a regular class is often clearer. If you need tuple-like compactness, `namedtuple` can still be enough.",
    ),
])

concepts.extend([
    c(
        "PY32",
        6,
        "The Iterator Protocol",
        ["PY24", "PY29"],
        "An iterator is any object that returns itself or another iterator from `__iter__()` and produces items from `__next__()` until it raises `StopIteration`.",
        [
            "How `for` loops desugar to `iter()` and `next()`",
            "Why `StopIteration` signals normal exhaustion",
            "How to build a custom iterable from scratch",
        ],
        "Iteration exists so one loop syntax can consume lists, files, generators, custom classes, and more without hard-coding a container type into the language.",
        "iterable -> iter() returns iterator -> repeated next() calls -> StopIteration ends the loop",
        [
            ex(
                "A custom `Range` iterator",
                "This shows the minimum protocol a `for` loop needs.",
                b('''
                class Range:
                    def __init__(self, start, stop):
                        self.current = start
                        self.stop = stop
                    def __iter__(self):
                        return self
                    def __next__(self):
                        if self.current >= self.stop:
                            raise StopIteration
                        value = self.current
                        self.current += 1
                        return value

                print(list(Range(2, 5)))
                '''),
                "Once `StopIteration` is raised, the loop ends normally rather than treating exhaustion as an error.",
            ),
            ex(
                "A `for` loop desugars to `iter()` plus `next()`",
                "The friendly syntax is just a wrapper around the iterator protocol.",
                b('''
                items = [10, 20, 30]
                iterator = iter(items)
                while True:
                    try:
                        print(next(iterator))
                    except StopIteration:
                        break
                '''),
                "This manual loop is what `for item in items` conceptually hides for you.",
            ),
            ex(
                "An iterable can return a separate iterator object",
                "Many containers are iterable without being their own iterator.",
                b('''
                text = "abc"
                iterator = iter(text)
                print(next(iterator), next(iterator), next(iterator))
                '''),
                "Strings are iterable, but the string itself is not advanced in place; the iterator object tracks progress.",
            ),
        ],
        "Implement the protocol only when you need custom iteration behavior. For one-off lazy sequences, generators are usually simpler.",
    ),
    c(
        "PY33",
        6,
        "Generators",
        ["PY24", "PY29"],
        "Generators produce values lazily with `yield`, suspending and resuming execution instead of building all results eagerly.",
        [
            "Why lazy evaluation saves memory",
            "How `yield` and `yield from` work",
            "Where generator expressions fit into data pipelines",
        ],
        "Generators exist because many sequences are too large, too slow, or even infinite to materialize all at once.",
        "generator function call -> generator object\nnext() resumes until next yield or StopIteration",
        [
            ex(
                "An infinite Fibonacci generator",
                "Lazy generation means the sequence can conceptually continue forever.",
                b('''
                def fib():
                    a, b = 0, 1
                    while True:
                        yield a
                        a, b = b, a + b

                stream = fib()
                print([next(stream) for _ in range(7)])
                '''),
                "The generator only computes as many numbers as the caller asks for.",
            ),
            ex(
                "`yield from` delegates to a sub-generator",
                "This lets one generator compose another without manual nested loops.",
                b('''
                def letters():
                    yield from "abc"

                print(list(letters()))
                '''),
                "Delegation is especially useful in recursive traversals and pipeline-style code.",
            ),
            ex(
                "Generators keep memory use low",
                "A list of a million numbers allocates the whole result; a generator only stores its current state.",
                b('''
                numbers = (n * n for n in range(1_000_000))
                print(numbers)
                print(next(numbers), next(numbers), next(numbers))
                '''),
                "The generator object is tiny compared with a full million-item list because values are produced on demand.",
            ),
        ],
        "If you need random access, repeated traversal, or the full data set immediately, a list may still be the better tool.",
    ),
    c(
        "PY34",
        6,
        "Coroutines Basics via Generators",
        ["PY24", "PY29"],
        "Before `async`/`await`, generator methods like `send`, `throw`, and `close` showed that suspended functions could also receive data and exceptions.",
        [
            "How generator coroutines differ from simple pull-based iteration",
            "What `send()`, `throw()`, and `close()` do",
            "Why this model set the stage for `asyncio`",
        ],
        "These generator capabilities matter because they prove a paused computation can be resumed from the outside, which is the conceptual bridge toward modern asynchronous programming.",
        "caller resumes suspended frame with data or exception -> coroutine handles it -> yields control again",
        [
            ex(
                "Receive data with `send()`",
                "A coroutine can wait at `yield` and accept a value from the caller when resumed.",
                b('''
                def accumulator():
                    total = 0
                    while True:
                        value = yield total
                        total += value

                coro = accumulator()
                print(next(coro))
                print(coro.send(5))
                print(coro.send(7))
                '''),
                "The coroutine yields its current total, then receives the next value through `send`.",
            ),
            ex(
                "Inject an exception with `throw()`",
                "External code can resume the suspended coroutine by raising into it.",
                b('''
                def worker():
                    try:
                        yield "ready"
                    except ValueError:
                        yield "recovered"

                coro = worker()
                print(next(coro))
                print(coro.throw(ValueError("boom")))
                '''),
                "`throw()` enters the coroutine at the suspension point, just as if the exception happened inside it.",
            ),
            ex(
                "A tiny cooperative scheduler idea",
                "Multiple generators can be resumed round-robin, which hints at how asynchronous schedulers work.",
                b('''
                def task(name):
                    for step in range(2):
                        yield f"{name}:{step}"

                tasks = [task("A"), task("B")]
                for generator in list(tasks):
                    for message in generator:
                        print(message)
                '''),
                "Modern `asyncio` is more powerful, but the core idea is the same: pause and resume units of work cooperatively.",
            ),
        ],
        "Today you should usually write new asynchronous code with `async`/`await`, but generator coroutines explain the historical model underneath.",
    ),
    c(
        "PY35",
        7,
        "Decorators",
        ["PY21", "PY25", "PY29"],
        "A decorator takes a callable or class, wraps or transforms it, and returns the replacement object bound to the original name.",
        [
            "How wrapper functions use closures and `@wraps`",
            "Why decorator stacking applies from the inside out",
            "How decorators with arguments differ from simple decorators",
        ],
        "Decorators exist because cross-cutting behavior like timing, retries, caching, logging, or access control should not require copy-pasting the same scaffolding into every function.",
        "target function -> decorator receives target -> returns wrapper -> original name now points at wrapper",
        [
            ex(
                "A simple timing decorator",
                "The wrapper adds behavior before and after the original function call.",
                b('''
                import functools
                import time

                def timer(func):
                    @functools.wraps(func)
                    def wrapper(*args, **kwargs):
                        start = time.perf_counter()
                        result = func(*args, **kwargs)
                        print(time.perf_counter() - start)
                        return result
                    return wrapper
                '''),
                "`@wraps` preserves metadata like the original function name and docstring.",
            ),
            ex(
                "A decorator with arguments",
                "A decorator factory returns the actual decorator when configuration is needed.",
                b('''
                import functools

                def retry(times):
                    def decorate(func):
                        @functools.wraps(func)
                        def wrapper(*args, **kwargs):
                            last_error = None
                            for _ in range(times):
                                try:
                                    return func(*args, **kwargs)
                                except Exception as exc:
                                    last_error = exc
                            raise last_error
                        return wrapper
                    return decorate
                '''),
                "The outer function handles configuration and the inner function wraps the target.",
            ),
            ex(
                "Decorator stack order",
                "`@A` above `@B` means `A(B(func))`, so the lower decorator runs closest to the original function.",
                b('''
                def A(func):
                    def wrapper():
                        print("A before")
                        func()
                        print("A after")
                    return wrapper

                def B(func):
                    def wrapper():
                        print("B before")
                        func()
                        print("B after")
                    return wrapper
                '''),
                "Mentally expand stacked decorators as nested function calls to predict execution order.",
            ),
        ],
        "Decorators are elegant for reusable wrapping behavior, but if the wrapper logic becomes hard to debug, a plain function call or explicit helper object may be clearer.",
    ),
])

concepts.extend([
    c(
        "PY36",
        7,
        "Context Managers",
        ["PY21", "PY25", "PY29"],
        "Context managers pair setup with guaranteed cleanup, usually through the `with` statement and the `__enter__`/`__exit__` protocol.",
        [
            "Why `with` is safer than manual setup and teardown",
            "How class-based and generator-based context managers differ",
            "When `ExitStack` helps with dynamic resource counts",
        ],
        "Resource lifetimes are easy to get wrong when cleanup must happen even on exceptions. Context managers put that cleanup rule in one place.",
        "with target as name -> __enter__ runs -> block executes -> __exit__ runs even on exception",
        [
            ex(
                "A class-based context manager",
                "This is the raw protocol behind file objects and many library resources.",
                b('''
                class Timer:
                    def __enter__(self):
                        print("start")
                        return self
                    def __exit__(self, exc_type, exc, tb):
                        print("stop")
                        return False

                with Timer():
                    print("work")
                '''),
                "`__exit__` runs whether the block succeeds or fails, which is why context managers are so good for cleanup.",
            ),
            ex(
                "A generator-based context manager",
                "`contextlib.contextmanager` lets you write setup before the `yield` and cleanup after it.",
                b('''
                from contextlib import contextmanager

                @contextmanager
                def managed(name):
                    print("open", name)
                    try:
                        yield name
                    finally:
                        print("close", name)

                with managed("db") as handle:
                    print(handle)
                '''),
                "The code after `yield` always runs on exit, mirroring a `finally` block.",
            ),
            ex(
                "`ExitStack` manages a dynamic number of contexts",
                "When you do not know the resource count ahead of time, nesting `with` statements manually is awkward.",
                b('''
                from contextlib import ExitStack

                with ExitStack() as stack:
                    resources = [stack.enter_context(managed(name)) for name in ["a", "b"]]
                    print(resources)
                '''),
                "`ExitStack` collects cleanup callbacks and unwinds them safely in reverse order.",
            ),
        ],
        "Use plain `try/finally` when a one-off cleanup is simpler than creating a reusable context manager object.",
    ),
    c(
        "PY37",
        7,
        "Descriptors",
        ["PY21", "PY25", "PY29"],
        "Descriptors are objects that customize attribute access through `__get__`, `__set__`, and `__delete__`.",
        [
            "How descriptors power `property`, functions-as-methods, and many ORM field systems",
            "When each descriptor hook runs",
            "How custom descriptors centralize validation logic",
        ],
        "Descriptors exist because attribute access is a fundamental operation in Python, and some attributes need behavior rather than dumb storage.",
        "attribute lookup -> class attribute is descriptor? -> descriptor hook runs instead of plain value access",
        [
            ex(
                "A validating descriptor",
                "Validation logic can live in one reusable object instead of being repeated in every setter.",
                b('''
                class TypeEnforced:
                    def __init__(self, expected_type):
                        self.expected_type = expected_type
                    def __set_name__(self, owner, name):
                        self.storage_name = "_" + name
                    def __get__(self, instance, owner):
                        if instance is None:
                            return self
                        return getattr(instance, self.storage_name)
                    def __set__(self, instance, value):
                        if not isinstance(value, self.expected_type):
                            raise TypeError("wrong type")
                        setattr(instance, self.storage_name, value)
                '''),
                "The descriptor decides how reads and writes happen for every class that uses it.",
            ),
            ex(
                "Use the descriptor inside a class",
                "Descriptors become powerful when multiple instances share the same access rule.",
                b('''
                class User:
                    age = TypeEnforced(int)
                    def __init__(self, age):
                        self.age = age

                print(User(30).age)
                '''),
                "The assignment goes through `TypeEnforced.__set__`, so invalid values are rejected before they land on the instance.",
            ),
            ex(
                "`property` is a descriptor",
                "The `property` object implements descriptor hooks for you.",
                b('''
                print(hasattr(property, "__get__"))
                print(hasattr(property, "__set__"))
                '''),
                "That is why `@property` can intercept attribute reads and writes without changing call syntax.",
            ),
        ],
        "Most projects should start with `@property`. Reach for custom descriptors when the same access policy must be reused across many attributes or classes.",
    ),
    c(
        "PY38",
        7,
        "Metaclasses",
        ["PY21", "PY25", "PY29"],
        "Metaclasses customize class creation itself. In Python, classes are objects too, and `type` is their default metaclass.",
        [
            "Why `type` is the metaclass of most classes",
            "How metaclass `__new__` and `__init__` run during class creation",
            "Why `__init_subclass__` is often a simpler alternative",
        ],
        "Metaclasses exist because some frameworks need to inspect or modify classes at definition time, but that is a much rarer need than ordinary instance behavior.",
        "class statement -> metaclass builds class object -> class later builds instances",
        [
            ex(
                "Build a class with `type()` directly",
                "This makes the 'class object built by a metaclass' idea concrete.",
                b('''
                Animal = type("Animal", (), {"kind": "animal"})
                Dog = type("Dog", (Animal,), {"speak": lambda self: "woof"})
                print(Dog().speak(), Dog.kind)
                '''),
                "`type` receives a class name, base classes, and a namespace dictionary, then returns a new class object.",
            ),
            ex(
                "A metaclass can auto-register subclasses",
                "This is a real use case for plugin systems and ORMs.",
                b('''
                registry = {}

                class RegisteringMeta(type):
                    def __new__(mcls, name, bases, namespace):
                        cls = super().__new__(mcls, name, bases, namespace)
                        registry[name] = cls
                        return cls

                class Plugin(metaclass=RegisteringMeta):
                    pass
                '''),
                "Defining a new class is enough to populate the registry because the metaclass runs during class creation.",
            ),
            ex(
                "`__init_subclass__` is usually simpler",
                "Many metaclass use cases can be handled with a normal base class hook instead.",
                b('''
                registry = []

                class PluginBase:
                    def __init_subclass__(cls, **kwargs):
                        super().__init_subclass__(**kwargs)
                        registry.append(cls.__name__)

                class CsvPlugin(PluginBase):
                    pass
                print(registry)
                '''),
                "If a base class hook solves the problem, prefer it over a metaclass because it is easier to read and combine.",
            ),
        ],
        "You almost never need a metaclass. They are powerful, but they multiply complexity quickly and can interact badly with multiple inheritance and tooling.",
    ),
])

concepts.extend([
    c(
        "PY39",
        8,
        "Modules",
        ["PY03"],
        "A module is a Python file loaded as an object, giving code a namespace and a reusable import boundary.",
        [
            "How `import` loads and caches modules",
            "Why `__name__ == \"__main__\"` matters",
            "How circular imports arise and how to break them",
        ],
        "Modules exist so code can be organized into files with explicit names instead of one giant global namespace.",
        "import statement -> finder/loader locate file -> module object created -> top-level code runs once -> module cached in sys.modules",
        [
            ex(
                "Inspect an imported module object",
                "Modules are objects with attributes just like many other things in Python.",
                b('''
                import math
                import sys

                print(math.__name__)
                print(math in sys.modules.values())
                print(math.sqrt(9))
                '''),
                "Importing loads the module and caches it in `sys.modules` so repeated imports reuse the same module object.",
            ),
            ex(
                "`__main__` distinguishes script execution from import",
                "A module often wants a small demo or CLI entry point that should not run on every import.",
                b('''
                if __name__ == "__main__":
                    print("running as a script")
                else:
                    print("running because of import")
                '''),
                "When the file is executed directly, `__name__` becomes `\"__main__\"`. When imported, it becomes the module's real name.",
            ),
            ex(
                "A circular import symptom",
                "Circular imports happen when two modules need each other during top-level initialization.",
                b('''
                print("module_a imports module_b")
                print("module_b imports module_a")
                print("fixes: move imports inside functions, extract shared code, or depend on interfaces instead")
                '''),
                "The core problem is top-level code needing names that are not ready yet. Breaking the cycle usually means moving or reorganizing responsibilities.",
            ),
        ],
        "Too many tiny modules can also hurt readability. Split code where the namespace and dependency boundary help, not just because a file got a little long.",
    ),
    c(
        "PY40",
        8,
        "Packages",
        ["PY03"],
        "A package groups related modules under a shared namespace, usually as a directory and often with an `__init__.py` file.",
        [
            "How absolute and relative imports differ inside packages",
            "What namespace packages are",
            "What `__all__` actually affects",
        ],
        "Packages exist because once one file is not enough, you need a way to structure many modules into a coherent API surface.",
        "package directory -> modules and subpackages -> optional __init__.py controls package namespace",
        [
            ex(
                "Basic package layout",
                "A package creates a stable import path for related modules.",
                b('''
                layout = """
                shop/
                    __init__.py
                    models.py
                    services.py
                """
                print(layout)
                '''),
                "With that structure, callers can import `shop.models` or symbols re-exported from `shop.__init__`.",
            ),
            ex(
                "`__all__` only affects star imports",
                "It does not hide attributes from direct access; it only controls what `from package import *` pulls in.",
                b('''
                __all__ = ["public_name"]
                public_name = 1
                internal_name = 2
                print(__all__)
                '''),
                "Tools and humans should still treat leading underscores and explicit exports as documentation signals, not hard security boundaries.",
            ),
            ex(
                "Namespace packages can span multiple directories",
                "Modern Python can treat directories without `__init__.py` as parts of one package namespace.",
                b('''
                print("namespace packages are useful when multiple distributions contribute to one top-level package")
                '''),
                "This is common in plugin ecosystems where separate installs extend the same package name.",
            ),
        ],
        "Relative imports can be handy inside a package, but overusing them can make large codebases harder to navigate than explicit absolute imports.",
    ),
    c(
        "PY41",
        8,
        "Virtual Environments & Dependency Management",
        ["PY03"],
        "Virtual environments isolate project dependencies so one project's package versions do not silently break another's.",
        [
            "Why `venv` changes import resolution",
            "What `pyproject.toml` standardizes",
            "Why editable installs matter during development",
        ],
        "Dependency isolation matters because Python projects share an interpreter by default, and shared global installs quickly become a conflict factory.",
        "system interpreter + isolated site-packages path -> project-specific imports and tools",
        [
            ex(
                "Show where packages are loaded from",
                "`sys.path` reveals why environments matter: it controls where imports search.",
                b('''
                import sys
                print(sys.prefix)
                print(sys.base_prefix)
                print(sys.path[:3])
                '''),
                "In a virtual environment, `sys.prefix` usually differs from `sys.base_prefix`, and the search path points at environment-local packages first.",
            ),
            ex(
                "A minimal `pyproject.toml`",
                "Modern builds declare project metadata and build requirements in one standard file.",
                b('''
                pyproject = """
                [build-system]
                requires = ["setuptools>=68", "wheel"]
                build-backend = "setuptools.build_meta"

                [project]
                name = "example-app"
                version = "0.1.0"
                dependencies = ["requests>=2.31"]
                """
                print(pyproject)
                '''),
                "PEP 517 and 518 moved packaging toward tool-neutral build metadata instead of ad hoc setup scripts alone.",
            ),
            ex(
                "Editable installs keep source and import path connected",
                "`pip install -e .` lets imports reflect your current working tree without rebuilding the package after every change.",
                b('''
                print("python -m venv .venv")
                print(".venv\\Scripts\\activate")
                print("pip install -e .")
                '''),
                "Editable installs are ideal during active development because your import target points at the source tree itself.",
            ),
        ],
        "Global installs are fine for throwaway experiments. For real projects, isolation is cheap insurance against version conflicts and machine-to-machine drift.",
    ),
])

concepts.extend([
    c(
        "PY42",
        9,
        "File Handling",
        ["PY18", "PY36"],
        "File I/O opens a stream to bytes on disk and lets you choose text or binary interpretation, access mode, and encoding strategy.",
        [
            "How `open()` modes affect reading and writing",
            "Why explicit encoding matters in text mode",
            "How binary mode works with structured bytes",
        ],
        "Programs need durable storage, but operating systems expose files as byte streams. Python adds text decoding, buffering, and safe cleanup on top.",
        "open file -> file object -> text decode/encode or raw bytes -> close on exit",
        [
            ex(
                "Write and read text with an explicit encoding",
                "Encoding bugs often come from relying on platform defaults instead of declaring the file format.",
                b('''
                from pathlib import Path

                path = Path("note.txt")
                path.write_text("café", encoding="utf-8")
                print(path.read_text(encoding="utf-8"))
                '''),
                "Explicit UTF-8 makes the file portable across machines with different default encodings.",
            ),
            ex(
                "Demonstrate an encoding mismatch",
                "A file written in one encoding may fail when read as another.",
                b('''
                from pathlib import Path

                path = Path("legacy.txt")
                path.write_bytes("£".encode("cp1252"))
                try:
                    print(path.read_text(encoding="utf-8"))
                except UnicodeDecodeError as exc:
                    print(type(exc).__name__, exc)
                '''),
                "This is the kind of bug that appears when a Windows-produced file meets a Linux UTF-8 assumption without an explicit encoding contract.",
            ),
            ex(
                "Binary mode with `struct`",
                "Binary I/O is for exact byte layouts rather than decoded text.",
                b('''
                import struct

                payload = struct.pack("<if", 7, 3.5)
                print(payload)
                print(struct.unpack("<if", payload))
                '''),
                "The `struct` format string controls byte layout exactly, which is useful for binary protocols and file formats.",
            ),
        ],
        "Use text mode for human-readable files and binary mode for precise byte-level formats. Mixing the two mental models causes subtle corruption bugs.",
    ),
    c(
        "PY43",
        9,
        "JSON, CSV, pickle",
        ["PY18", "PY36"],
        "Serialization turns Python data into a portable representation and back again, but different formats solve very different problems.",
        [
            "When to choose JSON, CSV, or pickle",
            "Why custom encoders are sometimes needed for JSON",
            "Why unpickling untrusted data is dangerous",
        ],
        "Programs exchange data with humans, spreadsheets, APIs, caches, and queues. One representation never fits every audience, so Python offers multiple serialization tools.",
        "Python objects -> serialized representation -> transport or storage -> deserialize later",
        [
            ex(
                "JSON with a custom datetime encoder",
                "JSON supports a small set of built-in types, so richer objects need explicit conversion.",
                b('''
                import datetime as dt
                import json

                def default(obj):
                    if isinstance(obj, dt.datetime):
                        return obj.isoformat()
                    raise TypeError(f"unsupported: {type(obj)!r}")

                raw = json.dumps({"when": dt.datetime(2026, 3, 6, 12, 0)}, default=default)
                print(raw)
                '''),
                "A custom encoder converts unsupported objects into JSON-friendly values before serialization.",
            ),
            ex(
                "CSV with `DictReader`",
                "CSV is simple and spreadsheet-friendly, but every field starts as text until you convert it.",
                b('''
                import csv
                import io

                data = io.StringIO("name,score\\nAda,98\\nGrace,99\\n")
                for row in csv.DictReader(data):
                    print(row["name"], int(row["score"]))
                '''),
                "`DictReader` maps column names to string values, which is friendlier than indexing raw split lines by position.",
            ),
            ex(
                "Pickle is powerful and unsafe for untrusted input",
                "Pickle can reconstruct arbitrary Python objects, which is exactly why it must not be used with data you do not trust.",
                b('''
                import pickle

                payload = pickle.dumps({"safe": [1, 2, 3]})
                print(type(pickle.loads(payload)))
                print("Never unpickle data from an untrusted source")
                '''),
                "Pickle is fine for trusted internal persistence but wrong for network-facing or user-supplied data.",
            ),
        ],
        "Choose the format that matches the audience: JSON for interoperable APIs, CSV for table-shaped text, and pickle only for trusted Python-to-Python persistence.",
    ),
    c(
        "PY44",
        9,
        "pathlib vs os.path",
        ["PY18", "PY36"],
        "`pathlib` models filesystem paths as objects with methods and operators, while `os.path` exposes mostly string-based helper functions.",
        [
            "Why object-oriented paths are easier to compose",
            "How path arithmetic with `/` improves readability",
            "Where `glob`, `rglob`, and `iterdir` fit",
        ],
        "Path handling is everywhere, and string concatenation is a brittle way to express filesystem intent across operating systems.",
        "Path object -> joins, queries, and traversal methods -> file operations",
        [
            ex(
                "Path arithmetic is clearer than manual joining",
                "The `/` operator on `Path` objects means 'descend into this path component', not numeric division.",
                b('''
                from pathlib import Path

                path = Path("data") / "reports" / "summary.txt"
                print(path)
                '''),
                "This reads like the directory structure instead of a pile of string concatenations and separators.",
            ),
            ex(
                "Common checks are methods on the path object",
                "`pathlib` keeps the path and the operations that make sense on it close together.",
                b('''
                from pathlib import Path

                path = Path(".")
                print(path.exists())
                print(path.resolve())
                '''),
                "Method-based APIs reduce the need to remember which `os.path` function pairs with which string you have in hand.",
            ),
            ex(
                "Directory traversal methods",
                "`iterdir`, `glob`, and `rglob` cover the most common directory-search cases.",
                b('''
                from pathlib import Path

                root = Path(".")
                print([p.name for p in root.iterdir()][:3])
                print([p.name for p in root.glob("*.py")][:3])
                '''),
                "Use `glob` for one level and `rglob` for recursive searches when you want intent to be obvious in the code.",
            ),
        ],
        "`os.path` still works and appears in older code, but `pathlib` is usually the clearer default for new Python applications.",
    ),
])

concepts.extend([
    c(
        "PY45",
        10,
        "Concurrency vs Parallelism vs Asynchrony",
        ["PY33", "PY34"],
        "Concurrency is about dealing with multiple tasks at once, parallelism is about doing work at the same instant on multiple cores, and asynchrony is about cooperative waiting without blocking a thread.",
        [
            "How CPU-bound and I/O-bound workloads differ",
            "Why threads, processes, and event loops solve different problems",
            "How to choose the right model before writing code",
        ],
        "These distinctions matter because using the wrong concurrency model can make code slower, harder to debug, or both.",
        "I/O wait -> threads or async can overlap\nCPU work -> parallel processes or native extensions help more",
        [
            ex(
                "A mental decision table",
                "The first question is always what your program spends time waiting on.",
                b('''
                print("CPU-bound -> multiprocessing or native code")
                print("I/O-bound with blocking APIs -> threading")
                print("I/O-bound with async APIs -> asyncio")
                '''),
                "If the work is mostly waiting on sockets or disks, overlap helps. If the work burns CPU, the GIL becomes part of the discussion.",
            ),
            ex(
                "Concurrency can overlap waiting even on one core",
                "Tasks do not need to run literally at the same instant to make better use of elapsed time.",
                b('''
                print("task A: wait on network")
                print("task B: run while A waits")
                print("That overlap is concurrency")
                '''),
                "Concurrency is about progress on multiple tasks, not necessarily simultaneous CPU execution.",
            ),
            ex(
                "Parallelism needs separate workers",
                "True CPU parallelism usually means separate OS processes in pure Python code.",
                b('''
                print("process 1 on core 1")
                print("process 2 on core 2")
                print("same moment, separate memory")
                '''),
                "Separate processes avoid the single-CPython-interpreter-thread bottleneck for CPU-bound pure-Python code.",
            ),
        ],
        "Do not pick a concurrency tool because it sounds advanced. Start with the workload shape, then choose the minimum model that matches it.",
    ),
    c(
        "PY46",
        10,
        "Threading",
        ["PY33", "PY34"],
        "Threads let one process make progress on multiple tasks concurrently, but in CPython the GIL means CPU-bound pure-Python threads do not execute Python bytecode in parallel.",
        [
            "What the GIL protects and what it does not",
            "Why threads are still useful for I/O-bound work",
            "How locks and coordination primitives avoid races",
        ],
        "Threads exist because overlapping waiting is valuable, and many operating-system or C-extension operations release the GIL while work is in progress.",
        "one process -> multiple threads share memory -> GIL coordinates bytecode execution -> synchronization still needed for shared state",
        [
            ex(
                "Threads still help with waiting",
                "The GIL does not stop overlap on blocking I/O because threads can switch while one is waiting.",
                b('''
                import threading
                import time

                def task(name):
                    time.sleep(0.2)
                    print(name)

                threads = [threading.Thread(target=task, args=(f"t{i}",)) for i in range(3)]
                [t.start() for t in threads]
                [t.join() for t in threads]
                '''),
                "The sleeps overlap, so total elapsed time is closer to one sleep than to three added together.",
            ),
            ex(
                "A race condition on shared state",
                "Shared mutable state is the danger zone for threads.",
                b('''
                import threading

                counter = 0
                lock = threading.Lock()
                with lock:
                    counter += 1
                print(counter)
                '''),
                "The example shows the fix shape: protect the critical section with a lock. Without synchronization, repeated updates can interleave unpredictably.",
            ),
            ex(
                "Other coordination primitives",
                "Threads need more than one tool depending on the coordination pattern.",
                b('''
                import threading
                print(threading.RLock)
                print(threading.Semaphore)
                print(threading.Event)
                print(threading.Condition)
                '''),
                "Use `Lock` for mutual exclusion, `RLock` for re-entrant locking, `Semaphore` to cap concurrency, `Event` for one-bit signaling, and `Condition` for coordinated waiting.",
            ),
        ],
        "Threads are often the simplest fix for I/O overlap, but once shared-state complexity dominates, a queue-based or process-based design may be easier to reason about.",
    ),
    c(
        "PY47",
        10,
        "Multiprocessing",
        ["PY33", "PY34"],
        "Multiprocessing uses separate processes to achieve real CPU parallelism for pure-Python code, at the cost of separate memory spaces and serialization overhead.",
        [
            "Why separate processes bypass the GIL",
            "How pools, queues, pipes, and shared memory differ",
            "Why picklability matters when sending work to workers",
        ],
        "Separate processes matter because CPU-bound Python work often needs more than concurrency; it needs multiple interpreters running at once.",
        "parent process -> worker processes -> tasks serialized to workers -> results serialized back",
        [
            ex(
                "A process pool maps work across inputs",
                "Pools are the high-level entry point for many CPU-bound batch jobs.",
                b('''
                from multiprocessing import Pool

                def square(n):
                    return n * n

                if __name__ == "__main__":
                    with Pool() as pool:
                        print(pool.map(square, [1, 2, 3, 4]))
                '''),
                "The guard is required on some platforms because worker processes import the module to start.",
            ),
            ex(
                "Queue versus pipe",
                "Both move data between processes, but they serve slightly different communication shapes.",
                b('''
                from multiprocessing import Pipe, Queue
                print(Queue)
                print(Pipe)
                '''),
                "Use queues for general producer-consumer patterns and pipes for simpler two-endpoint communication.",
            ),
            ex(
                "Arguments must usually be picklable",
                "Worker processes need a serialized form of the task and its data.",
                b('''
                print("top-level functions are safer than lambdas for multiprocessing tasks")
                print("avoid sending open file handles or non-picklable objects")
                '''),
                "If the work item cannot be pickled, the child process cannot reconstruct it. That is a common source of multiprocessing errors.",
            ),
        ],
        "Processes buy true parallelism, but startup cost, memory duplication, and serialization overhead mean they are not the answer to every workload.",
    ),
])

concepts.extend([
    c(
        "PY48",
        10,
        "asyncio",
        ["PY33", "PY34"],
        "`asyncio` provides cooperative concurrency with an event loop, coroutines, tasks, and non-blocking I/O-friendly APIs.",
        [
            "How the event loop schedules coroutines",
            "Why blocking the loop is the cardinal async mistake",
            "When `gather`, `wait`, and `TaskGroup` differ",
        ],
        "Async I/O exists because one thread can often manage many waiting network tasks efficiently if code cooperates instead of blocking.",
        "event loop -> ready task queue + I/O readiness notifications -> resume suspended coroutines",
        [
            ex(
                "Basic coroutine execution",
                "`async def` defines a coroutine function, and `asyncio.run` creates and drives the event loop for a top-level entry point.",
                b('''
                import asyncio

                async def greet():
                    await asyncio.sleep(0.1)
                    return "hello"

                print(asyncio.run(greet()))
                '''),
                "The `await` gives control back to the loop while the sleep is pending.",
            ),
            ex(
                "Run several coroutines together",
                "`gather` waits for a group of awaitables and returns their results in input order.",
                b('''
                import asyncio

                async def fetch(name):
                    await asyncio.sleep(0.1)
                    return name

                async def main():
                    print(await asyncio.gather(fetch("a"), fetch("b")))

                asyncio.run(main())
                '''),
                "`TaskGroup` in Python 3.11+ offers stronger structured-concurrency semantics for related tasks.",
            ),
            ex(
                "Do not block the event loop",
                "A blocking call freezes every coroutine sharing the loop until it finishes.",
                b('''
                import asyncio
                import time

                async def bad():
                    time.sleep(0.2)
                    return "blocked loop"
                '''),
                "Replace blocking work with non-blocking APIs or move it to a thread or executor so other tasks can keep progressing.",
            ),
        ],
        "Async code is not automatically faster. It shines when many tasks spend time waiting on network or other async-compatible I/O.",
    ),
    c(
        "PY49",
        11,
        "Type Hints",
        ["PY06", "PY30"],
        "Type hints describe expected shapes of values for humans and static analyzers, even though Python itself does not enforce most annotations at runtime.",
        [
            "How basic annotations, unions, literals, generics, and protocols fit together",
            "Why type variables and parameter specs matter for reusable APIs",
            "How hints improve tooling without changing runtime semantics by themselves",
        ],
        "Large codebases need machine-checkable documentation about data flow. Type hints provide that without giving up Python's dynamic runtime.",
        "annotation syntax -> metadata attached to function or variable -> static tool reads it later",
        [
            ex(
                "Basic function and variable annotations",
                "Annotations make intent explicit at the API boundary.",
                b('''
                from typing import Optional

                user_id: int = 7

                def find_name(user_id: int) -> Optional[str]:
                    return "Ada" if user_id == 7 else None
                '''),
                "`Optional[str]` means the function may return `str` or `None`.",
            ),
            ex(
                "Generics with `TypeVar`",
                "Generic code can stay precise without hard-coding one concrete type.",
                b('''
                from typing import TypeVar

                T = TypeVar("T")

                def first(items: list[T]) -> T:
                    return items[0]
                '''),
                "The type variable says the return type matches the element type of the input list.",
            ),
            ex(
                "Advanced hints for decorators and value restrictions",
                "`Literal`, `Annotated`, and `ParamSpec` cover narrower but important cases.",
                b('''
                from typing import Annotated, Literal

                Mode = Literal["r", "w"]
                Port = Annotated[int, "1..65535"]
                '''),
                "These hints communicate stronger intent to tools and readers, even though plain Python will not enforce them on its own.",
            ),
        ],
        "Hints should clarify APIs, not drown them in ceremony. Type every detail only when the extra precision actually helps readers or tools catch mistakes.",
    ),
    c(
        "PY50",
        11,
        "Static Analysis",
        ["PY06", "PY30"],
        "Static analyzers such as mypy and pyright read your code without running it and flag type inconsistencies, unreachable paths, and other issues earlier.",
        [
            "Why type hints alone do nothing at runtime",
            "How static tools catch bugs before execution",
            "When mypy and pyright differ in workflow and emphasis",
        ],
        "Static analysis matters because some bugs are easier and cheaper to catch from source code shape than from production failures.",
        "source + annotations -> analyzer builds model -> reports mismatches before runtime",
        [
            ex(
                "Annotations are metadata, not runtime enforcement",
                "Python will happily run code with the wrong value type unless you add your own checks or external validation.",
                b('''
                def add_one(value: int) -> int:
                    return value + 1

                print(add_one("7"))
                '''),
                "The code still runs until the unsupported operation triggers a runtime error. The annotation alone did not stop the call.",
            ),
            ex(
                "A mypy configuration sketch",
                "Static analysis becomes more useful when the tool settings are explicit and repeatable.",
                b('''
                config = """
                [mypy]
                python_version = 3.12
                warn_unused_ignores = True
                disallow_untyped_defs = True
                """
                print(config)
                '''),
                "Treat the configuration as part of the project contract, just like linting or test settings.",
            ),
            ex(
                "A hint can reveal a real bug",
                "The analyzer sees that a `None` branch was not handled even if your test path did not hit it yet.",
                b('''
                from typing import Optional

                def shout(name: Optional[str]) -> str:
                    return name.upper()
                '''),
                "A static checker complains because `name` might be `None`. That warning points to a real bug before production users hit it.",
            ),
        ],
        "Use static analysis as an assistant, not a religion. pyright is often faster and editor-friendly; mypy remains deeply configurable and widely adopted.",
    ),
])

concepts.extend([
    c(
        "PY51",
        12,
        "unittest",
        ["PY25", "PY35"],
        "`unittest` is Python's built-in xUnit-style testing framework with test case classes, fixtures, and many assertion helpers.",
        [
            "How `TestCase` organizes tests",
            "What `setUp`, `tearDown`, and class-level fixtures do",
            "Why assertion methods communicate intent better than plain `assert` in this framework",
        ],
        "Tests exist so code changes can be checked automatically. `unittest` provides a standard structure that ships with Python itself.",
        "test runner -> discovers TestCase methods -> runs fixtures -> executes assertions -> reports failures",
        [
            ex(
                "A `BankAccount` test case",
                "This continues the class example from the OOP layer and shows the basic xUnit structure.",
                b('''
                import unittest

                class BankAccount:
                    def __init__(self, balance=0):
                        self.balance = balance
                    def deposit(self, amount):
                        self.balance += amount
                        return self.balance

                class BankAccountTests(unittest.TestCase):
                    def setUp(self):
                        self.account = BankAccount(100)
                    def test_deposit(self):
                        self.assertEqual(self.account.deposit(25), 125)
                '''),
                "`setUp` runs before each test method, giving each test a fresh fixture.",
            ),
            ex(
                "Class-level fixtures",
                "Use these when setup is expensive and can safely be shared by all tests in the class.",
                b('''
                class DemoTests(unittest.TestCase):
                    @classmethod
                    def setUpClass(cls):
                        cls.shared = [1, 2, 3]
                    @classmethod
                    def tearDownClass(cls):
                        cls.shared = None
                '''),
                "Be careful with shared mutable state in class fixtures because tests can accidentally affect each other.",
            ),
            ex(
                "Assertion helpers communicate the check",
                "Framework-specific assertion methods produce better failure messages than hand-written if-statements.",
                b('''
                self.assertEqual(2 + 2, 4)
                self.assertTrue(True)
                self.assertRaises(ValueError)
                '''),
                "Each assertion names the expectation directly, which makes failures easier to scan in test output.",
            ),
        ],
        "`unittest` is reliable and standard, but many teams prefer pytest because it removes more boilerplate while staying compatible with much of the same ecosystem.",
    ),
    c(
        "PY52",
        12,
        "pytest",
        ["PY25", "PY35"],
        "pytest is a third-party testing framework that favors plain functions, powerful fixtures, and concise assertions.",
        [
            "Why pytest usually feels lighter than `unittest`",
            "How fixtures and parametrization scale test setup",
            "Where `conftest.py` and monkeypatching fit",
        ],
        "pytest exists because test code should be easy to write and easy to read. It removes ceremony so the test intent stays front and center.",
        "pytest discovers test functions -> injects fixtures by name -> rewrites asserts for rich failure output",
        [
            ex(
                "The same style without a test class",
                "Plain functions are often enough, which makes tests feel closer to normal Python code.",
                b('''
                def deposit(balance, amount):
                    return balance + amount

                def test_deposit():
                    assert deposit(100, 25) == 125
                '''),
                "pytest rewrites `assert` to show rich comparison output on failure, so plain asserts become pleasant to use.",
            ),
            ex(
                "A fixture and parametrized test",
                "Fixtures centralize setup and parametrization multiplies cases cleanly.",
                b('''
                import pytest

                @pytest.fixture
                def base_balance():
                    return 100

                @pytest.mark.parametrize("amount, expected", [(25, 125), (0, 100)])
                def test_deposit(base_balance, amount, expected):
                    assert base_balance + amount == expected
                '''),
                "This pattern scales far better than hand-copying almost identical tests.",
            ),
            ex(
                "`conftest.py` and monkeypatch",
                "Shared fixtures live in `conftest.py`, and `monkeypatch` lets tests temporarily replace behavior safely.",
                b('''
                def test_env(monkeypatch):
                    monkeypatch.setenv("APP_MODE", "test")
                    assert True
                '''),
                "Monkeypatching is useful for environment variables, module attributes, and small controlled substitutions during tests.",
            ),
        ],
        "pytest is usually the better default for new projects, but `unittest` knowledge still matters because the stdlib and older codebases use it heavily.",
    ),
    c(
        "PY53",
        12,
        "Mocking",
        ["PY25", "PY35"],
        "Mocking replaces collaborators with controllable doubles so a test can focus on one unit's behavior without touching real external systems.",
        [
            "How `Mock`, `MagicMock`, and `patch` differ",
            "Why patch location matters",
            "How over-mocking can make tests meaningless",
        ],
        "Mocks exist because real networks, clocks, payment gateways, and file systems make tests slow, flaky, or expensive when the unit under test does not need the real dependency.",
        "unit under test -> mocked dependency returns controlled values -> assertions check calls and behavior",
        [
            ex(
                "A basic mock object",
                "Mocks record calls and return configured values.",
                b('''
                from unittest.mock import Mock

                client = Mock()
                client.fetch.return_value = {"status": 200}
                print(client.fetch("/health"))
                print(client.fetch.call_count)
                '''),
                "You can assert both what was returned and how the mock was used.",
            ),
            ex(
                "`patch` as a context manager",
                "Patch where the code under test looks up the name, not where the original object was defined.",
                b('''
                from unittest.mock import patch

                with patch("module_under_test.requests.get") as fake_get:
                    fake_get.return_value.status_code = 200
                '''),
                "Location matters because imports copy names into module namespaces.",
            ),
            ex(
                "The over-mocking trap",
                "If every collaborator is mocked, you may stop testing anything real about the system.",
                b('''
                print("Mock HTTP clients, not your own pure functions")
                print("Prefer integration tests for boundaries that matter")
                '''),
                "A test full of mocks can pass while the real pieces fail to fit together. Balance unit isolation with integration coverage.",
            ),
        ],
        "Mock the parts that make the test slow or unstable, not every single dependency. Otherwise you end up testing your mocks instead of your code.",
    ),
])

concepts.extend([
    c(
        "PY54",
        13,
        "Profiling",
        ["PY01", "PY02", "PY03", "PY04", "PY05", "PY06", "PY07", "PY08", "PY09", "PY10", "PY11", "PY12", "PY13", "PY14", "PY15", "PY16", "PY17", "PY18", "PY19", "PY20", "PY21", "PY22", "PY23", "PY24", "PY25", "PY26", "PY27", "PY28", "PY29", "PY30", "PY31", "PY32", "PY33", "PY34", "PY35", "PY36", "PY37", "PY38", "PY39", "PY40", "PY41", "PY42", "PY43", "PY44", "PY45", "PY46", "PY47", "PY48", "PY49", "PY50", "PY51", "PY52", "PY53"],
        "Profiling measures where time or memory actually goes so you can optimize evidence, not guesses.",
        [
            "How `cProfile` summarizes call costs",
            "What line-level profilers add",
            "Why memory profiling matters separately from CPU time",
        ],
        "Performance work without measurement is mostly storytelling. Profilers turn vague suspicions into concrete hotspots.",
        "program run -> profiler records timing or memory -> report identifies hotspots",
        [
            ex(
                "`cProfile` a slow function",
                "Function-level profiling is the first pass for many problems.",
                b('''
                import cProfile

                def slow():
                    total = 0
                    for i in range(10000):
                        total += i * i
                    return total

                cProfile.run("slow()")
                '''),
                "The report shows how many times each function was called and where cumulative time accumulated.",
            ),
            ex(
                "Line profilers zoom in further",
                "Once you know the slow function, line-level tools help find the expensive statement inside it.",
                b('''
                print("Use line_profiler's @profile decorator when function-level timing is not precise enough")
                '''),
                "This is useful when one function contains both cheap and expensive branches.",
            ),
            ex(
                "Memory deserves separate attention",
                "CPU-fast code can still be memory-hungry.",
                b('''
                print("memory_profiler can reveal the line where a huge list or dataframe is allocated")
                '''),
                "Optimize the bottleneck you actually have: time, memory, or both.",
            ),
        ],
        "Profile before optimizing and again after optimizing. Without the second measurement, you do not know whether the change actually helped.",
    ),
    c(
        "PY55",
        13,
        "Python Memory Model Deep-Dive",
        ["PY01", "PY02", "PY03", "PY04", "PY05", "PY06", "PY07", "PY08", "PY09", "PY10", "PY11", "PY12", "PY13", "PY14", "PY15", "PY16", "PY17", "PY18", "PY19", "PY20", "PY21", "PY22", "PY23", "PY24", "PY25", "PY26", "PY27", "PY28", "PY29", "PY30", "PY31", "PY32", "PY33", "PY34", "PY35", "PY36", "PY37", "PY38", "PY39", "PY40", "PY41", "PY42", "PY43", "PY44", "PY45", "PY46", "PY47", "PY48", "PY49", "PY50", "PY51", "PY52", "PY53"],
        "CPython combines reference counting, cyclic garbage collection, object caching, and object-layout choices such as `__slots__` to manage memory.",
        [
            "Why small integers and some strings may be interned",
            "How reference counting and cyclic GC divide the work",
            "Where `__slots__` can materially reduce memory usage",
        ],
        "Memory behavior leaks into performance and even semantics, especially around identity, caching, and object lifetime.",
        "object allocation -> references increase/decrease -> refcount hits zero or cycle collector cleans unreachable graph",
        [
            ex(
                "Small integers are often cached",
                "This is why identity experiments with tiny integers can be misleading.",
                b('''
                a = 256
                b = 256
                print(a is b)
                '''),
                "CPython commonly interns integers from -5 to 256. That is an implementation optimization, not a value-equality rule.",
            ),
            ex(
                "Some strings are interned too",
                "Short identifier-like strings are frequent candidates for interning.",
                b('''
                x = "hello"
                y = "hello"
                print(x is y)
                '''),
                "This may print `True`, but you should still compare strings with `==` because interning is not the semantic rule.",
            ),
            ex(
                "`__slots__` removes per-instance dictionaries",
                "When you create huge numbers of simple objects, layout choices matter.",
                b('''
                class Plain:
                    def __init__(self):
                        self.x = 1
                        self.y = 2

                class Slotted:
                    __slots__ = ("x", "y")
                    def __init__(self):
                        self.x = 1
                        self.y = 2
                '''),
                "Slots trade flexibility for lower per-instance overhead, which can matter a lot at scale.",
            ),
        ],
        "Do not write correctness logic around caching or interning. Those are optimizations. Treat them as implementation details unless you are measuring performance.",
    ),
    c(
        "PY56",
        13,
        "Writing Faster Python",
        ["PY01", "PY02", "PY03", "PY04", "PY05", "PY06", "PY07", "PY08", "PY09", "PY10", "PY11", "PY12", "PY13", "PY14", "PY15", "PY16", "PY17", "PY18", "PY19", "PY20", "PY21", "PY22", "PY23", "PY24", "PY25", "PY26", "PY27", "PY28", "PY29", "PY30", "PY31", "PY32", "PY33", "PY34", "PY35", "PY36", "PY37", "PY38", "PY39", "PY40", "PY41", "PY42", "PY43", "PY44", "PY45", "PY46", "PY47", "PY48", "PY49", "PY50", "PY51", "PY52", "PY53"],
        "Fast Python starts with algorithmic complexity, then applies measurements and data-structure choices before micro-optimizations.",
        [
            "Why O(n log n) beats clever O(n²) code",
            "How local lookups and comprehensions can help a little",
            "When to move numeric heavy lifting to vectorized libraries",
        ],
        "Most performance wins come from changing the shape of the work, not shaving nanoseconds off the wrong loop.",
        "problem shape -> algorithm choice -> data structure choice -> only then small runtime tweaks",
        [
            ex(
                "Algorithmic wins dominate",
                "Changing complexity beats micro-tuning nearly every time.",
                b('''
                print("Prefer O(n log n) sorting over repeated O(n) scans inside an O(n) loop")
                '''),
                "If the algorithm is wrong, local tweaks only make the wrong approach fail slightly faster.",
            ),
            ex(
                "Local lookup is usually faster than global lookup",
                "Python resolves local names more cheaply than globals.",
                b('''
                import timeit
                setup = "x = 1\\n"
                print(timeit.timeit("x + 1", setup=setup, number=1_000_000))
                '''),
                "This difference exists, but it matters far less than choosing the right algorithm and data structure.",
            ),
            ex(
                "Vectorized libraries can change the game",
                "For heavy numeric work, pushing loops into optimized native code often dwarfs pure-Python tweaks.",
                b('''
                print("For array math, NumPy can be orders of magnitude faster than Python loops")
                '''),
                "The best optimization is often moving the hot path to a library designed for that workload.",
            ),
        ],
        "Benchmark representative workloads, not tiny artificial fragments detached from the real program.",
    ),
])

concepts.extend([
    c(
        "PY57",
        14,
        "Common Design Patterns in Python",
        ["PY01", "PY02", "PY03", "PY04", "PY05", "PY06", "PY07", "PY08", "PY09", "PY10", "PY11", "PY12", "PY13", "PY14", "PY15", "PY16", "PY17", "PY18", "PY19", "PY20", "PY21", "PY22", "PY23", "PY24", "PY25", "PY26", "PY27", "PY28", "PY29", "PY30", "PY31", "PY32", "PY33", "PY34", "PY35", "PY36", "PY37", "PY38", "PY39", "PY40", "PY41", "PY42", "PY43", "PY44", "PY45", "PY46", "PY47", "PY48", "PY49", "PY50", "PY51", "PY52", "PY53", "PY54", "PY55", "PY56"],
        "Python uses classic patterns too, but the most useful versions usually lean on functions, modules, and duck typing instead of heavy class hierarchies.",
        [
            "How Pythonic implementations differ from textbook UML-heavy versions",
            "Where singleton, factory, observer, strategy, and repository patterns show up",
            "Why patterns are tools, not badges of sophistication",
        ],
        "Patterns matter because recurring design problems deserve shared vocabulary, but Python often solves them with fewer moving parts than more ceremony-heavy languages.",
        "problem pattern -> choose lightest Python construct that preserves intent",
        [
            ex(
                "Singleton via module state",
                "In Python, a module is already a natural singleton because imports cache one module object.",
                b('''
                settings = {"mode": "prod"}
                print(settings)
                '''),
                "You often do not need a class-based singleton at all. A module-level object is simpler and clearer.",
            ),
            ex(
                "Factory maps names to classes",
                "A dictionary can be the whole factory when the decision is straightforward.",
                b('''
                class JsonExporter: pass
                class CsvExporter: pass

                factory = {"json": JsonExporter, "csv": CsvExporter}
                print(factory["json"]())
                '''),
                "This is more Pythonic than a long switch-like object hierarchy for many simple cases.",
            ),
            ex(
                "Strategy via functions",
                "A strategy can just be a callable passed in from the outside.",
                b('''
                def discount_10(price):
                    return price * 0.9

                def checkout(price, pricing_strategy):
                    return pricing_strategy(price)

                print(checkout(100, discount_10))
                '''),
                "Python's first-class functions make some classic class-heavy patterns much lighter.",
            ),
        ],
        "Use patterns to clarify design, not to impress yourself. If a plain function or dict solves the problem cleanly, that is the better pattern for Python.",
    ),
    c(
        "PY58",
        14,
        "Python Standard Library Tour",
        ["PY01", "PY02", "PY03", "PY04", "PY05", "PY06", "PY07", "PY08", "PY09", "PY10", "PY11", "PY12", "PY13", "PY14", "PY15", "PY16", "PY17", "PY18", "PY19", "PY20", "PY21", "PY22", "PY23", "PY24", "PY25", "PY26", "PY27", "PY28", "PY29", "PY30", "PY31", "PY32", "PY33", "PY34", "PY35", "PY36", "PY37", "PY38", "PY39", "PY40", "PY41", "PY42", "PY43", "PY44", "PY45", "PY46", "PY47", "PY48", "PY49", "PY50", "PY51", "PY52", "PY53", "PY54", "PY55", "PY56"],
        "The standard library is large enough that knowing where to look is often more valuable than memorizing every function name.",
        [
            "Which modules solve common real-world problems out of the box",
            "How `itertools`, `functools`, `contextlib`, `enum`, `typing`, and others complement the core language",
            "Why the stdlib is one of Python's biggest strengths",
        ],
        "Python's batteries-included philosophy matters because many tasks are already solved well enough without reaching for another dependency first.",
        "core language + standard library modules -> practical toolbox for everyday work",
        [
            ex(
                "A tiny `itertools` sampler",
                "These tools are great for iterator-heavy code.",
                b('''
                from itertools import chain, combinations
                print(list(chain([1, 2], [3])))
                print(list(combinations([1, 2, 3], 2)))
                '''),
                "`itertools` turns many nested-loop and windowing tasks into small, composable expressions.",
            ),
            ex(
                "`functools` and `enum` in everyday code",
                "These modules often remove repetitive boilerplate.",
                b('''
                from enum import Enum, auto
                from functools import cache

                class State(Enum):
                    READY = auto()
                    DONE = auto()

                @cache
                def square(n):
                    return n * n
                print(State.READY, square(4))
                '''),
                "`Enum` gives named constants and `cache` memoizes pure function calls with no size limit.",
            ),
            ex(
                "`contextlib` utilities",
                "The library includes helpers for temporary output redirection and controlled exception suppression.",
                b('''
                from contextlib import suppress

                with suppress(FileNotFoundError):
                    open("missing.txt")
                print("continued")
                '''),
                "This is safer and narrower than a bare `except` because it names the exact exception being tolerated.",
            ),
        ],
        "Before adding a dependency, check whether the standard library already solves the problem well enough. It often does.",
    ),
    c(
        "PY59",
        14,
        "Python Anti-Patterns",
        ["PY01", "PY02", "PY03", "PY04", "PY05", "PY06", "PY07", "PY08", "PY09", "PY10", "PY11", "PY12", "PY13", "PY14", "PY15", "PY16", "PY17", "PY18", "PY19", "PY20", "PY21", "PY22", "PY23", "PY24", "PY25", "PY26", "PY27", "PY28", "PY29", "PY30", "PY31", "PY32", "PY33", "PY34", "PY35", "PY36", "PY37", "PY38", "PY39", "PY40", "PY41", "PY42", "PY43", "PY44", "PY45", "PY46", "PY47", "PY48", "PY49", "PY50", "PY51", "PY52", "PY53", "PY54", "PY55", "PY56"],
        "Many painful Python bugs come from a handful of recurring anti-patterns that feel convenient in the moment but blur the language's real semantics.",
        [
            "Why mutable defaults, bare excepts, and `import *` keep hurting people",
            "How `is None` and `isinstance` express the right questions",
            "Why performance anti-patterns often start as innocent-looking loops",
        ],
        "Anti-patterns matter because avoiding a few traps saves disproportionate amounts of debugging time.",
        "tempting shortcut -> hidden semantic mismatch -> confusing bug later",
        [
            ex(
                "Mutable defaults keep state between calls",
                "This is one of Python's most common accidental bugs.",
                b('''
                def add(item, bucket=[]):
                    bucket.append(item)
                    return bucket

                print(add(1))
                print(add(2))
                '''),
                "The second call reuses the same list. Use `None` plus in-function initialization instead.",
            ),
            ex(
                "Bare `except` catches too much",
                "It can swallow `KeyboardInterrupt` and `SystemExit`, making programs harder to stop and debug.",
                b('''
                try:
                    raise KeyboardInterrupt
                except:
                    print("too broad")
                '''),
                "Catch the narrow exception you expect instead of erasing every possible signal.",
            ),
            ex(
                "Ask the right question: identity versus type hierarchy",
                "`is None` and `isinstance` express intent better than lookalikes.",
                b('''
                print(None is None)
                print(type(True) == int)
                print(isinstance(True, int))
                '''),
                "Use `is None` for the singleton and `isinstance` when subclasses should count. Also avoid `import *` and repeated string concatenation in loops for the same clarity and performance reasons.",
            ),
        ],
        "Most anti-patterns come from fighting the language model instead of working with it. Learn the model once and many bugs disappear.",
    ),
])


def validate_examples() -> None:
    for concept in concepts:
        for index, example in enumerate(concept["examples"], 1):
            source = example["code"]
            first_content = next((line for line in example["code"].splitlines() if line.strip()), "")
            if first_content[:1].isspace():
                raise ValueError(f"{concept['id']} example {index} still starts indented after normalization")
            try:
                list(tokenize.generate_tokens(io.StringIO(source if source.endswith("\n") else source + "\n").readline))
            except (tokenize.TokenError, IndentationError) as exc:
                raise ValueError(f"{concept['id']} example {index} is not lexically valid Python: {exc}") from exc


validate_examples()


def default_misconceptions(concept: dict[str, object]) -> list[dict[str, str]]:
    examples = concept["examples"]
    return [
        {
            "wrong": f"{concept['title']} is only syntax sugar with no runtime model behind it.",
            "code": examples[0]["code"],
            "correction": f"Run the first example and watch the behavior directly. {examples[0]['observe']}",
        },
        {
            "wrong": f"Once the common case for {concept['title']} works, the edge cases no longer matter.",
            "code": examples[1]["code"],
            "correction": f"The second example shows the tradeoff more clearly. {examples[1]['observe']}",
        },
    ]


def default_pitfalls(concept: dict[str, object]) -> list[dict[str, str]]:
    example = concept["examples"][2]
    return [
        {
            "title": f"A common trap around {concept['title']}",
            "code": example["code"],
            "analysis": "The bug comes from assuming the shortest form is always the clearest or safest form. In Python, the runtime model still matters.",
            "fix": example["observe"],
        }
    ]


def self_checks(concept: dict[str, object]) -> list[tuple[str, str]]:
    return [
        (f"What problem does {concept['title']} solve?", concept["problem"]),
        (f"What mental model should you picture for {concept['title']}?", ", ".join(concept["learn"])),
        (f"When should you limit or avoid {concept['title']}?", concept["why_not"]),
    ]


def graph_tables() -> tuple[dict[str, list[str]], dict[int, list[dict[str, object]]]]:
    dependents: dict[str, list[str]] = defaultdict(list)
    by_layer: dict[int, list[dict[str, object]]] = defaultdict(list)
    for concept in concepts:
        by_layer[concept["layer"]].append(concept)
        for prereq in concept["prereqs"]:
            dependents[prereq].append(concept["id"])
    return dependents, by_layer


def escape_embedded_string_newlines(text: str) -> str:
    result: list[str] = []
    i = 0
    quote: str | None = None
    triple = False
    escaped = False
    while i < len(text):
        char = text[i]
        if quote is None:
            if char in {"'", '"'}:
                if text[i:i + 3] == char * 3:
                    quote = char
                    triple = True
                    result.append(char * 3)
                    i += 3
                    continue
                quote = char
                triple = False
                result.append(char)
                i += 1
                continue
            result.append(char)
            i += 1
            continue
        if escaped:
            result.append(char)
            escaped = False
            i += 1
            continue
        if char == "\\":
            result.append(char)
            escaped = True
            i += 1
            continue
        if triple:
            if text[i:i + 3] == quote * 3:
                result.append(quote * 3)
                quote = None
                triple = False
                i += 3
                continue
            result.append(char)
            i += 1
            continue
        if char == "\n":
            result.append("\\n")
            i += 1
            continue
        if char == quote:
            quote = None
            result.append(char)
            i += 1
            continue
        result.append(char)
        i += 1
    return "".join(result)


def token_css_class(tok: tokenize.TokenInfo) -> str | None:
    if tok.type == tokenmod.STRING:
        return "tok-string"
    if tok.type == tokenmod.NUMBER:
        return "tok-number"
    if tok.type == tokenmod.COMMENT:
        return "tok-comment"
    if tok.type == tokenmod.OP:
        return "tok-operator"
    if tok.type == tokenmod.NAME:
        if keyword.iskeyword(tok.string):
            return "tok-keyword"
        if tok.string in BUILTIN_NAMES:
            return "tok-builtin"
    if tok.type == tokenmod.ERRORTOKEN and tok.string in {"@", "|", "&", "^", "~"}:
        return "tok-operator"
    return None


def build_highlighted_lines(raw: str) -> list[str]:
    lines = raw.split("\n") if raw else [""]
    source_lines = lines + [""]
    rendered: list[list[str]] = [[] for _ in lines]

    def append_range(start: tuple[int, int], end: tuple[int, int], css_class: str | None = None) -> None:
        if start == end:
            return
        start_line, start_col = start
        end_line, end_col = end
        for line_no in range(start_line, end_line + 1):
            if line_no < 1 or line_no > len(source_lines):
                continue
            source_line = source_lines[line_no - 1]
            fragment_start = start_col if line_no == start_line else 0
            fragment_end = end_col if line_no == end_line else len(source_line)
            fragment = source_line[fragment_start:fragment_end]
            if not fragment or line_no > len(rendered):
                continue
            html = escape(fragment)
            if css_class:
                html = f"<span class='{css_class}'>{html}</span>"
            rendered[line_no - 1].append(html)

    cursor = (1, 0)
    source = raw if raw.endswith("\n") else raw + "\n"
    try:
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type in {tokenmod.ENDMARKER, tokenmod.NEWLINE, tokenize.NL, tokenize.ENCODING}:
                cursor = tok.end
                continue
            if tok.start > cursor:
                append_range(cursor, tok.start)
            append_range(tok.start, tok.end, token_css_class(tok))
            cursor = tok.end
    except (tokenize.TokenError, IndentationError):
        return [escape(line) for line in lines]

    final_pos = (len(lines), len(lines[-1]))
    if cursor < final_pos:
        append_range(cursor, final_pos)
    return ["".join(parts) for parts in rendered]


def render_python_pre(code: str, label: str = "python") -> str:
    normalized = escape_embedded_string_newlines(code)
    normalized = dedent(normalized).strip("\n").replace(chr(0x2192), "->")
    highlighted_lines = build_highlighted_lines(normalized)
    multiline = len(highlighted_lines) > 1
    if multiline:
        body = "".join(
            f"<span class='code-line'><span class='line-no'>{index}</span><span class='line-text'>{line or '&nbsp;'}</span></span>"
            for index, line in enumerate(highlighted_lines, 1)
        )
        class_attr = " class='has-lines'"
    else:
        body = f"<span class='line-text'>{highlighted_lines[0] or '&nbsp;'}</span>"
        class_attr = ""
    return f"<pre data-lang='{escape(label)}'{class_attr}><code class='language-python'>{body}</code></pre>"


def render_examples(examples: list[dict[str, str]]) -> str:
    parts = []
    for index, item in enumerate(examples, 1):
        parts.append(
            """
            <article class='example-card'>
              <h4>Example {index}. {title}</h4>
              <p><strong>What this does and why:</strong> {why}</p>
              {code}
              <p><strong>What you should observe / what would happen if you changed X:</strong> {observe}</p>
            </article>
            """.format(
                index=index,
                title=escape(item["title"]),
                why=escape(item["why"]),
                code=render_python_pre(item["code"]),
                observe=escape(item["observe"]),
            )
        )
    return "".join(parts)


def render_misconceptions(items: list[dict[str, str]]) -> str:
    parts = []
    for item in items:
        parts.append(
            """
            <aside class='callout misconception misconception-card'>
              <div class='callout-title'>Misconception</div>
              <p><strong>Wrong assumption:</strong> {wrong}</p>
              {code}
              <p><strong>Correction:</strong> {correction}</p>
            </aside>
            """.format(
                wrong=escape(item["wrong"]),
                code=render_python_pre(item["code"]),
                correction=escape(item["correction"]),
            )
        )
    return "".join(parts)


def render_pitfalls(items: list[dict[str, str]]) -> str:
    parts = []
    for item in items:
        parts.append(
            """
            <aside class='callout pitfall pitfall-card'>
              <div class='callout-title'>{title}</div>
              {code}
              <p><strong>Root cause:</strong> {analysis}</p>
              <p><strong>Fix:</strong> {fix}</p>
            </aside>
            """.format(
                title=escape(item["title"]),
                code=render_python_pre(item["code"]),
                analysis=escape(item["analysis"]),
                fix=escape(item["fix"]),
            )
        )
    return "".join(parts)


def render_self_checks(items: list[tuple[str, str]]) -> str:
    return "".join(
        f"<details class='self-check'><summary>{escape(question)}</summary><div>{escape(answer)}</div></details>"
        for question, answer in items
    )


def prereq_badges(prereqs: list[str]) -> str:
    if not prereqs:
        return "<span class='badge badge-foundation'>No prerequisites</span>"
    return "".join(f"<a class='badge' href='#{pid}'>{pid}</a>" for pid in prereqs)


def wrap_table(table_html: str) -> str:
    return f"<div class='table-wrap'>{table_html}</div>"


def render_section(concept: dict[str, object], dependents: dict[str, list[str]], index: int) -> str:
    direct_dependents = dependents.get(concept["id"], [])
    next_id = concepts[index + 1]["id"] if index + 1 < len(concepts) else "quick-reference"
    misconceptions = default_misconceptions(concept)
    pitfalls = default_pitfalls(concept)
    checks = self_checks(concept)
    dependent_badges = "".join(
        f"<a class='badge badge-subtle' href='#{cid}'>{cid}</a>" for cid in direct_dependents[:6]
    ) or "<span class='badge badge-subtle'>No direct dependents listed</span>"
    explanation = (
        f"<p>{escape(concept['quick'])}</p>"
        f"<p>{escape(concept['problem'])} This section builds on {', '.join(concept['prereqs']) or 'no earlier concept IDs'} and prepares you for {', '.join(direct_dependents[:3]) or 'later integrations across the reference'}.</p>"
    )
    return f"""
<section id=\"{concept['id']}\" class=\"concept-section\" data-layer=\"{concept['layer']}\" data-title=\"{escape(concept['title'])}\">
  <div class=\"section-kicker\">{concept['id']} &middot; Layer {concept['layer']} &middot; {escape(LAYER_NAMES[concept['layer']])}</div>
  <h2>{escape(concept['title'])}</h2>
  <div class=\"section-meta\">
    <div class=\"prereq-wrap\"><span class=\"meta-label\">Read first</span>{prereq_badges(concept['prereqs'])}</div>
    <div class=\"prereq-wrap\"><span class=\"meta-label\">Used later in</span>{dependent_badges}</div>
  </div>
  <div class=\"what-youll-learn\"><h3>What you'll learn</h3><ul>{''.join(f'<li>{escape(item)}</li>' for item in concept['learn'])}</ul></div>
  <aside class=\"callout motivation\"><div class=\"callout-title\">Motivation Box</div><div class=\"callout-body\">{escape(concept['problem'])}</div></aside>
  <h3>Concept Explanation</h3>
  {explanation}
  <h3>Mental Model</h3>
  <pre class=\"mental-model\"><code>{escape(concept['mental'])}</code></pre>
  <h3>Worked Examples</h3>
  {render_examples(concept['examples'])}
  <h3>Common Misconceptions</h3>
  {render_misconceptions(misconceptions)}
  <h3>Why Not</h3>
  <p>{escape(concept['why_not'])}</p>
  <h3>Pitfalls &amp; Gotchas</h3>
  {render_pitfalls(pitfalls)}
  <h3>Self-Check Questions</h3>
  {render_self_checks(checks)}
  <div class=\"section-footer\"><a class=\"prev-link\" href=\"#dependency-table\">Back to Dependency Table</a><a class=\"next-link\" href=\"#{next_id}\">Next concept &rarr; {next_id}</a></div>
</section>
"""

def html_header(by_layer: dict[int, list[dict[str, object]]]) -> str:
    nav_groups = []
    for layer in range(15):
        links = "".join(
            f"<a href='#{concept['id']}' data-id='{concept['id']}'>{concept['id']} &middot; {escape(concept['title'])}</a>"
            for concept in by_layer[layer]
        )
        nav_groups.append(
            f"<section class='nav-group' data-layer='{layer}'><button class='group-toggle' type='button' data-layer='{layer}'><span>{NAV_LABELS[layer]}</span><span>&#9662;</span></button><div class='group-links'>{links}</div></section>"
        )
    template = """<!DOCTYPE html>
<html lang='en' data-theme='dark'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Python Complete Reference</title>
<link rel='preconnect' href='https://fonts.googleapis.com'>
<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>
<link id='darkThemeStylesheet' rel='stylesheet' href='styles-dark.css'>
<link id='lightThemeStylesheet' rel='stylesheet' href='styles-light.css' media='not all'>
<link rel='stylesheet' href='styles.css'>
<script>
try {
  const savedTheme = localStorage.getItem('python-reference-theme');
  const theme = savedTheme === 'light' ? 'light' : 'dark';
  document.documentElement.dataset.theme = theme;
  window.__initialTheme = theme;
  if (theme === 'light') {
    document.getElementById('darkThemeStylesheet').media = 'not all';
    document.getElementById('lightThemeStylesheet').media = 'all';
  }
} catch (error) {
  document.documentElement.dataset.theme = 'dark';
  window.__initialTheme = 'dark';
}
</script>
</head>
<body>
<!-- [TASK-1 START] -->
<button class='mobile-toggle' id='mobileToggle' aria-label='Toggle navigation'>&#9776;</button>
<div class='app-shell'>
<aside class='sidebar' id='sidebar'>
  <div class='sidebar-top'>
    <div class='theme-switch'>
      <div class='theme-meta'>
        <span class='theme-label'>Color Theme</span>
        <span class='theme-shortcut'><kbd>D</kbd> Toggle</span>
      </div>
      <div class='theme-toggle' role='group' aria-label='Color theme'>
        <button class='theme-option' id='themeLight' type='button' data-theme='light' aria-pressed='false'>Light</button>
        <button class='theme-option is-active' id='themeDark' type='button' data-theme='dark' aria-pressed='true'>Dark</button>
      </div>
    </div>
  </div>
  __NAV_GROUPS__
</aside>
<main>
<!-- [TASK-1 END] -->
<section class='hero' id='top'>
  <div class='section-kicker'>Python Complete Reference</div>
  <h1>Python from Runtime Basics to Expert Practice</h1>
  <p>This document is ordered by dependencies rather than as a loose glossary. Each topic appears only after its prerequisites, so you can learn the runtime model, core syntax, data structures, functions, OOP, protocols, packaging, concurrency, testing, and performance in a sequence that does not smuggle in unexplained concepts.</p>
  <p>The left sidebar is grouped by layer and highlights the active section as you scroll. Every concept section includes motivation, explanation, mental model, examples, misconceptions, pitfalls, and self-check questions so the file reads like a compact textbook instead of a cheatsheet.</p>
</section>"""
    return template.replace("__NAV_GROUPS__", "".join(nav_groups))

def render_dependency_table(dependents: dict[str, list[str]]) -> str:
    rows = []
    for concept in concepts:
        rows.append(
            f"<tr><td><a href='#{concept['id']}'>{concept['id']}</a></td><td>{escape(concept['title'])}</td><td>{concept['layer']}</td><td>{', '.join(concept['prereqs']) or 'None'}</td><td>{', '.join(dependents.get(concept['id'], [])) or 'None'}</td></tr>"
        )
    table_html = f"<table><thead><tr><th>ID</th><th>Concept Name</th><th>Layer</th><th>Direct Prerequisites</th><th>Direct Dependents</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"
    return f"""<!-- [TASK-2 START] --><section class='concept-section' id='dependency-table' data-title='Dependency Table'><div class='section-kicker'>Dependency Table</div><h2>Python Concept Dependencies</h2><p>Use this table as the overview for the reference. Each row shows a concept, the layer it belongs to, the concepts you should understand first, and the concepts that build on it later.</p>{wrap_table(table_html)}</section><!-- [TASK-2 END] -->"""


def render_resources_and_quickref() -> str:
    rows = []
    for concept in concepts:
        rows.append(
            f"<tr><td><a href='#{concept['id']}'>{concept['id']}</a></td><td>{concept['layer']}</td><td>{escape(concept['title'])}</td><td>{escape(concept['quick'])}</td></tr>"
        )
    quick_table = f"<table><thead><tr><th>ID</th><th>Layer</th><th>Concept</th><th>One-line Description</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"
    return f"""
<section class='resources' id='whats-next' data-title='What\'s Next?'>
  <div class='section-kicker'>What's Next?</div>
  <h2>Keep Going After This Reference</h2>
  <p>The official documentation stays authoritative for edge cases, the CPython source explains how the reference runtime behaves, and PEPs record the design reasoning behind major language changes. Once this document feels comfortable, the books below are excellent second passes because they focus on Pythonic design rather than raw syntax collection.</p>
  <ul>
    <li><a href='https://docs.python.org/3/'>Official Python docs</a></li>
    <li><a href='https://github.com/python/cpython'>CPython source on GitHub</a></li>
    <li><a href='https://peps.python.org/'>PEPs index</a></li>
    <li><cite>Fluent Python</cite> by Luciano Ramalho</li>
    <li><cite>Python Cookbook</cite> by David Beazley and Brian K. Jones</li>
  </ul>
</section>
<section class='quick-reference' id='quick-reference' data-title='Quick Reference'>
  <div class='section-kicker'>Quick Reference</div>
  <h2>All 59 Concepts at a Glance</h2>
  {wrap_table(quick_table)}
</section>
"""


def html_footer() -> str:
    return r"""
<!-- [TASK-11 START] -->
</main></div><button class='back-to-top' id='backToTop' aria-label='Back to top'>&uarr; Top</button>
<script>
const navLinks = [...document.querySelectorAll('.group-links a')];
const trackedSections = [...document.querySelectorAll('.concept-section, #quick-reference, #whats-next')];
const sidebar = document.getElementById('sidebar');
const mobileToggle = document.getElementById('mobileToggle');
const backToTop = document.getElementById('backToTop');
const darkThemeStylesheet = document.getElementById('darkThemeStylesheet');
const lightThemeStylesheet = document.getElementById('lightThemeStylesheet');
const themeButtons = [...document.querySelectorAll('.theme-option')];
const THEME_STORAGE_KEY = 'python-reference-theme';
let currentTheme = window.__initialTheme === 'light' ? 'light' : 'dark';
document.body.dataset.theme = currentTheme;

function syncThemeButtons(theme) {
  themeButtons.forEach((button) => {
    const active = button.dataset.theme === theme;
    button.classList.toggle('is-active', active);
    button.setAttribute('aria-pressed', String(active));
  });
}

function isTypingTarget(target) {
  return target instanceof HTMLElement && (target.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName));
}

function applyTheme(theme, persist = true) {
  const nextTheme = theme === 'light' ? 'light' : 'dark';
  if (nextTheme === currentTheme) {
    syncThemeButtons(currentTheme);
    return;
  }
  currentTheme = nextTheme;
  document.documentElement.dataset.theme = currentTheme;
  document.body.dataset.theme = currentTheme;
  darkThemeStylesheet.media = currentTheme === 'dark' ? 'all' : 'not all';
  lightThemeStylesheet.media = currentTheme === 'light' ? 'all' : 'not all';
  syncThemeButtons(currentTheme);
  if (persist) {
    try {
      localStorage.setItem(THEME_STORAGE_KEY, currentTheme);
    } catch (error) {
      // Ignore storage errors and keep the in-memory theme.
    }
  }
}

function copyBlockText(pre) {
  const lineTexts = [...pre.querySelectorAll('.line-text')];
  if (lineTexts.length) {
    return lineTexts.map((line) => line.textContent || '').join('\n');
  }
  return pre.querySelector('code')?.textContent || '';
}

document.querySelectorAll('pre[data-lang]').forEach((pre) => {
  const button = document.createElement('button');
  button.className = 'copy-btn';
  button.type = 'button';
  button.textContent = 'Copy';
  button.addEventListener('click', async () => {
    const raw = copyBlockText(pre);
    await navigator.clipboard.writeText(raw);
    button.textContent = 'Copied';
    setTimeout(() => { button.textContent = 'Copy'; }, 1200);
  });
  pre.appendChild(button);
});

themeButtons.forEach((button) => {
  button.addEventListener('click', () => {
    applyTheme(button.dataset.theme || 'dark');
  });
});

document.querySelectorAll('.group-toggle').forEach((button) => {
  button.addEventListener('click', () => {
    button.parentElement.classList.toggle('collapsed');
  });
});

mobileToggle.addEventListener('click', () => {
  sidebar.classList.toggle('open');
});

navLinks.forEach((link) => {
  link.addEventListener('click', () => {
    if (window.innerWidth < 769) {
      sidebar.classList.remove('open');
    }
  });
});

function updateScrollState() {
  backToTop.classList.toggle('visible', window.scrollY > 600);
}

const activeObserver = new IntersectionObserver((entries) => {
  const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio);
  if (!visible.length) {
    return;
  }
  const current = visible[0].target;
  navLinks.forEach((link) => {
    const active = link.getAttribute('href') === `#${current.id}`;
    link.classList.toggle('active', active);
    if (active) {
      link.closest('.nav-group')?.classList.remove('collapsed');
    }
  });
}, { rootMargin: '-18% 0px -58% 0px', threshold: [0.2, 0.45, 0.65] });
trackedSections.forEach((section) => activeObserver.observe(section));

backToTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

document.addEventListener('keydown', (event) => {
  if (event.defaultPrevented || event.ctrlKey || event.metaKey || event.altKey) {
    return;
  }
  if (event.key.toLowerCase() !== 'd') {
    return;
  }
  if (isTypingTarget(event.target)) {
    return;
  }
  event.preventDefault();
  applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
});

window.addEventListener('scroll', updateScrollState, { passive: true });
updateScrollState();
syncThemeButtons(currentTheme);
</script>
<!-- [TASK-11 END] -->
</body></html>
"""


def build_document() -> str:
    dependents, by_layer = graph_tables()
    parts = [html_header(by_layer), render_dependency_table(dependents)]
    ranges = {3:("PY01","PY08"),4:("PY09","PY14"),5:("PY15","PY18"),6:("PY19","PY24"),7:("PY25","PY31"),8:("PY32","PY38"),9:("PY39","PY50"),10:("PY51","PY59")}
    for task_num, (start_id, end_id) in ranges.items():
        parts.append(f"<!-- [TASK-{task_num} START] -->")
        start = next(i for i, c in enumerate(concepts) if c['id'] == start_id)
        end = next(i for i, c in enumerate(concepts) if c['id'] == end_id)
        for index in range(start, end + 1):
            parts.append(render_section(concepts[index], dependents, index))
        parts.append(f"<!-- [TASK-{task_num} END] -->")
    parts.append(render_resources_and_quickref())
    parts.append(html_footer())
    return ''.join(parts)


def validate(document: str) -> None:
    assert STYLESHEET.exists(), STYLESHEET
    assert LIGHT_STYLESHEET.exists(), LIGHT_STYLESHEET
    assert DARK_STYLESHEET.exists(), DARK_STYLESHEET
    for concept in concepts:
        cid = concept['id']
        assert document.count(f"id=\"{cid}\"") == 1, cid
        assert f"href='#{cid}'" in document or f'href=\"#{cid}\"' in document, cid
    assert "id='dependency-table'" in document or 'id="dependency-table"' in document
    assert "mermaid" not in document
    assert "concept-map" not in document
    assert 'lorem ipsum' not in document.lower()


if __name__ == '__main__':
    if len(concepts) != 59:
        raise SystemExit(f"Expected 59 concepts, found {len(concepts)}")
    document = build_document()
    validate(document)
    OUTFILE.write_text(document, encoding='utf-8')
    print(f"Wrote {OUTFILE}")
