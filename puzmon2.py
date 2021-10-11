#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 21:10:08 2021

@author: yuki
"""

#モジュールのインポート
import sys
from enum import Enum

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
        

#プロトタイプ宣言的な
def main():
    goDungeon()
    doBattle()
    printMonsterName()


def goDungeon(playerName,pDungeon):
    print(playerName+"はダンジョンに到着した")
    
    #そのダンジョンでバトルを繰り返す
    winCount=0
    for i in range(pDungeon[1]):
        winCount+=doBattle(playerName,pDungeon[0][i])
        
    print(playerName+"はダンジョンを制覇した")
    return winCount

def doBattle(playerName,pEnemy):
    printMonsterName(pEnemy)
    print("が現れた！")
    printMonsterName(pEnemy)
    print("を倒した！")
    return 1

def printMonsterName(pMonster):
    symbol=ELEMENT_SYMBOLS[pMonster.element]
    print('\033[3'+ELEMENT_COLORS[pMonster.element]+'m'+symbol+pMonster.name+symbol+'\033[0m',end=' ')





if __name__ == "__main__":
    #args=sys.argv
    args=["0","ミサキ"] #仮
    if(len(args) != 2):
        print("エラー：プレイヤー名を指定して起動してください")
        sys.exit() #強制終了
        
    print("*** Puzzle & Monsters ***")
    
    #ダンジョンの準備
    dungeonMonsters=[Monster("スライム",Element.WATER.value,100,100,10,5),
                                        Monster("ゴブリン",Element.EARTH.value,200,200,20,15),
                                        Monster("オオコウモリ",Element.WIND.value,300,300,30,25),
                                        Monster("ウェアウルフ",Element.WIND.value,400,400,40,30),
                                        Monster("ドラゴン",Element.FIRE.value,800,800,50,40)]
    dungeon=[dungeonMonsters,len(dungeonMonsters)]
    
    winCount = goDungeon(args[1],dungeon)