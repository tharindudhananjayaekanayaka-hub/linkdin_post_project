import os
import urllib.parse
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
import litellm

# 1. .env file එක load කරගැනීම
load_dotenv()

# Disable native tool calling for Groq stability
os.environ["LITELLM_USE_NATIVE_TOOL_CALLING"] = "False"
litellm.use_native_tool_calling = False

# 2. API Setup
groq_api_key = os.getenv("GROQ_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

os.environ["GROQ_API_KEY"] = groq_api_key if groq_api_key else ""
os.environ["SERPER_API_KEY"] = serper_api_key if serper_api_key else ""

# LLM Configuration
llm = LLM(
    model="openai/llama-3.1-8b-instant",
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key
)

# Search Tool Setup
try:
    search_tool = SerperDevTool(n_results=3)
except Exception as e:
    print(f"⚠️ Warning: {e}")
    search_tool = None

tools_list = [search_tool] if search_tool else []

# 3. Agents නිර්මාණය කිරීම
researcher = Agent(
    role='Expert Technology Researcher',
    goal='Find the 3 most important technology news stories from the past 7 days related to {topic}.',
    backstory="You are a skilled professional who analyzes technology news. You only use reliable and trustworthy sources.",
    tools=tools_list,
    llm=llm,
    verbose=True,
    max_iter=3,
    allow_delegation=False
)

writer = Agent(
    role='Expert LinkedIn Content Strategist',
    goal='Create an engaging LinkedIn post in {language} based on the data provided by the Research Agent.',
    backstory="You are skilled at writing technical content in a simple, informative, and professional manner.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

visual_artist = Agent(
    role='Visual Content Creator',
    goal='Create an English prompt to generate an AI image that matches the LinkedIn post.',
    backstory="You are an expert in digital art and highly skilled at crafting detailed image prompts.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# 4. Creating Tasks
research_task = Task(
    description="{topic} Identify 3 key developments that occurred in the past week in this field and provide a summary.",
    expected_output="A technical summary of the 3 most important updates of the week.",
    agent=researcher
)

writer_task = Task(
    description=(
        "1. Review the information provided by the Research Agent.\n"
        "2. Based on those insights, write an engaging LinkedIn post in {language}.\n"
        "3. Use bullet points, emojis, and hashtags.\n"
        "4. Include a call to action at the end."
    ),
    expected_output="A complete LinkedIn post in {language}.",
    agent=writer
)

image_task = Task(
    description="Write only a single-paragraph English image prompt that can be given to an AI, matching the created post.",
    expected_output="A highly detailed single-paragraph image prompt in English.",
    agent=visual_artist
)
# 5. Free Image URL Generator
def generate_free_image_url(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    return f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42&model=flux"

# 6. Crew Execution Function
def run_linkedin_ai_factory(user_topic, user_language):
    linkedin_crew = Crew(
        agents=[researcher, writer, visual_artist],
        tasks=[research_task, writer_task, image_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Crew එක run කිරීම
    linkedin_crew.kickoff(inputs={
        'topic': user_topic, 
        'language': user_language
    })
    
    # --- මෙන්න මෙතන තමයි වෙනස කළේ ---
    
    # 1. පෝස්ට් එකේ Description එක ගන්නේ writer_task එකෙන්
    final_post_content = writer_task.output.raw if writer_task.output else "Post generation failed."
    
    # 2. Image prompt එක image_task එකෙන් අරන් URL එක සාදා ගැනීම
    image_prompt = image_task.output.raw if image_task.output else f"Professional illustration for {user_topic}"
    final_image_url = generate_free_image_url(image_prompt)
    
    # පෝස්ට් එක සහ Image URL එක return කරනවා
    return final_post_content, final_image_url

# 7. Main Execution
if __name__ == "__main__":
    topic = input("Enter Topic: ")
    lang = input("Enter Language (Sinhala/English): ")
    
    try:
        post_output, image_url = run_linkedin_ai_factory(topic, lang)
        print("\n" + "="*50)
        print("✅ YOUR LINKEDIN POST DESCRIPTION:")
        print("="*50 + "\n")
        print(post_output)
        print("\n" + "="*50)
        print("🎨 AI IMAGE URL:")
        print("="*50 + "\n")
        print(image_url)
    except Exception as e:
        print(f"Error: {e}")