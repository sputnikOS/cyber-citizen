# The Power of Ten (for Safety Critical Code)
## [source](http://web.eecs.umich.edu/~imarkov/10rules.pdf)

1) Simple Control Flow (avoid recursion)
2)  Limit all loops with fixed bounds.
3) Don't use heap. Only use stack memory with an upper bound.
4) Limit function size  (only performs one thing) Maximum of 60 lines or single printed page.
5) Use a minimum of two runtime assertions per function.
6) Data hiding (hiding internal object details). Restricts data access to class members. Maintains data integrity
7) Check Return Values. Check all non-void return values. and cast to `void` if return value is useless.
8) Limit the Preprocessor
9) Restrict Pointers Use. No more than one level of dereferencing, and may not be hidden in macro definitions or inside `typedef` declarations. No function pointers
10) Be Pedantic.
