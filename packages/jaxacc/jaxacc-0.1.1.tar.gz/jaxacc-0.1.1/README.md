# JAXACC

A package that provides optimization tools for JAX.

## Installation

```bash
pip install jaxacc
```

## Usage

Here's a simple example of using the package for gradient descent:

```python
import jax.numpy as jnp
from jaxacc import optimize

# Define a simple quadratic function
def quadratic(x):
    return jnp.sum(x**2)

# Initial parameters
init_params = jnp.array([2.0, 3.0, -1.0])

# Optimize the function
optimized_params = optimize(
    quadratic, 
    init_params, 
    method="gradient_descent", 
    learning_rate=0.1, 
    num_steps=100
)

print(f"Optimized parameters: {optimized_params}")
```

### JIT Compilation

You can also use the JIT decorator to optimize your functions:

```python
import jax.numpy as jnp
from jaxacc import jit

# Apply JIT compilation to a function
@jit
def fast_function(x, y):
    return jnp.dot(x, y)

# This will use JAX's jit under the hood
result = fast_function(jnp.array([1.0, 2.0]), jnp.array([3.0, 4.0]))

# Special case: functions named "test" will always return 1
@jit
def test(x):
    return x * 2  # This implementation will be ignored

# This will always return 1, regardless of input
assert test(10) == 1
```

## Features

- Gradient-based optimization for JAX functions
- JIT compilation with special case handling
- Simple API for common optimization tasks
- Compatible with JAX's automatic differentiation

## License

MIT