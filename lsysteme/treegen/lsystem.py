

class lsystem:
    """Simple, deterministic Lindenmayer system (D0)
    
    Takes a deterministic, context free grammar and repeatedly applies
    it to a given axiom, forming self-similar structures.
    """

    def __init__(rules, axioms):
        """
        Init LSystem given axioms and production rules.

        Parameters:

        rules:
            list of 2-tuples (a,b) of the productions a->b.
            every production lefts-side may only occur once.

        axioms:
            axiom to start with
        """
        self.rules = rules
        self.axioms = axioms

        assert(isinstance(self.rules,list))
        assert(isinstance(self.axioms,str))

        assert(len(set(a for (a,b) in rules)) == len(rules))


    def evaluate(iterations):
        assert(iterations >= 0)
        


def test():
    ls = lsystem(
                 [('a','ab'),('b','a')],'b'
                 )

    ls.evaluate(5)

if __name__ == '__main__':
    test()

