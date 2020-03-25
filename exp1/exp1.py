import sys

print(sys.argv)


primes = [i for i in range(3, 100) if all(i % j != 0 for j in range(2, i))]
print(primes[::-1])