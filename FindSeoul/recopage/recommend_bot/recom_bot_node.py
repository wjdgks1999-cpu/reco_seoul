from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate,PromptTemplate, MessagesPlaceholder
from langchain_core.messages import ToolMessage, AIMessage
from pinecone import PineconeAsyncio
from langchain_pinecone import PineconeVectorStore

from FindSeoul.DB_connection import SessionLocal
from FindSeoul.DB_model import IdTable
from FindSeoul.recopage.recommend_bot.recom_bot_state import Recommend_Graph_State
from FindSeoul.data_model import TravelInfo, UserPreferences, EvaluationSpot, RecommendationResponse, Search_List

import os
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
openai_key = os.getenv('OPENAI_API_KEY', '')
pinecone_key = os.getenv('PINECONE_API_KEY', '')
pinecone_host = os.getenv('PINECONE_HOST', '')
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=openai_key)

#%% 2. 노드 : Scoring Agent
#(1). 프롬프트 구성
with open("FindSeoul/recopage/recommend_bot/prompt/reform_prompt_v3_ko.md", "r", encoding="utf-8") as f:
    reform_template = f.read()
reform_system = SystemMessagePromptTemplate.from_template(reform_template)

scoring_prompt = ChatPromptTemplate.from_messages([
    reform_system,
    MessagesPlaceholder(variable_name="conversation_history")
])

#(2). 대화 기록 처리 함수
def reform(messages_list : list):
    filtered_messages = [
        msg for msg in messages_list 
        if not (
            isinstance(msg, ToolMessage) or 
            (hasattr(msg, "tool_calls") and len(msg.tool_calls) > 0)
        )
    ]
    return filtered_messages

#(3). scoring agent 노드
async def scoring_agent(state: Recommend_Graph_State) -> Recommend_Graph_State :
    try:
        messages_list = state['messages']
        conversation_history = reform(messages_list)
        travel_purpose = state['travel_info'].travel_purpose
        
        input_data = {
            'travel_purpose' : travel_purpose,
            'conversation_history' : conversation_history
        }
        
        llm = ChatOpenAI(model="o3-mini", api_key=openai_key)
        
        preferences = await (scoring_prompt | llm.with_structured_output(UserPreferences)).ainvoke(
            input_data
        )
        return {"user_preferences": preferences}
    
    except Exception as e :
        return {
            "error": {
                "node": "scoring_agent",
                "message": str(e),
                "type": type(e).__name__
            }
        }

#%% 3. 노드 : first_analysis_agent
#(1). 프롬프트 구성
with open("FindSeoul/recopage/recommend_bot/prompt/first_analyze_prompt_ko.md", "r", encoding="utf-8") as f:
    first_analysis_template = f.read()
first_analysis_prompt = PromptTemplate.from_template(first_analysis_template)

#(2). first_analysis_agent 노드
async def first_analysis_agent(state : Recommend_Graph_State) -> Recommend_Graph_State :
    try :
        k = state["travel_info"].desired_daily_destinations * state["travel_info"].stay_duration * 2
        language = state['lang']
        user_info = state['travel_info'].user
        companions_info = state['travel_info'].companions
        travel_purpose = state['travel_info'].travel_purpose
        user_preferences = state['user_preferences']
        
        input_data = {
            'language' : language,
            'k' : k,
            'user_info' : user_info,
            'companions_info' : companions_info,
            'travel_purpose' : travel_purpose,
            'user_preferences' : user_preferences
        }
        
        llm = ChatOpenAI(model="o3-mini", api_key=openai_key)
        search_queries = await (first_analysis_prompt | llm.with_structured_output(Search_List)).ainvoke(
            input_data
            )
        return {"search_queries" : search_queries}
    
    except Exception as e :
        return {
            "error": {
                "node": "first_analysis_agent",
                "message": str(e),
                "type": type(e).__name__
            }
        }

#%% 4. 노드 : Retrieval Node
async def retrieval_node(state: Recommend_Graph_State) -> Recommend_Graph_State :
    try : 
        language = state.get('lang', 'en')
        if state.get('add_search_queries', None) :
            search_queries = state['add_search_queries']
            #1. 검색 실시
            searched_results = []
            async with PineconeAsyncio(api_key=pinecone_key) as pc :
                    for query in search_queries.search_queries :
                        query = query.search_query
                        async with pc.IndexAsyncio(host=pinecone_host) as idx :
                            vector_store = PineconeVectorStore(index=idx, embedding=embeddings, namespace=language)
                            retriever = vector_store.as_retriever(
                                    search_type="similarity", search_kwargs={'k': 3})
                            search_results = await retriever.ainvoke(query)
                        searched_results = searched_results + search_results
            #2. 이전 검색 결과와 결합
            previous_search_results = state['search_results']
            now_search_results = previous_search_results + searched_results
            #3. 중복 제거
            unique_results = {}
            for item in now_search_results :
                spot_id = item.metadata['id']
                if spot_id not in unique_results :
                    unique_results[spot_id] = item
            #4. 검색어 리스트 리뉴얼
            previous_search_queries = state['search_queries']
            new_search_queries = Search_List.model_construct(
                                search_queries = previous_search_queries.search_queries + search_queries.search_queries)                  
            
            return {"search_results": list(unique_results.values()), #추가한 목록 반영
                    "add_search_queries" : None,#add_search_queries 초기화
                    "search_queries" : new_search_queries,#search_queries에 추가된 검색어들 추가
                    }
        else :
            search_queries = state['search_queries']
            #1. 검색 실시
            searched_results = []
            async with PineconeAsyncio(api_key=pinecone_key) as pc :
                    for query in search_queries.search_queries :
                        query = query.search_query
                        async with pc.IndexAsyncio(host=pinecone_host) as idx :
                            vector_store = PineconeVectorStore(index=idx, embedding=embeddings, namespace=language)
                            retriever = vector_store.as_retriever(
                                    search_type="similarity", search_kwargs={'k': 3})
                            search_results = await retriever.ainvoke(query)
                        searched_results = searched_results + search_results
            #2. 중복 제거
            unique_results = {}
            for item in searched_results :
                spot_id = item.metadata['id']
                if spot_id not in unique_results :
                    unique_results[spot_id] = item
                    
            return {"search_results": list(unique_results.values())}
    except Exception as e:
        return {
            "error": {
                "node": "retrieval_node",
                "message": str(e),
                "type": type(e).__name__
            }
        }
        
#%% 5. 노드 : add_analysis_agents
#(1). 프롬프트 구성
with open("FindSeoul/recopage/recommend_bot/prompt/add_analyze_prompt_ko.md", "r", encoding="utf-8") as f:
    add_analysis_template = f.read()
add_analysis_prompt = PromptTemplate.from_template(add_analysis_template)

#(2). add_analysis_agent
async def add_analysis_agent(state : Recommend_Graph_State) -> Recommend_Graph_State :
    try :
        origin_k = state["travel_info"].desired_daily_destinations * state["travel_info"].stay_duration * 2
        completed_k = len(state['search_results'])
        k = origin_k - completed_k
        
        language = state['lang']
        user_info = state['travel_info'].user
        companions_info = state['travel_info'].companions
        travel_purpose = state['travel_info'].travel_purpose
        user_preferences = state['user_preferences']
        previous_queries = state['search_queries'].search_queries
        
        input_data = {
            'companions_info' : companions_info,
            'k' : k,
            'language' : language,
            'previous_queries' : previous_queries,
            'travel_purpose' : travel_purpose,
            'user_info' : user_info,
            'user_preferences' : user_preferences
        }
        llm = ChatOpenAI(model="o3-mini", api_key=openai_key)
        search_queries = await (add_analysis_prompt | llm.with_structured_output(Search_List)).ainvoke(
            input_data
            )
        return {"add_search_queries": search_queries}
    
    except Exception as e :
        return {
            "error": {
                "node": "add_analysis_agent",
                "message": str(e),
                "type": type(e).__name__
            }
        }
#%% 6. 노드 : evaluation_agent
with open("FindSeoul/recopage/recommend_bot/prompt/evaluator_prompt_v2_ko.md", "r", encoding="utf-8") as f:
    evaluate_template = f.read()
evaluate_prompt = PromptTemplate.from_template(evaluate_template)

#(2).evaluation_agent
async def evaluation_agent(state : Recommend_Graph_State) -> Recommend_Graph_State :
    try : 
        if state.get('rewrite_search_results') :
            #1. 입력값 설정
            language = state['lang']
            user_info = state['travel_info'].user
            companions_info = state['travel_info'].companions
            travel_purpose = state['travel_info'].travel_purpose
            user_preferences = state['user_preferences']
            rewrite_search_results = state['rewrite_search_results']
            
            input_data = {
                'companions_info' : companions_info,
                'language' : language,
                'search_results' : rewrite_search_results,
                'travel_purpose' : travel_purpose,
                'user_info' : user_info,
                'user_preferences' : user_preferences
            }
            
            #2. 평가 실행
            llm = ChatOpenAI(model="o3-mini", api_key=openai_key)
            evaluations = await (evaluate_prompt | llm.with_structured_output(EvaluationSpot)).ainvoke(
                input_data)
            evaluated_list = evaluations.evaluated_spots
            
            #3. 패스, 드랍 나누기
            new_passed_spots = []
            new_dropped_spots = []
            for evaluated_spot in evaluated_list :
                if evaluated_spot.matching_score >= 60 :
                    new_passed_spots.append(evaluated_spot)
                else :
                    new_dropped_spots.append(evaluated_spot)
            
            #4. 과거 평가 결과에 결합
            past_passed_spots = state['passed_spots']
            past_dropped_spots = state['dropped_spots']
            passed_spots = past_passed_spots + new_passed_spots
            dropped_spots = past_dropped_spots + new_dropped_spots
            
            #5. search_results 리뉴얼
            new_search_results = state['search_results'] + state['rewrite_search_results']
            return {"passed_spots": passed_spots,
                    "dropped_spots" : dropped_spots,
                    "search_results" : new_search_results,
                    "rewrite_search_results" : None}
        else :
            #1. 입력값 설정
            language = state['lang']
            user_info = state['travel_info'].user
            companions_info = state['travel_info'].companions
            travel_purpose = state['travel_info'].travel_purpose
            user_preferences = state['user_preferences']
            search_results = state['search_results']
            
            input_data = {
                'companions_info' : companions_info,
                'language' : language,
                'search_results' : search_results,
                'travel_purpose' : travel_purpose,
                'user_info' : user_info,
                'user_preferences' : user_preferences
            }
            
            #2. 평가 실행
            llm = ChatOpenAI(model="o3-mini", api_key=openai_key)
            evaluations = await (evaluate_prompt | llm.with_structured_output(EvaluationSpot)).ainvoke(
                input_data)
            evaluated_list = evaluations.evaluated_spots
            
            #3. 패스, 드랍 나누기
            passed_spots = []
            dropped_spots = []

            for evaluated_spot in evaluated_list :
                if evaluated_spot.matching_score >= 60 :
                    passed_spots.append(evaluated_spot)
                else :
                    dropped_spots.append(evaluated_spot)
                    
            return {"passed_spots": passed_spots,
                    "dropped_spots" : dropped_spots}
    except Exception as e :
        return {
            "error": {
                "node": "evaluation_agent",
                "message": str(e),
                "type": type(e).__name__
            }
        }
#%% 7. 노드 : Rewrite Agent
#(1). 프롬프트 구성
with open("FindSeoul/recopage/recommend_bot/prompt/rewrite_prompt_ko.md", "r", encoding="utf-8") as f:
    rewrite_analyze_template = f.read()
rewrite_analyze_prompt = PromptTemplate.from_template(rewrite_analyze_template)

async def rewrite_agent(state : Recommend_Graph_State) -> Recommend_Graph_State :
    try :
        #1. 입력정보 설정
        if state.get('rewrite_search_results') :
            origin_k = state["travel_info"].desired_daily_destinations * state["travel_info"].stay_duration * 2
            completed_k = len(state['passed_spots']) + len(state['rewrite_search_results'])
            p = origin_k - completed_k
        else :    
            origin_k = state["travel_info"].desired_daily_destinations * state["travel_info"].stay_duration * 2
            completed_k = len(state['passed_spots'])
            p = origin_k - completed_k
        language = state['lang']
        user_info = state['travel_info'].user
        companions_info = state['travel_info'].companions
        travel_purpose = state['travel_info'].travel_purpose
        user_preferences = state['user_preferences']
        previous_queries = state['search_queries'].search_queries
        passed_spots = state['passed_spots']
        dropped_spots = state['dropped_spots']

        input_data = {
            'companions_info' : companions_info,
            'dropped_spots' : dropped_spots,
            'language' : language,
            'p': p,
            'passed_spots' : passed_spots,
            'previous_queries': previous_queries,
            'travel_purpose' : travel_purpose,
            'user_info' : user_info,
            'user_preferences' : user_preferences
        }

        #2. 검색쿼리 생성
        llm = ChatOpenAI(model="o3-mini", api_key=openai_key)
        search_queries = await (rewrite_analyze_prompt | llm.with_structured_output(Search_List)).ainvoke(
            input_data)
        return {"add_search_queries" : search_queries}
    except Exception as e :
        return {
            "error": {
                "node": "rewrite_agent",
                "message": str(e),
                "type": type(e).__name__
            }
        }

#%% 8. 노드 : Rewrite 검색기
async def rewrite_retrieval_node(state : Recommend_Graph_State) -> Recommend_Graph_State :
    try :
        language = state['lang']
        search_queries = state['add_search_queries']

        #1. 검색 실시
        searched_results = []
        async with PineconeAsyncio(api_key=pinecone_key) as pc :
                for query in search_queries.search_queries :
                    query = query.search_query
                    async with pc.IndexAsyncio(host=pinecone_host) as idx :
                        vector_store = PineconeVectorStore(index=idx, embedding=embeddings, namespace=language)
                        retriever = vector_store.as_retriever(
                                search_type="similarity", search_kwargs={'k': 3})
                        search_results = await retriever.ainvoke(query)
                    searched_results = searched_results + search_results
        #2. 중복제거
        if state.get('rewrite_search_results') :
            previous_search_results = state['search_results'] + state['rewrite_search_results']
            previous_search_list= [doc.metadata['id'] for doc in previous_search_results]
            unique_new_item = []
            for item in searched_results :
                spot_id = item.metadata['id']
                if spot_id not in previous_search_list :
                    unique_new_item.append(item)
            add_new_item = state['rewrite_search_results'] + unique_new_item
        else :
            previous_search_results = state['search_results']
            previous_search_list= [doc.metadata['id'] for doc in previous_search_results]
            unique_new_item = []
            for item in searched_results :
                spot_name = item.metadata['id']
                if spot_name not in previous_search_list :
                    unique_new_item.append(item)
            add_new_item = unique_new_item
        
        #3. 검색어 리스트 리뉴얼
        previous_search_queries = state['search_queries']
        new_search_queries = Search_List.model_construct(
                            search_queries = previous_search_queries.search_queries + search_queries.search_queries)
        
        return {"rewrite_search_results": add_new_item, #추가한 목록 반영
                "add_search_queries" : None,#add_search_queries 초기화
                "search_queries" : new_search_queries,#search_queries에 추가된 검색어들 추가
                }
        
    except Exception as e :
        return {
            "error": {
                "node": "rewrite_retrieval_node",
                "message": str(e),
                "type": type(e).__name__
            }
        }

#%% 9. 노드 : recommendation agent
#(1). 프롬프트 구성
with open("FindSeoul/recopage/recommend_bot/prompt/reco_prompt_v2_ko.md", "r", encoding="utf-8") as f:
    reco_template = f.read()
reco_prompt = PromptTemplate.from_template(reco_template)

async def recommendation_node(state: Recommend_Graph_State) -> Recommend_Graph_State:
    try :
        #1. 입력값 구성
        language = state['lang']
        user_info = state['travel_info'].user
        companions_info = state['travel_info'].companions
        travel_purpose = state['travel_info'].travel_purpose
        user_preferences = state['user_preferences']

        recommend_items = state['passed_spots']
        info_items = state['search_results']

        info_evaluation_docs = []
        for recommend_item in recommend_items :
            for info_item in info_items :
                if info_item.metadata['spot_name'] == recommend_item.spot_name :
                    target_info = info_item
                    if target_info.metadata.get('subcategory') : 
                        info_evaluation_doc = {
                            'id' : target_info.metadata['id'],
                            'spot_name' : recommend_item.spot_name,
                            'category' : target_info.metadata['category'],
                            'subcategory' : target_info.metadata['subcategory'],
                            'description' : target_info.metadata['descriptions'],
                            'evaluation_score' : recommend_item.matching_score,
                            'evaluation_reason' : recommend_item.evaluation_reason,
                        }
                        info_evaluation_docs.append(info_evaluation_doc)
                    else :
                        info_evaluation_doc = {
                            'id' : target_info.metadata['id'],
                            'spot_name' : recommend_item.spot_name,
                            'category' : target_info.metadata['category'],
                            'description' : target_info.metadata['descriptions'],
                            'evaluation_score' : recommend_item.matching_score,
                            'evaluation_reason' : recommend_item.evaluation_reason,
                        }
                        info_evaluation_docs.append(info_evaluation_doc)

        input_data = {
            'companions_info' : companions_info,
            'info_evaluation_docs' : info_evaluation_docs,
            'language' : language,
            'travel_purpose' : travel_purpose,
            'user_info' : user_info,
            'user_preferences' : user_preferences
        }

        #2. 평가
        llm = ChatOpenAI(model="o3-mini", api_key=openai_key)
        reco_results = await (reco_prompt | llm.with_structured_output(RecommendationResponse)).ainvoke(
                     input_data)
        return {"reco_results": reco_results,
                "info_evaluation_docs" : info_evaluation_docs}
    except Exception as e:
        return {
            "error": {
                "node": "recommendation_node",
                "message": str(e),
                "type": type(e).__name__
            }
        }
#%% 10. 노드 : final_node
async def final_node(state: Recommend_Graph_State) -> Recommend_Graph_State :
    try : 
        #(1). 기본정보 세팅
        language = state['lang']
        info_docs = state['info_evaluation_docs']
        reco_results = state['reco_results']
        reco_results_dict = reco_results.model_dump()
        reco_results_list = reco_results_dict['recommendations']

        #(2). 1차 정리
        first_final_results = []
        for reco_result in reco_results_list :
            target_spot_id = reco_result['id']
            for info in info_docs :
                first_final_result = None
                if info['id'] == target_spot_id :
                    first_final_result = info.copy()
                    first_final_result['recommend_mention'] = reco_result['recommend_mention']
                    first_final_results.append(first_final_result)

        #(3). 추가정보를 DB로부터 불러오기
        items_id_list = [item['id'] for item in first_final_results]

        with SessionLocal() as session :
            rows = (
                session.query(IdTable)
                .filter(IdTable.original_id.in_(items_id_list))
                .all()
            )
            
        # 각 객체에서 원하는 필드만 꺼내 dict로 변환
        items_add_info = []
        if language == "ko" :
            for r in rows:
                obj = {
                    "original_id"       : r.original_id,
                    "google_maps_uri"   : r.google_maps_uri,
                    "image_url"         : r.image_url,
                    "formatted_address" : r.formatted_address,
                    "latitude"          : r.latitude,
                    "longitude"         : r.longitude,
                    "content_url"    : r.content_url_ko
                }
                items_add_info.append(obj)
        else : 
            for r in rows:
                obj = {
                    "original_id"       : r.original_id,
                    "google_maps_uri"   : r.google_maps_uri,
                    "image_url"         : r.image_url,
                    "formatted_address" : r.formatted_address,
                    "latitude"          : r.latitude,
                    "longitude"         : r.longitude,
                    "content_url"    : r.content_url_en,
                }
                items_add_info.append(obj)     

        #(4). final_results 생성
        final_results = []
        for recommend_item in first_final_results :
            target_spot_id = recommend_item['id']
            for add_info in items_add_info :
                final_result = None
                if add_info['original_id'] == target_spot_id :
                    final_result = recommend_item.copy()
                    final_result['google_maps_uri'] = add_info['google_maps_uri']
                    final_result['image_url'] = add_info['image_url']
                    final_result['formatted_address'] = add_info['formatted_address']
                    final_result['latitude'] = add_info['latitude']
                    final_result['longitude'] = add_info['longitude']
                    final_result['content_url'] = add_info['content_url']
                    final_results.append(final_result)
        return {"final_results": final_results}
    except Exception as e:
        return {
            "error": {
                "node": "final_node",
                "message": str(e),
                "type": type(e).__name__
            }
        }

#%% 11. 노드 : error_node
async def error_handling_node(state):
    # 에러 정보 추출
    error = state.get("error", {})
    error_type = error.get("type", "UnknownError")
    error_message = error.get("message", "알 수 없는 오류가 발생했습니다.")
    error_node = error.get("node", "unknown_node")
    
    # 에러 유형별 사용자 친화적 메시지 생성
    user_friendly_message = ""
    
    # 에러 유형에 따른 분류 및 메시지 생성
    if "BadRequestError" in error_type:
        if "context_length_exceeded" in error_message or "maximum context length" in error_message:
            user_friendly_message = "입력 또는 대화 내용이 너무 깁니다. 더 짧은 내용으로 다시 시도해주세요."
        elif "rate_limit" in error_message:
            user_friendly_message = "API 요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요."
        elif "invalid content" in error_message.lower():
            user_friendly_message = "부적절한 내용이 감지되었습니다. 다른 방식으로 요청해주세요."
        else:
            user_friendly_message = "AI 모델 요청 처리 중 오류가 발생했습니다. 다른 방식으로 시도해보세요."
    
    elif "ValidationError" in error_type:
        # Pydantic 유효성 검증 오류
        if "missing" in error_message.lower():
            user_friendly_message = "필수 정보가 누락되었습니다. 모든 필요한 정보를 제공해주세요."
        elif "not a valid" in error_message.lower():
            user_friendly_message = "입력된 정보의 형식이 올바르지 않습니다. 다시 확인해주세요."
        else:
            user_friendly_message = "입력 데이터 검증에 실패했습니다. 입력 형식을 확인해주세요."
    
    elif "JSONDecodeError" in error_type:
        # JSON 파싱 오류
        user_friendly_message = "데이터 형식을 처리하는 중 오류가 발생했습니다. 시스템이 응답을 올바르게 해석하지 못했습니다."
    
    elif "OutputParserException" in error_type:
        # 출력 파싱 오류
        user_friendly_message = "AI의 응답을 적절한 형식으로 변환하는 데 실패했습니다. 다시 시도해주세요."
    
    elif "ConnectionError" in error_type:
        # 네트워크 연결 오류
        if "timeout" in error_message.lower():
            user_friendly_message = "서버 응답 시간이 초과되었습니다. 네트워크 상태를 확인하고 다시 시도해주세요."
        else:
            user_friendly_message = "네트워크 연결 중 오류가 발생했습니다. 인터넷 연결을 확인해주세요."
            
    elif "GraphRecursionError" in error_type:
        # LangGraph 그래프 순환 참조 오류
        user_friendly_message = "사용 횟수를 초과하였습니다. 관리자에게 문의하세요."

    elif "OpenAI" in error_type:
        # LangGraph 그래프 순환 참조 오류
        user_friendly_message = "API 키 관련 오류가 발생했습니다. 관리자에게 문의하세요."
    
    else:
        # 그 외 모든 에러
        user_friendly_message = "알 수 없는 오류가 발생했습니다. [새로운 채팅]으로 다시 시도해주세요."
    
    # 노드별 추가 정보 제공
    node_specific_info = ""
    if error_node == "request_collect_agent":
        node_specific_info = "사용자 선호도 수집 중 오류가 발생했습니다."
    elif error_node == "scoring_agent":
        node_specific_info = "사용자 선호도 분석 중 오류가 발생했습니다."
    elif error_node == "first_analysis_agent":
        node_specific_info = "초기 검색 쿼리 생성 중 오류가 발생했습니다."
    elif error_node == "add_analysis_agent":
        node_specific_info = "추가 검색 쿼리 생성 중 오류가 발생했습니다."
    elif error_node == "retrieval_node":
        node_specific_info = "관광지 정보 검색 중 오류가 발생했습니다."
    elif error_node == "evaluation_agent":
        node_specific_info = "관광지 평가 중 오류가 발생했습니다."
    elif error_node == "recommendation_node":
        node_specific_info = "추천 생성 중 오류가 발생했습니다."
    elif error_node == "final_node":
        node_specific_info = "최종 결과 생성 중 오류가 발생했습니다."
    
    # 최종 에러 메시지 조합
    final_error_message = f"{node_specific_info} {user_friendly_message}"
    
    # 메시지 목록에 에러 메시지 추가
    add_error_message = AIMessage(content = final_error_message)
    
    return {
        "messages": [add_error_message],
        "error_handled": True,  # 에러 처리 완료 표시
    }

#%%12. 상태 정의 함수
from langgraph.graph import END

def scoring_route(state) :
    error = state.get("error", None)
    if error :
        return "error_handling_node"
    return "first_analysis_agent"

def first_analysis_route(state) :
    error = state.get("error", None)
    if error :
        return "error_handling_node"
    return "retrieval_node"

def add_analysis_route(state) :
    error = state.get("error", None)
    if error :
        return "error_handling_node"
    return "retrieval_node"

def retrieval_route(state) :
    error = state.get("error", None)
    if error :
        return "error_handling_node"
    else : 
        threshold = state["travel_info"].desired_daily_destinations * state["travel_info"].stay_duration * 2
        num_of_items = len(state['search_results'])
        if num_of_items >= threshold :
            return "evaluation_agent"
        else :
            return "add_analysis_agent"

def evaluation_route(state) :
    error = state.get("error", None)
    if error :
        return "error_handling_node"
    else :
        threshold = state["travel_info"].desired_daily_destinations * state["travel_info"].stay_duration * 2
        num_of_passed = len(state['passed_spots'])
        if num_of_passed >= threshold :
            return "recommendation_node"
        else :
            return "rewrite_agent"

def rewrite_agent_route(state) :
    error = state.get("error", None)
    if error :
        return "error_handling_node"
    return "rewrite_retrieval_node"

def rewrite_retrieval_route(state) :
    error = state.get("error", None)
    if error :
        return "error_handling_node"
    else :
        threshold = state["travel_info"].desired_daily_destinations * state["travel_info"].stay_duration * 2
        num_of_passed = len(state['passed_spots'])
        num_of_new = len(state["rewrite_search_results"])
        if (num_of_new + num_of_passed) >= threshold :
            return "evaluation_agent"
        else :
            return "rewrite_agent"

def recommendation_route(state) :
    error = state.get("error", None)
    if error :
        return "error_handling_node"
    return 'final_node'

def final_route(state) :
    error = state.get("error", None)
    if error :
        return "error_handling_node"
    return END