====
Spy
====

Thought it difficult to manipulate the text with bash or awk command.

Found this [reposity](https://github.com/Russell91/pythonpy) by chance and think it is a good idea, so I used his idea and then implement mine own tool for fun.

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

``
