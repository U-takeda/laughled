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

def callback_method(query):
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
		#pattern=r'\d\d'
		
		if re.search(r"voice/raspi01", query):
			#time = re.findall(pattern,querry)
			#rectime01 += time
			voice01 += 1
			print ("話した回数" + str(voice01))#デバッグログ
		if re.search(r"laugh/raspi01", query):
			laugh01 += 1
			print("笑った回数" + str(laugh01))#デバッグログ
		
		if re.search(r"voice/raspi02", query):
			voice02 += 1
			print ("話した回数" + str(voice02))#デバッグログ
		if re.search(r"laugh/raspi02", query):
			laugh02 += 1
			print("笑った回数" + str(laugh02))#デバッグログ
		
		if re.search(r"voice/raspi03", query):
			voice03 += 1
			print ("話した回数" + str(voice03))#デバッグログ
		if re.search(r"laugh/raspi03", query):
			laugh03 += 1
			print("笑った回数" + str(laugh03))#デバッグログ
		
		if re.search(r"voice/raspi04", query):
			voice04 += 1
			print ("話した回数" + str(voice04))#デバッグログ
		if re.search(r"laugh/raspi04", query):
			laugh04 += 1
			print("笑った回数" + str(laugh04))#デバッグログ
		return ['Hello', 'World!', 'with', query]

def server():
	CallbackServer.start(8000, callback_method)

def pause_plot():
	plt.rcParams.update({'font.size':15}) # フォントサイズ調整
	plt.figure(figsize=(8,6)) # グラフサイズ調整
	# fp = FontProperties(fname=r'C:\WINDOWS\Fonts\YuGothic.ttf', size=14) #Windows
	fp = FontProperties(fname=r'/System/Library/Fonts/ヒラギノ角ゴシック W2.ttc', size=14)
	w = 0.3 # 棒の幅
	
	#fig, ax1 = plt.subplots() # 2軸グラフ
	laugh = np.array([laugh01, laugh02, laugh03, laugh04])
	voice = np.array([voice01, voice02, voice03, voice04])
	x = np.arange(len(laugh))
	plt.bar(x, laugh, color="#ff7f00", width=w, label="笑った回数")
	plt.bar(x + w, voice, color="#377eb8", width=w, label="発言回数")
	#ax2 = ax1.twinx()  # 2つのプロットを関連付ける
	#plt.bar(x + w + w, time, color="", width=w, label="発言時間")
	plt.ylim(0, 50) # y軸の高さ制限
	plt.yticks([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]) # y軸のメモリ
	plt.ylabel("笑った回数・発言回数", fontproperties=fp)
	plt.legend(bbox_to_anchor=(1,1.01), loc=2, prop=fp) # 凡例
	
	# ここから無限にplotする
	while True:
		laugh = np.array([laugh01, laugh02, laugh03, laugh04])
		voice = np.array([voice01, voice02, voice03, voice04])
		#plt.text(0, 1, "Text!") # 指定した座標の上にテキストを追加
		plt.bar(x, laugh, color="#ff7f00", width=w, label="笑った回数", align="center")
		plt.bar(x + w, voice, color="#377eb8", width=w, label="発言回数", align="center")
		plt.xticks(x + w/2, ["raspi01", "raspi02", "raspi03", "raspi04"])
		#plt.text(x, laugh, laugh, ha='center', va='bottom')
		plt.pause(.01)

"""
class DetectionApp(App):
	def build(self):
	return voice01
"""

if __name__ == '__main__':	
	
	threading.Thread(target=server).start()
	
	pause_plot()
                      
	
	#DetectionApp().run()
		