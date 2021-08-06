class Solution:
    def myAtoi(self, s: str) -> int:
        result = s.strip()

        sign = ''

        if not result:
            return 0
        if result[0] in ['-', '+']:
            sign = result[0]
            if len(result) > 1 and not str.isdigit(result[1]):
                return 0  # '+-12' case

            digit: str = result[1:]
        elif not str.isdigit(result[0]):
            return 0
        elif str.isdigit(result[0]):

            digit: str = result
        
        
        digits = ''.join(list(filter(lambda s: str.isdigit(s) or s == '.', digit)))
        if digits not in digit:
            first_alpha = list(filter(lambda s: str.isalpha(s) or s in ['+', ' ', '-'], digit))
            if first_alpha:
                first_alpha = first_alpha[0]
            
                idx = digit.index(first_alpha)
                digit = digit[0:idx].strip().split()[0]
            else:
                digit = digit
            # return 0
        else:
            digit = digits
        try:
            output = int(sign + digit)
        except ValueError:
            try:
                output = int(float(sign + digit))
            except ValueError:
                return 0

        if output >= 2 ** 32 // 2:
            return 2 ** 32 // 2 -1
        elif output < -2 ** 32 // 2:
            return -2 ** 32 // 2
        else:
            return output


if __name__ == '__main__':
    s = Solution()
    print(s.myAtoi("    123 456"))