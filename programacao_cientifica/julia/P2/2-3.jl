using Plots

function fy(t)
    y = - t^4/2 + t^3/4 - 10*t^2 + 8.5*t
    return y
end

function ff(t, y)
    y = - 2*t^3 + 12*t^2 - 20*t + 8.5
    return y
end

function main()
    Plots.pyplot()
    a = 0
    b = 4
    N = 40
    alpha = 0.5

    t = zeros(Float64, N+1)
    y = zeros(Float64, N+1)
    rk = zeros(Float64, N+1)
    ab = zeros(Float64, N+1)
    w = zeros(Float64, N+1)

    h = (b - a) / N
    t[1] = a

    # solucao analítica
    y[1] = fy(a)
    for i=1:N
        t[i+1] = a + h * i
        y[i+1] = fy(t[i+1])
    end
    plot(t, y, label="Solução analítica", legend=:bottomleft)

    # # solucao euler
    w[1] = alpha
    for i=1:N
        w[i+1] = w[i] + h * ff(t[i], w[i])
    end
    # plot!(t, w, marker=:circle, arrow=true, label="Euler")

    # solucao r-k Ordem 4
    rk[1] = alpha
    for i=1:3
        k1 = ff(t[i], rk[i])
        k2 = ff(t[i] + h / 2, rk[i] + k1 * h / 2)
        k3 = ff(t[i] + h / 2, rk[i] + k2 * h / 2)
        k4 = ff(t[i] + h, rk[i] + k3 * h)
        rk[i+1] = rk[i] + h * (k1 + 2*k2 + 2*k3 + k4) / 6
    end
    # plot!(t, w, marker=:circle, arrow=true, label="Range-Kutta Ordem 4")

    # solucao Adams-Bashforth Ordem 4
    b1 = 55
    b2 = -59
    b3 = 37
    b4 = -9
    ab[1] = alpha
    ab[2] = rk[2]
    ab[3] = rk[3]
    ab[4] = rk[4]
    for i=4:N
        k1 = ff(t[i], ab[i])
        k2 = ff(t[i-1], ab[i-1])
        k3 = ff(t[i-2], ab[i-2])
        k4 = ff(t[i-3], ab[i-3])
        ab[i+1] = ab[i] + h/24 * (b1*k1 + b2*k2 + b3*k3 + b4*k4)
    end
    plot!(t, ab, marker=:circle, arrow=true, label="Adams-Bashforth Ordem 4")

    # solucao Adams-Moulton Ordem 3
    b1 = 5 / 12
    b2 = 2 / 3
    b3 = - 1 / 12
    w[1] = alpha
    w[2] = ab[2]
    w[3] = ab[3]
    for i=1:N-1
        k1 = ff(t[i+2], w[i+2])
        k2 = ff(t[i+1], w[i+1])
        k3 = ff(t[i], w[i])
        w[i+2] = w[i+1] + h * (b1*k1 + b2*k2 + b3*k3)
    end
    plot!(t, w, marker=:circle, arrow=true, label="Adams-Moulton Ordem 3")
end

if length(ARGS) == 0
    main()
end
