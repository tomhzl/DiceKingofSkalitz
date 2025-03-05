import random

# 定义一个函数，判断一个集合是否是另一个集合的子集
def is_subset(subset, superset):
    # 遍历子集中的每个元素
    return all(item in superset for item in subset)

class Dice:
    # 初始化骰子，设置每个面的概率
    def __init__(self, id, chance = [1,1,1,1,1,1]):
        self.index = 0  # 骰子的当前面
        self.chance = chance  # 骰子的每个面的概率
        self.selected = False  # 骰子是否被选中
        self.id = id
        pass
    
    # 掷骰子，返回骰子的当前面
    def roll(self):
        self.index = random.choices(range(len(self.chance)), weights=self.chance)[0] + 1
        return self.index
    
class Player:
    def __init__(self, name):
        self.name = name
        self.dices = {i:Dice(i) for i in range(6)}
        self.score = 0
        self.turn_score = 0
    
    def new_turn(self):
        # 重置每个骰子的选中状态
        for dice in self.dices:
            self.dices[dice].selected = False
        self.turn_score = 0
    def reset(self):
        # 重置每个骰子的选中状态
        for dice in self.dices:
            self.dices[dice].selected = False
        self.score = 0
        self.turn_score = 0
    
    def check_live(self, rolled):
        # 检查被掷出的骰子是否满足条件
        if is_subset([1,2,3,4,5,6], rolled):
            return True
        elif is_subset([1,2,3,4,5], rolled):
            # 如果被掷出的骰子中有两个1或者两个5，则满足条件
            if rolled.count(1) == 2:
                return True
            elif rolled.count(5) == 2:
                return True
        elif is_subset([2,3,4,5,6], rolled):
            # 如果被掷出的骰子中有两个5，则满足条件
            if rolled.count(5) == 2:
                return True
        # 遍历1到6的数字，检查被掷出的骰子中是否有6个、5个、4个、3个、2个或者1个相同的数字
        for i in range(1,7):
            if rolled.count(i) == 6:
                return True
            elif rolled.count(i) == 5:
                return True
            elif rolled.count(i) == 4:
                return True
            elif rolled.count(i) == 3:
                return True
            elif rolled.count(i) == 2:
                # 如果有2个1或者2个5，则满足条件
                if i == 1 or i==5:
                    return True
            elif rolled.count(i) == 1:
                # 如果有1个1或者1个5，则满足条件
                if i == 1 or i==5:
                    return True
        # 如果以上条件都不满足，则返回False
        return False
    
    def calc_score(self, selected):
        # 计算选中骰子的分数
        selected.sort()
        if selected == []:
            return 0, False
        score = 0
        # 判断各种顺子
        if selected == [1,2,3,4,5,6]:
            return 1500, True
        elif selected ==[1,1,2,3,4,5]:
            return 600, True
        elif selected == [1,2,3,4,5,5]:
            return 550, True
        elif selected == [1,2,3,4,5]:
            return 500, True
        elif selected == [2,3,4,5,5,6]:
            return 800, True
        elif selected == [2,3,4,5,6]:
            return 750, True
        single_point = [0, 100, 20, 30, 40, 50, 60]
        for i in range(1,7):
            # 计算每个数字出现的次数
            if selected.count(i) == 6:
                # 如果某个数字出现6次，则分数为该数字的单点数乘以80
                score += 80 * single_point[i]
            elif selected.count(i) == 5:
                # 如果某个数字出现5次，则分数为该数字的单点数乘以40
                score += 40 * single_point[i]
            elif selected.count(i) == 4:
                # 如果某个数字出现4次，则分数为该数字的单点数乘以20
                score += 20 * single_point[i]
            elif selected.count(i) == 3:
                # 如果某个数字出现3次，则分数为该数字的单点数乘以10
                score += 10 * single_point[i]
            elif selected.count(i) == 2:
                # 如果某个数字出现2次，则分数为该数字的单点数乘以2，但只有1和5可以出现2次
                if i == 1 or i==5:
                    score += 2 * single_point[i]
                else:
                    return 0, False
            elif selected.count(i) == 1:
                # 如果某个数字出现1次，则分数为该数字的单点数，但只有1和5可以出现1次
                if i == 1 or i==5:
                    score += single_point[i]
                else:
                    return 0, False
        return score, True

class HumanPlayer(Player):
    # 初始化HumanPlayer类，继承自Player类
    def __init__(self, name):
        super().__init__(name)
    def roll(self):
        dices = {}
        index = []
        # 遍历self.dices中的每个骰子
        for dice in self.dices:
            # 如果骰子已经被选中，则跳过
            if self.dices[dice].selected:
                continue
            # 掷骰子
            self.dices[dice].roll()
            # 打印骰子的索引
            print(self.dices[dice].index, end=' ')
            # 将被掷出的骰子添加到rolled列表中
            dices[dice] = self.dices[dice].index
            index.append(self.dices[dice].index)
        # 打印换行符
        print()
        live = self.check_live(index)
        if not live:
            self.turn_score = 0
        # 返回被掷出的骰子和被掷出的骰子的索引
        return {
            'dices': dices,
            'live': live
        }
    # 选择要保留的点数
    def select(self,selected):
        index = []
        for id in selected:
            index.append(self.dices[id].index)
        score, valid = self.calc_score(index)
        if not valid:
            return {
                "turn_score": 0,
                "valid": False
            }
        self.turn_score += score
        for dice in selected:
            self.dices[dice].selected = True
        for dice in self.dices:
            if not self.dices[dice].selected:
                return {
                    "turn_score": score,
                    "valid": True,
                    "reset_all_dices":False
                }
        for dice in self.dices:
            self.dices[dice].selected = False
        return {
            "turn_score": score,
            "valid": True,
            "reset_all_dices":True
        }
    
                
class AIPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
    def roll(self):
        # 定义一个空列表，用于存储被掷出的骰子
        rolled = []
        # 定义一个空列表，用于存储被掷出的骰子的索引
        rolled_index = []
        # 遍历self.dices中的每个骰子
        for dice in self.dices:
            # 如果骰子已经被选中，则跳过
            if self.dices[dice].selected:
                continue
            # 掷骰子
            self.dices[dice].roll()
            # 打印骰子的索引
            print(self.dices[dice].index, end=' ')
            # 将被掷出的骰子添加到rolled列表中
            rolled.append(self.dices[dice])
            # 将被掷出的骰子的索引添加到rolled_index列表中
            rolled_index.append(self.dices[dice].index)
        # 打印换行符
        print()
        # 返回被掷出的骰子和被掷出的骰子的索引
        return rolled, rolled_index
    
    def select(self, rolled):
        index = []
        select = []
        for dice in rolled:
            index.append(dice.index)
        score = 0
        # 如果骰子值为1-6，则选择1-6
        if is_subset([1,2,3,4,5,6], index):
            select = [1,2,3,4,5,6]
        # 如果骰子值为1-5，则选择1-5
        elif is_subset([1,2,3,4,5], index):
            if index.count(1) == 2:
                select = [1,1,2,3,4,5]
            elif index.count(5) == 2:
                select = [1,2,3,4,5,5]
        # 如果骰子值为2-6，则选择2-6
        elif is_subset([2,3,4,5,6], index):
            if index.count(5) == 2:
                select = [2,3,4,5,5,6]
        # 如果以上条件都不满足，则根据骰子值数量进行选择
        if not select:
            counts = {}
    
            # 遍历骰子值列表，并更新字典
            for value in index:
                if value in counts:
                    counts[value] += 1
                else:
                    counts[value] = 1
            
            # 将字典转换为列表，并按值数量从高到低排序
            sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
            ret = []
            for key, value in sorted_counts:
                ret.append(key)
            for i in ret:
                # 如果某个值出现6次，则选择该值6次
                if index.count(i) == 6:
                    select = [i]*6
                    break
                # 如果某个值出现5次，则选择该值5次
                elif index.count(i) == 5:
                    select = [i]*5
                # 如果某个值出现4次，则选择该值4次
                elif index.count(i) == 4:
                    select = [i]*4
                # 如果某个值出现3次，则选择该值3次
                elif index.count(i) == 3:
                    select += [i]*3
                    if len(select)==6:
                        break
                # 如果某个值出现2次，则选择该值2次
                elif index.count(i) == 2:
                    if i == 1 or i==5:
                        if len(index)-len(select)<=3:
                            select += [i]*2
                            if len(select) == len(index):
                                break
                # 如果某个值出现1次，则选择该值1次
                elif index.count(i) == 1:
                    if i == 1 or i==5:
                        if len(index)-len(select)<=2:
                            select.append(i)
                            if len(select) == len(index):
                                break
        # 如果以上条件都不满足，则选择1或5
        if select == []:
            if 1 in index:
                select = [1]
            elif 5 in index:
                select = [5]
        select_dices = select.copy()
        # 计算选择的骰子值得分
        score, _ = self.calc_score(select)
        print("select:", select, "score:", score)
        remain = len(rolled) - len(select)
        # 将选择的骰子值标记为已选择
        for dice in rolled:
            if dice.index in select:
                dice.selected = True
                select.remove(dice.index)
        return score, remain, select_dices
    
    def play(self):
        turn_data = {}
        turn_data["process"] = []
        # 重置游戏
        self.new_turn()
        # 打印当前玩家
        # 初始化当前回合得分
        turn_score = 0
        while True:
            data = {}
            remain = False
            # 检查是否有未选择的骰子
            for dice in self.dices:
                if not self.dices[dice].selected:
                    remain = True
                    break
            # 如果没有未选择的骰子，则将所有骰子标记为未选择
            if not remain:
                for dice in self.dices:
                    self.dices[dice].selected = False
            # 掷骰子
            rolled, rolled_index = self.roll()
            data["roll"] = rolled_index
            # 检查骰子是否可以继续选择
            if self.check_live(rolled_index):
                # 选择骰子
                score, remain, select_dices = self.select(rolled)
                data["select"] = select_dices
                data["select_score"] = score
                # 累加当前回合得分
                turn_score += score
                data["turn_score"] = turn_score
                # 打印当前回合得分和总得分
                print("score:", score, "total", turn_score)
                turn_data["process"].append(data)
                # 如果剩余骰子数量小于等于2，则结束当前回合
                if remain <= 2 and remain > 0:
                    break
            else:
                # 如果骰子不能继续选择，则当前回合得分置为0，并结束当前回合
                turn_score = 0
                data["select_score"] = 0
                data["turn_score"] = turn_score
                data["select"] = []
                turn_data["process"].append(data)
                break
        # 累加总得分
        self.score += turn_score
        turn_data["score"] = self.score
        turn_data["turn_score"] = turn_score
        return turn_data
    
class Game:
    # 初始化游戏，传入两个玩家
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
    
    def player_roll(self):
        ret = self.player1.roll()
        if not ret["live"]:
            self.player1.new_turn()
            ret["opponent_turn"] = self.player2.play()
            if self.player2.score >= 1500:
                ret["result"] = "Lose"
                self.player1.reset()
                self.player2.reset()
        return ret
    
    def player_select(self, selected):
        ret = self.player1.select(selected)
        return ret
    
    def player_select_stop(self, selected):
        ret = self.player1.select(selected)
        if ret["valid"]:
            self.player1.score += self.player1.turn_score
            if self.player1.score >= 1500:
                ret["result"] = "Win"
                ret["score"] = self.player1.score
                self.player1.reset()
                self.player2.reset()
        ret["score"] = self.player1.score
        self.player1.new_turn()
        ret["opponent_turn"] = self.player2.play()
        if self.player2.score >= 1500:
            ret["result"] = "Lose"
            self.player1.reset()
            self.player2.reset()
        return ret
