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
    goal='{topic} සම්බන්ධයෙන් පසුගිය දින 7 තුළ සිදු වූ වැදගත්ම තාක්ෂණික පුවත් 3ක් සොයා ගැනීම.',
    backstory="ඔබ තාක්ෂණික පුවත් විශ්ලේෂණය කරන ප්‍රවීණයෙකි. විශ්වාසදායක මූලාශ්‍ර පමණක් භාවිතා කරයි.",
    tools=tools_list,
    llm=llm,
    verbose=True,
    max_iter=3,
    allow_delegation=False
)

writer = Agent(
    role='Expert LinkedIn Content Strategist',
    goal='Research Agent ලබාදෙන දත්ත ඇසුරෙන් {language} භාෂාවෙන් ආකර්ෂණීය LinkedIn post එකක් නිර්මාණය කිරීම.',
    backstory="ඔබ තාක්ෂණික කරුණු ඉතා සරලව, කරුණු සහිතව සහ වෘත්තීය මට්ටමින් ලිවීමට දක්ෂය.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

visual_artist = Agent(
    role='Visual Content Creator',
    goal='පෝස්ට් එකට ගැළපෙන පරිදි AI image එකක් සෑදීමට අවශ්‍ය ඉංග්‍රීසි prompt එකක් නිර්මාණය කිරීම.',
    backstory="ඔබ ඩිජිටල් කලාව පිළිබඳ ප්‍රවීණයෙකි. ඉතා විස්තරාත්මක image prompt එකක් සැකසීමට ඔබ දක්ෂය.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# 4. Tasks නිර්මාණය කිරීම
research_task = Task(
    description="{topic} ක්ෂේත්‍රයේ පසුගිය සතියේ සිදු වූ වෙනස්කම් 3ක් සොයාගෙන සාරාංශයක් ලබා දෙන්න.",
    expected_output="සතියේ වැදගත්ම කරුණු 3ක තාක්ෂණික සාරාංශයක්.",
    agent=researcher
)

writer_task = Task(
    description=(
        "1. Research Agent ලබාදුන් තොරතුරු අධ්‍යයනය කරන්න.\n"
        "2. එම කරුණු ඇසුරෙන් ආකර්ෂණීය LinkedIn post එකක් {language} භාෂාවෙන් ලියන්න.\n"
        "3. Bullet points, Emojis සහ Hashtags භාවිතා කරන්න.\n"
        "4. අවසානයට Call to Action එකක් ඇතුළත් කරන්න."
    ),
    expected_output="A complete LinkedIn post in {language}.",
    agent=writer
)

image_task = Task(
    description="ලියන ලද පෝස්ට් එකට ගැළපෙන පරිදි, AI එකකට ලබා දිය හැකි එක ඡේදයක ඉංග්‍රීසි image prompt එකක් පමණක් ලියන්න.",
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