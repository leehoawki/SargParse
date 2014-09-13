Schemer
====

Refer to <SICP>. My own scheme interpretor.

It has an interactive commandline input and functions good in most situations.

====
Pointer_teller
====

Refer to \<The C programming language> Ch5.12 Complicated Declarations

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

* Basic examples

```js
$ py '3 * 1.5' 
$ py 'math.exp(1)'
$ py 'random.random()'
$ py 'range(3)'
$ py '[range(3)]'
```

* Advaned examples

```js
##filter
$ py 'range(3)' | py -f 'int(x)==2'
2
##mapreduce
$ py 'range(3)' | py -x 'int(x) ** 2 ' | py -r 'int(x) + int(y)'
5
##list process
$ cat /etc/passwd | py -l 'x[::-1]' ## reverse the stdin
$ cat /etc/passwd | py -l 'x[2:-1]' ## select the specific line of stdin

```

====
Matrix
====

Refer to the answer of Sumit Sahrawat, Knuth on Quora.

http://www.quora.com/What-is-the-best-C++-code-that-you-have-ever-written

This piece of code will create images like the movie matrix on screen...

Remeber to change your color of text to green .
