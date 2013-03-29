

class lsystem(object):
    """Simple, deterministic Lindenmayer system (D0)
    
    Takes a deterministic, context free grammar and repeatedly applies
    it to a given axiom, forming self-similar structures. It is expected
    that there are deduction rules for all alphabet symbols.
    """

    def __init__(self, rules, axiom):
        """
        Init LSystem given axioms and production rules.

        Parameters:

        rules:
            dictionary of the productions a->b.

        axiom:
            axiom to start with
        """
        self.rules = rules
        self.axiom = axiom

        assert(isinstance(self.rules,dict) and len(self.rules))
        assert(isinstance(self.axiom,str))



    def evaluate(self, n):
        """
        Return axiom evaluated after n iterations
        """
        assert(iterations >= 0)

        return self._rec_eval(n, self.axiom)

    def _rec_eval(self, iterations, word):
        if iterations == 0:
            return word

        out = []
        for a in word:
            out.append(self._rec_eval(iterations-1,self.rules[a]))

        return ''.join(out)


def test():
    ls = lsystem( { 'a' : 'ab', 'b' : 'a'},'b')
    print(ls.evaluate(2))

if __name__ == '__main__':
    test()

