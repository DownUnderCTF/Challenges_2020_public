import sys

try:
    input_file = sys.argv[1]
except:
    print("Need to give a valid file!")
    sys.exit()

with open(input_file, 'r') as f:
    data = f.read()

datalines = data.split('\n')
new_data = []
for line in datalines:
    if not len(line) == 0:
        if line[-1] == ' ':
            line = line[:-1]
    new_data.append(line)

with open('out.txt', 'w') as f:
    f.write('\n'.join(new_data))
