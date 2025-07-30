from fastapi import Depends, HTTPException, status, Request
from app.auth.jwt_interpreter import decode_access_token, oauth2_scheme
from app.services.redis_session import get_redis

async def get_current_user(token: str = Depends(oauth2_scheme), redis=Depends(get_redis)):
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    # Check if token is in Redis (session valid)
    session = await redis.get(token)
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid")
    return payload
