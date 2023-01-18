class Solution:
    def convert(self, s: str, numRows: int) -> str:
        m = [[''] * len(s) for i in range(numRows)]
        global_idx = 0
        column = 0
        while global_idx < len(s):

            for row_idx in range(numRows):
                m[row_idx][column] = s[global_idx]
                global_idx += 1
                if global_idx >= len(s):
                    break
            if global_idx < len(s):
                for rox_idx_up in range(numRows - 2):
                    column += 1
                    m[numRows - rox_idx_up - 2][column] = s[global_idx]
                    global_idx += 1
                    if global_idx >= len(s):
                        break
            column += 1

        return ''.join([m[r][c] for r in range(len(m)) for c in range(len(m[0]))])


if __name__ == '__main__':
    s = Solution()
    print(s.convert("PAYPALISHIRING", 3))