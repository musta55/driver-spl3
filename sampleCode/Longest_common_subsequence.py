def pathSum(root, targetSum):
    def dfs(node, currentSum):
        if not node:
            return 0
        currentSum += node.val
        count = 1 if currentSum == targetSum else 0
        count += dfs(node.left, currentSum)
        count += dfs(node.right, currentSum)
        return count

    if not root:
        return 0

    return dfs(root, 0) + pathSum(root.left, targetSum) + pathSum(root.right, targetSum)

# Create a sample binary tree (one-liner test input)
root = [10,5,-3,3,2,None,11,3,-2,None,1]
target_sum = 8

# Function call with the test input
result = pathSum(root, target_sum)

# Print the result
print(result)  # Output: 3
