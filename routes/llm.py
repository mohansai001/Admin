from fastapi import APIRouter #type: ignore
from vida.utils.llm import get_azure_response

router = APIRouter()

@router.get("/llm/test")
async def test_llm(prompt: str):
    return get_azure_response(prompt)