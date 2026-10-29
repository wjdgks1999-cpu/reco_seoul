from pydantic import BaseModel, Field
from typing import List, Dict, Optional

#1. 여행기본정보
class TravelInfo(BaseModel):
    user: str  = Field(description="사용자 본인의 연령대")
    companions: Optional[List[Dict]] = Field(None,description="함께 여행하는 동반자들의 정보 목록")
    check_in_date : str = Field(description="여행을 시작하는 날짜")
    check_out_date : str = Field(description="여행을 종료하는 날짜")
    stay_duration: int = Field(description="여행 체류 기간 (일 단위)")
    desired_daily_destinations: int = Field(description="하루에 방문하고 싶은 관광지 수")
    travel_purpose: list[str] = Field(description="여행의 주요 목적 및 선호활동")

#2. 유저 선호도 분석결과
class InterestCategory(BaseModel):
    interest_big_category : str = Field(description="관심 항목")
    interest_small_category : str = Field(description="세부 관심 항목")
    interest_level: Optional[int] = Field(None, description="관심도(1점-5점 척도)")
    confidence: float = Field(description="신뢰도 점수(0점-1점 척도)")
    reason : str = Field(description="관심도 부여 이유에 대한 설명")

class UserPreferences(BaseModel):
    preferences : List[InterestCategory]

#3. 검색어 폼
class Search_Query(BaseModel) :
    search_query : str = Field(description="추천 관광지 검색에 사용할 검색어")

class Search_List(BaseModel) :
    search_queries : List[Search_Query] = Field(description="추천 관광지 검색에 사용할 검색어 리스트")

#3. 검색 결과 평가 폼
class EvaluationForm(BaseModel):
    spot_name : str = Field(description="관광지명")
    matching_score: float = Field(description="0-100 사이의 매칭 점수")
    evaluation_reason: str = Field(description="점수 부여 이유에 대한 설명")

class EvaluationSpot(BaseModel) :
    evaluated_spots : List[EvaluationForm] = Field(description="평가된 관광지 리스트")

#4. 최종 추천 폼
class RecommendedSpot(BaseModel):
    """추천 관광지 정보"""
    id : str = Field(description = '관광지 아이디')
    spot_name: str = Field(description="관광지 이름")
    recommend_mention: str = Field(description="관광지에 대한 추천 멘트")

class RecommendationResponse(BaseModel):
    """추천 응답"""
    recommendations: List[RecommendedSpot] = Field(description="추천 관광지 목록")