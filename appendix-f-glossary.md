# Appendix F — Glossary

Every key term from the book, alphabetized, with the chapter that introduces it.

Terms are defined where they first do real work rather than where they are first mentioned in passing. A cross-reference such as *(Ch 11)* points to the chapter whose Key Terms section defines it, and where the surrounding explanation lives.

---


## A

**abstract class** — a class with at least one pure virtual function; cannot be instantiated. *(Ch 21)*

**access specifier** — `public`, `protected`, or `private`, controlling what may reach a member. *(Ch 18)*

**accessor** — a member function that reads state without modifying it. *(Ch 18)*

**accumulator** — a variable that builds a running total across loop passes. *(Ch 7)*

**adaptive maintenance** — changes responding to a changed environment. *(Ch 13)*

**address** — the number identifying one cell of main memory. *(Ch 1)*

**address-of operator** — `&`, giving the address of a variable. *(Ch 10)*

**aggregate initialization** — initializing a struct's members with a brace-enclosed list in declaration order. *(Ch 14)*

**agile** — a lifecycle model with short cycles, continuous feedback, and changing requirements. *(Ch 13)*

**algorithm** — a finite sequence of unambiguous, effective steps that solves a problem. *(Ch 5)*

**algorithm (STL)** — a standard function operating on an iterator range. *(Ch 23)*

**analysis** — the phase that models the problem precisely. *(Ch 13)*

**application software** — software that performs a task a user wants done, as opposed to managing the machine. *(Ch 1)*

**argument** — a value passed to a function at the call site. *(Ch 8)*

**array** — a collection of values of one type, stored under one name and reached by index. *(Ch 11)*

**ASCII** — a character encoding assigning the values 0–127 to English letters, digits, punctuation, and control codes. *(Ch 1)*

**assembler** — a program translating assembly language into machine language. *(Ch 1)*

**assembly language** — a low-level language with one short mnemonic per machine instruction, specific to a processor family. *(Ch 1)*

**assertion** — a checked statement of something that must be true, removed in release builds. *(Ch 16)*

**assignment** — storing a new value in an existing variable, written with `=`. *(Ch 3)*

**associativity** — the rule deciding the order among operators of equal precedence. *(Ch 4)*

**at()** — a bounds-checked element access that throws on an invalid index. *(Ch 12)*

**automatic storage** — memory for local variables, released when scope ends. *(Ch 22)*


## B

**base case** — the condition under which a recursive function returns without recursing. *(Ch 10)*

**base class** — a class from which another inherits. *(Ch 20)*

**binary** — base two, using the digits 0 and 1. *(Ch 1)*

**binary search** — a search that halves the remaining range each step; requires sorted data. *(Ch 17)*

**bit** — the smallest unit of data, holding one of two states. *(Ch 1)*

**bitwise operator** — an operator acting on the individual bits of a value. *(Ch 4)*

**block** — a group of statements enclosed in braces and treated as a unit. *(Ch 2)*

**bool** — a type holding exactly `true` or `false`. *(Ch 3)*

**Boolean expression** — an expression producing `true` or `false`. *(Ch 6)*

**bounds** — the valid range of indices for an array, 0 through size−1. *(Ch 11)*

**break** — a statement exiting a loop immediately. *(Ch 7)*

**breakpoint** — an instruction to pause execution at a particular line. *(Ch 16)*

**build tool** — a program that automates compiling a project of many files. *(Ch 2)*

**byte** — eight bits; the standard unit of storage; holds 256 distinct patterns. *(Ch 1)*

**bytecode** — an intermediate form produced by a hybrid language's compiler and executed by a virtual machine. *(Ch 1)*


## C

**C string** — a `char` array terminated by the null character `'\0'`. *(Ch 11)*

**call** — to invoke a function by name. *(Ch 8)*

**call stack** — the sequence of function calls leading to the current point. *(Ch 16)*

**capture list** — the `[]` of a lambda, naming what it takes from the surrounding scope. *(Ch 23)*

**cast** — an explicit conversion of a value to another type, written `static_cast<Type>(value)`. *(Ch 3)*

**catch** — a clause handling an exception of a stated type. *(Ch 24)*

**category weight** — the percentage of a final grade a category contributes. *(Ch 20)*

**char** — a type holding one character in one byte; also a small integer. *(Ch 3)*

**class** — a type bundling data with the functions that operate on it. *(Ch 18)*

**class template** — a class parameterized by one or more types. *(Ch 23)*

**code point** — the number Unicode assigns to a character. *(Ch 1)*

**coding standard** — a written agreement on formatting, naming, and documentation. *(Ch 13)*

**comment** — text in source code ignored by the compiler, written for human readers. *(Ch 2)*

**comparison function** — a function defining an ordering, passed to a sorting routine. *(Ch 17)*

**compile-time error** — a fault preventing the compiler from producing a program. *(Ch 4)*

**compiler** — a program translating an entire source program into machine code before it runs. *(Ch 1)*

**composition** — holding an object as a member, expressing "has-a". *(Ch 20)*

**compound assignment** — an operator such as `+=` combining an operation with assignment. *(Ch 4)*

**condition** — the Boolean expression a selection statement tests. *(Ch 6)*

**conditional breakpoint** — a breakpoint that pauses only when a condition holds. *(Ch 16)*

**conditional operator** — `? :`, which selects between two values. *(Ch 6)*

**const** — a qualifier marking a variable as unmodifiable. *(Ch 3)*

**const member function** — a member function that does not modify the object. *(Ch 18)*

**constructor** — a function run when an object is created, establishing its invariant. *(Ch 18)*

**container** — a class holding a collection of objects. *(Ch 23)*

**continue** — a statement skipping the rest of the current pass. *(Ch 7)*

**copy assignment** — the operation assigning one existing object to another. *(Ch 19)*

**copy constructor** — the constructor creating an object as a copy of another. *(Ch 19)*

**corrective maintenance** — fixing defects. *(Ch 13)*

**counter** — a variable counting the number of loop passes. *(Ch 7)*

**counter-controlled** — repetition running a known number of times. *(Ch 7)*


## D

**dangling pointer** — a pointer to memory that has been released. *(Ch 22)*

**debug build** — a build with debug information and no optimization. *(Ch 24)*

**debugger** — a tool for pausing a running program and inspecting its state. *(Ch 2)*

**decimal** — base ten, using the digits 0 through 9. *(Ch 1)*

**decision** — a flowchart symbol, drawn as a diamond, with one entry and two labelled exits. *(Ch 5)*

**declaration** — a statement bringing a variable into existence with a name and type. *(Ch 3)*

**decrement** — the `--` operator, subtracting one. *(Ch 4)*

**default argument** — a parameter value used when the caller omits that argument. *(Ch 9)*

**defect report** — a record of a fault's symptom, cause, fix, and verification. *(Ch 16)*

**definition** — a function's full declaration together with its body. *(Ch 9)*

**delimiter** — the character separating fields in a line of text. *(Ch 15)*

**dereference operator** — `*`, giving the value stored at an address. *(Ch 10)*

**derived class** — a class inheriting from another. *(Ch 20)*

**design** — the phase deciding how a system will be built. *(Ch 13)*

**desk check** — testing an algorithm by hand with specific values. *(Ch 5)*

**destructor** — a function run when an object is destroyed. *(Ch 18)*

**development** — the phase in which code is written, integrated, and tested. *(Ch 13)*

**distribution** — an object shaping raw random values into a desired range. *(Ch 8)*

**divide and conquer** — solving a problem by splitting it, solving the parts, and combining. *(Ch 17)*

**do/while** — a loop testing its condition after the body, so the body always runs once. *(Ch 7)*

**dot operator** — `.`, used to reach a member of a struct or object. *(Ch 14)*

**double** — the standard floating-point type, 8 bytes, about 15 digits of precision. *(Ch 3)*

**double free** — releasing the same memory twice. *(Ch 22)*

**dynamic binding** — deciding at run time which function a call invokes, based on the object's type. *(Ch 21)*

**dynamic library** — a library loaded when a program runs. *(Ch 24)*

**dynamic storage** — heap memory obtained with `new` and released with `delete`. *(Ch 22)*

**dynamic_cast** — a cast checking at run time whether an object is of a given type. *(Ch 21)*


## E

**editor** — the program in which source code is written. *(Ch 2)*

**element** — one value stored in an array. *(Ch 11)*

**encapsulation** — bundling data with behavior and restricting access to the data. *(Ch 18)*

**encoding** — a scheme for storing Unicode code points as bytes; UTF-8 is the most common. *(Ch 1)*

**enumerated type** — a type whose values are a small fixed named set. *(Ch 3)*

**error** — a problem that prevents the compiler from producing a program. *(Ch 2)*

**escape sequence** — a backslash followed by a character, representing one character that cannot be typed directly. *(Ch 3)*

**exception** — an object thrown to signal a condition the caller must handle. *(Ch 24)*

**exception safety** — the property that a failed operation leaves objects in a valid state. *(Ch 24)*

**executable** — a file containing machine code that the operating system can run. *(Ch 2)*

**explicit** — a qualifier preventing implicit conversion through a constructor. *(Ch 18)*

**expression** — any construct producing a value. *(Ch 4)*

**extraction operator** — `>>`, which reads a value from an input stream. *(Ch 3)*


## F

**fall-through** — continuing into the next `case` because `break` was omitted. *(Ch 6)*

**file stream** — a stream connected to a file. *(Ch 15)*

**float** — a smaller floating-point type, 4 bytes, about 6 digits of precision. *(Ch 3)*

**floating-point** — a representation of real numbers as a sign, mantissa, and exponent, offering wide range with limited precision. *(Ch 1)*

**flowchart** — a diagram showing the steps of an algorithm and the order in which they run. *(Ch 5)*

**for** — a loop gathering initialization, condition, and update into one line. *(Ch 7)*

**friend** — a function granted access to a class's private members. *(Ch 19)*

**function** — a named piece of code performing a task. *(Ch 8)*

**function pointer** — a variable holding the address of a function. *(Ch 17)*

**function template** — a function parameterized by one or more types. *(Ch 23)*


## G

**generator** — an object producing a sequence of pseudorandom values. *(Ch 8)*

**getline** — a function reading an entire line of text, including spaces. *(Ch 3)*

**global variable** — a variable declared outside every function, visible to all. *(Ch 10)*


## H

**hardware** — the physical components of a computer. *(Ch 1)*

**has-a** — a relationship expressed by composition. *(Ch 20)*

**header** — a file, brought in with `#include`, declaring facilities defined elsewhere. *(Ch 2)*

**header guard** — `#ifndef`/`#define`/`#endif` preventing a header from being processed twice. *(Ch 10)*

**heap** — the memory region for dynamically allocated objects. *(Ch 22)*

**hexadecimal** — base sixteen, using the digits 0–9 and letters A–F; each digit corresponds to four bits. *(Ch 1)*

**high-level language** — a language whose statements describe operations in terms closer to the problem than to the machine. *(Ch 1)*


## I

**IDE** — an integrated development environment, bundling editor, compiler, and debugger. *(Ch 2)*

**identifier** — a programmer-chosen name. *(Ch 3)*

**ifstream** — an input file stream. *(Ch 15)*

**implicit conversion** — an automatic type conversion performed by the compiler. *(Ch 4)*

**increment** — the `++` operator, adding one. *(Ch 4)*

**index** — the number identifying an element's position; also called a subscript. *(Ch 11)*

**infinite loop** — a loop whose condition never becomes false. *(Ch 7)*

**inheritance** — deriving a new class from an existing one. *(Ch 20)*

**initialization** — giving a variable a value at the moment it is declared. *(Ch 3)*

**initializer list** — the `: member(value)` syntax initializing members before the constructor body. *(Ch 18)*

**input** — data entering the computer from outside. *(Ch 1)*

**insertion operator** — `<<`, which sends data into an output stream. *(Ch 2)*

**insertion sort** — a sort that inserts each element into the sorted portion; adapts to input. *(Ch 17)*

**instance** — one object of a class. *(Ch 18)*

**instantiation** — the compiler's generation of concrete code from a template for a given type. *(Ch 23)*

**int** — the standard integer type, 4 bytes. *(Ch 3)*

**integer division** — division of two integers, discarding the remainder. *(Ch 4)*

**interface** — the set of operations an abstract class promises every derived class provides. *(Ch 21)*

**interpreter** — a program translating and executing source code line by line as it runs. *(Ch 1)*

**invariant** — a property that is always true of an object. *(Ch 18)*

**is-a** — a relationship expressed by inheritance. *(Ch 20)*

**iteration** — one pass through a loop body; also, repetition in general. *(Ch 7)*

**iterative model** — a lifecycle repeating all phases, producing working software each cycle. *(Ch 13)*

**iterator** — an object identifying a position in a container. *(Ch 23)*


## L

**lambda** — an unnamed function defined where it is used. *(Ch 23)*

**lifetime** — the period during which a variable exists. *(Ch 9)*

**linear search** — a search examining elements one at a time in order. *(Ch 17)*

**linked list** — a chain of nodes, each holding a value and a pointer to the next. *(Ch 22)*

**linker** — the tool that joins object files and library code into an executable. *(Ch 2)*

**literal** — a value written directly in source code. *(Ch 3)*

**loader** — the operating system component that copies an executable into memory and starts it. *(Ch 2)*

**local variable** — a variable declared inside a function, existing only while it runs. *(Ch 9)*

**logic error** — a fault in which a valid program produces a wrong result. *(Ch 4)*

**logical operator** — `&&`, `||`, or `!`, combining Boolean expressions. *(Ch 6)*

**loop control variable** — the variable a loop tests and updates. *(Ch 7)*


## M

**machine language** — the numeric instruction codes a processor executes directly. *(Ch 1)*

**magic number** — an unexplained numeric value in code; avoid by naming it. *(Ch 3)*

**main** — the function where execution of a C++ program begins. *(Ch 2)*

**main memory** — fast, volatile storage holding data and instructions in current use; also called RAM. *(Ch 1)*

**maintenance** — the phase in which working software is kept correct and current. *(Ch 13)*

**manipulator** — a value such as `std::fixed` that changes how a stream formats output. *(Ch 4)*

**mantissa** — the significant digits of a floating-point value. *(Ch 1)*

**map** — an associative container of key–value pairs, sorted by key. *(Ch 23)*

**member** — a variable declared inside a struct or class. *(Ch 14)*

**member function** — a function belonging to an object, called with a dot. *(Ch 12)*

**memory leak** — allocated memory that is never released. *(Ch 22)*

**merge** — combining two sorted sequences into one sorted sequence. *(Ch 17)*

**merge sort** — a divide-and-conquer sort with *n* log *n* comparisons. *(Ch 17)*

**modular design** — organizing a program as small parts, each doing one thing. *(Ch 9)*

**modulus** — the `%` operator, giving the remainder of integer division. *(Ch 4)*

**move semantics** — transferring a resource from one object to another instead of copying. *(Ch 22)*

**multilevel hierarchy** — a chain in which a derived class is itself a base. *(Ch 20)*

**mutator** — a member function that changes state. *(Ch 18)*


## N

**namespace** — a named scope grouping declarations to prevent collisions. *(Ch 23)*

**nested conditional** — a conditional statement inside another. *(Ch 6)*

**nested loop** — a loop contained within another loop. *(Ch 7)*

**nested struct** — a struct used as the type of a member of another struct. *(Ch 14)*

**newline** — the character `\n`, which moves output to the next line. *(Ch 2)*

**non-volatile** — retaining contents when power is removed. *(Ch 1)*

**npos** — the value `find` returns when nothing matches. *(Ch 12)*

**null pointer** — a pointer holding `nullptr`, pointing at nothing. *(Ch 10)*

**null terminator** — the `'\0'` character marking the end of a C string. *(Ch 11)*


## O

**object** — an instance of a class, holding its own state. *(Ch 18)*

**object file** — machine code produced from one source file, not yet runnable. *(Ch 2)*

**object slicing** — losing the derived part of an object by copying it into a base-typed variable. *(Ch 21)*

**object-oriented programming** — organizing a program as objects bundling data with operations. *(Ch 13)*

**octal** — base eight; each digit corresponds to three bits. *(Ch 1)*

**off-by-one error** — a loop running one pass too many or too few. *(Ch 7)*

**ofstream** — an output file stream. *(Ch 15)*

**operand** — a value an operator acts upon. *(Ch 4)*

**operator** — a symbol combining operands to produce a value. *(Ch 4)*

**operator overloading** — defining what an operator means for a user-defined type. *(Ch 19)*

**out of bounds** — an index outside the valid range; undefined behavior. *(Ch 11)*

**output** — data leaving the computer to the outside world. *(Ch 1)*

**overflow** — what happens when a value exceeds its type's range; the value wraps around. *(Ch 3)*

**overload resolution** — the compiler's choice among overloaded functions based on argument types. *(Ch 10)*

**overloading** — defining several functions with one name and different parameter lists. *(Ch 10)*

**override** — a keyword asking the compiler to verify that a function overrides a base virtual. *(Ch 21)*

**overriding** — replacing a base class function with one of the same signature. *(Ch 20)*


## P

**paradigm** — a style of organizing a program, such as procedural, object-oriented, or functional. *(Ch 1)*

**parallel arrays** — separate arrays in which the same index refers to related values. *(Ch 11)*

**parameter** — the name a function uses internally for an argument it receives. *(Ch 8)*

**parsing** — extracting structured values from text. *(Ch 15)*

**pass by reference** — passing a reference so a function can modify the caller's variable. *(Ch 10)*

**pass by value** — passing a copy of an argument, so the caller's variable is unaffected. *(Ch 9)*

**perfective maintenance** — adding capability users want. *(Ch 13)*

**persistence** — storing data so it survives after a program ends. *(Ch 15)*

**planning** — the phase deciding whether and what to build. *(Ch 13)*

**pointer** — a variable holding the address of another variable. *(Ch 10)*

**polymorphic collection** — a container of base pointers holding objects of several derived types. *(Ch 21)*

**polymorphism** — one call producing behavior determined by the object rather than the calling code. *(Ch 21)*

**pop_back** — removes the last element of a vector. *(Ch 12)*

**precedence** — the rule deciding which operator acts first. *(Ch 4)*

**precondition** — a requirement the caller must satisfy, stated with `@pre`. *(Ch 9)*

**preprocessor** — the tool that carries out `#include`, `#define`, and other directives before compilation. *(Ch 2)*

**preprocessor directive** — a line beginning with `#`, addressed to the preprocessor. *(Ch 2)*

**preventive maintenance** — changes making future modification easier. *(Ch 13)*

**priming read** — an input read before a sentinel loop, so the condition has something to test. *(Ch 7)*

**procedural programming** — organizing a program as procedures operating on separately held data. *(Ch 13)*

**process** — a flowchart symbol, drawn as a rectangle, representing a computation or assignment. *(Ch 5)*

**processor** — the component that fetches, decodes, and executes instructions; also called the CPU. *(Ch 1)*

**program** — a sequence of instructions telling a computer how to accomplish a task. *(Ch 1)*

**protected** — an access level permitting the class and its derived classes. *(Ch 20)*

**prototype** — a declaration of a function's signature without its body. *(Ch 9)*

**pseudocode** — a description of an algorithm in structured English. *(Ch 5)*

**pseudorandom** — generated deterministically from a seed but statistically resembling randomness. *(Ch 8)*

**pure virtual function** — a virtual function with no implementation, declared `= 0`. *(Ch 21)*

**push_back** — adds an element to the end of a vector. *(Ch 12)*


## R

**RAII** — Resource Acquisition Is Initialization; tying resource lifetime to object lifetime. *(Ch 22)*

**range** — a pair of iterators marking the beginning and one-past-the-end of a sequence. *(Ch 23)*

**range-based for** — a loop visiting every element of a collection without an index. *(Ch 12)*

**record** — a group of related values treated as one item; in C++, a struct. *(Ch 14)*

**recursion** — a function calling itself. *(Ch 10)*

**refactoring** — changing internal structure without changing behavior. *(Ch 13)*

**reference** — an alternative name for an existing variable. *(Ch 10)*

**regression test** — a test written for a specific defect, failing before the fix and passing after. *(Ch 16)*

**relational operator** — an operator comparing two values: `<`, `>`, `<=`, `>=`, `==`, `!=`. *(Ch 6)*

**release build** — an optimized build with assertions removed. *(Ch 24)*

**repetition** — a control structure that performs steps more than once. *(Ch 5)*

**requirements statement** — a plain-language description of what a program must do. *(Ch 5)*

**return** — a statement producing a function's result and exiting it. *(Ch 9)*

**return value** — the result a function hands back to its caller. *(Ch 8)*

**row-major order** — the layout in which each row of a two-dimensional array is stored contiguously. *(Ch 11)*

**Rule of Three** — needing any of destructor, copy constructor, or copy assignment implies needing all three. *(Ch 22)*

**run-time error** — a fault occurring while the program runs. *(Ch 4)*


## S

**scope** — the region of a program in which a name exists. *(Ch 6)*

**seed** — the starting value determining a pseudorandom sequence. *(Ch 8)*

**selection** — a control structure that chooses between paths based on a condition. *(Ch 5)*

**selection sort** — a sort that repeatedly moves the smallest remaining element into place. *(Ch 17)*

**sentinel** — a special input value signalling the end of data. *(Ch 7)*

**sentinel-controlled** — repetition running until a sentinel value appears. *(Ch 7)*

**sequence** — a control structure in which steps happen one after another in order. *(Ch 5)*

**shared_ptr** — a smart pointer with reference counting and shared ownership. *(Ch 22)*

**short-circuit evaluation** — stopping evaluation of a compound condition once the result is determined. *(Ch 6)*

**signature** — a function's return type, name, and parameter list. *(Ch 8)*

**size_t** — the unsigned type used for container sizes and indices. *(Ch 12)*

**smart pointer** — an object that owns a pointer and releases it automatically. *(Ch 22)*

**software** — the instructions a computer carries out. *(Ch 1)*

**software development lifecycle** — the phases through which software is planned, built, and maintained. *(Ch 13)*

**source code** — the text of a program as written by a programmer. *(Ch 1)*

**specification** — a precise, checkable description of inputs, processing, and outputs. *(Ch 5)*

**stability** — whether a sort preserves the relative order of equal elements. *(Ch 17)*

**stack** — the memory region holding function frames and local variables. *(Ch 22)*

**stack frame** — one function call's entry on the call stack, holding its local variables. *(Ch 16)*

**stack overflow** — a crash caused by recursion that never reaches its base case. *(Ch 10)*

**stack unwinding** — destroying local objects while leaving functions between a throw and its handler. *(Ch 24)*

**standard library** — the collection of facilities every C++ implementation provides. *(Ch 2)*

**state** — the data an object holds. *(Ch 18)*

**statement** — a single instruction, ending in a semicolon. *(Ch 2)*

**static binding** — deciding at compile time which function a call invokes. *(Ch 21)*

**static library** — a library copied into an executable at link time. *(Ch 24)*

**static local variable** — a local variable retaining its value between calls. *(Ch 10)*

**static member** — a member belonging to the class rather than to any object. *(Ch 19)*

**std** — the namespace containing the standard library. *(Ch 2)*

**std::cin** — the standard input stream, normally the keyboard. *(Ch 3)*

**std::string** — a type holding text of any length. *(Ch 3)*

**std::vector** — the standard growable sequence container. *(Ch 12)*

**step into** — execute the current line, entering any function it calls. *(Ch 16)*

**step out** — finish the current function and return to its caller. *(Ch 16)*

**step over** — execute the current line without entering functions it calls. *(Ch 16)*

**STL** — the Standard Template Library: containers, iterators, and algorithms. *(Ch 23)*

**storage** — non-volatile, slower memory holding data that must survive power loss. *(Ch 1)*

**stream** — a destination or source for sequential data, such as `std::cout`. *(Ch 2)*

**stream state** — the flags recording whether a stream has failed or reached its end. *(Ch 15)*

**string literal** — text enclosed in double quotes. *(Ch 2)*

**stringstream** — a stream reading from or writing to a string in memory. *(Ch 15)*

**struct** — a type grouping related values under one name. *(Ch 14)*

**structure chart** — a diagram showing what a program is composed of and which part calls which. *(Ch 5)*

**structured programming** — building programs from sequence, selection, and repetition only. *(Ch 5)*

**subscript** — the bracketed index used to reach an element. *(Ch 11)*

**substr** — a function returning part of a string. *(Ch 12)*

**switch** — a statement comparing one integral value against a list of constants. *(Ch 6)*

**symbolic debugger** — a debugger presenting a program in terms of its source names. *(Ch 16)*

**system software** — software managing the computer itself, such as an operating system. *(Ch 1)*


## T

**table-driven** — organized so that behavior is determined by data rather than by branching code. *(Ch 11)*

**tag** — a leading field identifying what kind of record a line holds. *(Ch 15)*

**technical debt** — the accumulated future cost of shortcuts taken now. *(Ch 13)*

**template** — a type parameterized by another type, as in `std::vector<double>`. *(Ch 12)*

**template parameter** — the placeholder type in a template, conventionally `T`. *(Ch 23)*

**terminator** — a flowchart symbol, drawn as a rounded rectangle, marking a start or end. *(Ch 5)*

**test case** — an input paired with an independently determined expected result. *(Ch 16)*

**this** — a pointer, available in member functions, to the object the function was called on. *(Ch 19)*

**throw** — to raise an exception. *(Ch 24)*

**top-down decomposition** — breaking a problem into parts, and those parts into smaller parts. *(Ch 5)*

**trace table** — a table recording the value of each variable at each step of a desk check. *(Ch 5)*

**translation unit** — the single expanded file the preprocessor produces from one source file. *(Ch 2)*

**truncate** — to empty a file when opening it for output. *(Ch 15)*

**truncation** — discarding a fractional part rather than rounding. *(Ch 4)*

**try block** — a region whose exceptions may be handled by following `catch` clauses. *(Ch 24)*

**two's complement** — the standard representation of signed integers, in which the leftmost bit carries a negative place value. *(Ch 1)*

**two-dimensional array** — an array of arrays, forming a grid. *(Ch 11)*

**type** — the property of a variable determining what values it can hold, how many bytes it occupies, and how its bits are interpreted. *(Ch 3)*


## U

**Unicode** — a standard assigning a code point to every character in every writing system. *(Ch 1)*

**unique_ptr** — a smart pointer with sole ownership, releasing on destruction. *(Ch 22)*

**unordered_map** — a hash-based associative container with faster lookup and no ordering. *(Ch 23)*

**unsigned** — an integer type with no negative values, using all its bits for magnitude. *(Ch 3)*

**UTF-8** — a Unicode encoding storing each character in one to four bytes, compatible with ASCII. *(Ch 1)*


## V

**variable** — a named memory location holding a value of a particular type. *(Ch 3)*

**version control** — a system recording every change to a codebase. *(Ch 13)*

**virtual destructor** — a destructor declared `virtual`, ensuring the full object is destroyed through a base pointer. *(Ch 21)*

**virtual function** — a member function whose implementation is chosen by the object's actual type. *(Ch 21)*

**virtual machine** — a program executing bytecode, allowing hybrid-language programs to run on many platforms. *(Ch 1)*

**void** — the return type of a function that returns no value. *(Ch 9)*

**volatile** — losing contents when power is removed. *(Ch 1)*


## W

**warning** — a report of something suspicious that did not prevent compilation. *(Ch 2)*

**watch expression** — an expression the debugger evaluates and displays as you step. *(Ch 16)*

**watchpoint** — a breakpoint that fires when a variable's value changes. *(Ch 16)*

**waterfall model** — a lifecycle completing each phase before beginning the next. *(Ch 13)*

**what()** — the member function returning an exception's message. *(Ch 24)*

**while** — a loop testing its condition before each pass. *(Ch 7)*

**word** — the amount of data a processor handles most naturally in one operation; commonly 64 bits. *(Ch 1)*
