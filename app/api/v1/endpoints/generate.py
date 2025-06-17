from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from os import getenv
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    response: str

@router.post("/", response_model=PromptResponse)
async def generate_text(request: PromptRequest):
    logger.info(f"Received text generation request with prompt length: {len(request.prompt)}")
    try:
        api_key = getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OpenAI API key not found in environment variables")
            raise HTTPException(status_code=500, detail="OpenAI API key not found")

        logger.info("Initiating OpenAI API request")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant that loves to use emojis to make responses more engaging and fun. Include relevant emojis throughout your responses to add visual appeal and emotion to the text."},
                        {"role": "user", "content": request.prompt}
                    ],
                },
                timeout=30.0,
            )
            
            if response.status_code != 200:
                logger.error(f"OpenAI API request failed with status {response.status_code}: {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            result = response.json()
            response_text = result["choices"][0]["message"]["content"]
            logger.info(f"Successfully generated response with length: {len(response_text)}")
            return {"response": response_text}
            
    except httpx.TimeoutException:
        logger.error("Request to OpenAI timed out after 30 seconds")
        raise HTTPException(status_code=504, detail="Request to OpenAI timed out")
    except Exception as e:
        logger.error(f"Unexpected error during text generation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 