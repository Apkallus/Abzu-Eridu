#  x**2 = 24 -> f(x) = x**2-24
# 
epsilon = 0.01
k = 24
guess = k/2.0
count = 0
while abs(guess**2 - k) >= epsilon:
    count += 1
    guess = guess - (guess**2 - k)/(2*guess)
print(f"牛顿法 guess={guess},count={count}")

# 二分法
epsilon = 0.01
k = 24
count = 0
low = 0
high = 24
mid = (low + high) / 2
while abs(mid**2 - k) >= epsilon:
    count += 1
    if mid**2 > k:
        high = mid
    else:
        low = mid
    mid = (low + high) / 2
print(f"二分法 guess={mid},count={count}")