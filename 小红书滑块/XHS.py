import random
import time
import requests
from json import loads
from jsonpath import jsonpath
from Crawler_Assist_Tools.CryptoPackage import CryptoAD
from Crawler_Assist_Tools.AuthCodeXYZ import IMG


class XHS(IMG):
    def __init__(self):
        super(XHS, self).__init__()
        self.requests = requests.session()
        self.requests.headers.update({
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Host': 'captcha.fengkongcloud.com',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 6P Build/MMB29N; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.117 Mobile Safari/537.36'
        })
        self.des = CryptoAD("DES", "ECB", padding='ZeroPadding')

    def requests_item(self, rid, mouse_data, start_time, end_time, true_width=400):
        print("滑块数组 -->", mouse_data)
        return {
            'protocol': 147,
            'organization': 'eR46sBuqF0fdw7KWFLYa',
            'ostype': 'web',
            'aw': 'UXcTRrZ9Oss=',
            'dl': self.des.encrypt(str(mouse_data[-1][0] / true_width), key='2575232a'),
            'xp': 'AQSNGqey9JA=',
            'rid': rid,
            'act.os': 'web_pc',
            'lx': 'y2aMBiuI98I=',
            'ux': '15PasxRW77o=',
            'rversion': '1.0.1',
            'vk': 'oi7kWzhqhiU=',
            'nm': self.des.encrypt(str(mouse_data).replace(' ', ''), key='4ee2f32f'),
            'xy': 'ul0oAv1ZYwo=',
            'sdkver': '1.1.3',
            'gi': 'uFbn5Z4ymF4=',
            'dy': self.des.encrypt(str(end_time - start_time), key='aee9ca04'),
            'oe': '4eIG9gpg/oI=',
            'callback': f'sm_{int(end_time * 1000)}'
        }

    @staticmethod
    def join_url(url):
        return 'https://castatic.fengkongcloud.cn' + url

    def get_img_code(self):
        res = loads(requests.get('https://captcha.fengkongcloud.cn/ca/v1/register?lang=zh-cn&sdkver=1.1.3&channel=web&rversion=1.0.1&appId=default&organization=eR46sBuqF0fdw7KWFLYa&callback=sm_1639627943456&model=slide&data=%7B%7D').text[17:-1])
        bg, fg = jsonpath(res, '$..[bg,fg]')
        bg, fg = self.join_url(bg), self.join_url(fg)
        print(bg, fg)
        ts = int(time.time() / 1000)

        s = self.methods_tow(bg, fg, (400, 200), (58, 58))[0][0]
        print('缺口', s)
        mouse_data = self.get_tracks(s)
        rid = jsonpath(res, '$..rid')[0]
        requests_data = self.requests_item(rid, mouse_data, ts, ts + random.randint(800, 1200))
        print("请求加密参数 --> ", requests_data)

        res = requests.get('https://captcha.fengkongcloud.cn/ca/v2/fverify?', params=requests_data)
        print(res.request)
        res = requests.get('https://captcha.fengkongcloud.cn/ca/v2/fverify?', params=requests_data).text
        res = loads(res[res.find('{'): res.rfind('}') + 1])
        print(res)

        data = {
            'callFrom': "web",
            "deviceId": "WHJMrwNw1k/HCN2/XtcRO4R4FPoXyZeFPVfcZO10lWfW/AQJISg0uYX1WM61JlYTGQ0RcD/m4NjJ0+JBAFFCb6r2mfdnYEY94dCW1tldyDzmQI99+chXEisPOUiXQnQriUs1VkbP/rUPdM5Ynl98g3W9hl4GeQEFSdxEry7bxbYqOys8OZPY8w2SGgyInzWFjcVR/zdiyo5k0sQ6YV1rbNBFOQB3sf95a16xDLq2jGQOZ0Bf7fTyNlyeNVNimczQ8zMFLKQpLMCB9QaAioK5ItA==1487582755342",
            'rid': rid,
            'status': 1
        }
        # print(requests.post('https://www.xiaohongshu.com/fe_api/burdock/v2/shield/captcha?c=pp', json=data).text)
        # print(requests.get(
        #     'https://captcha.fengkongcloud.cn/ca/v2/fverify?protocol=147&organization=eR46sBuqF0fdw7KWFLYa&ostype=web&dl=WZXWLKr4tmg%3D&aw=UXcTRrZ9Oss%3D&xp=AQSNGqey9JA%3D&rid=202112161242031454b3318b92219467&act.os=web_pc&lx=y2aMBiuI98I%3D&ux=15PasxRW77o%3D&rversion=1.0.1&vk=oi7kWzhqhiU%3D&nm=2Llzh5Trqkaj7qNZLf8vRmMRPjNJJSIFsNROW9mVzoukm%2FihEhCVyJn%2BuZQ8vOdhPtkiKyXr0PDP%2BGU8C5VW4RINL2ytAwBLqP86wVLWpUJtC5fNppdTGzYBqot5wINFgIZOerxvE8V3nUy9ofzBuF0F9AlUzA9OD5wXCnUYmZUOnZaUdgDOFjgN5qCQlGmbB2DAF3XwFAphT2I%2BMu3cVyyYEpa7v7mX4e%2BCJad2HZVS7U9ErwAPv9x4txBuAgl6lbRDCl7GQ8s%3D&xy=ul0oAv1ZYwo%3D&sdkver=1.1.3&gi=uFbn5Z4ymF4%3D&dy=eInJ06tAWVM%3D&oe=4eIG9gpg%2FoI%3D&callback=sm_1639629730264').text)
        # 'https://captcha.fengkongcloud.cn/ca/v2/fverify?%7B%22dl%22:%20%22RsV55zB4nZA=%22,%20%22nm%22:%20%222Llzh5TrqkakKoPAdBDORzZucQ5MwUr48OjDY2r1Z0L8fvL+8+njYsBKJAczQy6TvpfEhTGY8NbzkEoP1TdM1zCFGvRT3+S12ExyZVk84IfVna8lC0ZPb1XHObHgtlW3Vl+2ZnuzGRWVuQgsjXV1eIGK2/6ipjCWIjg6xA01tJYvKiZEAIilReGsWq0IM8UNTUvQSFMGp9KoYanYz7epXa0fy31+LSqp4+MHwhgO6xrSCd7cgWBciieDtv4DaDLU+q0oA7wH31iiwuo3P//CBYb1zNF8G+JYqEGBlBZhejrt6sInzqF2TU3SvHiWtx18dzA/n8z81E0ea2LyL2zl94ItagD9QrhK4YxR7/maRSFffJyv128zR6e5VsLig2nfuKSpOYh8WDcSNu/6ulT5dkO1v69o814kVQQmTcGJEMHTa6fMXt7/Fg==%22,%20%22dy%22:%20%22zDg/5V0CTjU=%22,%20%22lx%22:%20%22y2aMBiuI98I=%22,%20%22xy%22:%20%22ul0oAv1ZYwo=%22,%20%22act.os%22:%20%22web_pc%22,%20%22vk%22:%20%22oi7kWzhqhiU=%22,%20%22ux%22:%20%2215PasxRW77o=%22,%20%22xp%22:%20%22AQSNGqey9JA=%22,%20%22organization%22:%20%22eR46sBuqF0fdw7KWFLYa%22,%20%22aw%22:%20%22UXcTRrZ9Oss=%22,%20%22gi%22:%20%22uFbn5Z4ymF4=%22,%20%22oe%22:%20%224eIG9gpg/oI=%22,%20%22rid%22:%20%22202112161246013584939619ffa0aac2%22,%20%22rversion%22:%20%221.0.1%22,%20%22sdkver%22:%20%221.1.3%22,%20%22protocol%22:%20%22147%22,%20%22ostype%22:%20%22web%22,%20%22callback%22:%20%22sm_1639629%22%7D'
        if res['riskLevel'] == "PASS":
            return 1
        return 0


if __name__ == '__main__':
    xhs = XHS()
    # xhs.get_img_code()
    xxx = []
    for i in range(20):
        xxx.append(xhs.get_img_code())
    print(f"百次识别成功率： {xxx.count(1)}%")
