"""The Game of Hog. / Hog 游戏。"""

from dice import six_sided, make_test_dice
from ucb import main, trace, interact

GOAL = 100  # The goal of Hog is to score 100 points. / Hog 游戏的目标分数是 100 分。

######################
# Phase 1: Simulator / 第一阶段：模拟器 #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times.
    Return the sum of outcomes unless any outcome is 1; in that case, return 1.

    模拟恰好掷 DICE 共 NUM_ROLLS（> 0）次。
    返回所有点数之和；但只要任意一次结果为 1，则返回 1。

    num_rolls:  The number of dice rolls that will be made. / 本回合要掷骰子的次数。
    dice:       A function that simulates a single dice roll outcome. Defaults to six-sided dice. / 模拟一次掷骰结果的函数，默认是六面骰。
    """
    # These assert statements ensure that num_rolls is a positive integer.
    # 这些断言用于确保 num_rolls 是正整数。
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1 / 题目 1 开始
    "*** YOUR CODE HERE *** / 在这里写你的代码 ***"
    total = 0
    pig_out = False
    i = 0
    while i < num_rolls:
        outcome = dice()
        if outcome == 1:
            pig_out = True
        total += outcome
        i += 1
    if pig_out:
        return 1
    return total




        

    # END PROBLEM 1 / 题目 1 结束


def boar_brawl(player_score, opponent_score):
    """Return the points scored by rolling 0 dice according to Boar Brawl.
    根据 Boar Brawl 规则，返回掷 0 个骰子时获得的分数。

    player_score:     The total score of the current player. / 当前玩家总分。
    opponent_score:   The total score of the other player. / 对手总分。

    """
    # BEGIN PROBLEM 2 / 题目 2 开始
    "*** YOUR CODE HERE *** / 在这里写你的代码 ***"
    # END PROBLEM 2 / 题目 2 结束
    '''opponent = (opponent_score // 10) % 10.     best '''
    current = player_score % 10
    if opponent_score >= 100:
        opponent = max(opponent_score // 10, 1) % 10
       
    else:
        opponent = opponent_score // 10

    gain = 3 * abs(current - opponent)
    return max(1,gain)

def take_turn(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the points scored on a turn rolling NUM_ROLLS dice when the
    player has PLAYER_SCORE points and the opponent has OPPONENT_SCORE points.

    返回当前回合掷 NUM_ROLLS 个骰子所获得的分数。
    此时玩家分数为 PLAYER_SCORE，对手分数为 OPPONENT_SCORE。

    num_rolls:       The number of dice rolls that will be made. / 本回合要掷骰子的次数。
    player_score:    The total score of the current player. / 当前玩家总分。
    opponent_score:  The total score of the other player. / 对手总分。
    dice:            A function that simulates a single dice roll outcome. / 模拟一次掷骰结果的函数。
    """
    # Leave these assert statements here; they help check for errors.
    # 保留这些断言有助于检查错误。
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    # BEGIN PROBLEM 3 / 题目 3 开始
    "*** YOUR CODE HERE *** / 在这里写你的代码 ***"
    # END PROBLEM 3 / 题目 3 结束
    gain = 0
    if num_rolls == 0:
        gain = boar_brawl(player_score, opponent_score)
        return gain
    else:
        gain = roll_dice(num_rolls, dice)
        return gain


def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, ignoring Sus Fuss.

    返回玩家本回合结束后的总分。
    玩家以 PLAYER_SCORE 开始本回合，掷 NUM_ROLLS 个骰子，且忽略 Sus Fuss。
    """
    score = player_score + take_turn(num_rolls, player_score, opponent_score, dice)
    return score

def is_prime(n):
    """Return whether N is prime. / 返回 N 是否为质数。"""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True

def num_factors(n):
    """Return the number of factors of N, including 1 and N itself.
    返回 N 的因子个数（包括 1 和 N 本身）。
    """
    # BEGIN PROBLEM 4 / 题目 4 开始
    "*** YOUR CODE HERE *** / 在这里写你的代码 ***"
    # END PROBLEM 4 / 题目 4 结束

    if is_prime(n) == True:
        return 2
    elif n == 1:
        return 1
    else:
        i = 1
        factors = 0
        while i <= n:
            if n % i == 0:
                factors += 1
            i += 1
        return factors

            

def sus_points(score):
    """Return the new score of a player taking into account the Sus Fuss rule.
    根据 Sus Fuss 规则，返回玩家更新后的分数。
    """
    # BEGIN PROBLEM 4 / 题目 4 开始
    "*** YOUR CODE HERE *** / 在这里写你的代码 ***"
    # END PROBLEM 4 / 题目 4 结束
    if num_factors(score) == 3 or num_factors(score) == 4:
        i = score
        while num_factors(i) > 2:
            i +=1
        return i
    else:
        return score


def sus_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, including Sus Fuss.

    返回玩家本回合结束后的总分。
    玩家以 PLAYER_SCORE 开始本回合，掷 NUM_ROLLS 个骰子，且包含 Sus Fuss。
    """
    # BEGIN PROBLEM 4 / 题目 4 开始
    "*** YOUR CODE HERE *** / 在这里写你的代码 ***"
    # END PROBLEM 4 / 题目 4 结束
    return sus_points(player_score + take_turn(num_rolls, player_score, opponent_score, dice))




def always_roll_5(score, opponent_score):
    """A strategy of always rolling 5 dice, regardless of the player's score or
    the opponent's score.

    一种策略：无论双方分数如何，都固定掷 5 个骰子。
    """
    return 5


def play(strategy0, strategy1, update,
         score0=0, score1=0, dice=six_sided, goal=GOAL):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first and Player 1's score second.

    模拟一整局游戏并返回双方最终分数。
    返回顺序为：玩家 0 分数在前，玩家 1 分数在后。

    E.g., play(always_roll_5, always_roll_5, sus_update) simulates a game in
    which both players always choose to roll 5 dice on every turn and the Sus
    Fuss rule is in effect.

    例如，play(always_roll_5, always_roll_5, sus_update) 会模拟这样一局：
    双方每回合都选择掷 5 个骰子，并且启用 Sus Fuss 规则。

    A strategy function, such as always_roll_5, takes the current player's
    score and their opponent's score and returns the number of dice the current
    player chooses to roll.

    策略函数（如 always_roll_5）接收当前玩家分数和对手分数，
    返回当前玩家该回合要掷的骰子数。

    An update function, such as sus_update or simple_update, takes the number
    of dice to roll, the current player's score, the opponent's score, and the
    dice function used to simulate rolling dice. It returns the updated score
    of the current player after they take their turn.

    更新函数（如 sus_update 或 simple_update）接收要掷的骰子数、
    当前玩家分数、对手分数以及掷骰函数，并返回当前玩家完成该回合后的新分数。

    strategy0: The strategy for player0. / 玩家 0 使用的策略。
    strategy1: The strategy for player1. / 玩家 1 使用的策略。
    update:    The update function (used for both players). / 更新函数（双方都使用）。
    score0:    Starting score for Player 0 / 玩家 0 的起始分数。
    score1:    Starting score for Player 1 / 玩家 1 的起始分数。
    dice:      A function of zero arguments that simulates a dice roll. / 无参掷骰函数。
    goal:      The game ends and someone wins when this score is reached. / 达到该分数时游戏结束并产生胜者。
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second). / 当前即将行动的玩家：0（先手）或 1（后手）。
    # BEGIN PROBLEM 5 / 题目 5 开始
    "*** YOUR CODE HERE *** / 在这里写你的代码 ***"
    # END PROBLEM 5 / 题目 5 结束

    who = 0
    num_rolls = 0
    while score0 < goal and score1 < goal:
        if who == 0:
            num_rolls = strategy0(score0, score1)
            score0 = update(num_rolls,score0, score1,dice)
        else:
            num_rolls = strategy1(score1, score0)
            score1 = update(num_rolls,score1, score0,dice)
        who = 1 - who


    return score0, score1


#######################
# Phase 2: Strategies / 第二阶段：策略 #
#######################


def always_roll(n):
    """Return a player strategy that always rolls N dice.

    返回一个始终掷 N 个骰子的玩家策略。

    A player strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    玩家策略是一个函数，接收两个总分参数
    （当前玩家分数与对手分数），并返回当前回合要掷的骰子数。

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10
    # BEGIN PROBLEM 6 / 题目 6 开始
    "*** YOUR CODE HERE *** / 在这里写你的代码 ***"
    # END PROBLEM 6 / 题目 6 结束

    def fkrolls(score, oppent_score):
        return n
    return fkrolls

def catch_up(score, opponent_score):
    """A player strategy that always rolls 5 dice unless the opponent
    has a higher score, in which case 6 dice are rolled.

    一种策略：通常掷 5 个骰子；若对手分数更高，则掷 6 个。

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # Roll one more to catch up. / 为了追分，多掷一个。
    else:
        return 5


def is_always_roll(strategy, goal=GOAL):
    """Return whether STRATEGY always chooses the same number of dice to roll
    given a game that goes to GOAL points.

    在目标分数为 GOAL 的游戏中，判断 STRATEGY 是否总是选择同一个掷骰数。

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    # BEGIN PROBLEM 7 / 题目 7 开始
    first_choice = strategy(0, 0)
    score = 0
    while score < goal:
        opponent_score = 0
        while opponent_score < goal:
            if strategy(score, opponent_score) != first_choice:
                return False
            opponent_score += 1
        score += 1
    return True
    # END PROBLEM 7 / 题目 7 结束

    




def make_averaged(original_function, times_called=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TIMES_CALLED times.

    返回一个函数，计算 ORIGINAL_FUNCTION 调用 TIMES_CALLED 次的平均值。

    To implement this function, you will have to use *args syntax.
    实现此函数需要使用 *args 语法。

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # The avg of 10 4's, 10 2's, 10 5's, and 10 1's / 10 次 4、10 次 2、10 次 5、10 次 1 的平均值
    3.0
    """
    # BEGIN PROBLEM 8 / 题目 8 开始
    "*** YOUR CODE HERE *** / 在这里写你的代码 ***"
    # END PROBLEM 8 / 题目 8 结束

   
    def get_averaged(*args):
        i = 0
        total = 0
        while i < times_called:
            total += original_function(*args)
            i += 1
        return total / times_called
    return get_averaged







def max_scoring_num_rolls(dice=six_sided, times_called=1000):
    """Return the number of dice (1 to 10) that gives the maximum average score for a turn.
    Assume that the dice always return positive outcomes.

    返回能使单回合平均得分最大的掷骰数（1 到 10）。
    假设骰子结果始终为正数。

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9 / 题目 9 开始
    "*** YOUR CODE HERE *** / 在这里写你的代码 ***"
    # END PROBLEM 9 / 题目 9 结束

    n = 2
    current_averaged = 0
    averaged_roll = make_averaged(roll_dice, times_called)
    best_averaged = averaged_roll(1, dice)

    best_rolls = 1
    while n <=  10:
        current_averaged = averaged_roll(n, dice)

        if current_averaged > best_averaged:
            best_averaged = current_averaged
            best_rolls = n
        n += 1
    return best_rolls

   



def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise.
    若 strategy0 战胜 strategy1 则返回 0，否则返回 1。
    """
    score0, score1 = play(strategy0, strategy1, sus_update)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE.
    Averages the win rate when starting as player 0 and as player 1.

    返回 STRATEGY 对阵 BASELINE 的平均胜率。
    该值是先手（玩家 0）与后手（玩家 1）两种情况下胜率的平均。
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results.
    运行一系列策略实验并输出结果。
    """
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)

    print('always_roll(6) win rate:', average_win_rate(always_roll(6))) # near 0.5 / 接近 0.5
    print('catch_up win rate:', average_win_rate(catch_up))
    print('always_roll(3) win rate:', average_win_rate(always_roll(3)))
    print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    print('boar_strategy win rate:', average_win_rate(boar_strategy))
    print('sus_strategy win rate:', average_win_rate(sus_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish *** / 你可以按需添加更多实验 ***"



def boar_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice if Boar Brawl gives at least THRESHOLD
    points, and returns NUM_ROLLS otherwise. Ignore score and Sus Fuss.

    若 Boar Brawl 可获得至少 THRESHOLD 分，则该策略返回掷 0 个骰子；
    否则返回 NUM_ROLLS。忽略总分和 Sus Fuss。
    """
    # BEGIN PROBLEM 10 / 题目 10 开始
    if boar_brawl(score, opponent_score) >= threshold:
        return 0
    else:
        return num_rolls # Remove this line once implemented. / 实现完成后删除这一行。
    # END PROBLEM 10 / 题目 10 结束


def sus_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice when your score would increase by at least threshold.
    当你的分数将至少增加 threshold 时，该策略返回掷 0 个骰子。
    """
    # BEGIN PROBLEM 11 / 题目 11 开始
    current_score = score + boar_brawl(score, opponent_score)
    if sus_points(current_score) - score>= threshold:
        return 0
    else:
        return num_rolls
    
    return num_rolls  # Remove this line once implemented. / 实现完成后删除这一行。
    # END PROBLEM 11 / 题目 11 结束


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    简要描述你的最终策略。

    *** YOUR DESCRIPTION HERE *** / 在此填写你的描述 ***
    """
    # BEGIN PROBLEM 12 / 题目 12 开始
    return 6  # Remove this line once implemented. / 实现完成后删除这一行。
    # END PROBLEM 12 / 题目 12 结束


##########################
# Command Line Interface / 命令行接口 #
##########################

# NOTE: The function in this section does not need to be changed. It uses
# features of Python not yet covered in the course.
# 注意：本节函数无需修改，这里使用了课程尚未覆盖的一些 Python 特性。

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.
    读取命令行参数并调用对应函数。
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()