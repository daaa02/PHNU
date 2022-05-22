from distutils.command.clean import clean
from konlpy.tag import Komoran

komoran = Komoran()

class Dictionary():
    def __init__(self):
        
        self.Yes = ['네', '예', '응', '어', '맞아요', '맞아', '그래', '그렇습니다', '맞습니다', '맞어']

        self.No = ['아니', '아니오', '아니요', '안', '아뇨', '아닌', '아닙니다', '아냐', '아닐', '별로', 
                   '글쎄', '그다지', '딱히', '없습니다', '없어', '없네', '없는', '없다', '없고', '없음', '없으예', '없소']
        
        self.IDK = ["모르", "몰라", "모름", "모릅", "몰라요", "모릅니다", "모르겠어요", "기억이 안", "가물가물"]
        
        self.Number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']

        self.Number_Word = ['영', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구', '십', '십일']

class NLP():
    def __init__(self):
        self.komoran = Komoran()
        self.temp = {}
        
        
    def nlp_answer(self, user_said, dic):
        answer = ''
        for i in range(len(dic.Yes)):
            if dic.Yes[i] in user_said:
                answer = '네'
        for j in range(len(dic.No)):
            if dic.No[j] in user_said:
                answer = '아니오'
        for k in range(len(dic.IDK)):
            if dic.IDK[k] in user_said:
                answer = '모름'
        print(answer)
        return answer    
    
    
    def nlp_number(self, user_said, dic):
        number = -1
        ko = -1
        nb = -1
        for i, j in enumerate(dic.Number_Word):
            x = user_said.find(j)
            if x != -1:
                ko = i
        for i, j in enumerate(dic.Number):
            x = user_said.find(j)
            if x != -1:
                nb = i
        number = max(ko, nb)
        return number
    
    
    def nlp_medicine(self, sentence):
        answer = []
        clean = []        
        stopwords = ['이랑']
        nouns = komoran.nouns(sentence) 
        for i in range(len(nouns)):
            if nouns[i] not in stopwords:
                clean.append(nouns[i] + "약")
                # print(f"clean = {clean}")   # 나 진짜 천잰가                
            answer = clean         
        print(answer)
        return answer

    def nlp_komoran(self, sentence):
        answer = []
        clean = []
        stopwods = ['이랑']
        nouns = komoran.nouns(sentence)
        for i in range(len(nouns)):
            if nouns[i] not in stopwods:
                clean.append(nouns[i])
            answer = clean
        print(answer)
        return answer