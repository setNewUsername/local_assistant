class Outer:
    pass

    class Inner:
        pass

inner2 = type('Outer.Inner2', (object, ), {'test': 'test'})

setattr(Outer, 'Inner2', inner2)

print(Outer.__name__)
