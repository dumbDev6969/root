from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class QueryRequest(BaseModel):
    sql: str
    params: list = []

def run(app, crud):
    @app.post("/api/execute-query")
    async def execute_query(request: QueryRequest):
        try:
            result = crud.execute_query(request.sql, params=request.params)
            if result is None:
                raise HTTPException(status_code=400, detail="Query execution failed")
            return {"result": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.delete("/api/delete")
    async def delete_entry(table: str, id: int):
        try:
            crud.delete(table, id)
            return {"message": f"Record with id {id} deleted from {table} table."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
