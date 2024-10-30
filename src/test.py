import requests

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://publicnotices.washingtonpost.com',
    'priority': 'u=1, i',
    'referer': 'https://publicnotices.washingtonpost.com/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

json_data = {
    'search': ' ',
    'allFilters': [
        {
            'publishedtimestamp': {
                'from': 1727608795778,
                'to': 1730287195778,
            },
        },
        {
            'newspapername': [
                'The Washington Post',
            ],
        },
        {
            'county': [
                'Arlington',
                'Arlington County',
                'Washington',
            ],
        },
    ],
    'noneFilters': [
        {
            'all': [
                {
                    'county': 'Washington',
                },
                {
                    'noticetype': 'Trustee Sale',
                },
            ],
        },
    ],
    'sort': [
        {
            'publishedtimestamp': 'desc',
        },
    ],
    'pageSize': 20,
    'isDemo': True,
}

response = requests.post(
    'https://us-central1-enotice-demo-8d99a.cloudfunctions.net/api/search/public-notices',
    headers=headers,
    json=json_data,
)
print(response.json())

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
# data = '{"search":" ","allFilters":[{"publishedtimestamp":{"from":1727608795778,"to":1730287195778}},{"newspapername":["The Washington Post"]},{"county":["Arlington","Arlington County","Washington"]}],"noneFilters":[{"all":[{"county":"Washington"},{"noticetype":"Trustee Sale"}]}],"sort":[{"publishedtimestamp":"desc"}],"pageSize":20,"isDemo":true}'
# response = requests.post(
#    'https://us-central1-enotice-demo-8d99a.cloudfunctions.net/api/search/public-notices',
#    headers=headers,
#    data=data,
# )
# print(response.json())