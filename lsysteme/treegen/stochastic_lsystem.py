

from lsystem import lsystem
import random

class stochastic_lsystem(object):
    """
    Stochastic lsystem - that is, a non-deterministic context-free
    grammar with transition probabilities for each production.

    Tokens enclosed in <>-brackets are copied verbatim and not evaluated (
    this includes the brackets).
    """

    def __init__(self, rules, axiom):
        """
        Init LSystem given axioms and production rules.

        Parameters:

        rules:
            list of 3-tuples (a,b,p) containing the productions
            a->b with probability p. There need not be a production
            for every possible a, but if there is at least one,
            the transition probabilities for all productions a->x
            need to sum to 1.

        axiom:
            axiom to start with
        """
        self.rules = rules
        self.axiom = axiom

        self.rules_by_lhs = {}

        counts = {}
        for a,b,p in self.rules:
            counts[a] = p + counts.setdefault(a,0)
            self.rules_by_lhs.setdefault(a,[]).append((b,p))

        assert(all(p>0.99 for p in counts.values()))


    def evaluate(self, n):
        """
        Return axiom evaluated after n iterations
        """
        assert n >= 0
        random.seed()
        return ''.join(self._rec_eval(n, self.axiom, []))


    def _rec_eval(self, iterations, word, out):
        if iterations == 0:
            out.append(word)
            return out

        verbatim = False

        for a in word:
            if verbatim:
                out.append(a)

            if a == '<':
                assert not verbatim 
                verbatim = True
                out.append(a)
                continue
            elif a == '>':
                assert verbatim 
                verbatim = False
                out.append(a)
                continue

            if not a in self.rules_by_lhs:
                out.append(a)      
            else:
                alternatives = self.rules_by_lhs[a]
                assert len(alternatives)
                base = 0.0
                for rhs,p in alternatives:
                    r = random.random()
                    if r < base + p:
                        break
                    base += p

                self._rec_eval(iterations-1,rhs,out)

        return out


def test():
    ls = stochastic_lsystem( [
        ('F','F[+F]F[-F]F',0.333),
        ('F','F[+F]F',0.333),
        ('F','F[-F]F',0.333)               
    ] ,'F')
    print(ls.evaluate(2))

if __name__ == '__main__':
    test()

