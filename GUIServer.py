#from kivy.app import App
#from kivy.uix.button import Label,Button
#from kivy.uix.widget import Widget
#from kivy.uix.gridlayout import GridLayout
#from kivy.uix.anchorlayout import AnchorLayout
#from kivy.core.window import Window 
#from kivy.properties import ObjectProperty, NumericProperty
from matplotlib.font_manager import FontProperties
import subprocess
import http.server
import threading
import re
import sys
import CallbackServer
import matplotlib.pyplot as plt
import numpy as np
import datetime

# カウント用変数
voice01 = 0
laugh01 = 0
rectime01 = 0
voice02 = 0
laugh02 = 0
rectime02 = 0
voice03 = 0
laugh03 = 0
rectime03 = 0
voice04 = 0
laugh04 = 0
rectime04 = 0

# グラフ書く準備
plt.rcParams.update({'font.size':15}) # フォントサイズ調整
plt.figure(figsize=(12,4)) # グラフサイズ調整
# fp = FontProperties(fname=r'C:\WINDOWS\Fonts\YuGothic.ttf', size=14) # Win
fp = FontProperties(fname=r'/System/Library/Fonts/ヒラギノ角ゴシック W2.ttc', size=14) # Mac
plt.ion() 
w = 0.3 # 棒の幅
fig, ax = plt.subplots()
laugh = np.array([laugh01, laugh02, laugh03, laugh04])
voice = np.array([voice01, voice02, voice03, voice04])
vtime = np.array([rectime01, rectime02, rectime03, rectime04])
x = np.arange(len(laugh))
ax2 = ax.twinx()

ax.set_ylim(0) # y軸の高さ制限
ax2.set_ylim(0) # y軸の高さ制限
plt.xticks(x + w/2, ["raspi01", "raspi02", "raspi03", "raspi04"])
ax.set_yticks([0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200]) # y軸の目盛り
ax2.set_yticks([0, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400]) # y軸の目盛り
ax.set_ylabel("笑った回数・発言回数", fontproperties=fp)
ax2.set_ylabel("発言時間", fontproperties=fp)

laugh = np.array([laugh01, laugh02, laugh03, laugh04])
voice = np.array([voice01, voice02, voice03, voice04])
vtime = np.array([rectime01, rectime02, rectime03, rectime04])
p1 = ax.bar(x, laugh, color="#ff7f00", width=w, label="笑った回数", align="center")
p2 = ax.bar(x + w, voice, color="#377eb8", width=w, label="発言回数", align="center")
p3 = ax2.bar(x + w + w, vtime, color="#00b400", width=w, label="発言時間", align="center")
p = [p1, p2, p3]
ax.legend(p, [i.get_label() for i in p], prop=fp) # 凡例
plt.pause(0.001)

#def hello():
#    print ("helohelo")

#t=threading.Timer(5,hello)
#t.start()


def callback_method(query):# 笑った回数・発言回数・発言時間をカウントする

		global voice01
		global laugh01
		global rectime01
		global voice02
		global laugh02
		global rectime02
		global voice03
		global laugh03
		global rectime03
		global voice04
		global laugh04
		global rectime04
		global laugh
		global voice
		file = open("log126.text", "a")
		logtime = datetime.datetime.now().strftime("%m/%d:%H:%M:%S")
		#t=threading.Timer(5,hello)
		
		if re.search(r"voice/raspi01", query):
			#t.cancel()
			time = re.search("\d.\d\d\d\d", query)
			rectime = time.group()
			rectime01 += int(float(rectime))
			voice01 += 1
			print ("01：話した回数" + str(voice01))#デバッグログ
			print (rectime)
			string = ["raspi01", ",", "voice", ",", str(voice01), ",", str(logtime), ",", str(rectime01), "\n"]
			file.writelines(string)
			#t.start()
		if re.search(r"laugh/raspi01", query):
			laugh01 += 1
			print("01：笑った回数" + str(laugh01))#デバッグログ
			string = ["raspi01", ",", "laugh", ",", str(laugh01), ",", str(logtime), "\n"]
			file.writelines(string)
		
		if re.search(r"voice/raspi02", query):
			time = re.search("\d.\d\d\d\d", query)
			rectime = time.group()
			rectime02 += int(float(rectime))
			voice02 += 1
			print ("02：話した回数" + str(voice02))#デバッグログ
			string = ["raspi02", ",", "voice", ",", str(voice02), ",", str(logtime), ",", str(rectime02), "\n"]
			file.writelines(string)
		if re.search(r"laugh/raspi02", query):
			laugh02 += 1
			print("02：笑った回数" + str(laugh02))#デバッグログ
			string = ["raspi02", ",", "laugh", ",", str(laugh02), ",", str(logtime), "\n"]
			file.writelines(string)
		
		if re.search(r"voice/raspi03", query):
			time = re.search("\d.\d\d\d\d", query)
			rectime = time.group()
			rectime03 += int(float(rectime))
			voice03 += 1
			print ("03：話した回数" + str(voice03))#デバッグログ
			string = ["raspi03", ",", "voice", ",", str(voice03), ",", str(logtime), ",", str(rectime03), "\n"]
			file.writelines(string)
		if re.search(r"laugh/raspi03", query):
			laugh03 += 1
			print("03：笑った回数" + str(laugh03))#デバッグログ
			string = ["raspi03", ",", "laugh", ",", str(laugh03), ",", str(logtime), "\n"]
			file.writelines(string)
		
		if re.search(r"voice/raspi04", query):
			time = re.search("\d.\d\d\d\d", query)
			rectime = time.group()
			rectime04 += int(float(rectime))
			voice04 += 1
			print ("04：話した回数" + str(voice04))#デバッグログ
			string = ["raspi04", ",", "voice", ",", str(voice04), ",", str(logtime), ",", str(rectime04), "\n"]
			file.writelines(string)
		if re.search(r"laugh/raspi04", query):
			laugh04 += 1
			print("04：笑った回数" + str(laugh04))#デバッグログ
			string = ["raspi04", ",", "laugh", ",", str(laugh04), ",", str(logtime), "\n"]
			file.writelines(string)
		
		laugh = np.array([laugh01, laugh02, laugh03, laugh04])
		voice = np.array([voice01, voice02, voice03, voice04])
		vtime = np.array([rectime01, rectime02, rectime03, rectime04])
		p1 = ax.bar(x, laugh, color="#ff7f00", width=w, label="笑った回数", align="center")
		p2 = ax.bar(x + w, voice, color="#377eb8", width=w, label="発言回数", align="center")
		p3 = ax2.bar(x + w + w, vtime, color="#00b400", width=w, label="発言時間", align="center")
		plt.pause(0.001)
		return ['Hello', 'World!', 'with', query]
		file.close()

def server():
	CallbackServer.start(8000, callback_method)



"""
class DetectionApp(App):
	def build(self):
	return voice01
"""

if __name__ == '__main__':	
	
	server()
                      
	
	#DetectionApp().run()
		