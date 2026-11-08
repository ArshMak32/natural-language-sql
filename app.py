import json
from pathlib import Path
import streamlit as st
from core import SCHEMA, EXAMPLES, generate, execute

st.set_page_config(page_title="SQL Analyst Workbench", layout="wide")
st.title("SQL Analyst Workbench")
st.info("Four related synthetic tables. Review generated SQL before executing it.")
with st.expander("Schema and joins"):
    st.code(SCHEMA)
mode = st.radio("Mode", ["Offline reference queries", "Live LangChain generation"])
if mode == "Offline reference queries":
    st.caption("Predefined queries only. No LLM is used in this mode.")
    q = st.selectbox("Analytical question", list(EXAMPLES))
    sql = EXAMPLES[q]
    st.code(sql, language="sql")
    if st.button("Execute reference query"):
        st.dataframe(execute(sql))
else:
    st.caption(
        "Requires OPENAI_API_KEY and OPENAI_MODEL in environment. Schema and question are sent to provider. API usage may incur charges."
    )
    q = st.text_input(
        "Ask a question about customers, orders and products", max_chars=1000
    )
    if st.button("Generate SQL"):
        st.session_state.pop("draft", None)
        try:
            st.session_state["draft"] = generate(q).model_dump()
        except Exception:
            st.error(
                "Generation failed. Check credentials, model access and network. No SQL executed."
            )
    if "draft" in st.session_state:
        st.write(st.session_state["draft"]["explanation"])
        st.code(st.session_state["draft"]["sql"], language="sql")
        if st.button("Execute reviewed query"):
            try:
                df = execute(st.session_state["draft"]["sql"])
                st.dataframe(df)
                st.download_button(
                    "Download results", df.to_csv(index=False), "query_results.csv"
                )
            except Exception as exc:
                st.error("Query invalid or rejected: " + type(exc).__name__)
with st.expander("Benchmark evidence"):
    for file in ["results.json", "live_results.json"]:
        if Path(file).exists():
            st.json(json.loads(Path(file).read_text()))
st.caption(
    "Controls: isolated in-memory DB, SQLite authorization, query-only mode, statement/row/instruction limits. Not a production database connector."
)
