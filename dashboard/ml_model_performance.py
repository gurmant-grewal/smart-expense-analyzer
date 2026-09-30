import streamlit as st
import json


def show_model_performance():
    try:
        with open("saved/model_matrices.json","r") as file:
            metrices_history=json.load(file)
    except Exception:
        st.error("An error occurred while loading model performance metrics.")

    latest_metrices=metrices_history[-1]

    st.subheader("AI Model Performance")

    st.write(f"Accuracy :" f"{latest_metrices['accuracy']:.2f}")
    st.write(f"Precision :" f"{latest_metrices['precision']:.2f}")
    st.write(f"Recall :" f"{latest_metrices['recall']:.2f}")
    st.write(f"F1 Score :" f"{latest_metrices['f1_score']:.2f}")
    st.write(f"Categories :" f"{', '.join(latest_metrices['categories'])}")
    st.write(f"Training Samples: "f"{latest_metrices['training_samples']}")
    st.write(f"Last Trained: "f"{latest_metrices['last_trained']}")
    st.write("Classification Report:")
    st.text(latest_metrices["report"])
        
