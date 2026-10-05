from os.path import join

# Question 1
def question1():
  print("Hay nhap vao so nguyen n:")
  n = int(input())
  for i in range(1, n + 1):
    print(i, ": ", i * i)

# Question 2
def question2():
  print("Hay nhap vao so nguyen n:")
  n = int(input())
  uoc = []
  for i in range(1, n + 1):
    if n % i == 0:
      uoc.append(str(i))
  print("Cac uoc cua so", n, "la: ", ", ".join(uoc))

def timuoc(n):
  uoc = []
  for i in range(1, n + 1):
    if n % i == 0:
      uoc.append(i)
  return uoc

#Question3
def question3():
  print("Hay nhap vao so nguyen n:")
  n = int(input())
  idx = 1
  for i in range(1, n + 1):
    for j in range(1, i + 1):
      print(idx, end=" ")
      idx += 1
    print()

#Question 4:
def question4():
  print("Hay nhap vao so nguyen n:")
  n = int(input())
  uoc = timuoc(n)
  print("Cac uoc cua so", n, "la: ", ", ".join(map(str, uoc)))
  tonguoc = 0
  for i in uoc:
    if i != n:
      tonguoc += i
  print("Tong uoc nho hon", n, "la:", tonguoc)
  if tonguoc == n:
    print(n, "la so hoan hao")
  else:
    print(n, "khong la so hoan hao")

if __name__ == "__main__":
  question4()
