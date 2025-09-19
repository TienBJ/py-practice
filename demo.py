## TEST 1   
def divmod(a, b):
    print (a // b)
    print (a % b)
    return a // b, a % b

a, b = map(int, input().split())
print (f"{divmod(a, b)}")


## TEST 2
n = int(input())

names = []
marks = []

for i in range(n):
    line = input().split()
    name = line[0]
    score1 = float(line[1])
    score2 = float(line[2])
    score3 = float(line[3])
    
    names.append(name)
    marks.append([score1, score2, score3])

query_name = input()

for i in range(n):
    if names[i] == query_name:
        total = marks[i][0] + marks[i][1] + marks[i][2]
        avg = total / 3
        print(f"{avg:.2f}")


## TEST 3
text_message = input()
new_text = ""

for i in range(len(text_message)):
    if text_message[i] == " ":
        new_text += "-" 
    else:
        new_text += text_message[i]

print(new_text)

## TEST 4 (Medium 1)
def solve(s):
    result = ""
    for i in range(len(s)):
        if i == 0 or s[i-1] == " ":
            result += s[i].upper()
        else:
            result += s[i]
    return result


## TEST 5 (Medium 3)
k = int(input())
rooms = list(map(int, input().split()))

count = {}
for room in rooms:
    count[room] = count.get(room, 0) + 1
    
for room, c in count.items():
    if c == 1:
        print(room)

## Test 6 (Medium 2)
n, m = map(int, input().split())

half = n // 2

for i in range(half):
    count = 2 * i + 1
    text = ".|." * count
    total_dash = m - len(text)
    left_dash = total_dash // 2
    right_dash = total_dash - left_dash
    print("-" * left_dash + text + "-" * right_dash)

welcome = "WELCOME"
total_dash = m - len(welcome)
left_dash = total_dash // 2
right_dash = total_dash - left_dash
print("-" * left_dash + welcome + "-" * right_dash)

for i in range(half - 1, -1, -1):
    count = 2 * i + 1
    text = ".|." * count
    total_dash = m - len(text)
    left_dash = total_dash // 2
    right_dash = total_dash - left_dash
    print("-" * left_dash + text + "-" * right_dash)


## TEST 7 (HARD 1)
n = int(input())
for i in range(1, n): print((10**i - 1) // 9 * i)

## TEST 8 (HARD 2)

## TEST 9 (HARD 3)
n = int(input())
for i in range(1, n + 1): print(((10**i - 1) // 9) ** 2)