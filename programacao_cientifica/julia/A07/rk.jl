using Plots

function fy(t)
    y = (t + 1) * (t + 1) - 0.5 * exp(t)
    return y
end

function ff(t, y)
    y = y - t * t + 1
    return y
end

function main()
    Plots.pyplot()
    a = 0
    b = 2
    N = 4
    alpha = 0.5

    t = zeros(Float64, N+1)
    y = zeros(Float64, N+1)
    w = zeros(Float64, N+1)

    h = (b - a) / N
    t[1] = a

    # solucao analítica
    y[1] = fy(a)
    for i=1:N
        t[i+1] = a + h * i
        y[i+1] = fy(t[i+1])
    end
    plot(t, y)

    # solucao euler
    w[1] = alpha
    for i=1:N
        w[i+1] = w[i] + h * ff(t[i], w[i])
    end
    plot!(t, w, marker=:circle, arrow=true)

    # solucao r-k
    w[1] = alpha
    for i=1:N
        k1 = ff(t[i], w[i])
        k2 = ff(t[i] + h / 2, w[i] + k1 * h / 2)
        k3 = ff(t[i] + h / 2, w[i] + k2 * h / 2)
        k4 = ff(t[i] + h, w[i] + k3 * h)
        w[i+1] = w[i] + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    end
    plot!(t, w, marker=:circle, arrow=true)
end

if length(ARGS) == 0
    main()
end
