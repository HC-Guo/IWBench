from html_custom_element import compare_element
    
# def compare_func(item1, item2):
#     # 这是一个示例比较函数，假设返回两个元素之间的六个维度分数
#     return [0.9, 0.95, 0.9, 0.88, 0.93, 0.91]

def is_match(item1, item2, threshold=0.9):
    scores = compare_element(item1, item2)
    # 先验减枝
    if scores[0] == 0.0:
        return False
    return sum(scores) / len(scores) >= threshold

def count_matches(a, b, threshold=0.9):
    count = 0
    for item_a in a:
        if any(is_match(item_a, item_b, threshold=threshold) for item_b in b):
            count += 1
    return count

def find_lcs(a, b, threshold=0.9):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if is_match(a[i - 1], b[j - 1], threshold=threshold):
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

def compare(a, b, threshold):
    match_count = count_matches(a, b, threshold=threshold)
    lcs_result = find_lcs(a, b, threshold=threshold)
    len_a = len(a)
    return (match_count/len_a, lcs_result/len_a) if len_a != 0.0 else (1.0, 1.0)


if __name__=="__main__":
    a = []
    b = []
    match_count = count_matches(a, b)
    lcs_result = find_lcs(a, b)
    score = compare(a, b, 0.9)
    print(match_count, lcs_result, score)


