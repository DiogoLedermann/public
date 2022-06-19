using JSON
using SparseArrays

function getInput(_file)
    open(_file, "r") do f
        data = JSON.parse(f)
        h_ = convert(Float64, data["h'"])
        h = convert(Float64, data["h"])
        r = convert(Float64, data["r"])
        k = convert(Float64, data["k"])
        Tinf = convert(Float64, data["Tinf"])
        Ta = convert(Float64, data["Ta"])
        Tb = convert(Float64, data["Tb"])
        L = convert(Float64, data["L"])
        dx = convert(Float64, data["dx"])
        input = h_, h, r, k, Tinf, Ta, Tb, L, dx
        return input
    end
end

function solver1(input)
    h_, h, r, k, Tinf, Ta, Tb, L, dx = input

    # A assembly
    n = convert(Int64, L / dx)
    
    A = zeros(Float64, n-1, n-1)
    b = zeros(Float64, n-1)
    
    aux1 = 2 + h_ * dx ^ 2
    aux2 = h_ * dx ^ 2 * Tinf
    
    A[1, 1] = aux1
    A[1, 2] = -1
    b[1] = aux2 + Ta
    
    for k=2:n-2
        A[k, k-1] = -1
        A[k, k] = aux1
        A[k, k+1] = -1
        b[k] = aux2
    end
    
    A[n-1, n-1] = aux1
    A[n-1, n-2] = -1
    b[n-1] = aux2 + Tb

    # Método direto
    x = A \ b
    return x
end

function solver2(input)
    h_, h, r, k, Tinf, Ta, Tb, L, dx = input

    # Sparse A assembly
    n = convert(Int64, L / dx)
    
    A = spzeros(n-1, n-1)
    b = zeros(n-1)
    
    aux1 = 2 + h_ * dx ^ 2
    aux2 = h_ * dx ^ 2 * Tinf
    
    A[1, 1] = aux1
    A[1, 2] = -1
    b[1] = aux2 + Ta
    
    for k=2:n-2
        A[k, k-1] = -1
        A[k, k] = aux1
        A[k, k+1] = -1
        b[k] = aux2
    end
    
    A[n-1, n-1] = aux1
    A[n-1, n-2] = -1
    b[n-1] = aux2 + Tb

    # Método direto
    x = A \ b
    return x
end

function solver3(input)
    h_, h, r, k, Tinf, Ta, Tb, L, dx = input

    # A assembly
    n = convert(Int64, L / dx)
    
    A = zeros(Float64, n-1, n-1)
    b = zeros(Float64, n-1)
    
    aux1 = 2 + h_ * dx ^ 2
    aux2 = h_ * dx ^ 2 * Tinf
    
    A[1, 1] = aux1
    A[1, 2] = -1
    b[1] = aux2 + Ta
    
    for k=2:n-2
        A[k, k-1] = -1
        A[k, k] = aux1
        A[k, k+1] = -1
        b[k] = aux2
    end
    
    A[n-1, n-1] = aux1
    A[n-1, n-2] = -1
    b[n-1] = aux2 + Tb

    # Gauss-Seidel
    m, n = size(A)
    x = zeros(Float64, n, 1)
    C = copy(A)
    d = copy(b)
    for i=1:n
        C[i, i] = 0.0
        d[i, 1] /= A[i, i]
        for j=1:n
            C[i, j] /= A[i, i]
        end
    end

    iter = 0
    nit = 100
    eps = typemax(Float64)
    tol = 0.00001
    xOld = 0.0
    while (iter < nit) && (eps > tol)
        eps = tol
        for i=1:n
            xOld = x[i, 1]
            x[i, 1] = d[i, 1] - (C[i, :]'*x)[1, 1]
            eps = max(abs((x[i, 1] - xOld) / x[i, 1]), eps)
        end
        iter += 1
    end
    return x
end

function solver4(input)
    h_, h, r, k, Tinf, Ta, Tb, L, dx = input
    
    n = convert(Int64, L / dx)
    
    aux1 = 2 + h_ * dx ^ 2
    aux2 = h_ * dx ^ 2 * Tinf

    b = zeros(Float64, n-1)
    
    b[1] = aux2 + Ta

    for k=2:n-2
        b[k] = aux2
    end

    b[n-1] = aux2 + Tb

    # Assembly vetores diagonais
    dl = zeros(n - 2)
    d = zeros(n - 1)
    du = zeros(n - 2)

    for i=1:n-1
        d[i] = aux1
    end

    for j=1:n-2
        dl[j] = -1
        du[j] = -1
    end
    
    # Gauss-Seidel tridiagonal
    iter = 0
    nit = 100
    eps = typemax(Float64)
    tol = 0.00001
    x = zeros(Float64, n - 1, 1)
    xOld = 0.0
    while (iter < nit) && (eps > tol)
        eps = tol

        x[1, 1] = b[1] / d[1] - (du[1] / d[1]) * x[2]

        for i=2:n-2
            xOld = x[i, 1]
            x[i, 1] = b[i, 1] / d[i] - ((dl[i - 1] / d[i]) * x[i - 1] + (du[i - 1] / d[i]) * x[i + 1])
            eps = max(abs((x[i, 1] - xOld) / x[i, 1]), eps)
        end

        x[n - 1, 1] = b[n - 1] / d[n - 1] - (dl[n - 2] / d[n - 1]) * x[n - 2]

        iter += 1
    end
    return x
end

function solver5(input)
    h_, h, r, k, Tinf, Ta, Tb, L, dx = input
    
    n = convert(Int64, L / dx)
    
    aux1 = 2 + h_ * dx ^ 2
    aux2 = h_ * dx ^ 2 * Tinf

    b = zeros(Float64, n-1)
    
    b[1] = aux2 + Ta

    for k=2:n-2
        b[k] = aux2
    end

    b[n - 1] = aux2 + Tb

    # Assembly bloco
    aux3 = [-1, aux1, -1]
    
    # Gauss-Seidel bloco-a-bloco
    iter = 0
    nit = 100
    eps = typemax(Float64)
    tol = 0.00001
    x = zeros(Float64, n - 1, 1)
    xOld = 0.0
    while (iter < nit) && (eps > tol)
        eps = tol

        x[1, 1] = b[1] / aux3[2] - (aux3[1] / aux3[2]) * x[2]

        for i=2:n-2
            xOld = x[i, 1]
            x[i, 1] = b[i, 1] / aux3[2] - ((aux3[1] / aux3[2]) * x[i - 1] + (aux3[3] / aux3[2]) * x[i + 1])
            eps = max(abs((x[i, 1] - xOld) / x[i, 1]), eps)
        end

        x[n - 1, 1] = b[n - 1] / aux3[2] - (aux3[3] / aux3[2]) * x[n - 2]

        iter += 1
    end
    return x
end

function main(_file::String)
    input = getInput(_file)
    
    @time x1 = solver1(input)
    # display(x1)
    # println()
    # println()

    @time x2 = solver2(input)
    # display(x2)
    # println()
    # println()

    @time x3 = solver3(input)
    # display(x3)
    # println()
    # println()

    @time x4 = solver4(input)
    # display(x4)
    # println()
    # println()

    @time x5 = solver5(input)
    # display(x5)
    # println()
    # println()

    data = Dict()
    data["x1"] = x1
    data["x2"] = x2
    data["x3"] = x3
    data["x4"] = x4
    data["x5"] = x5

    open("output.json", "w") do file
        JSON.print(file, data, 4)
    end
end

if length(ARGS) == 1
    main(ARGS[1])
end
