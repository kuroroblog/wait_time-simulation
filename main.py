# シミュレーション1の場合のみを考えます。
# 客一人が到着するのにかかる平均時間 : 1 / λ = 30.0 ⏩ λ = 1 / 30.0(平均到着率)
# 客一人が受けるサービスにかかる時間(シミュレーション1の場合) : 1 / μ = 0.8 * 1 / μe + 0.2 * 1 / μc ⏩ 1 / μ = 0.8 * 15.0 + 0.2 * 25.0 = 17.0 ⏩ μ = 1 / 17.0(平均サービス率)
# 参考文献1 : http://objectclub.jp/technicaldoc/monkey/s_wait
# 参考文献2 : https://teratail.com/questions/283038

import simpy
import random
import matplotlib.pyplot as plt

###########################################
# シミュレーションを実行する。

# 到着イベント
def arrive():
    global time, stay, canserve
    # 時間に到達するまで、無限に人を増やし続ける。
    while True:
        # 人が来る時間を生成する。平均到着率から算出。
        yield env.timeout(random.expovariate(1 / 30.0))
        # 人が到着した時間を記録する。
        time.append(env.now)
        # 人を増やす。
        stay += 1
        # サービスを受けることのできる状態ならば、queue関数を実行。
        if(canserve):
            env.process(queue())

# 待ち行列に並ぶ
def queue():
    global time, stay, canserve
    canserve = False
    # 人が一人でもいれば、サービスを提供し続ける。
    while len(time) > 0:
        # stay : 待ち行列に並んでいる人数。(自分も含む。)
        # env.now : 現在時刻。
        # env.now - time[0] : 待ち行列先頭の人の、到着してからサービスを受ける前までの待ち時間
        result.append([stay, env.now - time[0]])

        # 人一人がサービスを受けている時間を生成する。
        # 平均サービス率から算出。
        yield env.timeout(random.expovariate(1 / 17.0))

        # サービスを受けた人の、到着した時間を削除する。
        time = time[1:]

        # 人が店から出る。
        stay -= 1

    canserve = True

# 客が到着するしたときの時刻
time = [0]
# 客の滞在人数
stay = 0
# サービスを提供できる状態かどうか?
canserve = True
# シミュレーション結果情報
result = []

# 客の到着率、サービス率は指数分布に従う。
# 指数分布とは? : https://rikei-logistics.com/exponential-distribution
env = simpy.Environment()

# 実行
env.process(arrive())
env.run(until = 1000000)

###########################################

###########################################
# シミュレーションをグラフ化する。

x_position_list = ['15', '45', '75', '105', '135', '165', '195', '225', '255', '285', '315', '345', '375', '405', '435', '465', '495']

tmp = []
for _ in range(len(x_position_list)):
    tmp.append([])

# シミュレーションの結果を分析する。
for i in range(len(result)):
    stay_cnt = result[i][0]
    wait_time = result[i][1]
    for j in range(1, len(x_position_list) - 1):
        range_a = int(x_position_list[j - 1])
        range_b = int(x_position_list[j])

        # (例) : 15~45分待たされた人は、15分のグラフに分布する。
        # (例) : 45~75分待たされた人は、45分のグラフに分布する。
        if range_a <= wait_time <= range_b:
            tmp[j - 1].append(stay_cnt)
            break

y_position_list = []
for t in tmp:
    t_len = len(t)
    if t_len > 0:
        # (例) 15分待たされた場合に、平均してどれくらいの人が待機していたのか算出する。
        # (例) 45分待たされた場合に、平均してどれくらいの人が待機していたのか算出する。
        y_position_list.append(1 / (sum(t) / t_len))
    else:
        y_position_list.append(0)

# 参考 : http://tarao-mendo.blogspot.com/2018/04/matplotlib-xtwins-graph.html
# figureの作成
fig = plt.figure()

# subplotの作成
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()

ax1.bar(x_position_list, y_position_list)
ax2.plot(x_position_list, y_position_list, color='red')

# グラフタイトルとラベル
ax1.set_title('1 / μe = 15.0, 1 / μc = 25.0')
ax1.set_xlabel("Waiting time")
ax1.set_ylabel("Distribution of the number of customers")

plt.show()
###########################################
