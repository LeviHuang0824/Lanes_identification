import cv2
import numpy as np

'''
灰階處理: 主要是用來降低運算量
高斯模糊: 用來降低影響雜訊，但是會使得影像變得模糊
Hough Transform: 找出窗點最多以決定(m,n)的直
'''
# 取得邊緣影像
def get_edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 灰階處理
    blur = cv2.GaussianBlur(gray, (13,13), 0) # 高斯模糊
    canny = cv2.Canny(blur, 50, 150) # Canny邊緣偵測
    return canny

# 建立遮罩並且取得所需的部分圖像
def get_roi(canny):
    # 建立與輸入圖片一樣尺寸大小的黑色紙板(像素0為黑色)
    mask = np.zeros_like(canny) 
    # 指定多邊形範圍座標(維度須與遮罩相同)
    points = np.array([[[146 ,539], [781, 539], [515, 417], [296, 397]]])
    cv2.fillPoly(mask, points, 255) # 繪製多邊形(像素255為白色)
    roi = cv2.bitwise_and(canny, mask) # 兩張圖做and運算，只保留白色多邊形的部分
    return roi

# 繪製道路路線
def draw_lines(img, lines):
    for line in lines:
        points = line.reshape(4,) # 轉成一維
        x1, y1, x2, y2 = points 
        # 繪製道路直線
        cv2.line(img, (x1, y1), (x2, y2), (0,0,255), 3)

    return img

# 使用最小平方法取得道路左右平均線
# 參數為Hough Transform後，所找到的線段座標點
def get_averagelines(lines):
    rights = [] # 道路右車線
    lefts = [] # 道路左車線
    if lines is None:
        print("沒有偵測到線段")
        return None
    
    for line in lines:
        points = line.reshape(4,) # 轉成一維
        x1, y1, x2, y2 = points
        # 最小平方法(deg=1 代表1次多項式)
        slope, b = np.polyfit((x1, x2), (y1, y2), deg=1)
        # print(f"y = {slope}x + {b}")
        # 判斷斜率正負，分別對應到圖像的左右車線
        # 影像處理中，y軸在下，與直角坐標表示相反
        # 所以斜率正負代表的方向相反
        if slope > 0:
            rights.append([slope, b])
        else:
            lefts.append([slope, b])

    # 計算左右車線平均值
    if rights and lefts: # 需同時有左右車線兩邊的座標
        rights_avg = np.average(rights, axis=0) # 垂直計算平均
        lefts_avg = np.average(lefts, axis=0) 
        return np.array([rights_avg, lefts_avg])
    else:
        print("沒有同時偵測到左右車線")
        return None

# 自訂車線出現的範圍
def get_subline(img, avglines):
    sublines = [] # 儲存線段座標
    for line in avglines: # 取出平均過後的直線線段
        slope, b  = line # y = {slope}x + b
        y1 = img.shape[0] # 取得影像高度(影像最底部的線段)
        y2 = int(y1 * (3/5)) # 取得影像高度3/5處，當作線段的另一端
        x1 = int((y1-b) / slope) # x = (y-b)/slope
        x2 = int((y2-b) / slope) 
        sublines.append([x1, y1, x2, y2])
    return np.array(sublines) # 轉成ndarray


        