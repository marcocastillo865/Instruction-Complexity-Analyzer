import streamlit as st
import pickle
import pandas as pd
import numpy as np
import textstat

# --- Loading the Saved Model ---
# This loads the "brain" of the application
with open('complexity_model.pkl', 'rb') as f:
    model = pickle.load(f)

# --- Feature Engineering Function
def create_features_final(full_text):
    features = {}
    if not full_text.strip():
        return None
    
    words = full_text.split()
    word_count = len(words)
    if word_count == 0:
        return None
    
    features['word_count'] = word_count
    features['sentence_count'] = textstat.sentence_count(full_text)
    features['avg_sentence_length'] = np.mean([len(s.split()) for s in full_text.split('.') if s.strip()])
    features['avg_word_length'] = np.mean([len(w) for w in words])
    features['unique_word_count'] = len(set(words))
    features['flesch_reading_ease'] = textstat.flesch_reading_ease(full_text)
    features['flesch_kincaid_grade'] = textstat.flesch_kincaid_grade(full_text)
    features['num_warnings'] = 0 # Placeholder as we can't get this from raw text
    features['num_tips'] = 0 # Placeholder as we can't get this from raw text
    features['avg_steps_per_method'] = 0 # Placeholder as we can't get this from raw text

    return features

# --- Streamlit App Interface ---
st.title("Instruction Complexity Analyzer")

st.write(
    "Paste a set of isntructions (like a recipe or a DIY Guide) below to get a "
    "predicted complexity score. A score closer to 1.0 is more complex."
)

# Text area for user input
user_text = st.text_area("Paste your instructions here:", height = 250)

# Analyze button
if st.button("Analyze Complexity"):
    if user_text:
        features = create_features_final(user_text)

        if features:
            # Convert features to a DataFrame with the correct column order
            X_columns = ['word_count', 'sentence_count', 'avg_sentence_length', 'avg_word_length', 'unique_word_count', 'flesch_reading_ease', 'flesch_kincaid_grade', 'num_warnings', 'num_tips', 'avg_steps_per_method']
            features_df = pd.DataFrame([features], columns = X_columns)

            # Make a prediction
            predicted_score = model.predict(features_df)[0]

            # Display the results
            st.subheader("Analysis Result")
            st.metric(label = "Predicted Complexity Score", value = f"{predicted_score:.4f}")

            if predicted_score > 0.6:
                st.error("This task appears to be highly complex.")
            elif predicted_score > 0.3:
                st.warning("This task appears to be moderately complex.")
            else:
                st.success("This task appears to be relatively simple.")

            with st.expander("What does this score mean?"):
                st.write("""
                    - **0.0 - 0.3 (Low Complexity):** This task is likely straightforward and should require minimal preparation.
                    - **0.3 - 0.6 (Moderate Complexity):** This task has multiple steps and may require some focus. It's a good idea to read through all the steps before starting.
                    - **0.6+ (High Complexity):** This is a complex task. We recommend setting aside dedicated time and ensuring you have all materials ready before you begin.
                """)

            st.subheader("Extracted Linguistic Features")
            st.write("The model made its prediction based on these features extracted from your text:")
            st.dataframe(features_df)

            with st.expander("Learn more about these features"):
                st.markdown("""
                - **word_count:** The total number of words in the text. Longer texts are generally more complex.
                - **sentence_count:** The total number of sentences. More sentences often mean more individual ideas or steps to process.
                - **avg_sentence_length:** The average number of words per sentence. Longer sentences can increase cognitive load.
                - **avg_word_length:** The average length of words. Longer words can be more difficult to read.
                - **unique_word_count:** The number of unique words (vocabulary size). A larger vocabulary can indicate more specialized or technical content.
                - **flesch_reading_ease:** A standard score where higher values (closer to 100) mean the text is *easier* to read.
                - **flesch_kincaid_grade:** Estimates the U.S. school grade level required to understand the text.
                - *(The other features are placeholders in this demo, as they require structured data to calculate.)*
                """)

    else:
        st.error("The text box is empty. Please paste some instructions.")