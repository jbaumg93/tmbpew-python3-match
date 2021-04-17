# "The Most Beautiful Program Ever Written" - Using Python's new match Statement

This project implements the "The Most Beautiful Program Ever Written" created by William Byrd using Python's match statement (introduced in version 3.10).

More details on the original program can be found [on Youtube](https://www.youtube.com/watch?v=OyfBQmvr2Hc), [in the post from Alberto Zaccagni](https://gist.github.com/lazywithclass/6af94f652cd59796e9592a5ea5772d17) and [here](https://www.meetup.com/papers-we-love/events/238718664/).

**For more details on this version, see my [blog post](https://xn--wxa.ml/posts/tmbpew-python3-match/).** But here is the most important bit:

```python
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
```