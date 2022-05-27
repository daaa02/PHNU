from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# python module
import os
import sys
import time
import json
import csv

# my module
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from question_list import question_list
from connect import Connection
from NLP import NLP, Dictionary
# from speech_to_text import speech_to_text

connect = Connection()
nlp = NLP()
dic = Dictionary()
QL = question_list

# 0. Greeting: 문진 시작
def Greeting():
    print("\n")
    print(QL['Greeting'][0])
    user_said = input("답변: ")
    
    user_said = nlp.nlp_answer(user_said, dic)
    print(f"답변: {user_said}")
    
    if user_said == "네":
        return Symptoms()
    else:
        print("\nwait ...")
        return Greeting()
    
    
# 1. Symptoms: 통증 위치/강도/양상
def Symptoms():        
    while True:
        print("\n")
        print(QL['Symptoms'][0])
        user_said = input("답변: ")    
         
        user_said = nlp.nlp_answer(user_said, dic)
        print(f"답변: {user_said}")
        
        if user_said == "네":
            print("\n")
            print(QL['Symptoms'][3])
            user_said = input("답변: ")                       
            
            pain_point = []                                                 # 리스트 생성      
            position = []      
            nlp.watson_position(user_said=user_said, list_name=pain_point)  # watson intent 분석
            # position.append(nlp.nlp_komoran(user_said))
            print(f"통증 부위: {pain_point} ")                  # 분석 결과 
            
            print("\n")
            print(QL['Symptoms'][4])    # 다음 아픈 부위는 ~
            user_said = input("답변: ") 
            
            nlp.watson_position(user_said=user_said, list_name=pain_point)
            print(f"통증 부위: {pain_point}")
            
            while True:            
                if user_said == "없다":                    
                    break
                else:
                    user_said = input("답변: ")
                    
                    nlp.watson_position(user_said=user_said, list_name=pain_point)
                    print(f"통증 부위: {pain_point}")                    
                    continue
                break  
            
            print("\n")
            print(QL['Symptoms'][5] + pain_point[0] + QL['Symptoms'][7])   # 이제 얼마나 아픈지 ~
            user_said = input("답변: ")
                              
            severity = nlp.nlp_number(user_said, dic)    
            print(f"통증 강도: {severity}")
            
            print("\n")
            print(QL['Symptoms'][8])    # 이 부위가 어떻게 ~
            user_said = input("답변: ") 
            
            symptoms = []
            nlp.watson(user_said=user_said, list_name=symptoms)
            print(f"통증 양상: {symptoms}")
              
            n = len(pain_point)
            for i in range(0, n-1):   # 통증 개수만큼 반복 (n = '없다')  
                print("\n")
                print(QL['Symptoms'][6] + pain_point[i] + QL['Symptoms'][7]) 
                user_said = input("답변: ") 
                
                user_said = nlp.nlp_number(user_said, dic)    
                print(f"통증 강도: {user_said}")
                
                print("\n")
                print(QL['Symptoms'][8])
                user_said = input("답변: ") 
                
                nlp.watson(user_said=user_said, list_name=symptoms)
                print(f"통증 양상: {symptoms}")
                
                i = i + 1      
            
            print("\n")    
            print(QL['Symptoms'][9])
            user_said = input("답변: ")
            
            symptoms_other = []
            nlp.watson(user_said=user_said, list_name=symptoms_other)
            print(f"통증 양상: {symptoms_other}")    
            
            while True:            
                if user_said == "아니오":   # 없다
                    break
                else:
                    user_said = input("답변: ")
                    
                    nlp.watson(user_said=user_said, list_name=symptoms_other)
                    print(f"통증 양상: {symptoms_other}")
                    continue
                break                 
            break      
        
        elif user_said == "아니오":
            print("\n")
            print(QL['Symptoms'][1])    # 아프지 않으시다면 ~
            user_said = input("답변: ")        
            
            symptoms = []
            nlp.watson(user_said=user_said, list_name=symptoms)
            print(f"증상: {symptoms}")
            
            print("\n")
            print(QL['Symptoms'][2])    # 또 다른 증상이~
            user_said = input("답변: ")
            
            user_said = nlp.watson(user_said=user_said, list_name=symptoms)
            
            while True:            
                if user_said == "없다":                    
                    break
                else:
                    user_said = input("답변: ") 
                    
                    nlp.watson(user_said=user_said, list_name=symptoms)
                    print(f"증상: {symptoms}")
                    continue
                break     
        
        else:
            print("\n다시 말씀해 주세요.")
            return Symptoms()        
        break    
    
    return Occurrence()   
 
 
# 2. Occurrence: 통증 발생 시기(년/월/일)            
def Occurrence():
    print("\n")
    print(QL['Occurrence'][0])
    user_said = input("답변: ")
    user_input = nlp.nlp_answer(user_said, dic)
    
    if user_input == "모름":
        print(QL['Occurrence'][1])
        user_said = input("답변: ")

        tmp = []    
        nlp.watson_time(user_said=user_said, list_name=tmp)
 
                               
        while True:
            if len(tmp) != 0:
                # tmp.sort(key=lambda x: x[1], reverse=True)
                occurrence = tmp
                print(f"통증 발생 시점: {occurrence} 전")
                break            
            else:
                print("\n다시 말씀해 주세요.")
                user_said = input("답변: ")
                
                nlp.watson_time(user_said=user_said, list_name=tmp)  
                continue              
            break
            
    elif user_input != "모름":             
        tmp = []
        nlp.watson_time(user_said=user_said, list_name=tmp)
        
        while True:        
            if len(tmp) != 0:                  
                # tmp.sort(key=lambda x: x[1], reverse=False)
                occurrence = tmp
                print(f"통증 발생 시기: {occurrence}")      
                break
            
            else:
                print("\n다시 말씀해 주세요.")
                user_said = input("답변: ")
                
                nlp.watson_time(user_said=user_said, list_name=tmp)  
                print(f"통증 발생 시기: {tmp}")
                
                continue              
            break            
    
    else:
        print("다시 말씀해 주세요.")
        return Occurrence()        

    return Cause()
    
    
# 3. Cause: 증상 발생 원인    
def Cause():  
    print("\n")  
    print(QL['Cause'][0])
    user_said = input("답변: ")
    print(f"사고와 관련 여부: {user_said}")
    
    if user_said == "네":
        print("\n")
        print(QL['Cause'][1])
        user_said = input("답변: ")
        
        accident = []
        nlp.watson(user_said=user_said, list_name=accident)
        print(f"사고 유형: {accident}")
        
        if accident == "교통사고":
            print("\n")
            print(QL['Cause'][2])
            user_said = input("답변: ")
            
            user_said = nlp.nlp_answer(user_said, dic)
            print(f"답변: {user_said}")
        
            if user_said == "아니오":
                print("\n")
                print(QL['Cause'][3])
                user_said = input("답변: ")
                user_said = nlp.nlp_answer(user_said, dic)

        elif accident == "넘어짐":
            print("\n")
            print(QL['Cause'][4])
            user_said = input("답변: ")
            
            user_said = nlp.nlp_komoran(sentence=user_said)
            print(f"낙상 장소: {user_said}")
            
        elif accident == "떨어짐":
            print("\n")
            print(QL['Cause'][5])
            user_said = input("답변: ")
            
            user_said = nlp.nlp_number(user_said, dic)            
            print(f"추락 높이: {user_said}")
            
        elif accident == "구름":
            print("\n")
            print(QL['Cause'][6])
            user_said = input("답변: ")
            
            user_said = nlp.nlp_number(user_said, dic) 
            print(f"구른 정도: {user_said}")
            
        elif accident == "폭행":
            pass
        
        print("\n")
        print(QL['Cause'][7])
        user_said = input("답변: ")
        
        user_said = nlp.nlp_answer(user_said, dic)
        print(f"산재 처리: {user_said}")

    elif user_said == "아니오":
        pass

    else:
        print("다시 말씀해 주세요.")
        return Cause() 
    
    return CheckUp()


# 4. CheckUp: 검사 이력
def CheckUp():
    print("\n")
    print(QL['CheckUp'][0])
    user_said = input("답변: ")
    print(f"검사 이력: {user_said}")
    
    if user_said == "네":
        print("\n")
        print(QL['CheckUp'][1])
        user_said = input("답변: ")
        
        user_said = nlp.nlp_answer(user_said, dic)
        print(f"검사 종류 아는지: {user_said}")
        
        while True:
            if user_said == "네":
                print("\n")
                print(QL['CheckUp'][2])
                user_said = input("답변: ")
                
                checkup = nlp.nlp_komoran(user_said)
                print(f"검사 종류: {checkup}")
                break                
            elif user_said == "아니오":
                break            
            else: 
                print("다시 말씀해 주세요.")
                continue            
            break

    elif user_said == "아니오":
        pass
    
    else:
        print("다시 말씀해 주세요.")
        return CheckUp()
        
    return Treatment()


# 5. Treatment: 치료 여부 
def Treatment():
    print("\n")
    print(QL['Treatment'][0])
    user_said = input("답변: ")
    
    user_said = nlp.nlp_answer(user_said, dic)
    print(f"치료 이력: {user_said}")
    
    if user_said == "네":
        print("\n")
        print(QL['Treatment'][1])
        user_said = input("답변: ")
        
        user_said = nlp.nlp_answer(user_said, dic)
        print(f"치료 종류 아는지: {user_said}")
        
        while True:
            if user_said == "네":
                print("\n")
                print(QL['Treatment'][2])
                user_said = input("답변: ")
                
                treatment = nlp.nlp_komoran(user_said)   
                print(f"치료 종류: {treatment}")             
                break
            elif user_said == "아니오":
                break            
            else: 
                print("다시 말씀해 주세요.")
                continue
            break
        
    elif user_said == "아니오":
        pass
    
    else:
        print("다시 말씀해 주세요.")
        return Treatment()
    
    return Medicine()


# 6. Medicine: 복용중인 약
def Medicine():
    print("\n")
    print(QL['Medicine'][0])    # 현재 드시고 있는 ~
    user_said = input("답변: ")
    
    user_said = nlp.nlp_answer(user_said, dic)
    print(f"복용 여부: {user_said}")
    
    if user_said == "네":
        print("\n")
        print(QL['Medicine'][1])    # 지혈을 억제하는 ~
        user_said = input("답변: ")
        
        user_said = nlp.nlp_answer(user_said, dic)
        print(f"항응고제 복용 여부: {user_said}")
        
    elif user_said == "아니오":
        pass
    
    else:
        print("다시 말씀해 주세요.")
        return Medicine()
    
    print("\n")
    print(QL['Medicine'][2])    # 그 외에 드시고 있는 ~
    user_said = input("답변: ")
    
    medicine = nlp.nlp_medicine(user_said)
    print(f"복용 중인 약: {medicine}")
    
    return Anamnesis()


# 7. Anamnesis: 과거 병력
def Anamnesis():
    print("\n")
    print(QL['Anamnesis'][0])
    user_said = input("답변: ")
    
    anamnesis = nlp.nlp_komoran(user_said)
    print(f"과거 병력: {anamnesis}")
    
    return Surgery()    


# 8. Surgery: 수술 이력
def Surgery():
    print("\n")
    print(QL['Surgery'][0])     # 예전에 수술이나 ~
    user_said = input("답변: ")
    
    user_said = nlp.nlp_answer(user_said, dic)
    
    if user_said == "네":
        print("\n")
        print(QL['Surgery'][1])     # 가장 최근에 수술 ~
        user_said = input("답변: ")
        
        surgery_point = []
        nlp.watson_position(user_said=user_said, list_name=surgery_point)
        print(f"수술 부위: {surgery_point}")
        
        print("\n")
        print(QL['Surgery'][2])    # 그 다음 수술 ~
        user_said = input("답변: ")
        
        nlp.watson_position(user_said=user_said, list_name=surgery_point)
        print(f"수술 부위: {surgery_point}")
        
        while True:            
            if user_said == "없다":                    
                break
            else:
                user_said = input("답변: ")
                nlp.nlp.watson(user_said=user_said, list_name=surgery_point)
                print(f"수술 부위: {surgery_point}")
                continue
            break         
        
    elif user_said == "아니오":
        pass
        
    else:
        print("다시 말씀해 주세요.")
        return Surgery()
    
    return End()

def End():
    print("문진이 종료되었습니다.")
    sys.exit(0)


if __name__ == "__main__":
    print(connect.assistant_connect)
    Greeting()
