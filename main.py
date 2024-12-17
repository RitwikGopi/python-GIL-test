import concurrent.futures
import multiprocessing
import random
import timeit

import requests


def is_prime(num):
    """
    Check if a number is prime.

    Args:
    num (int): The number to check.

    Returns:
    bool: True if the number is prime, False otherwise.
    """
    if num <= 1:  # Numbers less than or equal to 1 are not prime
        return False
    if num <= 3:  # 2 and 3 are prime
        return True
    if num % 2 == 0 or num % 3 == 0:  # Eliminate multiples of 2 and 3
        return False

    # Check factors from 5 to sqrt(num) skipping even numbers
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6

    return True


def loop(numbers):
    result = {}
    for number in numbers:
        result[number] = is_prime(number)
    return result


def split_threaded(numbers):
    mid_point = len(numbers) // 4
    split_1 = numbers[:mid_point]
    split_2 = numbers[mid_point:mid_point * 2]
    split_3 = numbers[mid_point * 2:mid_point * 3]
    split_4 = numbers[mid_point * 3:]
    inputs = [split_1, split_2, split_3, split_4]

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(loop, inp) for inp in inputs]
        for future in concurrent.futures.as_completed(futures):
            future.result()


def split_multiprocessing(numbers):
    mid_point = len(numbers) // 4
    split_1 = numbers[:mid_point]
    split_2 = numbers[mid_point:mid_point * 2]
    split_3 = numbers[mid_point * 2:mid_point * 3]
    split_4 = numbers[mid_point * 3:]
    inputs = [split_1, split_2, split_3, split_4]
    with multiprocessing.Pool(4) as pool:
        pool.map(loop, inputs)


def api(numbers):
    url = "http://0.0.0.0:5000/loop"
    headers = {
        'Content-Type': 'application/json'
    }
    return requests.request("POST", url, headers=headers, json=numbers)


def split_threaded_api(numbers):
    mid_point = len(numbers) // 4
    split_1 = numbers[:mid_point]
    split_2 = numbers[mid_point:mid_point * 2]
    split_3 = numbers[mid_point * 2:mid_point * 3]
    split_4 = numbers[mid_point * 3:]
    inputs = [split_1, split_2, split_3, split_4]

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(api, inp) for inp in inputs]
        for future in concurrent.futures.as_completed(futures):
            future.result()


def measure_func(func, arg, iterations=5):
    result = timeit.timeit(lambda: func(arg), number=iterations)
    print(f"[{func.__name__}]: Total time for {iterations} calls: {result:.4f} seconds")


def main():
    numbers = [random.randrange(10000) for _ in range(10**8)]
    measure_func(loop, numbers)
    measure_func(split_threaded, numbers)
    measure_func(split_multiprocessing, numbers)
    measure_func(split_threaded_api, numbers)


if __name__ == "__main__":
    main()
