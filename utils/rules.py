from utils.llm_utils import generate_response
import random

TOPIC_TEMPLATES = [
    "The secret to {theme} that nobody talks about",
    "5 minute {theme} solutions for busy people",
    "How {theme} changed my life",
    "Beginner-friendly {theme} techniques",
    "{theme} myths debunked by science",
    "Advanced {theme} strategies for professionals",
    "{theme} on a budget: Free resources",
    "Why {theme} matters more than you think",
    "{theme} success stories from our community",
    "The future of {theme}: Trends to watch"
]

def generate_topics(theme, num_days):
    # Get base topics from LLM
    prompt = (
        f"Generate {num_days} unique social media post topics about {theme}. "
        "Make them creative, engaging, and varied. "
        "Return ONLY a numbered list with no additional text."
    )
    
    response = generate_response(prompt, max_tokens=512)
    
    # Parse numbered list
    topics = []
    for line in response.split('\n'):
        if line.strip() and line[0].isdigit():
            topic = line.split('.', 1)[-1].strip()
            topics.append(topic)
    
    # Fallback if LLM fails
    if len(topics) < num_days:
        base_topics = [t.format(theme=theme) for t in TOPIC_TEMPLATES]
        # Create variations
        modifiers = ["Ultimate Guide to", "Quick Tips for", "Secrets of", "5-Minute", "Science-Backed"]
        topics = [f"{random.choice(modifiers)} {theme}" for _ in range(num_days)]
    
    return topics[:num_days]