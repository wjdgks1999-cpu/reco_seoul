reco_translation = {
    "ko": {
        "start_ment": """
        지금부터 관광지 추천을 위한 분석을 시작하겠습니다. 
        순서는 유저님의 선호도 분석 -> 선호도와 매칭되는 관광지 검색 -> 검색된 관광지 평가 -> 최종 추천 순으로 진행됩니다.
        """,
        "user_preferences_ment" : "지난 대화 내역을 분석하여 유저님의 선호도를 정리했습니다~!~!~!",
        "search_results_ment" : "유저님의 목적 및 선호도에 기반하여 관광지를 검색하였습니다~!~!~!",
        'add_analysis_ment' : "관광지 개수가 충분하지 않아 재검색하고 있어요~!~!~!",
        "evaluation_ment" : "검색한 관광지가 유저님에게 적절한지 평가해보았습니다~!~!~!~!",
        'recommendation_ment' : '추천할 모든 관광지 정보를 선정했습니다. 관광지 정보를 정리합니다.',
        'error_ment' : '예상치 못한 시스템 문제가 발생하였습니다. 에러 페이지로 이동합니다.',
        "end_ment" : """
            유저님만을 위한 추천 관광지가 완성되었어요!
            저의 역할은 여기까지입니다. 즐거운 서울 여행되세요~~!~!~!
        """,
        "preferences_item_text" : ["카테고리", "세부항목", "관심도", "신뢰도", "점수 산정 근거"],
        "search_results_card_text" : ["관광지명", "관광지 종류", "관광지 소개"],
        "evaluation_card_text" : ['관광지명', '평가 점수', '평가 이유', '패스한 관광지', '드랍된 관광지'],
        "tourist_spot_card_text": ['관광지 종류', '관광지 설명', '유저님을 위한 추천', '유저님과의 매칭 수준',
                                   '관광지 주소', 'VISIT SEOUL의 소개', "VISIT SEOUL 소개 바로가기",
                                   "구글맵 URI", "구글맵 URI 바로가기"],
        "final_progress_button_text" : ['선호도 분석 결과', '관광지 검색 결과', '관광지 평가 결과', '유저님을 위한 추천']
    },
    "en": {
        "start_ment": "We will now begin the analysis for recommending tourist attractions. The process will proceed in the following order: analyzing your preferences → searching for attractions that match your preferences → evaluating the searched attractions → final recommendation.",
        "user_preferences_ment": "I've analyzed our past conversations and summarized your preferences!!!",
        "search_results_ment": "I've searched for tourist attractions based on your goals and preferences!!!",
        'add_analysis_ment' : "The number of tourist attractions is not enough, so we are researching again!!!",
        "evaluation_ment": "I've evaluated whether the searched attractions are suitable for you!!!!",
        'recommendation_ment' : 'We have selected all of your recommended destinations and are organizing your destination information.',
        'error_ment' : 'Unexpected system problem occurred. Go to the error page.',
        "end_ment": "Your personalized list of recommended tourist attractions is now complete! That's all I can do. Enjoy your trip to Seoul!!!",
        "preferences_item_text": ["Category", "Subcategory", "Interest Level", "Reliability", "Scoring Basis"],
        "search_results_card_text": ["Attraction Name", "Spot Category", "Spot Description"],
        "evaluation_card_text": ["Attraction Name", "Evaluation Score", "Evaluation Reason", "Passed Attractions", "Dropped Attractions"],
        "tourist_spot_card_text": ["Spot Category", "Spot Description", "Recommendation for You", "Match Level", "Address", "VISIT SEOUL' Introduction", "VISIT SEOUL Info Link", "Google Maps URI", "Google Maps Link"],
            "final_progress_button_text": ["Preference Analysis Results","Tourist Spot Search Results","Tourist Spot Evaluation Results","Recommendations for You"
    ]
    }
}