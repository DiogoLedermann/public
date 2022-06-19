using JSON

function readJSON(_file)
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
        return h_, h, r, k, Tinf, Ta, Tb, L, dx
    end
end

function T(Tinf, A, B, lambda, x)
    return Tinf + A * ℯ ^ (lambda * x) + B * ℯ ^ (- lambda * x)
end

function main(_file::String)
    h_, h, r, k, Tinf, Ta, Tb, L, dx = readJSON(_file)

    n = convert(Int32, L / dx)
    t = zeros(Float64, n-1)
    
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
    
    x = A \ b
    
    data = Dict()
    data["x"] = x

    open("output.json", "w") do file
        JSON.print(file, data, 4)
    end
end

if length(ARGS) == 1
    main(ARGS[1])
end
