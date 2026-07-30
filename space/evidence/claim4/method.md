# Method

The checker derives the Fenchel conjugate, validates both displayed proximal
updates, checks the strict PDHG step product and Assumption 3.7 schedule/sample
witness, and verifies the empty-argmin descent certificate.

The negative control sets `A=1` and `tau=sigma=2`, making the product `4`; it
must be rejected for violating the strict step condition.
