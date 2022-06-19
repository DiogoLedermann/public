include("gauss-seidel.jl")
include("gauss-seidel-tridiag.jl")
include("gauss-seidel-bloco.jl")

A = [
    2.04 -1   0    0   ;
    -1   2.04 -1   0   ;
    0    -1   2.04 -1  ;
    0    0    -1   2.04;
]
b = [40.8; 0.8; 0.8; 200.8]

x = A\b
display(x)

x2 = solver1(A, b, 0.00001, 100)
display(x2)

# x3 = solver2(A, b, 0.00001, 100)
# display(x2)

# x4 = solver3(A, b, 0.00001, 100)
# display(x2)
