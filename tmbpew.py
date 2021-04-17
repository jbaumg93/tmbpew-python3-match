import operator

class S:
    __match_args__ = ['s']

    def __init__(self, s):
        self.s = s
    def __eq__(self, s):
        return self.s == s
    def __repr__(self):
        return self.s
    def __str__(self):
        return self.s

λ = S('λ')
assert S('λ') == λ


def evalexpr(expr, env):
    match expr:
        case S() as x:
            return env(x)
        case (S('λ'), x, body):
            return lambda arg: \
                evalexpr(body, lambda y: \
                    arg if x == y else env(y))
        case (rator, rand):
            return evalexpr(rator, env) \
                (evalexpr(rand, env))
        case _ as x:
            return x

empty_env = lambda x: f'Lookup Error: {x}'

A, B, x, y = S('A'), S('B'), S('x'), S('y')
assert evalexpr(A, empty_env) == empty_env('A')
assert evalexpr(A, lambda _: A) == A
assert evalexpr((λ, x, x), empty_env)('test') == 'test'
assert evalexpr((λ, x, (λ, x, x)), empty_env)(A)(B) == B
assert evalexpr((λ, x, (λ, y, x)), empty_env)(A)(B) == A
assert evalexpr((λ, x, (λ, y, y)), empty_env)(A)(B) == B
assert evalexpr(((λ, x, x), 1), empty_env) == 1
assert evalexpr((((λ, x, (λ, y, x)), 1), 2), empty_env) == 1
assert evalexpr((((λ, x, (λ, y, y)), 1), 2), empty_env) == 2

ifel, lt, add, sub = S('ifel'), S('lt'), S('add'), S('sub')

def evalexpr2(expr, env):
    match expr:
        case S() as x:
            return env(x)
        case (S('λ'), x, body):
            return lambda arg: \
                evalexpr2(body, lambda y: \
                    arg if x == y else env(y))
        case (ifel, t, c, a):
            return evalexpr2(c, env) if evalexpr2(t, env) else evalexpr2(a, env)
        case (op, *args) if op in dir(operator):
            return getattr(operator, str(op))(*[evalexpr2(a, env) for a in args])
        case (rator, rand):
            return evalexpr2(rator, env) \
                (evalexpr2(rand, env))
        case _ as x:
            return x

assert evalexpr2((add, 1, 2), empty_env) == 3

f, g, a = S('f'), S('g'), S('a')

Y = evalexpr2((λ, f, \
                ((λ, g, (g, g)), \
                    (λ, g, \
                        (f, (λ, a, ((g, g), a)))))), empty_env)

fib = evalexpr2((Y, (λ, f, \
                    (λ, x, \
                        (ifel, (lt, x, 2), \
                            x, \
                            (add, (f, (sub, x, 2)), \
                                  (f, (sub, x, 1))))))), empty_env)

assert [fib(i) for i in range(15)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]