def centuryFromYear(year):
    return (year // 100) if year % 100 == 0 else (year // 100) + 1


print(centuryFromYear(101))
