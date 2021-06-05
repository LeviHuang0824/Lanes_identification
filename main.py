import numpy as np
import cv2
# 使用自訂義的模組
from packages import module as m


video = cv2.VideoCapture("C:\\python_jupyter\\Lanes_Identification\\road.mp4") # 建立VideoCapture物件
print(video.isOpened())
if video.isOpened(): # 判斷是否讀取成功
    # 動態影像是看做由一大堆連續的影像堆疊而成
    # 使用迴圈來抽取單一影像，進行處理
    while True:
        sucess, img = video.read() # 讀取影像
        if sucess:
            edge = m.get_edge(img) # 邊緣偵測
            roi = m.get_roi(edge) # 取得roi
            lines = cv2.HoughLinesP(
                image=roi,
                rho=3,
                theta=np.pi/180,
                threshold=30,
                minLineLength=50,
                maxLineGap=40)
            # 取得左右兩條平均線方程式
            avglines = m.get_averagelines(lines)
            
            if avglines is not None:
                # 取得要畫出的左兩條線段
                lines = m.get_subline(img, avglines)
                img = m.draw_lines(img, lines) # 劃q出線段
            cv2.imshow("pic", img) # 顯示影像
        k = cv2.waitKey(1) # 檢查是否有按鍵輸入
        # 如果按下Q鍵，則結束迴圈
        if k== ord("q") or k== ord("Q"):
            print("exit")
            cv2.destroyAllWindows() # 關閉視窗
            video.release() # 關閉影片
            break
else:
    print("開啟影片失敗")
