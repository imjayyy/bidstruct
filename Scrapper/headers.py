


cat_codes = {
    "CODES": [  "236220",
                "236210",
                "237310",
                "236116",
                "236115",
                "237990",
                "237130",
                "237110",
                "237120",
                "238310",
                "238210",
                "328990",
                "238350",
                "238330",
                "238130",
                "238150",
                "238140",
                "238390",
                "238320",
                "238220",
                "238110",
                "238160",
                "238170",
                "238910",
                "238120",
                "238340" ]
}


def get_headers(urlPortal, cookie_str, visitId = "52631901"):
    new_headers = {
        'Authority' : 'pbsystem.planetbids.com',
        'Method' : 'GET',
        'accept':'application/vnd.api+json',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control':'no-cache',
        'company-id':str(urlPortal),
        'cookie': cookie_str,
        'dnt':'1',
        'em-version':'1.2.8',
        'pragma':'no-cache',
        'referer':f'https://pbsystem.planetbids.com/portal/{urlPortal}/bo/bo-search',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile':'?1',
        'sec-ch-ua-platform':'"Android"',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
        'vendor-id':'null',
        'vendor-login-id':'null',
        'visit-id': str(visitId)
        }
    return new_headers
