from unittest.mock import MagicMock, patch
import pytest

from openai import OpenAI

from main import (
    get_openai_client,
    get_picker_code,
    get_stock_info_from_picker,
    get_summary_from_web_result_with_stock_info,
    get_web_search_result_from_query,
    get_openai_api_key,
    get_web_search_keyword_from_user_query,
    print_summary,
    test_scenario,
)
from settings.settings import settings


def test_get_openai_client() -> None:
    client = get_openai_client()
    assert isinstance(client, OpenAI)
    assert client.api_key == settings.openai_api_key


@pytest.mark.parametrize(
    "query, expected",
    [
        ("엔비디아 주가", "엔비디아 최신 뉴스 정보"),
        ("마이크로소프트 주가", "마이크로소프트 최신 뉴스 정보"),
        ("애플 주가", "애플 최신 뉴스 정보"),
    ],
)
def test_get_web_search_keyword_from_user_query(query: str, expected: str) -> None:
    mock_client = MagicMock(spec=OpenAI)
    mock_response = MagicMock()
    mock_response.choices[0].message.content = expected
    mock_client.chat.completions.create.return_value = mock_response

    assert get_web_search_keyword_from_user_query(mock_client, query) == expected
    mock_client.chat.completions.create.assert_called_once()


@pytest.mark.parametrize(
    "query, expected",
    [
        ("엔비디아", "NVDA"),
        ("마이크로소프트", "MSFT"),
        ("애플", "AAPL"),
    ],
)
def test_get_picker_code(query: str, expected: str) -> None:
    mock_client = MagicMock(spec=OpenAI)
    mock_response = MagicMock()
    mock_response.choices[0].message.content = expected
    mock_client.chat.completions.create.return_value = mock_response

    assert get_picker_code(mock_client, query) == expected
    mock_client.chat.completions.create.assert_called_once()


@pytest.mark.parametrize(
    "query",
    [
        "엔비디아 기업 정보",
        "마이크로소프트 기업 정보",
        "애플 기업 정보",
    ],
)
def test_get_web_search_result_from_query(query: str) -> None:
    mock_ddgs_instance = MagicMock()
    mock_search_results = [{"body": f"Mocked result for {query}"}]
    mock_ddgs_instance.text.return_value = mock_search_results

    with patch("main.DDGS", return_value=mock_ddgs_instance) as mock_ddgs_client:
        assert get_web_search_result_from_query(query) == f"Mocked result for {query}"
        mock_ddgs_client.assert_called_once_with()
        mock_ddgs_instance.text.assert_called_once_with(query, max_results=5)


@pytest.mark.parametrize(
    "picker",
    [
        "NVDA",
        "MSFT",
        "APPL",
    ],
)
def test_get_stock_info_from_picker(picker: str) -> None:
    mock_ticker_instance = MagicMock()
    mock_ticker_instance.info = f"Mocked stock info for {picker}"

    with patch(
        "main.yf.Ticker", return_value=mock_ticker_instance
    ) as mock_ticker_class:
        assert get_stock_info_from_picker(picker) == f"Mocked stock info for {picker}"
        mock_ticker_class.assert_called_with(picker)


# def test_get_openai_api_key() -> None:

#     assert len(get_openai_api_key()) > 0


def test_get_summary_from_web_result_with_stock_info() -> None:
    mock_llm_client = MagicMock(spec=OpenAI)
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Mocked Summary"
    mock_llm_client.chat.completions.create.return_value = mock_response

    web_result = "Mocked web client"
    stock_info = "Mocked stock info"

    summary = get_summary_from_web_result_with_stock_info(
        mock_llm_client, web_result, stock_info
    )

    assert summary == "Mocked Summary"
    mock_llm_client.chat.completions.create.assert_called_once()


def test_print_summary(capfd) -> None:
    summary = "This is a test summary."
    print_summary(summary)
    captured = capfd.readouterr()
    assert captured.out == f"Summary: {summary}\n"
    assert captured.err == ""


def test_test_scenario() -> None:
    with patch("main.get_openai_client") as mock_get_openai_client, patch(
        "main.get_web_search_keyword_from_user_query"
    ) as mock_get_web_search_keyword, patch(
        "main.get_web_search_result_from_query"
    ) as mock_get_web_search_result, patch(
        "main.get_picker_code"
    ) as mock_get_picker_code, patch(
        "main.get_stock_info_from_picker"
    ) as mock_get_stock_info_from_picker, patch(
        "main.get_summary_from_web_result_with_stock_info"
    ) as mock_get_summary:

        mock_llm_client = MagicMock(spec=OpenAI)
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Mocked Result"
        mock_llm_client.chat.completions.create.return_value = mock_response

        mock_get_openai_client.return_value = mock_llm_client
        mock_get_web_search_keyword.return_value = "엔비디아 최신 뉴스 정보"
        mock_get_web_search_result.return_value = "Mocked web result"
        mock_get_picker_code.return_value = "NVDA"
        mock_get_stock_info_from_picker.return_value = "Mocked stock info"
        mock_get_summary.return_value = "Mocked summary"

        test_scenario()

        mock_get_openai_client.assert_called_once()
        mock_get_web_search_keyword.assert_called_once_with(
            mock_llm_client, "엔비디아 주가"
        )
        mock_get_web_search_result.assert_called_once_with("엔비디아 최신 뉴스 정보")
        mock_get_picker_code.assert_called_once_with(mock_llm_client, "엔비디아 주가")
        mock_get_stock_info_from_picker.assert_called_once_with("NVDA")
        mock_get_summary.assert_called_once_with(
            mock_llm_client, "Mocked web result", "Mocked stock info"
        )
