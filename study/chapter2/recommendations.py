# coding=utf-8


# origin data.
critics = {
    'Lisa Rose':
        {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
         'The Night Listener': 3.0},
    'Gene Seymour':
        {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
         'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
         'You, Me and Dupree': 3.5},
    'Michael Phillips':
        {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
         'Superman Returns': 3.5, 'The Night Listener': 4.0},
    'Claudia Puig':
        {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
         'The Night Listener': 4.5, 'Superman Returns': 4.0,
         'You, Me and Dupree': 2.5},
    'Mick LaSalle':
        {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
         'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
         'You, Me and Dupree': 2.0},
    'Jack Matthews':
        {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
         'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
    'Toby':
        {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}
}

from math import sqrt


# return the similarity between person1 and person2. 欧几里得距离
def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    # no same item. return 0.
    if len(si) == 0: return 0

    # cal all diff's power.
    sum_of_squares = sum(
        [pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sqrt(sum_of_squares))


# 皮尔逊距离
def sim_pearson(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1

    # 得到列元素的个数
    n = len(si)

    if n == 0:
        return 1

    # 对所有偏好求和
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # 求平方和
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # 求乘积和
    pSum = sum(prefs[p1][it] * prefs[p2][it] for it in si)

    # 计算评价值
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0

    r = num / den

    return r


# 查找最佳匹配的人
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]

    scores.sort()
    scores.reverse()
    return scores[0:n]


# 开始推荐物品了。
# 利用所有他人评价值的加权平均，为某人提供建议
def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # 不要和自己做比较
        if other == person: continue
        sim = similarity(prefs, person, other)

        # 忽略评价值为零或小于零的情况
        if sim <= 0: continue
        for movie in prefs[other]:

            # 只对自己还未曾看过的影片进行评价
            if movie not in prefs[person] or prefs[person][movie] == 0:
                # 相似度 * 评价值
                totals.setdefault(movie, 0)
                totals[movie] += prefs[other][movie] * sim
                # 相似度之和
                simSums.setdefault(movie, 0)
                simSums[movie] += sim

    # 建立一个归一化的列表
    rankings = [(total / simSums[movie], movie) for movie, total in totals.items()]

    # 返回排序过的列表
    rankings.sort()
    rankings.reverse()
    return rankings


if __name__ == '__main__':
    print "欧几里得算法相似度"
    print sim_distance(critics, 'Lisa Rose', 'Toby')
    print "皮尔逊算法相似度"
    print sim_pearson(critics, 'Lisa Rose', 'Toby')
    print("欧几里得算法的最佳匹配")
    print topMatches(critics, 'Toby', 3, sim_distance)
    print("皮尔逊算法的最佳匹配")
    print topMatches(critics, 'Toby', 3, sim_pearson)

    print("皮尔逊算法为Toby推荐")
    print getRecommendations(critics, 'Toby')
    print("欧几里得算法为Toby推荐")
    print getRecommendations(critics, 'Toby', similarity=sim_distance)
