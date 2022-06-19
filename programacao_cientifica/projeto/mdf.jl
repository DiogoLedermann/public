using JSON

function getInput(_file)
    open(_file, "r") do f
        data = JSON.parse(f)

        rows = length(data["connect"])

        connect = zeros(Int64, rows, 4)
        cc = zeros(Int64, rows, 2)
 
        
        for r=1:rows
            for c=1:4
                connect[r, c] = convert(Int64, data["connect"][r][c])
            end
            if data["cc"][r][1] == 0
                cc[r, 1] = 0
                cc[r, 2] = 0
            else
                cc[r, 1] = 1
                cc[r, 2] = convert(Int64, data["cc"][r][2])
            end
        end
        
        @show connect
        @show cc
        return connect, cc
    end
end

function main(_file::String)
    connect, cc = getInput(_file)

    bloco = [4 -1 -1 -1 -1]

    n, temp = size(connect)
    A = zeros(Float64, n, n)
    b = zeros(Float64, n, 1)

    #assembly
    for i=1:n
        A[i, i] = bloco[1]
        for j=1:4
            col = connect[i, j]
            if col != 0
                if cc[col, 1] == 0
                    A[i, col] = bloco[j + 1]
                else
                    b[i, 1] = b[i, 1] - bloco[j + 1] * cc[col, 2]
                end
            end
        end
    end

    #apply bounder condition
    for i=1:n
        if cc[i, 1] == 1
            A[i, :] = zeros(Float64, 1, n)
            A[i, i] = 1
            b[i, 1] = cc[i, 2]
        end
    end

    x = A \ b
    @show x
end

if length(ARGS) == 1
    main(ARGS[1])
end
