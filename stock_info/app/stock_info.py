# import streamlit as st
# import pandas as pd
# import FinanceDataReader as fdr
# import datetime
# import matplotlib.pyplot as plt
# import matplotlib 
# import io
# import plotly.graph_objects as go
# import pandas as pd

# import plotly.express as px 
# import plotly.figure_factory as ff

# buffer = io.BytesIO()

# st.header('무슨 주식을 사야 부자가 되려나...')

# st.sidebar.markdown('회사 이름과 기간을 입력하세요')

# # Using object notation
# stock_name = st.sidebar.text_input("회사 이름")

# today = datetime.datetime.now()
# next_year = today.year + 1
# jan_1 = datetime.date(next_year, 1, 1)
# dec_31 = datetime.date(next_year, 12, 31)

# # Using "with" notation
# with st.sidebar:
#     d = st.date_input(
#     "시작일 - 종료일",
#     (jan_1, datetime.date(next_year, 1, 7)),
#     # jan_1,
#     # dec_31,
#     format="MM.DD.YYYY",
# )
# # st.write(d) # (datetime.date(2024, 1, 4), datetime.date(2024, 1, 6))

# accept = st.sidebar.button("주가 데이터 확인")
    
# def get_stock_info():
#     base_url = "http://kind.krx.co.kr/corpgeneral/corpList.do"
#     method = "download"
#     url = "{0}?method={1}".format(base_url, method)
#     df = pd.read_html(url, header=0, encoding='cp949')[0]
#     df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")     
#     df = df[['회사명','종목코드']]
#     return df

# def get_ticker_symbol(company_name):
#     df = get_stock_info()
#     code = df[df['회사명']==company_name]['종목코드'].values
#     ticker_symbol = code[0]
#     return ticker_symbol

# @st.cache_data
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv().encode('utf-8')

# def download_excel(df, filename='주가데이터.xlsx'):
#     df.to_excel('주가데이터.xlsx', index=False)

# # 코드 조각 추가
# if accept:
#     ticker_symbol = get_ticker_symbol(stock_name)
#     start_p = d[0]
#     end_p = d[1] + datetime.timedelta(days=1)
#     df = fdr.DataReader(ticker_symbol, start_p, end_p, exchange="KRX")
#     df.index = df.index.date
#     st.subheader(f"[{stock_name}] 주가 데이터")
#     st.dataframe(df.head())
#     # st.plotly_chart(df, x=df.index, y='Close',range_x=['start_p', 'end_p'])
#     # fig = ff.create_distplot(df, group_labels=)
#     # st.plotly_chart(fig, use_container_width=True)
#     chart_data = pd.DataFrame(df, columns=["Close"])
#     st.line_chart(chart_data)

#     csv = convert_df(df)

#     col1, col2 = st.columns(2)
#     col1.download_button(
#         label="Download data as CSV",
#         data=csv,
#         file_name='주가데이터.csv',
#         mime='text/csv',
#     )
#     # excel_path = 'temp_data.xlsx'
#     # if col2.button('Download data as Excel'):
#     #     df.to_excel(excel_path, index=False)
#     #     st.download_button(
#     #         label="Download data as Excel",
#     #         data=open(excel_path, 'rb'),  # 파일을 바이너리 모드로 열기
#     #         file_name='주가데이터.xlsx',  # 파일 이름 지정
#     #         mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # MIME 타입 지정
#     #     )
#     excel_data = io.BytesIO()      
#     df.to_excel(excel_data)

#     col2.download_button("Download data as Excel", 
#                          excel_data, 
#                          file_name='stock_data.xlsx')

import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
import datetime
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import plotly.graph_objects as go
import plotly.express as px


st.header('무슨 주식을 사야 부자가 되려나...')
st.sidebar.markdown('회사 이름과 기간을 입력하세요')
# Using object notation
stock_name = st.sidebar.text_input("회사 이름")
today = datetime.datetime.now()
next_year = today.year + 1
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)
# Using "with" notation
with st.sidebar:
    d = st.date_input(
    "시작일 - 종료일",
    (jan_1, datetime.date(next_year, 1, 7)),
    # jan_1,
    # dec_31,
    format="YYYY-MM-DD",
)
# st.write(d) # (datetime.date(2024, 1, 4), datetime.date(2024, 1, 6))
accept = st.sidebar.button("주가 데이터 확인")
def get_stock_info():
    base_url = "http://kind.krx.co.kr/corpgeneral/corpList.do"
    method = "download"
    url = "{0}?method={1}".format(base_url, method)
    df = pd.read_html(url, header=0, encoding='cp949')[0]
    df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")
    df = df[['회사명','종목코드']]
    return df
def get_ticker_symbol(company_name):
    df = get_stock_info()
    code = df[df['회사명']==company_name]['종목코드'].values
    ticker_symbol = code[0]
    return ticker_symbol


# 코드 조각 추가
if accept:
    ticker_symbol = get_ticker_symbol(stock_name)
    start_p = d[0]
    end_p = d[1] + datetime.timedelta(days=1)
    df = fdr.DataReader(ticker_symbol, start_p, end_p, exchange="KRX")
    df.index = df.index.date
    st.subheader(f"[{stock_name}] 주가 데이터")
    st.dataframe(df.head())
    
    # 주석 처리된 코드 수정
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode='lines', name='Close'))
    st.plotly_chart(fig)
    
    col1, col2 = st.columns(2)

    # 다운로드 버튼 생성 (CSV)
    csv_data = df.to_csv().encode('utf-8')
    col1.download_button(
        label="주가 데이터 다운로드 (CSV)",
        data=csv_data,
        file_name=f"{stock_name}_stock_data.csv",
        mime="text/csv"
    )

    excel_data = BytesIO()      
    df.to_excel(excel_data)     

    col2.download_button("주가 데이터 다운로드 (Excel)", 
        excel_data, file_name='stock_data.xlsx')