from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

@app.get("/jwt")
async def get_jwt(uid: str = None, password: str = None, access_token: str = None):
    
    try:
        # Case 1: uid & password se
        if uid and password:
            async with httpx.AsyncClient() as client:
                token_res = await client.get(
                    "https://utp-to-accesstoken.vercel.app/access_token",
                    params={"uid": uid, "password": password}
                )
            
            token_data = token_res.json()

            if not token_data.get("success"):
                raise HTTPException(status_code=400, detail="Invalid UID or Password")

            access_token = token_data.get("access_token")

        # Case 2: direct access_token
        if access_token:
            async with httpx.AsyncClient() as client:
                jwt_res = await client.get(
                    "https://api.freefireservice.dnc.su/oauth/account:login",
                    params={"data": access_token}
                )

            jwt_data = jwt_res.json()
            jwt_token = jwt_data.get("8")

            if not jwt_token:
                raise HTTPException(status_code=400, detail="JWT not found")

            return {
                "token": jwt_token
            }

        raise HTTPException(status_code=400, detail="Missing parameters")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))