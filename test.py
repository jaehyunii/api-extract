import pefile
import pandas as pd
import os

a=[] #csv파일을 만들기 위한 dataFrame형식 위해 빈 배열 생성
a1 = pd.DataFrame(a) #dataFrame 생성
a1.to_csv("C:/Users/User/PycharmProjects/APIEXT/APItest.csv")

path1 = r'C:/exefiles'  #exe 파일 저장한 경로
file_list2 = os.listdir(path1)  #exe파일 저장한 경로에 있는 모든 파일 도출
file_list = [file for file in file_list2 if file.endswith(".exe")]  #위의 경로에 있는 모든 파일 중 exe파일만 도출
file_list.append('q')  #마지막에 반복문을 마무리하기 위해 'q'를 append 한다.

path = input("시작하려면 start, 종료하려면 q를 입력하시오.")

while path != "q" :  # q 입력 시 반복문 종료
    for i in file_list : #변수 i에 file_list에 있는 string을 불러온다.
        path = path1 + "/" + i #각 파일의 이름과 exe파일들을 저장한 경로를 붙여 파일들에 대한 최종경로 생성
        if path == path1 + "/" + file_list[-1]:  #마지막 파일에 대한 반복문이 끝났을 때
            break  #반복문 종료
        pe = pefile.PE(path)

        file = open("C:/Users/User/PycharmProjects/APIEXT/"+i[:-4]+".txt", 'w') #API_name.txt 를 생성

        file.write(i[:-4] + "\n")  # 각 열 구분하기 위해 exe파일의 이름을 추가
        for entry in pe.DIRECTORY_ENTRY_IMPORT : #txt파일에 api 목록들을 넣음 (dataframe 을 쉽게 나누기 위해 줄바꿈단위로 입력)
            file.write("'" + str(entry.dll)[2:] +"\n")
            for imp in entry.imports:
                file.write("'" + str(imp.name)[2:] +"\n")

        file.close()
        f1 = pd.read_csv("C:/Users/User/PycharmProjects/APIEXT/"+i[:-4]+".txt", delimiter='\t')  #APIList.txt를 줄바꿈단위로 pandas로  csv 읽음
        f2 = f1[i[:-4]].value_counts() #중복된 api횟수를 count하기 위한 함수 -> dataframe이 아닌 series 형태
        df1 = pd.DataFrame(data = f2.index, columns =['api name'])
        df2 = pd.DataFrame(data = f2.values, columns =['counter'])
        df = pd.merge(df1, df2, left_index = True, right_index=True) #Series를 dataframe type으로 바꿔줌
        df.to_csv("C:/Users/User/PycharmProjects/APIEXT/"+i[:-4]+"_count.csv")
        csv1 = pd.read_csv("C:/Users/User/PycharmProjects/APIEXT/APItest.csv")
        csv1.drop(csv1.columns[0:1], axis='columns')  #첫번째 열 제거 (열번호가 적혀서 출력되어 병합할때 문제가 생김)

        finalcsv = pd.concat([csv1,f1], axis=1) # 두 csv를 병합
        finalcsv = finalcsv.drop(finalcsv.columns[0:1], axis='columns')  #첫번째 열 제거
        finalcsv.to_csv("C:/Users/User/PycharmProjects/APIEXT/APItest.csv")  #최종적으로 저장
    break

print("end")

