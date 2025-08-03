import pandas as pd

def format_output(state):
    # Ensure content_plan exists
    if "content_plan" not in state:
        raise KeyError("Missing 'content_plan' in state for formatting")
    
    # Create DataFrame
    df = pd.DataFrame(state["content_plan"])
    
    # Return updated state with DataFrame
    return {**state, "df": df}