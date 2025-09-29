from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd, io, os, sqlite3, tempfile, uuid

app = FastAPI(title="AI Data Agent - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

UPLOAD_DIR = "uploads"
DB_PATH = "db.sqlite3"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def excel_to_sqlite(excel_bytes, db_path=DB_PATH):
    # Read all sheets into DataFrames and write to sqlite
    xls = pd.read_excel(io.BytesIO(excel_bytes), sheet_name=None)
    conn = sqlite3.connect(db_path)
    for sheet_name, df in xls.items():
        # sanitize sheet/table name
        table = str(sheet_name).strip().replace(' ', '_')[:64] or f"sheet_{uuid.uuid4().hex[:8]}"
        # Drop completely empty columns
        df = df.dropna(axis=1, how='all')
        # Replace unnamed columns
        df.columns = [c if str(c).strip()!='' else f"col_{i}" for i,c in enumerate(df.columns)]
        df.to_sql(table, conn, if_exists='replace', index=False)
    conn.close()
    return True

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Please upload an Excel file.")
    contents = await file.read()
    fname = os.path.join(UPLOAD_DIR, file.filename)
    with open(fname, "wb") as f:
        f.write(contents)
    excel_to_sqlite(contents)
    return {"status":"ok", "message":"file processed and stored to sqlite"}

@app.post("/nlq")
async def nlq(query: dict):
    # Very simple NLQ: expects {"question": "..."}
    q = query.get("question","").lower()
    if not q:
        raise HTTPException(status_code=400, detail="question is required")
    # For demo: support questions like "list tables" or "show columns from sales"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if "list tables" in q or "show tables" in q:
        cur.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
        tables = [r[0] for r in cur.fetchall()]
        conn.close()
        return {"tables": tables}
    if q.startswith("show columns from "):
        tab = q.replace("show columns from ","").strip()
        try:
            cur.execute(f"PRAGMA table_info('{tab}')")
            cols = [r[1] for r in cur.fetchall()]
            conn.close()
            return {"table": tab, "columns": cols}
        except Exception as e:
            conn.close()
            return JSONResponse(status_code=400, content={"error": str(e)})
    # Fallback: run a simple aggregate if user asks "sum of <col> group by <col2> from <table>"
    if "sum of" in q and "from" in q:
        try:
            # naive parse
            # "sum of sales group by region from sheet1" - this is fragile but works for demo
            parts = q.split(" from ")
            agg_part = parts[0]
            table = parts[1].split()[0]
            if "group by" in agg_part:
                agg_col = agg_part.split("sum of ")[1].split(" group by")[0].strip()
                group_col = agg_part.split("group by ")[1].strip()
                sql = f"SELECT {group_col}, SUM({agg_col}) as total FROM {table} GROUP BY {group_col} LIMIT 100"
                cur.execute(sql)
                rows = cur.fetchall()
                conn.close()
                return {"sql": sql, "rows": rows}
        except Exception as e:
            conn.close()
            return JSONResponse(status_code=400, content={"error": str(e)})
    conn.close()
    return {"answer":"I couldn't parse the question. Try: 'list tables', 'show columns from <table>', or 'sum of <col> group by <col2> from <table>'"}
