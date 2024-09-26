"""
该脚本用于模拟掷骰子。
骰宝（sic bo）是一种掷骰子的赌博游戏，参考 https://en.wikipedia.org/wiki/Sic_bo
规则如下：
- 每局游戏同时掷三个骰子，每个骰子可能得到 1~6 的点数，相当于产生三个随机数。
- 玩家可以押注多种掷骰结果：
    - 大（tai）
        - ：三个骰子的点数之和大于等于 11 。
        - 赔率为 1:1 。比如玩家押注 1 元，猜对了就余额增加 1 元，猜错了就余额减少 1 元。
        - 理论上，买大猜对的概率为 0.4861 。假设玩家玩无数局，则余额会变成最初的 0.4861*(1+1)≈0.9722 倍。
    - 小（sai）
        - ：三个骰子的点数之和小于等于 10 。
        - 赔率为 1:1 。
    - 豹子（triple）
        - ：如果三个骰子的点数全部相同，比如 1,1,1 或 2,2,2 ，则称为围骰。从 1 到 6 ，总共有 6 种可能的围骰取值。出现任何一种围骰时，俗称为豹子，此时玩家买大或买小，都算输。
        - 赔率为 1:30 。
        - 理论上，豹子出现的概率为 6/216≈0.0277 。假设玩家玩无数局，则余额会变成最初的 0.0277*(1+30)≈0.8587 倍。与买大、买小相比，赢利的数学期望低得多。
"""
import random


class Roll:
    odds = {'tai': 1, 'sai':1, 'tripler': 30}
    all_triple = [[i,i,i] for i in range(1,7)]

    def __init__(self, dice_count=1, max_point=6):
        """ 同时掷 dice_count 个骰子，得到一组数字并返回 """
        self.points = [random.randint(1, max_point) for _ in range(dice_count)]

    def is_tai(self):
        return True if sum(self.points) >= 11 else False

    def is_sai(self):
        return True if sum(self.points) <= 10 else False

    def is_triple(self):
        return True if self.points in self.all_triple else False


# 玩家
class Player:
    def __init__(self):
        self.balance = 100    # 玩家的钱包余额
        self.gain = 0         # 玩家的累计获利
        self.win_count = 0    # 玩家的累计赌中次数
        self.bet = 1          # 玩家在每局游戏的下注金额
        self.choice = 'skip'  # 玩家在下一局游戏的决策

    def make_a_choice(self, roll_history=[]):
        """ 玩家查看以前几局的掷骰子结果，决定下一局游戏的押注 """
        # 行为策略：总是买大
        self.choice = 'tai'

        # 决策逻辑：
        #   - 连续 2 局小的概率为 0.25 ，连续 3 局小的概率为 0.125 ，假设玩无数局，则前者出现的次数会比后者多一倍。因此遇到连续 2 局小的情况时，就反向买大。
        #   - 这两种概率的差值，远大于出现豹子的概率，因此可忽略出现豹子的损失。
        #   - 虽然理论上每局的骰子点数，是独立随机事件，但玩家难免存在惯性思维，想在连续 n 局小时跟着押注，或者反向押注。
        # 行为策略：
        #   - 如果最近 2 局游戏都是小（包括豹子），则下一局买大，否则不下注。每局下注金额固定，不会按马丁格尔策略那样加倍下注。
        if len(roll_history) < 2 :
            self.choice = 'skip'
        elif roll_history[-1].is_sai() and roll_history[-2].is_sai():
            self.choice = 'tai'
        else:
            self.choice = 'skip'

    def is_out(self):
        """ 如果玩家的余额小于等于 0 ，则出局，提前结束游戏 """
        if self.balance <= 0:
            return True
        else:
            return False


# 庄家
class Banker:

    def run_game(self, game_count=1):
        roll_history = []
        player = Player()
        for _game_count in range(game_count):
            print(f'第 {_game_count+1} 局游戏，', end='')
            player.make_a_choice(roll_history)
            print(f'玩家决策为：{player.choice :<5} ，', end='')

            roll = Roll(dice_count=3, max_point=6)
            print(f'掷骰子结果为：{roll.points} ，', end='')
            if player.choice == 'skip':
                player.gain = 0
            # 优先判断是否出现豹子。如果没出现豹子，才判断大、小
            elif roll.is_triple():
                if player.choice == 'triple':
                    player.gain = player.bet * roll.odds['triple']
                else:
                    player.gain = player.bet * -1
            elif roll.is_tai():
                if player.choice == 'tai':
                    player.gain = player.bet * roll.odds['tai']
                else:
                    player.gain = player.bet * -1
            elif roll.is_sai():
                if player.choice == 'sai':
                    player.gain = player.bet * roll.odds['sai']
                else:
                    player.gain = player.bet * -1

            player.balance += player.gain
            if player.gain > 0:
                tips_on_win_or_lose = '赌赢了'
                player.win_count += 1
            elif player.gain < 0:
                tips_on_win_or_lose = '赌输了'
            else:
                tips_on_win_or_lose = '没变化'
            print(f'因此，玩家{tips_on_win_or_lose}，获利为 {player.gain :>2} ，余额为 {player.balance}')

            roll_history.append(roll)


if __name__ == '__main__':
    Banker().run_game(game_count=100_000)
