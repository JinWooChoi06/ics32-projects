# project0.py

# Starter code for project 0 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Jin Woo Choi
# jinwc4@uci.edu
# 61646260

def square(height):
    ans = ""
    space = "  "
    for i in range(height):
        ans += space * (i-1)
        if i == 0 or i == height:
            ans += "+-+\n"
            ans += space * i + "| |\n"
        else:
            ans += "+-+-+\n"
            ans += space * i + "| |\n"
    ans += space * i + "+-+\n"
    return ans

def main():
    n = int(input())
    while n < 0:
        n = int(input())
    if n == 0:
        print()
    else:
        print(square(n))

if __name__ == "__main__":
    main()
