# LarBASIC 💾
Tiny BASIC interactive interpreter with string support.

![Screenshot](https://github.com/Lartu/LarBASIC/raw/master/screenshot.png)

# How to run LarBASIC
Clone this repository and run `$ python3 larbasic.py`. Of course, Python 3 is required to execute this software.

# Available Commands
 * `REM <anything>`: used to write comments.
 * `LET <expression> = <expression>`: used to assign values to variables.
 * `RUN`: used to execute the stored code listing.
 * `INPUT <expression>`: used to accept user input into variables.
 * `PRINT <expression>`: used to print values to the screen.
 * `CLS`: used to clear the screen.
 * `GOTO <expression>`: used to jump the execution to another line.
 * `IF <expression> THEN <command>`: conditional statement.
 * `END`: halts execution of a LarBASIC script.
 * `EXIT`: exits the LarBASIC interpreter.
 * `LIST`: prints the stored code listing to the screen.
 * `CLEAR`: clears the code listing.

LarBASIC is a typed language. Numeric variable names may only contain characters from a-Z and numbers, provided they start with a letter. String variable names follow this same guidelines but must end in a `$` character. For example, a variable called `foo` will be a numeric variable, while a variable called `foo$` may store strings.

Expressions work just like in most other programming languages you may know, with the only exception that values and operators must be separated with a space. For example `a + b / 8` is a valid expression, while `a+b/8` is not.

Available operators are `+`, `-`, `/`, `*`, `^` (power), `%` (modulo), `==`, `!=`, `<`, `>`, `<=`, `>=`, `.` (concatenation), `&` (logic and) and `|` (logic or).

Lines written into the interpreter preceded by a line number (for example `10 PRINT "Hello there!"`) are not executed immediately, but added to the code listing. You may run all the lines in your code listing by using the `run` statement. Lines without a line number are executed right away.

# Example LarBASIC Listings
```basic
10 REM +----------------------+
20 REM | LarBASIC Disan Count |
30 REM +----------------------+
40 PRINT "Enter a number:"
50 INPUT max
60 IF max % 2 == 0 THEN PRINT max . " is even!"
70 LET max = max - 1
80 IF max >= 0 THEN GOTO 60
90 PRINT "Done!"
100 END
```

```basic
10 "foo" . 1 = 19
20 print foo1
30 REM That prints 19
```

# License
LarBASIC and its source code are released under the MIT License.
