from typing import Callable

import yfinance as yf
from ddgs import DDGS
from openai import OpenAI

from settings.settings import settings


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=settings.openai_api_key)


# DI 패턴 쓸 예정
def get_web_search_keyword_from_user_query(llm_client: OpenAI, query: str) -> str:
    prompt = f"Generate a search keyword for the query: {query}"
    response = llm_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
    )
    return response.choices[0].message.content.strip()


def get_picker_code(llm_client: OpenAI, query: str) -> str:
    prompt = f"Extract the stock ticker code from the query: {query}"
    response = llm_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
    )
    return response.choices[0].message.content.strip()


def get_web_search_result_from_query(query: str) -> str:
    results = DDGS().text(query, max_results=5)
    # print(type(results))
    # print(results)
    return results[0]["body"] if results else "No results found"


def get_stock_info_from_picker(ticker: str) -> str:
    dat = yf.Ticker(ticker)
    return dat.info


def get_openai_api_key() -> str:
    return settings.openai_api_key


# # 리펙토링 케이스
# class Pipe:
#     def __init__(self, name: str):
#         self.name = name

#     def add_llm(self, llm_model: OpenAI) -> None:
#         self.llm_model = llm_model

#     def add_step(self, step: str) -> None:
#         print(f"Adding step: {step} to pipe: {self.name}")

#     def run(self, query: str) -> str:
#         return f"Running {self.name} with query: {query}"


def get_summary_from_web_result_with_stock_info(
    llm_client: OpenAI, web_result: str, stock_info: str
) -> str:
    prompt = f"Summarize the following web result with stock info:\nWeb Result: {web_result}\nStock Info: {stock_info}"
    response = llm_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
    )
    return response.choices[0].message.content.strip()


def print_summary(summary: str) -> None:
    print(f"Summary: {summary}")


# pipe = Pipe("")
# pipe.add_llm(get_openai_api_key)

# 1-A. 웹 검색을 위한 검색 키워드를 LLM으로 부터 얻어온다. (get_web_search_keyword_from_user_query)
# 2-A. 검색 키워드를 기반으로 DuckDuckGo에서 검색 결과를 얻어온다. (get_web_search_result_from_picker)
# 1-B. 주가 정보 검색을 위해 피커 정보를 get_picker_code로 부터 얻어온다.
# 2-B. 피커 정보를 기반으로 yfinance를 이용하여 주가 정보를 얻어온다.
# 3. get_summary_from_web_result_with_stock_info 함수를 이용하여 웹 검색 결과와 주가 정보를


def test_scenario() -> None:
    query = "엔비디아 주가"
    llm_client = get_openai_client()

    # Step 1-A
    search_keyword = get_web_search_keyword_from_user_query(llm_client, query)

    # Step 2-A
    web_result = get_web_search_result_from_query(search_keyword)

    # Step 1-B
    picker_code = get_picker_code(llm_client, query)

    # Step 2-B
    stock_info = get_stock_info_from_picker(picker_code)

    # Step 3
    summary = get_summary_from_web_result_with_stock_info(
        llm_client, web_result, stock_info
    )

    # Step 4
    print_summary(summary)


if __name__ == "__main__":
    test_scenario()
