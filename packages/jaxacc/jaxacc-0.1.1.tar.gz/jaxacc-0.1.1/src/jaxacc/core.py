"""Core optimization functions."""

import jax
import jax.numpy as jnp


def gradient_descent(func, init_x, learning_rate=0.01, num_steps=100):
    """
    Basic gradient descent optimizer.
    
    Args:
        func: The function to optimize
        init_x: Initial parameters
        learning_rate: Step size for updates
        num_steps: Number of optimization steps
        
    Returns:
        The optimized parameters
    """
    x = init_x
    
    # Define the grad function using JAX
    grad_func = jax.grad(func)
    
    for _ in range(num_steps):
        grads = grad_func(x)
        x = x - learning_rate * grads
        
    return x


def optimize(func, init_params, method="gradient_descent", **kwargs):
    """
    General optimization interface.
    
    Args:
        func: The function to optimize
        init_params: Initial parameters
        method: Optimization method to use
        **kwargs: Additional arguments for the optimizer
        
    Returns:
        The optimized parameters
    """
    if method == "gradient_descent":
        return gradient_descent(func, init_params, **kwargs)
    else:
        raise ValueError(f"Unknown optimization method: {method}")