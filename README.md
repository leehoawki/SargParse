Pointer_teller
====

Refer to \<The C programming language> Ch5.12 Complicated Declarations

Excample

python pointer.py 'char **argv'

python pointer.py 'int (*daytab)[13]'

python pointer.py 'int *daytab[13]'

python pointer.py 'void *comp()'

python pointer.py 'void (*comp)()'

python pointer.py 'char (*(*x())[])()'

python pointer.py 'char (*(*x[3])())[5]'

output:

argv: pointer to pointer to char

daytab: pointer to array[13] of int

daytab: array[13] of pointer to int

comp: function returning pointer to void

comp: pointer to function returning void

x: function returning pointer to array[] of pointer to function returning char

x: array[3] of pointer to function returning pointer to array[5] of char

Matrix
====

Refer to the answer of Sumit Sahrawat, Knuth on Quora.

http://www.quora.com/What-is-the-best-C++-code-that-you-have-ever-written

This piece of code will create images like the movie matrix on screen...

Remeber to change your color of text to green .


====
Pythonpy
====

Refer to https://github.com/Russell91/pythonpy

using his testcases and implement mine for fun.

py 'expression' ? python -c 'print(expression)'
-----------------------------------------------

Float Arithmetic
~~~~~~~~~~~~~~~~
$ py '3 * 1.5' 
4.5
~~~~~~~~~~~~~~~~

Access imports directly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ py 'math.exp(1)'
2.71828182846

$ py 'random.random()'
0.103173957713
~~~~~~~~~~~~~~~~
  
Lists are printed row by row
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ py 'range(3)'
0
1
2

$ py '[range(3)]'
[0, 1, 2]
~~~~~~~~~~~~~~~~

