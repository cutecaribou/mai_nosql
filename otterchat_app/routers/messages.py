from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_messages_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_messages():
    return fake_messages_db


@router.get("/{message_id}")
async def read_message(message_id: str):
    if message_id not in fake_messages_db:
        raise HTTPException(status_code=404, detail="message not found")
    return {"name": fake_messages_db[message_id]["name"], "message_id": message_id}


@router.put(
    "/{message_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_message(message_id: str):
    if message_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the message: plumbus"
        )
    return {"message_id": message_id, "name": "The great Plumbus"}
