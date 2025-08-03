from utils.llm_utils import generate_response
import re

def sanitize_output(text):
    """Less aggressive cleaning keeping essential content"""
    text = re.sub(r'(Caption|Post|Idea)\s*:\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^[\d\.\)\s]+', '', text)  # Remove numbering
    return text.strip('"').strip()

def generate_caption(topic):
    prompt = (
        f"You're a social media manager. Write a 2-sentence Instagram caption for the topic: '{topic}'. "
        f"Make it friendly, creative, and engaging. Avoid repeating the topic. Don't explain how to write it—just write the post."
    )
    result = generate_response(prompt)
    cleaned = sanitize_output(result)
    
    # Ensure minimum quality
    if len(cleaned) < 30 or cleaned.startswith(("I would", "As an AI")):
        return f"🌟 Let's explore {topic}! What's your experience with this? Share below! 👇"
    return cleaned

def generate_hashtags(topic):
    prompt = (
        f"Generate 3-5 highly relevant hashtags for this topic: {topic} "
        "Return ONLY space-separated hashtags with no other text. "
        "Example: #DigitalMarketing #SEO #ContentStrategy"
    )
    result = generate_response(prompt, max_tokens=100)
    
    # Extract hashtags reliably
    hashtags = re.findall(r'#\w+', result)
    hashtags = [h for h in hashtags if len(h) > 2 and not h.endswith('...')]
    
    # Fallback logic
    if len(hashtags) < 2:
        keywords = re.findall(r'\b\w{4,}\b', topic)
        hashtags = [f"#{kw.capitalize()}" for kw in keywords[:3]] + ["#Tips", "#HowTo"]
    
    return " ".join(set(hashtags))[:120]  # Ensure length limit

def generate_content(state):
    topics = state["topics"]
    content_plan = []
    
    for i, topic in enumerate(topics, start=1):
        # Retry mechanism for poor generations
        for attempt in range(2):
            caption = generate_caption(topic)
            hashtags = generate_hashtags(topic)
            
            if caption and hashtags:
                content_plan.append({
                    "Day": i,
                    "Topic": topic,
                    "Caption": caption,
                    "Hashtags": hashtags
                })
                break
        else:  # Fallback if both attempts fail
            content_plan.append({
                "Day": i,
                "Topic": topic,
                "Caption": f"Exploring {topic} today! What are your thoughts?",
                "Hashtags": "#" + topic.replace(" ", "")[:15] + " #Tips"
            })
    
    return {**state, "content_plan": content_plan}