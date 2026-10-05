import random

from numpy.ma.core import append, multiply
from numpy.matrixlib.defmatrix import matrix


# Question 1
def question1():
  print("Hay nhap danh sach so nguyen:")
  list = []
  average = 0

  while True:
    n = input()
    if n == "$":
      break
    list.append(int(n))

  for i in list:
    average += i
  if len(list) != 0:
    average /= len(list)
  print("Danh sach so nguyen da nhap:", ", ".join(map(str, list)))
  print(f"Tong trung binh cac so da nhap: {average:.2f}")

# Question 2
def question2():
  print("Hay nhap kich thuoc ma tran:")
  print("M:", end=" ")
  M = int(input())
  print("N:", end=" ")
  N = int(input())

  # Input Matrix
  print("Hay nhap cac phan tu cua ma tran "
        "(tu trai sang phai va tren xuong):")
  matrix = []
  for i in range(M):
    row = []
    for j in range(N):
      row.append(int(input()))
    matrix.append(row)

  # Print Matrix
  print("Ma tran", M, "x", N, "da nhap:" )
  for row in matrix:
    for i in row:
      print(i, end=" ")
    print()

  print("Hay nhap hang can tinh tong"
        "(thu tu cua hang):")
  row_idx = int(input()) - 1
  row_total = 0
  for i in matrix[row_idx]:
    row_total += i
  print("Tong hang thu", row_idx + 1,"la:", row_total)

# Question 3
def question3():
  matrix = []
  order = 1
  for i in range(5):
    row = []
    for j in range(5):
      row.append(order)
      order += 1
    matrix.append(row)

  # Print Matrix
  print("Ma tran 5 x 5 la:")
  for row in matrix:
    for i in row:
      print(i, end="\t")
    print()

  print("Hay nhap hang can tinh tong "
        "(thu tu cua hang):")
  row_idx = int(input()) - 1
  row_total = 0
  for i in matrix[row_idx]:
    row_total += i
  print("Tong hang thu", row_idx + 1,"la:", row_total)

# Question 4
def question4():
  matrix = []
  order = 1
  for i in range(5):
    row = []
    for j in range(5):
      row.append(order)
      order += 2
    matrix.append(row)

  # Print Matrix
  print("Ma tran 5 x 5 la:")
  for row in matrix:
    for i in row:
      print(i, end="\t")
    print()

  row_idx = 1
  row_total = 0
  for i in matrix[row_idx]:
    row_total += i
  print("Tong hang thu", row_idx + 1,"la:", row_total)

# Matrix Class
class Matrix:
  def __init__(self, M: int, N: int):
    self.M = M
    self.N = N
    self.matrix = []

  def add_row(self, row) -> bool:
    if len(row) != self.N:
      return False
    for i in row:
      self.matrix.append(i)
    return True

  def add_column(self, column) -> bool:
    if len(column) != self.M:
      return False
    new_matrix = []
    for i in range(self.M):
      start = i * self.N
      end = start + self.N
      new_matrix.extend(self.matrix[start:end])
      new_matrix.append(column[i])
    self.matrix = new_matrix
    self.N += 1
    return True

  def check_row(self, row_idx):
    return 0 <= row_idx < self.M

  def check_column(self, column_idx):
    return 0 <= column_idx < self.N

  def get_row(self, row_order: int):
    row_idx = row_order - 1
    if self.check_row(row_idx):
      row = []
      for i in range(self.N):
        idx = row_idx * self.N + i
        row.append(self.matrix[idx])
      return row
    return False

  def get_column(self, column_order: int):
    column_idx = column_order - 1
    if self.check_column(column_idx):
      column = []
      for i in range(self.M):
        idx = i * self.N + column_idx
        column.append(self.matrix[idx])
      return column
    return False

  def get_m(self):
    return self.M

  def get_n(self):
    return self.N

  def get_val(self, i: int, j: int):
    idx = i * self.N + j
    return self.matrix[idx]

  def add_val(self, val):
    self.matrix.append(val)

  def change_val(self, i, j, val):
    idx = i * self.N + j
    self.matrix[idx] = val

  def swap_val(self, x1, y1, x2, y2):
    temp = self.get_val(x1, y1)
    self.change_val(x1, y1, self.get_val(x2, y2))
    self.change_val(x2, y2, temp)

  def swap_row(self, row_order1, row_order2):
    row_idx1 = row_order1 - 1
    row_idx2 = row_order2 - 1
    if self.check_row(row_idx1) and self.check_row(row_idx2):
      for i in range(self.N):
        self.swap_val(row_idx1, i, row_idx2, i)

  def swap_column(self, column_order1, column_order2):
    column_idx1 = column_order1 - 1
    column_idx2 = column_order2 - 1
    if self.check_column(column_idx1) and self.check_column(column_idx2):
      for i in range(self.M):
        self.swap_val(i, column_idx1, i, column_idx2)

  def print_matrix(self):
    for i in range(self.M):
      for j in range(self.N):
        print(self.get_val(i, j), end="\t")
      print()

  @staticmethod
  def multiply_matrix(matrix1: Matrix, matrix2: Matrix):
    if matrix1.get_n() != matrix2.get_m():
      return False
    multiply_level = matrix1.get_n()
    multi_matrix = Matrix(matrix1.get_m(), matrix2.get_n())
    for i in range(multi_matrix.M):
      matrix1_row = matrix1.get_row(i + 1)
      for j in range(multi_matrix.N):
        matrix2_column = matrix2.get_column(j + 1)
        sum_multiply = 0
        for k in range(multiply_level):
          sum_multiply += matrix1_row[k] * matrix2_column[k]
        multi_matrix.add_val(sum_multiply)
    return multi_matrix

# Question 5
def question5():
  print("Hay nhap kich thuoc ma tran:")
  print("M:", end=" ")
  M = int(input())
  print("N:", end=" ")
  N = int(input())

  print("Hay nhap cac phan tu cua ma tran "
        "(tu trai sang phai va tren xuong):")
  mtrx = Matrix(M, N)
  for i in range(mtrx.get_m()):
    for j in range( mtrx.get_n()):
      n = int(input())
      mtrx.add_val(n)

  # Print Matrix
  print("Ma tran", M, "x", N, "la:")
  mtrx.print_matrix()

  print("Cot thu nhat:", end=" ")
  column_order1 = int(input())
  print("Cot thu hai:", end=" ")
  column_order2 = int(input())
  print("Ma tran sau khi doi cot la:")
  mtrx.swap_column(column_order1, column_order2)
  mtrx.print_matrix()

# Question 6
def question6():
  print("Hay nhap kich thuoc ma tran thu nhat Mtrx1:")
  print("M:", end=" ")
  M = int(input())
  print("N:", end=" ")
  N = int(input())

  print("Hay nhap cac phan tu cua ma tran Mtrx1"
        "(tu trai sang phai va tren xuong):")
  mtrx1 = Matrix(M, N)
  for i in range(mtrx1.get_m()):
    for j in range(mtrx1.get_n()):
      n = int(input())
      mtrx1.add_val(n)

  print("Hay nhap kich thuoc ma tran thu hai Mtrx2:")
  print("M:", end=" ")
  M = int(input())
  print("N:", end=" ")
  N = int(input())

  print("Hay nhap cac phan tu cua ma tran Mtrx2"
        "(tu trai sang phai va tren xuong):")
  mtrx2 = Matrix(M, N)
  for i in range(mtrx2.get_m()):
    for j in range(mtrx2.get_n()):
      n = int(input())
      mtrx2.add_val(n)

  result = Matrix.multiply_matrix(mtrx1,mtrx2)
  if result:
    print("Tich hai ma tran la:")
    result.print_matrix()
  else:
    print("Hai ma tran khong the nhan")

# Question 7
def question7():
  mydict = {}
  print("Hay nhap so luong nguyen tu khoa:")
  n = int(input())
  for i in range(1, n + 1):
    mydict.update({str(i): i * i})
  print(mydict)

# Question 8
def question8():
  mydict = {}
  for i in range(1, 11):
    mydict[i] = random.randint(1, 10)
  print(mydict)
  matrix = []
  for key, value in mydict.items():
    row = [key, value]
    matrix.append(row)
  print(matrix)

# Question 9
def question9():
  mydict = {}
  print("Hay nhap so luong nguyen tu khoa:")
  n = int(input())
  for i in range(1, n + 1):
    mydict.update({str(i): i * i})
  print(mydict)

if __name__ == "__main__":
  question8()