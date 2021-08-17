import fitz
import time
import re
import os

def pdf2pic(path, pic_path):
    '''
    # 從pdf中提取圖片
    :param path: pdf的路徑
    :param pic_path: 圖片儲存的路徑
    :return:
    '''
    t0 = time.process_time()
    # 使用正則表示式來查詢圖片
    checkXO = r"/Type(?= */XObject)" 
    checkIM = r"/Subtype(?= */Image)"
    # 開啟pdf
    doc = fitz.open(path)
    # 圖片計數
    imgcount = 0
    lenXREF = doc.xref_length()

    # 列印PDF的資訊
    print("檔名:{}, 頁數: {}, 物件: {}".format(path, len(doc), lenXREF - 1))
    for i in range(1, lenXREF):
        # 定義物件字串
        text = doc.xref_object(i)
        isXObject = re.search(checkXO, text)
        # 使用正則表示式檢視是否是圖片
        isImage = re.search(checkIM, text)
        # 如果不是物件也不是圖片，則continue
        if not isXObject or not isImage:
            continue
        imgcount += 1
        # 根據索引生成影象
        pix = fitz.Pixmap(doc, i)
        # 根據pdf的路徑生成圖片的名稱
        new_name = path.replace('\\', '_')\
        .replace('.pdf',"_img{}.png".format(imgcount))
        new_name = new_name.replace(':', '')
        # 如果pix.n<5,可以直接存為PNG
        if pix.n < 4:
            pix.writePNG(os.path.join(pic_path, new_name))
        # 否則先轉換CMYK
        else:
            pix0 = fitz.Pixmap(fitz.csRGB, pix)
            pix0.writePNG(os.path.join(pic_path, new_name))
            pix0 = None
        # 釋放資源
        pix = None
        t1 = time.process_time()
        print("執行時間:{}s".format(t1 - t0))
        print("提取了{}張圖片".format(imgcount))
        
if __name__=='__main__':
    # pdf路徑
    input_filename=input("輸入pdf檔名:")
    input_filename+='.pdf' if input_filename[-4:]!='.pdf' else ''
    path = r'./{}'.format(input_filename)
    pic_path = r'./{}image'.format(path.replace('\\', '_').replace('.pdf','_'))
    # 建立儲存圖片的資料夾
    if not os.path.isfile(path):
        print("檔名錯誤或檔案不存在")
        os.system("pause")
        raise SystemExit
    if os.path.exists(pic_path):
        print("資料夾名稱重複，請刪除或更改pdf檔名")
        os.system("pause")
        raise SystemExit
    else:
        os.mkdir(pic_path)
    m = pdf2pic(path, pic_path)

    
os.system("pause")