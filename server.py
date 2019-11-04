# -*- coding: utf-8 -*-
import random #암호화 구축 위해
import hashlib	# MD5를 구하기 위해 import
import pyautogui
import bluetooth#블루투스 통신을 위해
import re #패스프레이즈 변환을 위해
import socket #소켓통신을 위해 이제 필요 없
import json #json 파일의 작성, 생성을 위해
import os, time #json파일의 존재 파악 위해
from collections import OrderedDict #딕셔너리형 변수 사용 위해
import sys #임폴트 경로떄문
sys.path.insert(0, '/home/pi/smart_mirror/')
from ui_object import t #ui에 메시지 표출을 하기 위해
from caldavclient.schedule_handler import certifications


def list_process(u_str): #암호화
	seed = 'abcdefghijklmnopqrstuvwxyz123456789' #원문의 암호화시 필요한 데이터들
	num = 1
	u_list = []
	if len(u_str)%2 == 1:#평문 짝수, 홀수 검증
		compare = 1
	else :
		compare = 0

	while num != (len(u_str)*2): #평문 변환할 리스트 생성
		u_list.append('')
		num = num + 1

	for n in range(len(u_str)):#평문을 리스트의 짝수 주소지에 배치
		u_list[n*2] = u_str[n]
	for n in range(len(u_list)):
		if n%2 != 0:
			u_list[n] = random.choice(seed)#랜덤 값을 리스트의 홀수 주소지에 배치
	
	if compare == 0: #짝수일때
		for n in range(len(u_list)):#0과2 4와6 스왑
			if n==0:
				tmp=u_list[n]
				u_list[n]=u_list[n+2]
				u_list[n+2]=tmp
				verify=4
			elif n == verify or n == (len(u_list)-3):
				tmp=u_list[n]
				u_list[n]=u_list[n+2]
				u_list[n+2]=tmp
				if n != (len(u_list)-5):
					verify=verify+4

	elif compare == 1: #홀수일때
		for n in range(len(u_list)):#0과2 4와6 6과0 스왑
			if n==0:
				tmp=u_list[n]
				u_list[n]=u_list[n+2]
				u_list[n+2]=tmp
				verify=4
			elif n == verify or n == (len(u_list)-5):
				tmp=u_list[n]
				u_list[n]=u_list[n+2]
				u_list[n+2]=tmp
				if n != (len(u_list)-5):
					verify=verify+4
			elif n==len(u_list)-1:
				tmp=u_list[n]
				u_list[n]=u_list[0]
				u_list[0]=tmp
	return u_list

def string_processing(in_str):#스트링 형 변수를 리스트로 재구축
	c_num = 0
	str_list = []
	while c_num != len(in_str):
		str_list.append(in_str[c_num])
		c_num = c_num + 1
	return str_list

def list_processed(u_s_list): # 복호화
	if len(u_s_list)%4 == 3 or len(u_s_list) == 4: #원문이 짝수
		compare_t = 0
	elif len(u_s_list)%4 == 1: #원문이 홀수
		compare_t = 1
	
	if compare_t == 0: #짝수일때
		for n in range(len(u_s_list)):#0과2 4와6 스왑
			if n==0:
				tmp = u_s_list[n]
				u_s_list[n] = u_s_list[n+2]
				u_s_list[n+2] = tmp
				verify = 4
			elif n == verify or n == (len(u_s_list)-3):
				tmp = u_s_list[n]
				u_s_list[n] = u_s_list[n+2]
				u_s_list[n+2] = tmp
				if n != (len(u_s_list)-5):
					verify = verify + 4
	
	elif compare_t == 1: #홀수일때
		for n in range(len(u_s_list)):# 0과2 4와 6 6과 0 스왑
			if n==0:
				tmp=u_s_list[n]
				u_s_list[n]=u_s_list[len(u_s_list)-1]
				u_s_list[len(u_s_list)-1]=tmp
				verify=4
			elif n == verify or n == (len(u_s_list)-5):
				tmp=u_s_list[n]
				u_s_list[n]=u_s_list[n+2]
				u_s_list[n+2]=tmp
				if n != (len(u_s_list)-5):
					verify=verify+4
			elif n==len(u_s_list)-1:
				tmp=u_s_list[0]
				u_s_list[0]=u_s_list[2]
				u_s_list[2]=tmp
	
	txt_list=[]
	txt_len=(len(u_s_list)+1)/2
	num_txt = 0
	while num_txt != txt_len:#평문의 길이만큼 리스트 생성
		txt_list.append('')
		num_txt = num_txt + 1
	
	for n in range(len(u_s_list)):#암호문 리스트의 짝수번지를 평문 담을 리스트에 배치
		if n  == 0 :
			txt_list[n] = u_s_list[n]
		if n % 2 == 0 :
			txt_list[int(n/2)] = u_s_list[n]
	return txt_list

def do_some_stuffs_with_input(input_string):
	#통신시 받을 내용 줄바꿈해서 저장
	list_u = input_string.split('\n')
	
	return list_u

def hashing_passphrase(passphras):
	pattern = re.compile(r'\s+') #공백(space) 패턴 객체화
	passphras = re.sub(pattern, '', passphras) #패턴 객체화된 공백을 ''로 바꿈 -> 띄어쓰기 제거
	print(passphras)# 공백 제거 확인 위함(삭제필요)
	passphras=passphras.encode("utf8")#utf8로 인코딩
	has_func = hashlib.md5()	# MD5 hash function
	has_func.update(passphras)   # hashing!
	passphras=has_func.hexdigest()# 메시지 다이제스트를 얻음(16진수 해시값)
	print(has_func.hexdigest())
	return passphras

def new_user(n_pwp, n_uid, n_upw):
	global t
	t.mirror.ment_lb.setText("신규 사용자 정보 입력") 
	time.sleep(1)
	n_pwp=hashing_passphrase(n_pwp)# 패스프레이즈 해싱
	if certifications(n_uid, n_upw) == 1: # 칼다브 클라이언트 이용해 사용자 id, pw의 검증
		n_upw = (''.join(list_process(n_upw)))#평문 암호화알고리즘에 적용해 스트링 형식으로 배치
		if os.path.exists('/home/pi/smart_mirror/text_directory/user_info.json') :		 #처음 구동시 DB.TXT있는지 유무확인후 없으면 생성 필요
			with open('/home/pi/smart_mirror/text_directory/user_info.json') as data_file:	#파일이 존재하면 값을 읽어옴
				dict = json.load(data_file) #해당 .json 의 값을 dict에 읽어들임
			t.mirror.ment_lb.setText("'.json' load")
		
			if dict.get(n_pwp): #이미 존재하는 값이면
				t.mirror.ment_lb.setText("이미 존재하는 패스 프레이즈 입니다.")
				return 1 #패스프레이즈의 중복 
			else: #같은 값이 없으면 실행
				dict[n_pwp] = [n_uid, n_upw] #새롭게 추가된 값 dict에 추가
				print(dict)
				with open('/home/pi/smart_mirror/text_directory/user_info.json','w',encoding='utf-8')as make_file: #.json파일 쓰기형식, utf-8 로 인코딩해 오픈
					json.dump(dict, make_file, ensure_ascii=False, indent="\t")
				t.mirror.ment_lb.setText("정보가 정상적으로 등록 되었습니다.")
				return 0 #사용자 정보의 성공적인 등록

		else : #.json파일 존재 안하면
			dict={n_pwp:[n_uid, n_upw]}#새롭게 추가된 값 dict에 추가
			# print(dict)#dict 안에 저장된 값 확인위해(삭제필요)
			with open('/home/pi/smart_mirror/text_directory/user_info.json','w',encoding='utf-8')as make_file: #.json파일 쓰기형식, utf-8 로 인코딩해 오픈
				json.dump(dict, make_file, ensure_ascii=False, indent="\t")	#dict의 값을 .json에 씀
			return 0 #사용자 정보의 성공적인 등록
	else :
		t.mirror.ment_lb.setText("ID 혹은 PW를 잘못 입력하셨습니다.")
		return 5 #id, pw의 오류

def exist_user(e_pwp, e_del_pwp, e_uid, e_upw):
	global t
	t.mirror.ment_lb.setText("기존 사용자 정보 변경")
	time.sleep(1)
	e_pwp=hashing_passphrase(e_pwp)
	e_del_pwp=hashing_passphrase(e_del_pwp)

	if certifications(e_uid, e_upw) == 1: # 칼다브 클라이언트 이용해 사용자 id, pw의 검증
		if os.path.exists('/home/pi/smart_mirror/text_directory/user_info.json') :		 #처음 구동시 DB.TXT있는지 유무확인후 없으면 생성 필요
			with open('/home/pi/smart_mirror/text_directory/user_info.json') as data_file:	#파일이 존재하면 값을 읽어옴
				dict = json.load(data_file) #해당 .json 의 값을 dict에 읽어들임
			t.mirror.ment_lb.setText("'.json' load")
			compare_Uinfo=dict.get(e_del_pwp) #해당 패스프레이즈를 키값으로하는 사용자 정보 load
			if compare_Uinfo is None: #해당 패스프레이즈로 검색한 값에 대한 검증
				return 2 #사용자가 입력한 패스프레이즈의 오류
			else :
				e_last_uid = compare_Uinfo[0]
				e_last_upw = list_processed(string_processing(compare_Uinfo[1])) #로드한 정보 복호화하여 저장

			if(e_last_uid == e_uid)and(''.join(e_last_upw)==e_upw): #저장되어있던 패스프레이즈의 사용자 정보와 입력한 사용자 정보의 비교
				if dict.get(e_del_pwp): #패스프레이즈를 이용해 dict에서 값 가져옴
					del dict[e_del_pwp] #변경전 패스프레이즈 정보 삭제
					dict[e_pwp] = [e_uid, (''.join(list_process(e_upw)))] #변경후 패스프레이즈 정보 등록
					with open('/home/pi/smart_mirror/text_directory/user_info.json','w',encoding='utf-8')as make_file: #.json파일 쓰기형식, utf-8 로 인코딩해 오픈
						json.dump(dict, make_file, ensure_ascii=False, indent="\t") #json 파일에 dict등록
					return 4 #사용자 정보 성공적으로 변경
				else:
					t.mirror.ment_lb.setText("패스프레이즈를 잘못 입력하셨습니다.")
					return 2 #기존 패스프레이즈 잘못입	

			else:
				t.mirror.ment_lb.setText("ID 혹은 PW를 잘못 입력하셨습니다.")
				return 5 #id, pw 오류
		else : #.json파일 존재 안하면
			dict={e_pwp:[e_uid, e_upw]}#새롭게 추가된 값 dict에 추가
			print(dict)#dict 안에 저장된 값 확인위해(삭제필요)
			with open('/home/pi/smart_mirror/text_directory/user_info.json','w',encoding='utf-8')as make_file: #.json파일 쓰기형식, utf-8 로 인코딩해 오픈
				json.dump(dict, make_file, ensure_ascii=False, indent="\t")	#dict의 값을 .json에 씀
			t.mirror.ment_lb.setText("정상적으로 정보를 입력하였습니다.")
			return 4 #사용자 정보 성공적으로 변경
	else :
		t.mirror.ment_lb.setText("ID 혹은 PW를 잘못 입력하셨습니다.")
		return 5 #id, pw 오류

def del_user(d_pwp, d_uid, d_upw):
	global t
	
	d_pwp=hashing_passphrase(d_pwp)
	t.mirror.ment_lb.setText("사용자 정보 삭제")
	time.sleep(1)

	if os.path.exists('/home/pi/smart_mirror/text_directory/user_info.json') :		 #처음 구동시 DB.TXT있는지 유무확인후 없으면 생성 필요
		with open('/home/pi/smart_mirror/text_directory/user_info.json') as data_file:	#파일이 존재하면 값을 읽어옴
			dict = json.load(data_file) #해당 .json 의 값을 dict에 읽어들임
		compare_Uinfo=dict.get(d_pwp)
		if compare_Uinfo is None:#입력한 패스프레이즈의 값이 존재안하면
			t.mirror.ment_lb.setText("존재하지 않는 사용자 정보 입니다.")
			return 7 #사용자가 입력한 정보가 잘못된 정보

		else :
			d_last_uid = compare_Uinfo[0]
			d_last_upw = list_processed(string_processing(compare_Uinfo[1]))
			
		if(d_last_uid == d_uid)and(''.join(d_last_upw) == d_upw): #기존 저장된 사용자 정보와 삭제하고싶은 사용자 정보의 비교
			if dict.get(d_pwp): #입력한 패스프레이즈의 값이 존재하면 
				del dict[d_pwp] #해당 내용을 dict에서 삭제
				with open('/home/pi/smart_mirror/text_directory/user_info.json','w',encoding='utf-8')as make_file: #.json파일 쓰기형식, utf-8 로 인코딩해 오픈
					json.dump(dict, make_file, ensure_ascii=False, indent="\t")	#dict의 값을 .json에 씀
				t.mirror.ment_lb.setText("사용자 정보를 성공적으로 삭제 하였습니다.")
				return 6 #사용자 정보의 성공적인 삭제
			else:
				t.mirror.ment_lb.setText("입력한 정보가 잘못된 정보 입니다.")
				return 7 #사용자가 입력한 정보가 잘못된 정보
		else:
			t.mirror.ment_lb.setText("입력한 정보가 잘못된 정보 입니다.")
			return 7 #사용자가 입력한 정보가 잘못된 정보
	else : #.json파일 존재 안하면
		t.mirror.ment_lb.setText("저장된 사용자 정보가 없습니다.")
		return 8 #등록된 정보가 없을때

def add_address(u_address):#사용자 주소입력 위한 함수
	global t
	t.mirror.ment_lb.setText("사용자 주소 입력") 
	time.sleep(1)
	if os.path.exists('/home/pi/smart_mirror/text_directory/user_address.txt') :#처음 구동시 .TXT있는지 유무확인후 없으면 생성 필요
		with open('/home/pi/smart_mirror/text_directory/user_address.txt','w',encoding='utf-8') as data_file:
			data_file.write(u_address)
		t.mirror.ment_lb.setText("사용자 주소를 갱신하였습니다.")
		return 9 #사용자 정보의 성공적인 등록
	else : #.json파일 존재 안하면
		with open('/home/pi/smart_mirror/text_directory/user_address.txt','w',encoding='utf-8')as make_file: #.json파일 쓰기형식, utf-8 로 인코딩해 오픈
			make_file.write(u_address)	#dict의 값을 .json에 씀
		t.mirror.ment_lb.setText("사용자 주소 등록 성공")
		return 9 #사용자 정보의 성공적인 등록

def data_Processing(r_data):
	global t
	for n in range(len(r_data)): #어플리케이션 으로부터 전송된 리스트를 각각의 스트링에 저장하기위함
		if n%5==0:
			d_info=r_data[n] #정보등록, 정보변경, 정보삭제인지 확인할 값
			if d_info == '4':#주소 등록시 사용하기 위한 설정
				return d_info, r_data[1], '', '', ''
		if n%5==1:
			d_pwp=r_data[n] #사용자가 현 시점부터 사용할 패스프레이즈
		if n%5==2:
			d_del_pwp=r_data[n] #사용자가 더이상 사용하지 않는 패스프레이즈
		if n%5==3:
			d_uid=r_data[n] #사용자가 사용하는 id
		if n%5==4:
			d_upw=r_data[n] #사용자가 사용하는 pw
	return d_info, d_pwp, d_del_pwp, d_uid, d_upw #스트링 형식으로 바꿔 반환

def error_messge(error_num, er_pwp, er_uid, er_upw): #알맞는 에러메시지와 complite메시지를 반환하기위한 함수
	if error_num == 0: #성공
		e_message="사용자의 정보가 성공적으로\n등록 되었습니다.\n"
		sand_client=b'\n\n pwp : '+er_pwp.encode()+b'\n\n id : '+er_uid.encode()+b'\n\n pw : '+er_upw.encode()+b'\n\n'+e_message.encode()
	elif error_num == 1: #에러
		e_message="\n동일한 패스프레이즈가 존재합니다.\n새로운 패스프레이즈를 입력하세요.\n"
		sand_client=e_message.encode()
	elif error_num == 2: #에러
		e_message="\n입력한 기존 문장이 잘못된 문장입니다.\n올바른 문장을 입력해 주세요.\n"
		sand_client=e_message.encode()
	elif error_num == 3: #에러
		e_message="\n입력된 ID,PW 또는 변경할 문장이\n기존 정보와 다릅니다.\n다시 입력해 주세요.\n"
		sand_client=e_message.encode()	
	elif error_num == 4: #성공
		e_message="사용자 정보가 성공적으로\n변경 되었습니다.\n"
		sand_client=b'\n\n pwp : '+er_pwp.encode()+b'\n\n id : '+er_uid.encode()+b'\n\n pw : '+er_upw.encode()+b'\n\n'+e_message.encode()
	elif error_num == 5: #에러
		e_message="\n입력하신 ID,PW 가 잘못된 정보입니다.\n올바른 id, pw를 입력해 주세요.\n"
		sand_client=e_message.encode()
	elif error_num == 6: #성공
		e_message="의\n 사용자 정보가 성공적으로\n삭제 되었습니다.\n"
		sand_client=b'\n\n id : '+er_uid.encode()+b''+e_message.encode()
	elif error_num == 7: #에러
		e_message="\n입력하신 정보가 잘못된 정보입니다.\n올바른 정보를 입력해 주세요.\n"
		sand_client=e_message.encode()
	elif error_num == 8: #에러
		e_message="\n등록된 정보가 없습니다.\n"
		sand_client=e_message.encode()
	elif error_num == 9:#성공
		e_message="\n주소등록 성공\n\n"
		sand_client=e_message.encode()+b'**'+er_pwp.encode()+b'**\n'
	else: #예상하지 못한 에러
		e_message="치명적인 오류 발생\n어플리케이션의 재부팅이\n필요합니다.\n"
		sand_client=e_message.encode()
	t.mirror.ment_lb.setText(e_message)
	return sand_client

def server_start():

	global t # ui에 메시지를 출력하기 위해
	try:
		pairing = 'sudo hciconfig hci0 piscan'
		unpairing = 'sudo hciconfig hci0 noscan'
		
		os.system(pairing)
		t.mirror.ment_lb.setText("장치를 검색해주세요")
		
	
		verify=0
		checker = True
	
		while checker:
			server_scoket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
			port = 1
			server_scoket.bind(("",port))
			server_scoket.listen(1)
			client_socket,address = server_scoket.accept()
			t.mirror.ment_lb.setText("☻연결되었습니다☻")
			time.sleep(1)
			pyautogui.press('right')
			pyautogui.press('enter')
			time.sleep(1)
			pyautogui.press('tab')
			pyautogui.press('enter')
			os.system(unpairing)
			data = client_socket.recv(2048) # 소켓에서 (bufsize) 만큼 데이터를 수신
			data = data.decode("utf8").strip()
			if not data: break #수신한 데이터가 없을시 정지
			# 수신한 데이터저장
			res = do_some_stuffs_with_input(data) #함수를 이용해 전달받은 사용자 정보를 리스트에 배치
			#클라이언트에게 답을 보냄
			einfo, pwp, del_pwp, uid, upw = data_Processing(res) #리스트에 배치된 사용자 정보 각각의 스트링 변수에 저장
			t.mirror.ment_lb.setText("데이터를 정상적으로 수신")
			if einfo == '0': #사용자 정보 등록
				verify  = new_user(pwp, uid, upw)
			elif einfo == '1': #사용자 정보 변경
				verify = exist_user(pwp, del_pwp, uid, upw)
			elif einfo == '2': #사용자 정보 삭제
				verify = del_user(pwp, uid, upw)
			elif einfo == '4': #사용자 주소 등록
				pwp=pwp[5:len(pwp)]#맨 앞의 '대한민국 ' 제거하기위해
				verify = add_address(pwp)#사용자 주소가 임시로 pwp에 저장됨
			else: #지정하지 않은 값 전달시(예상하지 못한 에러 발생)
				client_socket.sendall(error_messge(13, pwp, uid, upw).encode())
				client_socket.close()
				break

			client_socket.sendall(error_messge(verify, pwp, uid, upw))

			time.sleep(2)

			if verify == 0 or verify == 4 or verify == 6 or verify == 9: #성공적인 작동시 while문 정지후 연결 닫음
				checker = False
				t.mirror.ment_lb.setText("연결을 종료합니다")
			elif verify == 8:
				checker = False
				t.mirror.ment_lb.setText("등록되지 않은 사용자 정보입니다. 연결을 종료합니다")
			else:
				t.mirror.ment_lb.setText("어플리케이션의 연결버튼을 다시 눌러주세요")
				
			client_socket.close()
			server_scoket.close()
			time.sleep(1)
	except:
		t.mirror.ment_lb.setText("오류가 발생하였습니다 다시 시도해주세요")
		time.sleep(2)
