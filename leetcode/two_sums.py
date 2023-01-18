
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

        hash_keys = {}

        for idx, num in enumerate(nums):
            if target - num in hash_keys:
                print(hash_keys[target - num], idx)
            else:
                hash_keys[num] = idx

if __name__ == '__main__':
    s = Solution()
    s.twoSum([3,3], 6)