from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class QueryRequest(BaseModel):
    sql: str
    params: list = []

@router.post("/api/execute-query")
async def execute_query(request: QueryRequest, crud):
    try:
        result = crud.execute_query(request.sql, params=request.params)
        if result is None:
            raise HTTPException(status_code=400, detail="Query execution failed")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/delete")
async def delete_entry(table: str, id: int, crud):
    try:
        crud.delete(table, id)
        return {"message": f"Record with id {id} deleted from {table} table."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
