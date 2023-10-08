from multiprocessing import Pool, cpu_count

def factorize(number):
    factors = []
    for i in range(1, number+1):
        if number % i == 0:
            factors.append(i)
    return factors

def parallel_factorize(numbers):
    with Pool(cpu_count()) as pool:
        return pool.map(factorize, numbers)
