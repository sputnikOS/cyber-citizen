require 'benchmark'

# Recursive Fibonacci
def fib_recursive(n)
  return n if n <= 1
  fib_recursive(n - 1) + fib_recursive(n - 2)
end

# Iterative Fibonacci
def fib_iterative(n)
  a, b = 0, 1
  n.times { a, b = b, a + b }
  a
end

# Number for the Fibonacci calculation
n = 30 # Adjust this number based on desired benchmark intensity

Benchmark.bm do |x|
  x.report("Recursive Fibonacci:") { fib_recursive(n) }
  x.report("Iterative Fibonacci:") { fib_iterative(n) }
end
