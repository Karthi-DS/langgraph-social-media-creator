import gradio as gr
from graph_builder import build_graph
import tempfile

# Initialize the graph once at startup
graph = build_graph()

def generate_content(theme, days):
    try:
        days = int(days)
        if days < 1 or days > 365:
            raise ValueError("Days must be between 1-365")
        
        # Run the content generation pipeline
        state = {"theme": theme, "days": days}
        final_state = graph.invoke(state)
        
        # Return the DataFrame directly
        df = final_state["df"]
        
        # Create a temporary CSV file for download
        temp_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
        df.to_csv(temp_file.name, index=False)
        temp_file.close()
        
        return df, temp_file.name, f"✅ Generated {days} days of content for '{theme}'"
    
    except Exception as e:
        return None, None, f"❌ Error: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="Social Media Content Creator", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🚀 Social Media Content Creator")
    gr.Markdown("Generate 30-day content plans with captions and hashtags")
    
    with gr.Row():
        with gr.Column():
            theme_input = gr.Textbox(
                label="Content Theme",
                placeholder="e.g., Fitness for Busy Professionals",
                max_lines=1
            )
            days_input = gr.Slider(
                label="Number of Days",
                minimum=1,
                maximum=90,
                value=30,
                step=1
            )
            generate_btn = gr.Button("Generate Content", variant="primary")
            
        with gr.Column():
            status_output = gr.Textbox(label="Status", interactive=False)
            csv_output = gr.Dataframe(
                label="Content Calendar",
                headers=["Day", "Topic", "Caption", "Hashtags"],
                interactive=False,
                wrap=True,
                datatype=["number", "str", "str", "str"]
            )
            download_file = gr.File(label="Download CSV", visible=False)
    
    # Event handling
    generate_btn.click(
        fn=generate_content,
        inputs=[theme_input, days_input],
        outputs=[csv_output, download_file, status_output]
    )
    
    # Show download button when data is generated
    csv_output.change(
        fn=lambda df: gr.File(visible=bool(df is not None)),
        inputs=[csv_output],
        outputs=[download_file]
    )

if __name__ == "__main__":
    app.launch(server_port=7860, share=True)