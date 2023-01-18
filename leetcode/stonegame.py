'''
Alex and Lee play a game with piles of stones.  There are an even number of piles arranged in a row, and each pile has a positive integer number of stones piles[i].

The objective of the game is to end with the most stones.  The total number of stones is odd, so there are no ties.

Alex and Lee take turns, with Alex starting first.  Each turn, a player takes the entire pile of stones from either the beginning or the end of the row. 
This continues until there are no more piles left, at which point the person with the most stones wins.

Assuming Alex and Lee play optimally, return True if and only if Alex wins the game.
'''

'''
Input: piles = [5,3,4,5]
Output: true
Explanation:
Alex starts first, and can only take the first 5 or the last 5.
Say he takes the first 5, so that the row becomes [3, 4, 5].
If Lee takes 3, then the board is [4, 5], and Alex takes 5 to win with 10 points.
If Lee takes the last 5, then the board is [3, 4], and Alex takes 4 to win with 9 points.
This demonstrated that taking the first 5 was a winning move for Alex, so we return true.
'''

''' DP SOLUTION'''
'''
What if piles.length can be odd?
What if we want to know exactly the diffenerce of score?
Then we need to solve it with DP.

dp[i][j] means the biggest number of stones you can get more than opponent picking piles in piles[i] ~ piles[j].
You can first pick piles[i] or piles[j].

If you pick piles[i], your result will be piles[i] - dp[i + 1][j]
If you pick piles[j], your result will be piles[j] - dp[i][j - 1]
So we get:
dp[i][j] = max(piles[i] - dp[i + 1][j], piles[j] - dp[i][j - 1])
We start from smaller subarray and then we use that to calculate bigger subarray.

Note that take evens or take odds, it's just an easy strategy to win when the number of stones is even.
It's not the best solution!
I didn't find a tricky solution when the number of stones is odd (maybe there is).
'''
from typing import List

class Solution:

    def stoneGame(self, piles: List[int]) -> bool:
        n = len(piles)
        dp = [[0] * n for i in range(n)]
        for i in range(n): dp[i][i] = piles[i]
        for d in range(1, n):
            for i in range(n - d):
                dp[i][i + d] = max(piles[i] - dp[i + 1][i + d], piles[i + d] - dp[i][i + d - 1])
        return dp[0][-1] > 0


if __name__ == '__main__':
    s = Solution()
    print(s.stoneGame([5,3,4,5]))