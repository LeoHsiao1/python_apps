"""
该脚本的用途：模拟骰宝赌博，只考虑单骰这种玩法。
规则如下：
- 每局同时掷三个骰子，得到三个随机数，比如 2,4,6 。
- 玩家赌上述三个数字中会出现数字 x ，并为此下注 y 元。
  - 如果未出现数字 x ，则 gain 为 -y 。换句说法，这种情况的赔率是 1:1 。
  - 如果出现一个数字 x ，则 gain 为 +y 。换句说法，这种情况的赔率是 1:1 。
  - 如果出现两个数字 x ，则 gain 为 +2y 。换句说法，这种情况的赔率是 1:2 。
  - 如果出现三个数字 x ，则 gain 为 +3y 。换句说法，这种情况的赔率是 1:3 。
"""
import random

def roll_dice(dice_count=1, game_count=1):
    """ 同时掷出 dice_count 个骰子，得到一组数字。可以重复游戏 game_count 次 """
    for _ in range(game_count):
        yield [random.randint(1, 6) for _ in range(dice_count)]


x = 2     # 每局游戏赌哪个数字会出现
y = 10    # 每局游戏下注的金额
gain = 0  # 玩家的累计获利
game_count = 1000000  # 总共玩多少局
win_count = 0  # 玩家赌中的次数
for roll_result in roll_dice(3, game_count):
    appearances = roll_result.count(x)
    if appearances == 0:
        gain += -y
    else:
        gain += appearances*y
        win_count += 1

print(f'掷骰子玩了 {game_count} 局，玩家的累计获利为 {gain}, 胜率为 {win_count/game_count}')
