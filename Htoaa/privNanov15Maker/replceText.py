import sys
infile = sys.argv[1]
search_text = sys.argv[2]
replace_text = sys.argv[3]
with open(infile, 'r') as file:

    data = file.read()
    data = data.replace(search_text, replace_text)

with open(infile, 'w') as file:
    file.write(data)
