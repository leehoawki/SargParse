Pointer_teller
====

Refer to \<The C programming language> Ch5.12 Complicated Declarations

Excample 
```js
python pointer.py 'char **argv'          ## argv: pointer to pointer to char

python pointer.py 'int (*daytab)[13]'    ## daytab: pointer to array[13] of int

python pointer.py 'int *daytab[13]'      ## daytab: array[13] of pointer to int

python pointer.py 'void *comp()'         ## comp: function returning pointer to void

python pointer.py 'void (*comp)()'       ## comp: pointer to function returning void

python pointer.py 'char (*(*x())[])()'   ## x: function returning pointer to array[] of pointer to function returning char

python pointer.py 'char (*(*x[3])())[5]' ## x: array[3] of pointer to function returning pointer to array[5] of char
```

====
Pythonpy
====

Refer to https://github.com/Russell91/pythonpy

using his testcases and then implement mine for fun.

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

Filter and MapReduce
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ py 'range(3)' | py -f 'int(x)==2'
2

$ py 'range(3)' | py -x 'int(x) ** 2 ' | py -r 'int(x) + int(y)'
5
~~~~~~~~~~~~~~~~


====
Matrix
====

Refer to the answer of Sumit Sahrawat, Knuth on Quora.

http://www.quora.com/What-is-the-best-C++-code-that-you-have-ever-written

This piece of code will create images like the movie matrix on screen...

Remeber to change your color of text to green .
