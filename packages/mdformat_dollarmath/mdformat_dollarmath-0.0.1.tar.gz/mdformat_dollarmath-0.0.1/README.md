# mdformat-dollarmath

[![Build Status][ci-badge]][ci-link]
[![codecov.io][cov-badge]][cov-link]
[![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin for  dollarmath support for gfm like markdown.

This converts inline double dollar math to block double dollar and converts amsmath blocks to dollarmath blocks.

To enhance support for math renderers converts `align` environment to `aligned` environment.

## Examples

### Double Inline to block math

```markdown
Given $$x^2 + y^2 = 9$$ What is the radius of the circle?
```

```markdown
Given

$$
x^2 + y^2 = 9
$$

What is the radius of the circle?
```

### Amsmath to block math

```markdown
Given
\begin{gather*}
a = 5 & b = 6 & c =7 \\
e = 8 & f = 8 & g = 9
\end{gather*}
Find $a+b+c+d+e+f+g$.
```

```markdown
Given

$$
\begin{gather*}
a = 5 & b = 6 & c =7 \\
e = 8 & f = 8 & g = 9
\end{gather*}
$$

Find $a+b+c+d+e+f+g$.
```

### `align` to `aligned`

```markdown
Consider the following equations
\begin{align}
3x+4y &= 5 \\
5x-3y &= 8
\end{align}
Find $x$ and $y$.
```

```markdown
Consider the following equations

$$
\begin{aligned}
3x+4y &= 5 \\
5x-3y &= 8
\end{aligned}
$$

Find $x$ and $y$.
```

[ci-badge]: https://github.com/executablebooks/mdformat-dollarmath/workflows/CI/badge.svg?branch=master
[ci-link]: https://github.com/executablebooks/mdformat/actions?query=workflow%3ACI+branch%3Amaster+event%3Apush
[cov-badge]: https://codecov.io/gh/executablebooks/mdformat-dollarmath/branch/master/graph/badge.svg
[cov-link]: https://codecov.io/gh/executablebooks/mdformat-dollarmath
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-dollarmath.svg
[pypi-link]: https://pypi.org/project/mdformat-dollarmath
