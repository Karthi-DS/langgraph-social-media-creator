import pandas as pd
import logging

def save_csv(state):
    try:
        # Try to get DataFrame directly
        df = state["df"]
    except KeyError:
        # Fallback: Try to create from content_plan
        try:
            df = pd.DataFrame(state["content_plan"])
            logging.warning("Created DataFrame from content_plan (df key missing)")
        except KeyError:
            raise KeyError("State missing both 'df' and 'content_plan' keys")
    
    # Save to CSV
    df.to_csv("content_calendar.csv", index=False)
    
    # Return the DataFrame for UI use
    return {**state, "df": df}