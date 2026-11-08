# SQL Analyst Workbench: Multi-Table Generation and Evaluation

Portfolio version 2. See `MODEL_CARD.md`, tests and included `*results.json` reports for evidence and limits.

## Mac setup
Python 3.11 or 3.12:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m streamlit run app.py
```
The app displays included evaluation artifacts. It does not retrain on every interaction. Open the local URL shown in Terminal. Stop with Control+C.

## Reproduce

```bash
python evaluate.py
```
Live mode requires your own API key and model. Set in the same Terminal before launching:
```bash
export OPENAI_API_KEY='your-key'
export OPENAI_MODEL='a-model-available-to-your-account'
python -m streamlit run app.py
```
Run the live development benchmark with `python evaluate.py --live` (12 API calls, may incur charges). Live benchmark and credentials are not supplied. The included offline report is reference-query regression, NOT an LLM accuracy measurement.

## Design
Four related synthetic tables: customers, products, orders and order_items. Structured SQL plus explanation from LangChain ChatOpenAI. Explicit review before execution. SQLite authorizer denies table writes, system-table reads and nonallowlisted functions. Query-only DB, isolated in-memory fixture, single statement, row cap and VM instruction budget. The deliberately limited SQL subset is not a production sandbox guarantee.

Twelve analytical reference cases cover joins, aggregation, dates, HAVING and missing relationships. Execution-result comparison tolerates column aliases and ignores ordering; it does not validate ranked output order. Visible development questions do not establish generalization. Offline mode is fixed SQL only. Schema and questions leave your machine in live mode; no transaction rows are sent by this code. No API key is committed. `.env.example` is documentation only; files are not auto-loaded.
