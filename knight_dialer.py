MOD = (10**9 + 7)

class Solution:
    def knightDialer(self, n: int) -> int:
        if n == 1: return 10
        v = [1 for _ in range(10)]
        tmp = [0 for _ in range(10)]
        v[5]=0
        for i in range(n-1):
            tmp[0] = v[4]+v[6]
            tmp[1] = v[8]+v[6]
            tmp[2] = v[7]+v[9]
            tmp[3] = v[4]+v[8]
            tmp[4] = v[0]+v[3]+v[9]
            tmp[6] = v[0]+v[1]+v[7]
            tmp[7] = v[2]+v[6]
            tmp[8] = v[1]+v[3]
            tmp[9] = v[4]+v[2]
            for j in range(10):
                v[j] = tmp[j]
                
        sm = 0
        for i in range(10):
            sm += v[i] 
            sm %= MOD
        return sm

    


from typing import List
class Solution2:
    transitions = {
        1: [6, 8],
        2: [7, 9],
        3: [4, 8],
        4: [3, 9, 0],
        5: [],
        6: [1, 7, 0],
        7: [2, 6],
        8: [1, 3],
        9: [2, 4],
        0: [4, 6]
        }
    def step_comb(self, inp: str) -> str:
        inp = int(inp[-1])
        allowed_transition = self.transitions[inp]
        for i in allowed_transition:
            yield str(i)
    def knightDialer(self, n: int) -> int:
        if n == 0: return 0
        combs: List[str] = []
        for start_number in range(10):
            combs.append(str(start_number))
        if n ==1: return 1
        n -= 1
        while n != 0:
            new_combs = []
            for i, comb in enumerate(combs):
                print(comb)
                for extra in self.step_comb(comb):
                    new_combs.append(comb+extra)
                    print('- ', comb+extra)
            combs = new_combs
            n -= 1
        return len(combs)
# c = Solution()
# print(c.knightDialer(4))


if __name__ == '__main__':
    knight = Solution2().knightDialer(4)
    print(knight)