#coding:utf8
import sys

dizhu = ['9','9','9','11','11','53','54']
nongmin = ['3','3','3','3','4','5','6','7','10','10','14','14','14','14']

#dizhu = ['9','9','9']
#nongmin = ['3','3','3','3']


def validate(cards,outcards):
    cards_count = {}
    outcards_count = {}
    for card in cards:
        if card in cards_count:
            cards_count[card]+=1
        else:
            cards_count[card]=1
    for outcard in outcards:
        if outcard in outcards_count:
            outcards_count[outcard]+=1
        else:
            outcards_count[outcard]=1
    for outcard in outcards_count:
        if outcards_count[outcard] > cards_count[outcard]:
            return False
    return True
def candidate(cards):
    one_card = {}
    two_cards = {}
    three_cards = {}
    zhadan_cards = {}
    sandaiyi_cards = {}
    five_cards = {}
    sidaier_cards = {}
    wangzha_cards = {}
    list.sort(cards)
    #one card
    for i in range(0,len(cards)):
        #单牌
        one_card[cards[i]] = 1
#    for card in one_card.keys():
#        print card
#    print '------------------'
    #two cards
    for i in range(0,len(cards)-1):
        a = cards[i]
        b = cards[i+1]
        #一对
        if a==b :
            two_cards["%s %s" % (a ,b)] = 1
        #王炸，作为4张牌处理
        if a=='53'and b=='54':
            wangzha_cards["%s %s" % (a ,b)] = 1
 #   for card in two_cards.keys():
 #       print card
 #   print '------------------'
    #three cards
    for i in range(0,len(cards)-2):
        a = cards[i]
        b = cards[i+1]
        c = cards[i+2]
        #三张相同牌
        if a==b and b==c:
            three_cards["%s %s %s" % (a ,b,c)] = 1
 #   for card in three_cards.keys():
 #       print card
 #   print '------------------'
    #four cards
    for i in range(0,len(cards)-3):
        a = cards[i]
        b = cards[i+1]
        c = cards[i+2]
        d = cards[i+3]
        #炸弹
        if a==b and b==c and c==d:
            zhadan_cards["%s %s %s %s" % (a ,b,c,d)] = 1
        #三带一
        for i in three_cards:
            for j in one_card:
                if j in i:
                    continue
                temp = "%s %s" % (i,j)
                val = validate(cards,temp.split(" "))
                if val:
                    sandaiyi_cards[temp] = 1
 #   for card in zhadan_cards.keys():
 #       print card
 #   print '------------------'
 #   for card in sandaiyi_cards.keys():
 #       print card
 #   print '------------------'
    #five cards
    for i in range(0,len(cards)-4):
        a = int(cards[i])
        b = int(cards[i+1])
        c = int(cards[i+2])
        d = int(cards[i+3])
        e = int(cards[i+4])
        #顺子
        if a+1==b and b+1==c and c+1==d and d+1==e:
            five_cards["%s %s %s %s %s" % (a ,b,c,d,e)] = 1
 #   for card in five_cards.keys():
 #       print card
 #   print '------------------'
    #six cards
    for i in range(0,len(cards)-5):
        #四带二
        for i in zhadan_cards:
            if i  == '53 54':
                continue
            for j in two_cards:
                temp = "%s %s" % (i,j)
                val = validate(cards,temp.split(" "))
                if val:
                    sidaier_cards[temp] = 1
 #   for card in sidaier_cards.keys():
 #       print card

    combine = {'one':one_card.keys(),'two':two_cards.keys(),'three':three_cards.keys(),'sandaiyi':sandaiyi_cards.keys(),'zhadan':zhadan_cards.keys(),'five':five_cards.keys(),'sidaier':sidaier_cards.keys()}
    return combine

def cards_out(cards,out_cards,new_cards):
    for card in cards:
        if card in out_cards:
            out_cards.remove(card)
        else:
            new_cards.append(card)

def compare(last_out,new_out):
    last_type = judge_type(last_out)
    new_type = judge_type(new_out)
    if new_type == "wangzha":
        return True
    if new_type == "zhadan":
        if last_type == "wangzha":
            return False
        else:
            if int(new_out[0])>int(last_out[0]):
                return True
    if new_type == "sandaiyi":
        if last_type=="sandaiyi":
            if int(new_out[0])>int(last_out[0]):
                return True
        else:
            return False
    if new_type == "three":
        if last_type=="three":
            if int(new_out[0])>int(last_out[0]):
                return True
        else:
            return False
    if new_type == "two":
        if last_type=="two":
            if int(new_out[0])>int(last_out[0]):
                return True
        else:
            return False
    if new_type == "one":
        if last_type=="one":
            if int(new_out[0])>int(last_out[0]):
                return True
        else:
            return False

    return False

def solve(a,b,a_name,b_name,last_out,history):
    #print a
    #print b
    #print last_out
    if len(a)==0 or len(b)==0:
        winner = ""
        if len(a)==0:
            #print "%s win" % (a_name)
            winner = a_name
        else:
            #print "%s win" % (b_name)
            winner = b_name
        if winner == "nongmin":
            print history
        #print history
        return True
    #如果没有出牌，先手出牌
    if len(last_out) == 0:
        cand_a = candidate(a)
        for type in cand_a.keys():
            for out_cards in cand_a[type]:
                new_cards = []
                cards_out(a,str(out_cards).split(" "),new_cards)
                new_history = history + "%s:%s\t" % (a_name,out_cards)
                solve(b,new_cards,b_name,a_name,str(out_cards).split(" "),new_history)
    #如果已经出牌，比大小进行新一轮出牌
    else:
        #print "bidaxiao"
        is_bigger = False
        cand_a = candidate(a)
        for type in cand_a.keys():
            for out_cards in cand_a[type]:
                if compare(last_out,str(out_cards).split(" ")):
                    is_bigger = True
                    new_cards = []
                    cards_out(a,str(out_cards).split(" "),new_cards)
                    new_history = history + "%s:%s\t" % (a_name,out_cards)
                    solve(b,new_cards,b_name,a_name,str(out_cards).split(" "),new_history)
                else:
                    continue
        #如果所有手牌都没有对方大，换对方出
        if not is_bigger:
            solve(b,a,b_name,a_name,[],history)


def judge_type(cards):
    c_num = len(cards)
    if c_num == 1:
        return "one"
    if c_num == 2:
        return "two"
    if c_num == 3:
        return "three"
    if c_num == 4:
        if cards[0]==cards[1] and cards[1]==cards[2] and cards[2]==cards[3]:
            return "zhadan"
        else:
            return "sandaiyi"
    if c_num == 5:
        return "five"
    if c_num == 6:
        return "sidaier"
    if cards[0]=="53" and cards[1]=="54":
        return "wangzha"

if __name__ == '__main__':
    print "start"
    solve(nongmin,dizhu,"nongmin","dizhu",[],"")





