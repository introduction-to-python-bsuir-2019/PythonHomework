
from typing import List

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """

        carry = 0
        head = first_head =  ListNode()
        
        while l1 or l2 or carry:
            result = 0
            if l1:
                result += l1.val
                l1 = l1.next
            if l2:
                result += l2.val
                l2 = l2.next
            if carry:
                result += carry
                
            carry = result // 10
            val = result % 10
            head.next = ListNode(val)
            head = head.next
        return first_head.next

    def stringToListNode(self,number_string: List[int]):
            previousNode = None
            first = None
            for i in number_string:
                currentNode = ListNode(i)
                if first is None:
                    first = currentNode
                if previousNode is not None:
                    previousNode.next = currentNode
                previousNode = currentNode
            return first

if __name__ == '__main__':
    s = Solution()
    l1 = s.stringToListNode([2,4,3])
    l2 = s.stringToListNode([5,6,4])
    s.addTwoNumbers(l1, l2)