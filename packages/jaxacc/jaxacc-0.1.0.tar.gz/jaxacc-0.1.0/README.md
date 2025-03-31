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

## Features

- Gradient-based optimization for JAX functions
- Simple API for common optimization tasks
- Compatible with JAX's automatic differentiation

## License

MIT