portal_data = {

    "portal": "41481",
    "portal_data": [
        {
            "CategoriesList": [
                "237187 - Engineering Services",
                "237191 - Surveying and Mapping (except Geophysical) Services",
                "237196 - Other Specialized Design Services",
                "237206 - Environmental Consulting Services"
            ],
            "County": "Los Angeles",
            "bidDueDate": "2023-12-12 15:00:00.000",
            "bidId": 111500,
            "bidResponseFormat": 3,
            "bidResponseFormatStr": "Electronic and Paper",
            "bidTemplateType": 4,
            "bidTypeId": 4,
            "byInvitation": False,
            "categoryIds": "541330, 541370, 541490, 541620",
            "companyId": 41481,
            "estimatedBid": "",
            "invitationNum": "PR-RFP-035",
            "issueDate": "2023-11-07 12:45:22.337",
            "page_scrape": 1,
            "stageId": 3,
            "stageStr": "Bidding",
            "title": "On-Call Plan Check Services",
            "url": "https://pbsystem.planetbids.com/portal/41481/bo/bo-detail/111500"
        },
        {
            "CategoriesList": [
                "237187 - Engineering Services",
                "237201 - Administrative Management and General Management Consulting Services",
                "237205 - Other Management Consulting Services",
                "237419 - Public Finance Activities",
                "237437 - Administration of Urban Planning and Community and Rural Development",
                "237558 - Land Subdivision"
            ],
            "County": "Los Angeles",
            "bidDueDate": "2024-01-11 12:00:00.000",
            "bidId": 112227,
            "bidResponseFormat": 1,
            "bidResponseFormatStr": "Electronic",
            "bidTemplateType": 4,
            "bidTypeId": 4,
            "byInvitation": False,
            "categoryIds": "237210, 541330, 541611, 541618, 921130, 925120",
            "companyId": 41481,
            "estimatedBid": "",
            "invitationNum": "PR-CED-004",
            "issueDate": "2023-12-04 11:12:08.100",
            "page_scrape": 1,
            "stageId": 3,
            "stageStr": "Bidding",
            "title": "Development Impact Fee Study",
            "url": "https://pbsystem.planetbids.com/portal/41481/bo/bo-detail/112227"
        }
    ],
    "time": "Thu, 07 Dec 2023 21:48:28 GMT"
}




for data in portal_data['portal_data']:
    print(data['url'])
    print(data['CategoriesList'])
    print(data['County'])