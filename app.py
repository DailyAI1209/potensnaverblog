import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import re
import streamlit as st
import base64
from io import BytesIO

# Potens AI 테마 색상
POTENS_DARK_BLUE = "#1A237E"  # 포텐스 로고 및 배경의 진한 파란색
POTENS_ORANGE = "#FF6D00"  # 포텐스 로고의 주황색 점
POTENS_WHITE = "#FFFFFF"  # 흰색 텍스트
POTENS_LIGHT_BLUE = "#2E3FBF"  # 밝은 파란색 (하이라이트용)
POTENS_GRAY = "#F2F2F2"  # 배경 그레이
POTENS_DARK_GRAY = "#404040"  # 헤더용 진한 회색

# CSS 스타일링
def local_css():
    st.markdown(f"""
    <style>
        /* 전체 배경 */
        .stApp {{
            background-color: {POTENS_WHITE};
            font-size: 0.85rem;  /* 기본 글씨 크기 축소 */
            padding-top: 0.5rem !important; /* 상단 여백 축소 */
        }}
        
        /* 로고 위치 조정 */
        .logo-container {{
            position: relative;
            background-color: {POTENS_DARK_BLUE};
            padding: 0.5rem 1rem;
            height: 2.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 5px;
            margin-bottom: 0.8rem;
            width: 100%;
        }}
        
        /* 아이콘 스타일 */
        .simple-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-right: 0.4rem;
            color: {POTENS_WHITE};
            font-size: 0.9rem;
        }}
        
        /* 헤더 스타일 */
        .main-header {{
            background-color: {POTENS_DARK_BLUE};
            padding: 0.5rem 1rem;
            border-radius: 5px;
            color: {POTENS_WHITE};
            text-align: center;
            margin-bottom: 0.8rem;
            height: 2.5rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            width: 100%;
        }}
        
        /* 헤더 텍스트 크기 축소 */
        .main-header h1 {{
            font-size: 1.5rem;
            margin: 0; /* 여백 제거 */
            line-height: 1.3;
        }}
        
        .main-header p {{
            font-size: 0.85rem;
            margin: 0;
            line-height: 1.2;
        }}
        
        /* 서브 헤더 스타일 */
        .sub-header {{
            background-color: {POTENS_LIGHT_BLUE};
            padding: 0.35rem 0.7rem;
            border-radius: 5px;
            color: {POTENS_WHITE};
            margin-bottom: 0.6rem;
            display: flex;
            align-items: center;
        }}
        
        /* 서브 헤더 텍스트 크기 축소 */
        .sub-header h3 {{
            font-size: 1rem;
            margin: 0;
        }}
        
        /* 카드 스타일 */
        .card {{
            background-color: {POTENS_GRAY};
            padding: 0.8rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
            margin-bottom: 0.6rem;
        }}
        
        /* 버튼 스타일 */
        .stButton>button {{
            background-color: {POTENS_DARK_BLUE};
            color: {POTENS_WHITE};
            border: none;
            font-weight: bold;
            border-radius: 4px;
            padding: 0.4rem 0.8rem;
            font-size: 0.9rem;
        }}
        
        .stButton>button:hover {{
            background-color: {POTENS_LIGHT_BLUE};
        }}
        
        /* 강조 텍스트 */
        .highlight {{
            color: {POTENS_ORANGE};
            font-weight: bold;
        }}
        
        /* 로고 스타일 */
        .logo-text {{
            font-size: 1.2rem;
            font-weight: bold;
            margin: 0;
            color: {POTENS_WHITE};
            line-height: 1;
        }}
        
        .logo-dot {{
            color: {POTENS_ORANGE};
            font-size: 1.4rem;
            line-height: 1;
        }}
        
        /* 입력 필드 스타일 */
        div[data-baseweb="input"] {{
            border-radius: 4px;
        }}
        
        /* 프로그레스 바 스타일 */
        .stProgress > div > div {{
            background-color: {POTENS_ORANGE};
        }}
        
        /* DataFrames */
        .dataframe {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }}
        
        .dataframe th {{
            background-color: {POTENS_DARK_BLUE};
            color: white;
            padding: 6px;
            text-align: left;
        }}
        
        .dataframe td {{
            padding: 6px;
            border-bottom: 1px solid #ddd;
            white-space: pre-line; /* 줄바꿈 처리 */
        }}
        
        .dataframe tr:nth-child(even) {{
            background-color: {POTENS_GRAY};
        }}
        
        /* 다운로드 버튼 컨테이너 */
        .download-button-container {{
            margin-bottom: 1rem;
        }}
        
        /* 스트림릿 기본 요소 크기 조정 */
        .streamlit-expanderHeader {{
            font-size: 0.9rem;
        }}
        
        /* 성공/오류 메시지 */
        .stSuccess, .stError {{
            font-size: 0.9rem;
            padding: 0.6rem;
        }}
        
        /* 푸터 스타일 */
        .footer {{
            font-size: 0.85rem;
            text-align: center;
            margin-top: 1.5rem;
            padding: 0.6rem;
            background-color: #f5f5f5;
            border-radius: 5px;
        }}
        
        .footer p {{
            margin: 0.2rem 0;
        }}
        
        /* 스트림릿 기본 위젯 폰트 크기 조정 */
        .stTextInput label, .stNumberInput label, .stSelectbox label {{
            font-size: 0.9rem;
        }}
        
        .stTextInput input, .stNumberInput input, .stSelectbox span {{
            font-size: 0.9rem;
        }}
        
        /* Streamlit 기본 여백 조정 */
        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            margin-top: 0 !important;
        }}
        
        /* 상단 툴바 여백 조정 */
        header {{
            visibility: hidden;
        }}
    </style>
    """, unsafe_allow_html=True)

def clean_text(text):
    """
    텍스트에서 불필요한 문자와 줄바꿈을 제거하는 함수
    VBA의 CleanText 함수와 유사
    """
    # 제로 폭 공백 및 BOM 제거
    text = text.replace('\u200b', '').replace('\ufeff', '')
    
    # 줄바꿈 정규화
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # 시작과 끝의 공백 제거
    text = text.strip()
    
    return text

def get_content_from_document(driver, status_text=None):
    """
    다양한 컨테이너 후보를 사용하여 블로그에서 콘텐츠 추출
    VBA의 GetContentFromDocument 함수와 유사
    """
    content_text = ""
    found = False
    current_url = driver.current_url
    
    if status_text:
        status_text.text(f"콘텐츠 추출 시도 중... URL: {current_url}")
    
    # "se-main-container" 클래스에서 콘텐츠 찾기 시도 (네이버 블로그)
    try:
        elements = driver.find_elements(By.CLASS_NAME, "se-main-container")
        if elements:
            content_text = elements[0].text
            found = True
            if status_text:
                status_text.text(f"네이버 블로그 - se-main-container에서 콘텐츠 추출 성공")
    except:
        pass
    
    # "post_ct" 클래스에서 콘텐츠 찾기 시도 (네이버 블로그)
    if not found:
        try:
            elements = driver.find_elements(By.CLASS_NAME, "post_ct")
            if elements:
                content_text = elements[0].text
                found = True
                if status_text:
                    status_text.text(f"네이버 블로그 - post_ct에서 콘텐츠 추출 성공")
        except:
            pass
    
    # "tt_article_useless_p_margin contents_style" 클래스에서 콘텐츠 찾기 시도 (티스토리)
    if not found:
        try:
            elements = driver.find_elements(By.CLASS_NAME, "tt_article_useless_p_margin")
            if elements:
                content_text = elements[0].text
                found = True
                if status_text:
                    status_text.text(f"티스토리 블로그 - tt_article_useless_p_margin에서 콘텐츠 추출 성공")
        except:
            pass
    
    # "entry-content" 클래스에서 콘텐츠 찾기 시도 (티스토리 대체 클래스)
    if not found:
        try:
            elements = driver.find_elements(By.CLASS_NAME, "entry-content")
            if elements:
                content_text = elements[0].text
                found = True
                if status_text:
                    status_text.text(f"티스토리 블로그 - entry-content에서 콘텐츠 추출 성공")
        except:
            pass
            
    # article 태그에서 콘텐츠 찾기 시도 (티스토리 대체 방법)
    if not found:
        try:
            elements = driver.find_elements(By.TAG_NAME, "article")
            if elements:
                content_text = elements[0].text
                found = True
                if status_text:
                    status_text.text(f"블로그 - article 태그에서 콘텐츠 추출 성공")
        except:
            pass
    
    # JavaScript를 사용하여 티스토리 콘텐츠 추출 시도
    if not found and "tistory.com" in current_url:
        try:
            # 모든 텍스트 블록 추출 시도
            js_content = driver.execute_script("""
                // 모든 article, div.entry-content, div.tt_article_useless_p_margin 등을 찾습니다
                const containers = [
                    document.querySelector('article'), 
                    document.querySelector('.entry-content'),
                    document.querySelector('.tt_article_useless_p_margin'),
                    document.querySelector('.contents_style'),
                    document.querySelector('.post-content')
                ].filter(el => el !== null);
                
                if (containers.length > 0) {
                    // 첫 번째 유효한 컨테이너의 텍스트 반환
                    return containers[0].innerText;
                }
                
                // 아무것도 찾지 못했다면 본문에 있는 모든 텍스트 콘텐츠 수집
                return Array.from(document.querySelectorAll('p, h1, h2, h3, h4, h5, h6'))
                    .map(el => el.innerText)
                    .filter(text => text.trim().length > 0)
                    .join('\\n\\n');
            """)
            
            if js_content and len(js_content) > 100:  # 최소 길이 확인
                content_text = js_content
                found = True
                if status_text:
                    status_text.text(f"티스토리 블로그 - JavaScript 방식으로 콘텐츠 추출 성공")
        except Exception as e:
            if status_text:
                status_text.text(f"JavaScript 추출 실패: {str(e)}")
    
    if not found:
        content_text = "콘텐츠를 찾을 수 없습니다"
        if status_text:
            status_text.text(f"블로그 콘텐츠 추출 실패: {current_url}")
    
    return content_text

def get_blog_contents_and_save_excel(search_query, max_blogs=5, progress_bar=None, status_text=None):
    """
    블로그 콘텐츠를 크롤링하고 Excel로 저장하는 메인 함수
    VBA의 GetBlogContentsAndSaveExcel_UsingSeleniumForContentAndClean 서브와 유사
    
    max_blogs: 크롤링할 최대 블로그 수
    """
    # 진행 상황 텍스트 업데이트 (Streamlit용)
    if status_text:
        status_text.text("===== [START] 크롤링 시작 =====")
    
    # 크롬 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창 표시 없이 실행
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 최신 Selenium 4.0 이상에서는 webdriver_manager 없이 직접 Chrome 생성 가능
    driver = webdriver.Chrome(options=chrome_options)
    
    # 결과 저장용 배열 초기화
    titles = []
    links = []
    contents = []
    dates = []
    
    blogs_found = 0
    page = 1
    
    # 최대 10페이지까지 검색 (또는 원하는 블로그 수에 도달할 때까지)
    while blogs_found < max_blogs and page <= 10:
        # 검색 URL 생성 (사용자 검색어로 동적 생성)
        encoded_query = search_query.replace(' ', '+')
        if page == 1:
            search_url = f"https://search.naver.com/search.naver?sm=tab_hty.top&ssc=tab.blog.all&query={encoded_query}"
        else:
            search_url = f"https://search.naver.com/search.naver?sm=tab_hty.top&ssc=tab.blog.all&query={encoded_query}&start={(page-1)*10+1}"
        
        if status_text:
            status_text.text(f"페이지 {page} 검색 URL: {search_url}")
        
        # 검색 페이지 열기
        driver.get(search_url)
        if status_text:
            status_text.text(f"페이지 {page} - 크롬 드라이버 시작 및 페이지 로딩 중...")
        time.sleep(5)  # 페이지 로드 대기
        if status_text:
            status_text.text(f"페이지 {page} - 페이지 로딩 대기 완료")
        
        # "title_link" 클래스를 가진 모든 링크 찾기
        anchor_all = driver.find_elements(By.TAG_NAME, "a")
        if status_text:
            status_text.text(f"페이지 {page} - 전체 a 태그 개수: {len(anchor_all)}")
        
        anchor_links = []
        for anchor in anchor_all:
            try:
                if anchor.get_attribute("class") == "title_link":
                    anchor_links.append(anchor)
                    if len(anchor_links) + blogs_found >= max_blogs:
                        break
            except:
                continue
        
        count = len(anchor_links)
        if status_text:
            status_text.text(f"페이지 {page} - title_link 클래스를 가진 a 태그 개수: {count}")
        
        if count == 0:
            if status_text:
                status_text.text(f"페이지 {page} - 검색 결과에서 'title_link' 요소를 찾지 못했습니다.")
            page += 1
            continue
        
        # 진행 상황 바 업데이트 준비 (Streamlit용)
        if progress_bar:
            progress_bar.progress(blogs_found / max_blogs)
        
        # 각 블로그 링크 처리
        for i, a_tag in enumerate(anchor_links, 1):
            # 제목 추출
            title = a_tag.text
            titles.append(title)
            
            # 링크 추출 및 필요한 경우 모바일 버전으로 변환
            link_url = a_tag.get_attribute("href")
            
            # 네이버 블로그인 경우 모바일 버전으로 변환
            if "blog.naver.com" in link_url and "m.blog" not in link_url:
                link_url = link_url.replace("blog", "m.blog")
                
            links.append(link_url)
            
            if status_text:
                status_text.text(f"블로그 [{blogs_found + i}/{max_blogs}] 제목: {title}\n링크: {link_url}")
            
            # 새 브라우저 인스턴스를 사용하여 콘텐츠 추출
            blog_chrome_options = Options()
            blog_chrome_options.add_argument("--headless")
            blog_chrome_options.add_argument("--window-size=1920,1080")
            blog_chrome_options.add_argument("--disable-gpu")
            blog_chrome_options.add_argument("--no-sandbox")
            blog_chrome_options.add_argument("--disable-dev-shm-usage")
            blog_chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
            
            blog_driver = webdriver.Chrome(options=blog_chrome_options)
            blog_driver.get(link_url)
            if status_text:
                status_text.text(f"블로그 [{blogs_found + i}/{max_blogs}] 페이지 로딩 중... URL: {link_url}")
            
            # 티스토리의 경우 페이지 로딩에 시간이 더 필요할 수 있음
            if "tistory.com" in link_url:
                time.sleep(7)  # 티스토리는 로딩 시간을 좀 더 줌
            else:
                time.sleep(5)  # 일반 페이지 렌더링 대기
            
            # 콘텐츠 추출
            blog_content = get_content_from_document(blog_driver, status_text)
            
            # 콘텐츠 정리
            blog_content = clean_text(blog_content)
            contents.append(blog_content)
            
            # 실행 날짜 기록
            today_date = datetime.now().strftime("%Y-%m-%d")
            dates.append(today_date)
            
            if status_text:
                status_text.text(f"블로그 [{blogs_found + i}/{max_blogs}] 본문 추출 완료 (길이: {len(blog_content)})")
            
            # 블로그 페이지 브라우저 닫기
            blog_driver.quit()
            
            # 진행 상황 바 업데이트 (Streamlit용)
            if progress_bar:
                progress_bar.progress((blogs_found + i) / max_blogs)
        
        blogs_found += count
        
        # 원하는 블로그 수에 도달했으면 종료
        if blogs_found >= max_blogs:
            if status_text:
                status_text.text(f"원하는 블로그 수({max_blogs}개)에 도달했습니다.")
            break
        
        page += 1
    
    # 검색 페이지 브라우저 닫기
    driver.quit()
    if status_text:
        status_text.text("검색 페이지용 크롬 드라이버 종료")
    
    if blogs_found == 0:
        if status_text:
            status_text.text("크롤링된 블로그가 없습니다.")
        return None
    
    # 최대 블로그 수로 결과 제한
    titles = titles[:max_blogs]
    links = links[:max_blogs]
    contents = contents[:max_blogs]
    dates = dates[:max_blogs]
    
    # 결과로 DataFrame 생성
    df = pd.DataFrame({
        "실행날짜": dates,
        "제목": titles,
        "본문": contents,
        "링크": links
    })
    
    return df

def to_excel(df):
    """
    DataFrame을 엑셀 파일로 변환하고 다운로드 링크를 생성하는 함수
    """
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    
    # 포맷 적용
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    
    # 열 너비 설정
    # 실행날짜와 제목 열의 너비를 1/2로 축소
    date_column_width = 6  # 12를 6으로 축소 (1/2)
    
    # 본문 열의 기준 너비
    content_column_width = 65
    
    # 제목 열 너비는 본문 열의 정확히 2/3로 설정 후 1/2로 축소
    title_column_width = int(content_column_width * 2/3 * 0.5)  # 65 * 2/3 * 0.5 = 21.5
    
    # 링크 열 너비는 이전 너비(30)의 정확히 1/2로 설정
    link_column_width = 15  # 30 / 2 = 15
    
    # 열 너비 적용
    worksheet.set_column('A:A', date_column_width)   # 실행날짜
    worksheet.set_column('B:B', title_column_width)  # 제목 - 기존 너비의 1/2로 축소
    worksheet.set_column('C:C', content_column_width) # 본문
    worksheet.set_column('D:D', link_column_width)   # 링크
    
    # 형식 만들기
    header_format = workbook.add_format({
        'bg_color': POTENS_DARK_GRAY,  # 진한 회색
        'font_color': 'white',
        'border': 1,
        'border_color': 'black',
    })
    
    cell_format = workbook.add_format({
        'valign': 'top',
        'border': 1,
        'border_color': 'black',
        'text_wrap': True,
    })
    
    # 헤더 형식 적용
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    
    # 데이터에 셀 형식 적용
    for row_num in range(1, len(df) + 1):
        worksheet.set_row(row_num, 100)  # 행 높이를 100으로 설정
        for col_num in range(len(df.columns)):
            cell_value = df.iloc[row_num-1, col_num]
            worksheet.write(row_num, col_num, cell_value, cell_format)
    
    # URL 열을 하이퍼링크로 변환
    for row_num in range(1, len(df) + 1):
        url = df.iloc[row_num-1, 3]
        worksheet.write_url(row_num, 3, url, cell_format, string=url)
    
    writer.close()
    processed_data = output.getvalue()
    
    return processed_data

def get_table_download_link(df, filename="naver_blog_results.xlsx"):
    """
    엑셀 파일 다운로드 링크 생성 함수
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}" style="background-color:{POTENS_DARK_BLUE}; color:{POTENS_WHITE}; padding:0.4rem 0.8rem; border-radius:4px; text-decoration:none; font-weight:bold; font-size:0.9rem;">📥 엑셀 파일 다운로드</a>'

def make_clickable(link):
    """링크를 클릭 가능하게 만드는 함수"""
    return f'<a target="_blank" href="{link}" style="color:{POTENS_DARK_BLUE}; text-decoration:none; font-size:0.85rem;">{link}</a>'

# 로고 생성
def display_logo():
    st.markdown(
        f'<div class="logo-container"><span class="logo-text">Potens<span class="logo-dot">.</span></span></div>', 
        unsafe_allow_html=True
    )

# 헤더 생성
def display_header(title, subtitle):
    st.markdown(f'<div class="main-header"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

# 서브 헤더 생성
def display_subheader(text, icon=None):
    icon_html = f'<span class="simple-icon">{icon}</span>' if icon else ''
    st.markdown(f'<div class="sub-header"><h3>{icon_html}{text}</h3></div>', unsafe_allow_html=True)

# Streamlit 앱 정의
def main():
    st.set_page_config(
        page_title="Potens.|네이버 블로그 크롤러",
        page_icon="🔍",
        layout="wide"
    )
    
    # CSS 적용
    local_css()
    
    # CSS를 사용하여 헤더 영역을 조정
    st.markdown("""
    <style>
    .main-banner {
        display: flex;
        flex-direction: column;
        background-color: #1A237E;
        border-radius: 5px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        height: 5rem; /* 배너 높이 유지 */
        width: 100%;
        position: relative;
    }
    
    .logo-section {
        position: absolute;
        top: 0.5rem;
        left: 0.8rem;
    }
    
    .header-section {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        width: 100%;
    }
    
    .logo-text {
        font-size: 1.2rem; /* 로고 크기 2/3로 축소 */
        font-weight: bold;
        color: white;
        line-height: 1;
    }
    
    .logo-dot {
        color: #FF6D00;
        font-size: 1.35rem; /* 로고 크기 2/3로 축소 */
        line-height: 1;
    }
    
    /* 로고 컨테이너 클래스는 더 이상 필요하지 않으므로 스타일 비활성화 */
    .logo-container {
        display: none !important;
    }
    
    /* 기존 헤더 클래스는 더 이상 필요하지 않으므로 스타일 비활성화 */
    .main-header {
        display: none !important;
    }
    
    /* 테이블 열 너비 강제 적용을 위한 스타일 */
    table {
        table-layout: fixed !important;
        width: 100% !important;
        border-collapse: collapse !important;
    }
    
    /* 실행날짜 열: 원래 크기의 1/2 */
    table th:nth-child(1), table td:nth-child(1) {
        width: 6% !important;
    }
    
    /* 제목 열: 본문 열의 2/3에서 1/2로 축소 */
    table th:nth-child(2), table td:nth-child(2) {
        width: 21.5% !important;
    }
    
    /* 본문 열: 기준 너비 */
    table th:nth-child(3), table td:nth-child(3) {
        width: 65% !important;
    }
    
    /* 링크 열: 이전의 1/2 너비 */
    table th:nth-child(4), table td:nth-child(4) {
        width: 15% !important;
    }
    
    /* 테이블 셀 공통 스타일 */
    table td {
        word-break: break-word !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 헤더 영역을 단일 div로 감싸서 통일감 있게 표시
    st.markdown("""
    <div class="main-banner">
        <div class="logo-section">
            <span class="logo-text">Potens<span class="logo-dot">.</span></span>
        </div>
        <div class="header-section">
            <h1 style="font-size: 1.33rem; margin: 0; line-height: 1.3; color: white; text-align: center;">
                네이버 블로그 <span style="color: #FF6D00; font-weight: bold;">크롤러</span>
            </h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 화면을 왼쪽/오른쪽으로 분할 (왼쪽 영역 축소, 오른쪽 영역 확대)
    left_col, right_col = st.columns([1, 3])  # 비율: 왼쪽 1, 오른쪽 3
    
    with left_col:
        display_subheader("입력 정보", "📋")
        
        # 검색어 입력 필드
        search_query = st.text_input("검색어를 입력하세요", value="코멘토 직무부트캠프")
        
        # 크롤링할 블로그 수 입력 필드
        blog_count = st.number_input(
            "크롤링할 블로그 수", 
            min_value=1, 
            max_value=50, 
            value=5,
            step=1,
            help="크롤링할 블로그 게시물 수를 입력하세요 (최대 50개)"
        )
        
        # 크롤링 시작 버튼
        start_button = st.button("크롤링 시작", use_container_width=True)
        
        # 도움말 섹션
        with st.expander("💡 사용 방법"):
            st.markdown("""
            1. 검색어를 입력하세요 (기본값: "코멘토 직무부트캠프")
            2. 크롤링할 블로그 수를 입력하세요 (기본값: 5개, 최대 50개)
            3. '크롤링 시작' 버튼을 클릭하세요
            4. 크롤링이 완료되면 결과가 표시되고 Excel 파일을 다운로드할 수 있습니다
            
            **참고:**
            - 이 크롤러는 네이버 블로그와 티스토리 블로그 모두 지원합니다
            - 크롤링은 시간이 걸릴 수 있습니다 (블로그 수에 비례)
            - 블로그 수가 많을수록 크롤링 시간이 길어집니다
            """)
    
    with right_col:
        display_subheader("크롤링 결과", "📊")
        
        # 진행 상황 표시 영역
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # 결과 컨테이너
        result_container = st.container()
        
        if start_button:
            with result_container:
                try:
                    # 크롤링 실행 (블로그 수 인자 추가)
                    df = get_blog_contents_and_save_excel(search_query, blog_count, progress_bar, status_text)
                    
                    if df is not None and not df.empty:
                        # 링크를 클릭 가능하게 만들기
                        df_display = df.copy()
                        df_display['링크'] = df_display['링크'].apply(make_clickable)
                        
                        # 결과 표시
                        st.success(f"크롤링이 완료되었습니다! 총 {len(df)}개의 블로그 포스트를 찾았습니다.")
                        
                        # 엑셀 파일 다운로드 링크 생성 (상단에 배치)
                        st.markdown('<div class="download-button-container">', unsafe_allow_html=True)
                        st.markdown(get_table_download_link(df), unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # 데이터프레임 표시 (HTML 형식으로 링크 클릭 가능)
                        st.markdown("<h4 style='font-size:1.1rem; margin-bottom:0.3rem;'>수집 결과</h4>", unsafe_allow_html=True)
                        
                        # 표 스타일 개선
                        colgroup_html = '<colgroup>' + ''.join(['<col style="width:200px;">' for _ in range(len(df_display.columns))]) + '</colgroup>'
                        styled_df_html = df_display.to_html(escape=False, index=False)
                        styled_df_html = styled_df_html.replace('<table', '<table style="width:100%; font-size:0.85rem; table-layout:fixed;"')
                        styled_df_html = styled_df_html.replace('<thead>', f'{colgroup_html}<thead>')
                        styled_df_html = styled_df_html.replace('<td>', '<td style="padding:6px; vertical-align:top; overflow:hidden; text-overflow:ellipsis; width:200px; white-space:nowrap;">')

                        
                        st.markdown(styled_df_html, unsafe_allow_html=True)
                    else:
                        st.error("크롤링 중 문제가 발생했거나 결과가 없습니다.")
                except Exception as e:
                    st.error(f"오류 발생! 설명: {str(e)}")
    
    # 푸터
    st.markdown("""
    <div class="footer">
        <p>©2025 주식회사 코멘토 © Copyright All rights reserved</p>
        <p style="font-size: 0.8rem; color: #666;">이 자료는 ㈜ 코멘토의 허가 없이 복제, 배포, 수정할 수 없습니다.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
