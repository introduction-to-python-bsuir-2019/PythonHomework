from typing import Tuple, List


class Solution:
    def longestPalindrome(self, s: str) -> str:
        # max_result_length = 0
        # max_result_idx = 0
        # d = {}
        # times = 0
        # for idx in range(len(s)):
        #     if len(s) - idx < max_result_length:
        #         break
        #     for count_letters in range(1, len(s) + 1):
        #         if count_letters < max_result_length:
        #             continue
        #         substring_to_check = s[idx:count_letters]
        #         if substring_to_check not in d:
        #             is_palindrom, n = self.is_palindrom(substring_to_check)
        #             times += 1
        #             if is_palindrom:
        #                 if n > max_result_length:
        #                     max_result_length = n
        #                     max_result_idx = idx
        #                     d[substring_to_check] = (True, idx, n)
        #             else:
        #                 d[substring_to_check] = (False, idx, n)
        
        #         # is_palindrom, n = self.is_palindrom(substring_to_check)
        #         # times += 1
        #         # if is_palindrom:
        #         #     if n > max_result_length:
        #         #         max_result_length = n
        #         #         max_result_idx = idx
        #         #         d[substring_to_check] = (True, n)
        # output = s[max_result_idx: max_result_length + max_result_idx]
        # return output
        dp: List[List[bool]] = [[False] * len(s) for _ in range(len(s))]
        length: int = 0
        result: str = ''
        times = 0
        temp_results = []
        for end in range(len(s)):
            for start in range(end+1):
                if start == end:
                    dp[start][end] = True
                elif start + 1 == end:
                    dp[start][end] = s[start] == s[end]
                else:
                    dp[start][end] = s[start] == s[end] and dp[start+1][end-1]

                if dp[start][end] and end-start+1 > length:
                    times += 1
                    length = end-start+1
                    result = s[start:end+1]
                    temp_results.append(result)

        return result
    def is_palindrom(self, s: str) -> Tuple[bool, int]:
        if s == s[::-1]:
            return True, len(s)
        else:
            return False, 0

if __name__ == '__main__':
    s = Solution()
    # print(s.longestPalindrome("cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"))
    # print(s.longestPalindrome('forgeeksskeegfor'))
    # print(s.longestPalindrome('a'))
    print(s.longestPalindrome('twbiqwtafgjbtolwprpdnymaatlbuacrmzzwhkpvuwdtyfjsbsqxrlxxtqkjlpkvpxmlajdmnyepsmczmmfdtjfbyybotpoebilayqzvqztqgddpcgpelwmriwmoeeilpetbxoyktizwcqeeivzgxacuotnlzutdowiudwuqnghjgoeyojikjhlmcsrctvnahnoapmkcrqmwixpbtirkasbyajenknuccojooxfwdeflmxoueasvuovcayisflogtpxtbvcxfmydjupwihnxlpuxxcclbhvutvvshcaikuedhyuksbwwjsnssizoedjkbybwndxpkwcdxaexagazztuiuxphxcedqstahmevkwlayktrubjypzpaiwexkwbxcrqhkpqevhxbyipkmlqmmmogrnexsztsbkvebjgybrolttvnidnntpgvsawgaobycfaaviljsvyuaanguhohsepbthgjyqkicyaxkytshqmtxhilcjxdpcbmvnpippdrpggyohwyswuydyrhczlxyyzregpvxyfwpzvmjuukswcgpenygmnfwdlryobeginxwqjhxtmbpnccwdaylhvtkgjpeyydkxcqarkwvrmwbxeetmhyoudfuuwxcviabkqyhrvxbjmqcqgjjepmalyppymatylhdrazxytixtwwqqqlrcusxyxzymrnryyernrxbgrphsioxrxhmxwzsytmhnosnrpwtphaunprdtbpwapgjjqcnykgspjsxslxztfsuflijbeebwyyowjzpsbjcdabxmxhtweppffglvhfloprfavduzbgkw'))