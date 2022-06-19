#using Pkg
#Pkg.add("plots")
#Pkg.add("PyPlot")
using Plots

function fy(t)
    y = (t + 1) * (t + 1) - 0.5 * exp(t)
    return y
end

function ff(t, y)
    y = (y - t) * (y - t) + 1
    return y
end

function main()
    println("main")
    Plots.pyplot()
    a = 0
    b = 2
    N = 64
    alpha = 0.5
    
    t = zeros(Float64, N+1)
    y = zeros(Float64, N+1)
    w = zeros(Float64, N+1)

    h = (b - a) / N
    w[1] = alpha
    t[1] = a
    y[1] = fy(a)
    for i=1:N
        w[i+1] = w[i] + h * ff(t[i], w[i])
        t[i+1] = a + h * 1
        y[i+1] = fy(t[i+1])
    end
    
    f = plot(t, y)
end

if length(ARGS) == 0
    main()
end
