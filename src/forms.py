import json

import requests
from bs4 import BeautifulSoup


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'wp_devicetype=0; wp_ak_kywrd_ab=1; wp_ak_signinv2=1|20230125; wp_ak_om=1|20230731; wp_ak_wab=0|1|0|0|1|1|1|1|0|20230418; wp_ak_v_mab=0|0|3|0|20240926; wp_geo=ID|JK|||INTL; wp_ak_bt=1|20200518; wp_ak_bfd=1|20201222; wp_ak_tos=1|20211110; wp_ak_sff=1|20220425; wp_ak_lr=0|20221020; wp_ak_co=2|20220505; wp_ak_btap=1|20211118; wp_ak_pp=1|20210310; wp_ttrid="176f0679-fa2d-44ba-85e4-2cf5e0c277e9"; wp_ak_pw=1|20240725; wp_pwapi_ar="H4sIAAAAAAAA/6uuBQBDv6ajAgAAAA=="; wp_usp=1---; _cb=B4sFLJDXTScVCy4FzA; _cb_svref=https%3A%2F%2Fwww.google.com%2F; _v__chartbeat3=DBXDyjChv5Dxh0zRs; _t_tests=eyJCZ3NMekJzRW9DNlluIjp7ImNob3NlblZhcmlhbnQiOiJCIiwic3BlY2lmaWNMb2NhdGlvbiI6WyJlemVmZyJdfSwiZUkyekIyVjVxbGs5YSI6eyJjaG9zZW5WYXJpYW50IjoiQyIsInNwZWNpZmljTG9jYXRpb24iOlsiQ0M1Q1JrIl19LCI1ZDlwanppc1RlRmtZIjp7ImNob3NlblZhcmlhbnQiOiJCIiwic3BlY2lmaWNMb2NhdGlvbiI6WyJEdDFFQmciXX0sImxpZnRfZXhwIjoibSJ9; _ga=GA1.1.1029122116.1730243195; __stripe_mid=07c4a8f4-1af6-431d-8ac1-00b14e502196790fe3; __stripe_sid=9b812067-c5f3-412b-829a-6c9bddda4cfce2280f; _chartbeat2=.1730243193818.1730243503879.1.CFgPGGCnikQO4QvByCdlecpDraGFV.3; wp_s=T.1.1730243191.1730243504.1.3.0.3; permutive-id=fcbf0efb-e70c-4abe-8ab7-cb51528da343; __gads=ID=6dce38fa5d375dc5:T=1730243195:RT=1730243507:S=ALNI_MYS4T6FeM-iF1VpanfHwJD6vlE25Q; __gpi=UID=00000f42ecbba565:T=1730243507:RT=1730243507:S=ALNI_MYHEHthVTbsYBB743HE98rnI2HHJg; __eoi=ID=338f670e734f0d3b:T=1730243507:RT=1730243507:S=AA-AfjYKXqkMSGCiVjxhqpHVF1bb; _ga_WRCN68Y2LD=GS1.1.1730243194.1.1.1730243505.0.0.0; _ga_FKYRQ5TJZM=GS1.1.1730243506.1.1.1730243668.0.0.0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

response = requests.get('https://publicnotices.washingtonpost.com/', headers=headers)

print(response.text)

soup = BeautifulSoup(response.text, "lxml")
print(soup.prettify())
forms_json = soup.find("script", {"id": "__NEXT_DATA__"}).contents[0]
forms_json = json.loads(str(forms_json))
print(json.dumps(forms_json, indent=4))