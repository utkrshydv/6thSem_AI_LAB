n = int(input("Enter a three digit number: "))

def check_prime(num):
  if num == 1 or num == 0:
    return False
  if num == 2:
    return True
  
  fact_count = 0
  for i in range(1, num):
    if num%i == 0:
      fact_count += 1

  if fact_count > 1:
    return False
  else:
    return True
  

for i in range(0, n+1):
  if check_prime(i):
    print(i, " ")

