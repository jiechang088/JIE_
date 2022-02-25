import cv2
import requests
import numpy as np
from PIL import Image
from io import BytesIO
from jsonpath import jsonpath


class DX:
    def __init__(self):
        pass

    @staticmethod
    def join_url(url):
        return 'https://static.dingxiang-inc.com/picture' + url

    @staticmethod
    def img_recover(location_array, img_url):
        """ 图片拼合 """
        img = np.array(Image.open(BytesIO(requests.get(url=img_url, verify=False).content)))
        new_img = np.zeros((200, 400, 3), dtype=np.uint8)
        lk = len(location_array)
        for cp in range(lk):
            c = location_array[cp] % lk * 12
            xp = cp % lk * 12
            slice_img = img[0: 200, c: c + 12]
            new_img[0: 200, xp:xp + len(slice_img[0])] = slice_img
        return new_img

    def get_img_code(self):
        url = 'https://cap.dingxiang-inc.com/api/a?w=300&h=150&s=50&ak=99de95ad1f23597c23b3558d932ded3c&c=61bcc136zUAfFvysgId6jstyk9BydOvSS25IoSq1&jsv=1.5.7.3&aid=dx-1639760233988-75438723-4&wp=1&de=0&uid=&lf=0&tpc=&cid=86398605&_r=0.11700541296953149'
        res = requests.get(url).json()
        print(res)
        p1, p2 = jsonpath(res, '$..[p1,p2]')
        p1, p2 = self.join_url(p1), self.join_url(p2)

        print('验证码链接 --> ', p1, p2)
        print(self.img_verify_discern(self.img_recover(self.ar(p1[p1.rfind('/')+1: p1.rfind('.')]), p1), p2))
        # data = {
        #     'ac': '',  # 加密
        #     'ak': res['ak'],
        #     'c': res['c'],
        #     'uid': '',  # 无
        #     'jsv': '1.5.7.3',  # 版本
        #     'sid': res['sid'],
        #     'aid': 'dx-1639766590285-36006062-3',  # 时间
        #     'x': '72',
        #     'y': res['y']
        # }

    @staticmethod
    def img_verify_discern(jp, pg):
        """验证码识别 """
        notch_background = cv2.cvtColor(np.asarray(jp), cv2.COLOR_RGB2GRAY)

        # 清除图片的空白区域，这里主要清除滑块的空白
        img = cv2.imdecode(np.frombuffer(requests.get(url=pg, verify=False).content, np.uint8), cv2.IMREAD_UNCHANGED)
        margin_index = np.unravel_index(img.argmax(), img.shape)[0]
        img1 = img[margin_index: -margin_index, margin_index: -margin_index]

        bg_edge = cv2.Canny(notch_background, 100, 200)
        tp_edge = cv2.Canny(img1, 100, 200)

        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

        br = tuple(map(lambda x, y: x + y, max_loc, tp_pic.shape[:2]))  #  右下角点的坐标
        cv2.rectangle(notch_background, max_loc, br, (0, 0, 255), 2)  # 绘制矩形
        cv2.imwrite('new_img.png', notch_background)  #  保存在本地
        return max_loc[0]  # 一般滑块取位置取br的第一个值

    def ar(self, r):
        """ 拼合数字计算 """
        t = []
        for n in range(len(r)):
            e = ord(r[n])
            if 32 == n:
                break
            while e % 32 in t:
                e += 1
            t.append(e % 32)
        return t

    def text(self):
        url = 'https://static.dingxiang-inc.com/picture/dx/39tYvUqtgD/zib3/86c9a2bb6108461b811e5ba4831084a6.webp'
        u2 = 'https://static.dingxiang-inc.com/picture/dx/39tYvUqtgD/zib3/48293db4e09f43159ddfe0606a0cbf36.webp'


if __name__ == '__main__':
    dx = DX()
    dx.get_img_code()
    # dx.text()
