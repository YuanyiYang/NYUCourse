# NYU Courses 

Some code from assignments for various classes, including Programming Language, Open Source Tool, Operating System... Just for fun.
## Operating System
### Memory Management Unit(MMU)
This is to simulate the algorithm to find a victim when a page fault occurs. Algorithm consists of Aging, LRU, NRU, Clock, FIFO, Second Chance, Random.

### Process Scheduler
This is to simulate process dispatcher in CPU. Implement algorithm including FIFO, LIFO, SJF, Round-Robin and Priority Queue.

### Two-Pass Linker
This is to simulate a linker before loading a program. It need two passes over the code.


## Programming Language
### Scheme Interpreter
####Overview
A mini-interpreter written in scheme, able to interpret itself. 
####Files
<b>myInterpreter.scm</b>: supports syntaxes including: _define, if, cold, let, let*, letrec, quote, apply, and, or_

<b>library.scm</b>: contains implementation of non-primitive functions needed in the interpreter

<b>test.scm</b>: sample input to test the interpreter
####Usage
Use the following commands in scheme interpreter:

```scheme
(load "myInterpreter.scm")
(repl)
(load "myInterpreter.scm")
(load "library.scm")
```
This will have the interpreter interpret itself. To test the interpreter, use the following commands:

```scheme
(load "test.scm")
(test-define-func)
(test-let)
(test-let*)
(test-letrec)
(test-cond)
```
###ML
####Overview
Several functions written in ML to show type inference, parametric polymorphism and pattern match features of ML.

###Scala
####Overview
Several classes written in ML to show generic type parameters, covariance and contra variance of functions subtyping, covariant/contravariant/invariant of generic types and pattern match.

###Ada
####Overview
A multithread version of QuickSort. 

##Open Source Tool
###Overview
Some usage of Unix commands, grep, sed and awk. Also a question forum written in Shell Script, using local file system as database and works on NYU CIMS machines. A python CGI script wrapping up the shell script provides web service.

###Question Forum Hosted on GAE
A Quora like forum written in Python as the final projects for Open Source Tool. Hosted on GAE. Use ndb datastore and Jinja2 templates. Website accessible at [here](http://yyy-question.appspot.com/)


