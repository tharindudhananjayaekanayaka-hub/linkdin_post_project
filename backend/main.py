import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# අපේ CrewAI logic එක තියෙන app.py එකෙන් function එක import කරගන්නවා
try:
    from app import run_linkedin_ai_factory
except Exception as e:
    print(f"❌ Error importing 'app.py': {str(e)}")
    import traceback
    traceback.print_exc()
    run_linkedin_ai_factory = None

app = FastAPI(title="LinkedIn AI Factory API")

# 1. React Frontend එකට Backend එකට කතා කිරීමට අවසර දීම (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request එකේ ආකෘතිය (Data Schema)
class TopicRequest(BaseModel):
    topic: str
    language: str  # 'Sinhala' හෝ 'English' ලෙස ලැබෙනු ඇත

# 2. Default Route
@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "LinkedIn AI Factory Backend is Running!",
        "docs": "/docs"
    }

# 3. පෝස්ට් එක සහ Image එක Generate කරන ප්‍රධාන API එක
@app.post("/generate-post")
async def generate_post(request: TopicRequest):
    if not request.topic:
        raise HTTPException(status_code=400, detail="මාතෘකාවක් (Topic) ඇතුළත් කිරීම අනිවාර්යයි.")
    
    try:
        if run_linkedin_ai_factory is None:
            raise Exception("Backend logic (app.py) was not loaded correctly. Please check server logs.")
            
        print(f"🚀 Processing Topic: {request.topic} | Language: {request.language}")
        
        # CrewAI kickoff කර ප්‍රතිඵල දෙක ලබා ගැනීම (Post content සහ Image URL)
        # මෙතන 'post_content' එකට දැන් ලැබෙන්නේ writer_task එකේ description එකයි
        post_content, image_url = run_linkedin_ai_factory(request.topic, request.language)
        
        # React එකට යවන JSON response එක
        return {
            "status": "success",
            "topic": request.topic,
            "language": request.language,
            "post": post_content,  # මෙතන කෙලින්ම post_content එක pass කරනවා
            "image_url": image_url
        }
        
    except Exception as e:
        import traceback
        print(f"❌ Error occurred: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail={
                "message": "Agent හට වැඩ කිරීමට නොහැකි විය (Agent failed to process)",
                "error": str(e)
            }
        )

# 4. Backend එක Run කිරීම
if __name__ == "__main__":
    print("✨ LinkedIn AI Factory Backend එක ආරම්භ වේ...")
    # Port 8000 එකේ backend එක run කිරීම
    uvicorn.run(app, host="127.0.0.1", port=8000)