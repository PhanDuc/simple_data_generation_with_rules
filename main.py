import base64

import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

from logic_rule import prepared_file_uploaded, export2file, data_generating


def get_table_download_link_csv(df):
    csv = df.to_csv().encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="captura.csv" target="_blank">Download file data</a>'
    return href


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    """
    """
    st.sidebar.info("Data Generating!")
    st.sidebar.info("Please upload a file with rules for generating data!")
    n_try = st.sidebar.number_input('Attempts to generating', min_value=1, max_value=10, value=5)
    file_uploaded = st.file_uploader("Upload File")
    if file_uploaded is not None:
        listData = prepared_file_uploaded(file_uploaded)
        dataCombination = data_generating(listData, n_try=n_try)
        data2export = export2file(dataCombination)
        st.info("Data Overview!")
        st.info(f"Data after generated had {data2export.shape[0]} rows")
        st.dataframe(data2export.head(10))
        st.markdown(get_table_download_link_csv(data2export), unsafe_allow_html=True)

        pr = ProfileReport(data2export, explorative=True)
        st.title("Data Statistic")
        st_profile_report(pr)
