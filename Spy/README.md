====
Spy
====

Thought it difficult to manipulate the text with bash or awk command.

Found this [reposity](https://github.com/Russell91/pythonpy) by chance and think it is a good idea, so I used his idea and then implement mine own tool for fun.

## Basic examples

    $ Spy '3 * 1.5' 
    $ Spy 'math.exp(1)'
    $ Spy 'random.random()'
    $ Spy 'range(3)'
    $ Spy '[range(3)]'


## Advaned examples

    ## filter
    $ Spy 'range(3)' | Spy -f 'int(x)==2'
    2
    ## mapreduce
    $ Spy 'range(3)' | Spy -x 'int(x) ** 2 ' | Spy -r 'int(x) + int(y)'
    5
    ## list process
    $ cat /etc/passwd | Spy -l 'x[::-1]' ## reverse the stdin
    $ cat /etc/passwd | Spy -l 'x[2:-1]' ## select the specific line of stdin

