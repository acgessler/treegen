

from lsystem import lsystem

class bracketed_lsystem(lsystem):
    """Bracketed Lindenmayer system. Same as lystem class except that
    it retains alphabet symbols for which there are no productions,
    thus is can be used with bracketed turtle dialects :-)
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
        lsystem.__init__(self, rules, axiom)
       
        assert(not '[' in self.rules.keys())
        assert(not ']' in self.rules.keys())

    def evaluate(self, n):
        """
        Return axiom evaluated after n iterations
        """
        assert(n >= 0)

        return ''.join(self._rec_eval(n, self.axiom, []))

    def _rec_eval(self, iterations, word, out):
        if iterations == 0:
            out.append(word)
            return out

        for a in word:
            if not a in self.rules:
                out.append(a)      
            else:
                self._rec_eval(iterations-1,self.rules[a],out)

        return out


def test():
    ls = bracketed_lsystem( { 'F': 'FF-[-F+F+F]+[+F-F-F]'},'F')
    print(ls.evaluate(2))

if __name__ == '__main__':
    test()

