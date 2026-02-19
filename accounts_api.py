#!/usr/bin/env python3
"""Basic FastAPI app: create and retrieve accounts."""

from fastapi import FastAPI, HTTPException

app = FastAPI()

accounts: dict[int, str] = {}
next_id = 1


@app.post("/accounts")
def create_account(username: str):
    """Create an account with the given username."""
    global next_id
    account_id = next_id
    accounts[account_id] = username
    next_id += 1
    return {"id": account_id, "username": username}


@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    """Retrieve an account by id."""
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"id": account_id, "username": accounts[account_id]}
