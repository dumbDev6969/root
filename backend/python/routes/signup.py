from fastapi import FastAPI, Query, HTTPException, Request


def run(app,crud):
    @app.post("/api/signup/jobseeker")
    async def jobseeker(request: Request):
        try:
            body = await request.json()
            table = body['table']
            data_to_insert = body['data']
        
            crud.create(table, **data_to_insert)
            return {"message": f"Record created in {table} table."}
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail=str(e))
        
    @app.post("/api/signup/recruter")
    async def recruter(request: Request):
        try:
            body = await request.json()
            table = body['table']
            data_to_insert = body['data']
        
            crud.create(table, **data_to_insert)
            return {"message": f"Record created in {table} table."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))