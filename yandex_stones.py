def get_input_values(file):
    rows = ['', '']
    with open(file, 'r') as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        rows[idx] = '' if not line.strip().split() else line.strip().split()[0]

    return rows

def main():

    j, s = get_input_values('input.txt')
    jeweleries = set(s).intersection(j)
    answer = sum(s.count(jew) for jew in jeweleries)
    print(answer)

if __name__ == '__main__':
    main()