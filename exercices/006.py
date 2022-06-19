def fareEstimator(ride_time, ride_distance, cost_per_minute, cost_per_mile):
    return [ride_time*i + ride_distance*j for i, j in zip(cost_per_minute, cost_per_mile)]


print(fareEstimator(30, 7, [0.2, 0.35, 0.4, 0.45], [1.1, 1.8, 2.3, 3.5]))
