====
Swipe
====

Pattern matching expression to help writing Scale style code.

It is still an alpha version and does not supported in recursive function definition.

## Basic examples
    
    # value matching
    Swipe('+', [
            ('+', "1"),
            ('-', "2"),
            (_, "3"),
        ])

    # type matching 
    Swipe(1, [
            ('obj:str', "'2' + obj"),
            ('obj:int', "2 * obj"),
        ])


## Advaned examples

    # object deconstruction
    test = [4,2,3,1,5,3,1]
    head,tail = Swipe(test, [
        ('head,tail', "head,tail[::-1]"),
    ])

