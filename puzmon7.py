#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 21:47:35 2021

@author: yuki
"""

#モジュールのインポート
import sys
from enum import Enum
import random

#列挙型宣言
#(a)属性
class Element(Enum):
    FIRE=0
    WATER=1
    WIND=2
    EARTH=3
    LIFE=4
    EMPTY=5
    
#(b)属性別の記号
ELEMENT_SYMBOLS=('$','~','@','#','&',' ')


#(c)属性別のカラーコード 
ELEMENT_COLORS=('1','6','2','3','5','0')


#(d)バトルフィールドに並ぶ宝石の数
MAX_GEMS = 14

#構造体宣言
#(f)モンスター
class Monster:
    def __init__(self,name,element,maxhp,hp,attack,defense):
        self.name=name
        self.element=element
        self.maxhp=maxhp
        self.hp=hp
        self.attack=attack
        self.defense=defense
        
        
#(g)ダンジョン
class Dungeon:
    def __init__(self,monsters,numMonsters):
        self.monsters=monsters
        self.numMonsters=numMonsters
        
        
#(h)パーティ
class Party:
    def __init__(self,playerName,monsters,numMonsters,maxHp,hp,defense):
        self.playerName=playerName
        self.monsters=monsters
        self.numMonsters=numMonsters
        self.maxHp=maxHp
        self.hp=hp
        self.defense=defense
        
        
#(i)バトルフィールド
class BattleField:
    def __init__(self,pParty,pEnemy,gems):
        self.pParty=pParty
        self.pEnemy=pEnemy
        self.gems=gems


#(j)連続配置宝石の位置情報
class BanishInfo:
    def __init__(self,pos,leng,element):
        self.pos=pos
        self.leng=leng
        self.element=element

#プロトタイプ宣言的な
def main():
    goDungeon()
    doBattle()
    organizeParty()
    showParty()
    onPlayerTurn()
    doAttack()
    onEnemyTurn()
    doEnemyTurn()
    showBattleField()
    checkValidCommand()
    evaluateGems()
    checkBanishable()
    vanishGems()
    spawnGems()
    
    #ユーティリティ
    printMonsterName()
    fillGems()
    printGems()
    printGem()
    moveGem()
    swapGem()
    countGems()


#(2)ダンジョン開始から終了までの流れ
def goDungeon(pParty,pDungeon):
    print("{}のパーティ（HP={}）はダンジョンに到着した".format(pParty.playerName,pParty.hp))
    showParty(pParty)
    
    #そのダンジョンでバトルを繰り返す
    winCount=0
    for i in range(pDungeon.numMonsters):
        winCount+=doBattle(pParty,pDungeon.monsters[i])
        if(pParty.hp<=0):
            print("{}はダンジョンから逃げ出した...".format(pParty.playerName))
            break
        else:
            print("{}はさらに奥へと進んだ\n".format(pParty.playerName))
            print("================\n")
        
    print("{}はダンジョンを制覇した".format(pParty.playerName))
    return winCount



#(3)バトル開始から終了までの流れ
def doBattle(pParty,pEnemy):
    printMonsterName(pEnemy)
    print("が現れた！")
    
    #バトルフィールドの宝石スロットの準備と初期化
    gems=[0 for i in range(MAX_GEMS)]
    field = BattleField(pParty,pEnemy,gems)
    fillGems(field.gems,False)
    
    while(True):
        onPlayerTurn(field)
        if pEnemy.hp<0:
            printMonsterName(pEnemy)
            print("を倒した!")
            return 1
        onEnemyTurn(field)
        if pParty.hp<=0:
            print("{}は倒れた...".format(pParty.playerName))
            return 0

#(4)パーティ編成処理
def organizeParty(playerName,monsters,numMonsters):
    sumHp=0
    sumDefense=0
    for i in range(numMonsters):
        sumHp+=monsters[i].hp
        sumDefense+=monsters[i].defense
        
    avgDefense=sumDefense/numMonsters
    
    p = Party(playerName,monsters,numMonsters,sumHp,sumHp,avgDefense)
    return p


#(5)パーティ情報の表示
def showParty(pParty):
    print("＜パーティ編成＞----------")
    for i in range(pParty.numMonsters):
        printMonsterName(pParty.monsters[i])
        print("  HP={:4d} 攻撃={:3d} 防御={:3d}".format(pParty.monsters[i].hp,pParty.monsters[i].attack,pParty.monsters[i].defense))
    print("------------------------\n")

#(6)プレイヤーターン
def onPlayerTurn(pField):
    print("\n 【{}のターン】 \n".format(pField.pParty.playerName))
    showBattleField(pField)
    
    command="  "
    while checkValidCommand(command)==False:
        print("コマンド？>",end=' ')
        command=input()
    
    moveGem(pField.gems,ord(command[0])-ord('A'),ord(command[1])-ord('A'),True)
    evaluateGems(pField)


#(7)パーティの攻撃
def doAttack(pField):
    pField.pEnemy.hp -= 80
    print("ダミー攻撃で80のダメージを与えた")
    
#(8)敵モンスターターン
def onEnemyTurn(pField):
    print("\n 【{}のターン】 \n".format(pField.pEnemy.name))
    doEnemyAttack(pField)
    
#(9)敵モンスターの攻撃
def doEnemyAttack(pField):
    pField.pParty.hp-=20
    print("20のダメージを受けた")
    
#(10)バトルフィールド情報の表示
def showBattleField(pField):
    print("------------------------------\n")
    print("          ")
    printMonsterName(pField.pEnemy)
    print("\n       HP= {:4d} / {:4d}\n".format(pField.pEnemy.hp,pField.pEnemy.maxhp))
    print("\n")
    for i in range(pField.pParty.numMonsters):
        printMonsterName(pField.pParty.monsters[i])
        #print("  ")
    print("\n")
    print("\n       HP= {:4d} / {:4d}\n".format(pField.pParty.hp,pField.pParty.maxHp))
    print("------------------------------")
    print("  ")
    for i in range(MAX_GEMS):
        print("{} ".format(chr(65+i)),end=' ')
    print("\n")
    printGems(pField.gems)
    print("------------------------------")
    
    
#(11)入力コマンドの正当性判定
def checkValidCommand(c):
    if(len(c)!=2):
        return False
    if(c[0]==c[1]):
        return False
    if(ord(c[0])<ord('A') or ord(c[0])>ord('A')+MAX_GEMS-1):
        return False
    if(ord(c[1])<ord('A') or ord(c[1])>ord('A')+MAX_GEMS-1):
        return False
    
    return True

#(12)宝石スロットを評価解決する
def evaluateGems(pField):
    bi = checkBanishable(pField.gems)
    if bi.leng!=0:
        banishGems(pField,bi)
        shiftGems(pField.gems)
        spawnGems(pField.gems)
        
        
#(13)宝石の消滅可能箇所判定
def checkBanishable(gems):
    BANISH_GEMS=3
    
    for i in range(MAX_GEMS-BANISH_GEMS+1):
        targetGem=Element(gems[i])
        leng=1
        if targetGem==Element.EMPTY.value:
            continue
        for j in range(i+1,MAX_GEMS):
            if gems[i] == gems[j]:
                leng+=1
            else:
                break
        if (leng>=BANISH_GEMS):
            found = BanishInfo(i,leng,targetGem)
            return found
        
        
    notfound = BanishInfo(0,0,Element.EMPTY.value)
    return notfound

#(14)指定箇所の宝石を消滅させ効果発動
def banishGems(pField,bi):
    
    for i in range(bi.pos,bi.pos+bi.leng):
        pField.gems[i] = Element.EMPTY.value
        
    printGems(pField.gems)
    
    doAttack(pField)
    
#(15)空いている部分を左詰めしていく
def shiftGems(gems):
    
    numEmpty = countGems(gems,Element.EMPTY.value)
    
    for i in range(MAX_GEMS-numEmpty):
        if gems[i]==Element.EMPTY.value:
            moveGem(gems,i,MAX_GEMS-1,False)
            i-=1
            
    printGems(gems)
    
    
    
#(16)空き領域に宝石が沸く
def spawnGems(gems):
    fillGems(gems,True)
    printGems(gems)
    
    
#(A)モンスター名のカラー表示
def printMonsterName(pMonster):
    symbol=ELEMENT_SYMBOLS[pMonster.element]
    print('\033[3'+ELEMENT_COLORS[pMonster.element]+'m'+symbol+pMonster.name+symbol+'\033[0m',end=' ')



#(B)スロットをランダムな宝石で埋める
def fillGems(gems,emptyOnly):
    for i in range(MAX_GEMS):
        if not(emptyOnly) or gems[i]==Element.EMPTY.value:
            gems[i] = random.randint(0, Element.EMPTY.value-1)
            
            
#(C)スロットに並ぶ宝石を表示する
def printGems(gems):
    for i in range(MAX_GEMS):
        printGem(gems[i])
    print("\n")
    

#(D)1個の宝石の表示
def printGem(e):
    symbol=ELEMENT_SYMBOLS[e]
    print('\033[4'+ELEMENT_COLORS[e]+'m'+symbol+'\033[0m'+' ',end=' ')
    

#(E)指定の宝石を指定の位置まで１つずつ移動させる
def moveGem(gems,fromPos,toPos,printProcess):
    
    step = 1 if toPos>fromPos else -1
    
    printGems(gems)
    
    int_i = fromPos
    while(int_i != toPos):
        swapGem(gems,int_i,step)
        if printProcess:
            printGems(gems)
        int_i+=step


#(F)pos番目の宝石を、step個隣の宝石と交換する
def swapGem(gems,pos,step):
    
    buf = gems[pos]
    gems[pos] = gems[pos+step]
    gems[pos+step] = buf


#(G)指定種類の宝石カウント
def countGems(gems,target):
    
    num=0
    for i in range(MAX_GEMS):
        if gems[i] == target:
            num+=1
            
    return num


if __name__ == "__main__":
    #args=sys.argv
    args=["0","ミサキ"] #仮
    if(len(args) != 2):
        print("エラー：プレイヤー名を指定して起動してください")
        sys.exit() #強制終了
        
    print("*** Puzzle & Monsters ***")
    
    #パーティの準備
    partyMonsters=[Monster("朱雀",Element.FIRE.value,150,150,25,10),
                                  Monster("青龍",Element.WIND.value,150,150,15,10),
                                  Monster("白虎",Element.EARTH.value,150,150,20,5),
                                  Monster("玄武",Element.WATER.value,150,150,20,15)]
    
    party=organizeParty(args[1],partyMonsters,len(partyMonsters))
    
    
    #ダンジョンの準備
    dungeonMonsters=[Monster("スライム",Element.WATER.value,100,100,10,5),
                                        Monster("ゴブリン",Element.EARTH.value,200,200,20,15),
                                        Monster("オオコウモリ",Element.WIND.value,300,300,30,25),
                                        Monster("ウェアウルフ",Element.WIND.value,400,400,40,30),
                                        Monster("ドラゴン",Element.FIRE.value,800,800,50,40)]
    dungeon=Dungeon(dungeonMonsters,len(dungeonMonsters))
    
    #いざ、ダンジョンへ
    winCount = goDungeon(party,dungeon)
    
    #冒険終了後
    if winCount == dungeon.numMonsters:
        print("***GAME CLEAR!***")
    else:
        print("***GAME OVER***")
        
    print("倒したモンスター数＝{}".format(winCount))



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        