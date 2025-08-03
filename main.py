import argparse
from ui import app

def cli_mode():
    theme = input("Enter your content theme: ").strip()
    if not theme:
        print("Error: Content theme is required")
        return
        
    duration = input("How many days? (default 30): ").strip()
    days = int(duration) if duration.isdigit() else 30

    from graph_builder import build_graph
    graph = build_graph()
    final_state = graph.invoke({"theme": theme, "days": days})
    print("✅ Content calendar generated as 'content_calendar.csv'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Social Media Content Creator")
    parser.add_argument("--ui", action="store_true", help="Launch web UI")
    args = parser.parse_args()
    
    if args.ui:
        print("Launching UI on http://localhost:7860")
        app.launch(server_port=7860)
    else:
        cli_mode()