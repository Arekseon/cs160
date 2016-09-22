f = open('users.txt', 'r')
for line in f:
        pair = line.split()
        user =  pair[0]
        password = pair[2]

with open("users.txt", "a") as f:
     f.write("\nnew line")