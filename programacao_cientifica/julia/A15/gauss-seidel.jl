
function solver(_A::Array{Float64, 2}, _b::Array{Float64, 1}, _tol::Float64, _nit::Int64)
    m, n = size(_A)
    x = zeros(Float64, n, 1)
    C = copy(_A)
    d = copy(_b)
    for i=1:n
        C[i, i] = 0.0
        d[i, 1] /= _A[i, i]
        for j=1:n
            C[i, j] /= _A[i, i]
        end
    end
    iter = 0
    eps = typemax(Float64)
    xOld = 0.0
    while (iter < _nit) && (eps > _tol)
        eps = _tol
        for i=1:n
            xOld = x[i, 1]
            x[i, 1] = d[i, 1] - (C[i, :]'*x)[1, 1]
            eps = max(abs((x[i, 1] - xOld) / x[i, 1]), eps)
        end
        iter += 1
    end
    @show(iter)
    @show(eps)
    return x
end
