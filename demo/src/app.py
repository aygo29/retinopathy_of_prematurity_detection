import os
from pathlib import Path
import streamlit as st
import constants
import inference_pipeline
from PIL import Image

def view_handler(model):
    st.subheader(model)
    
    model_idx = constants.MODELS.index(model)

    inference_pipeline.set_label(constants.MODEL_LABELS[model_idx])
    inference_pipeline.set_model(constants.MODEL_H5[model_idx])
    
    file = st.file_uploader("Upload image", type=["png"])


    if file:
        img = file.read()

        temp_saved_file_path = f"{constants.TEMPDIR}/{file.name}"

        with open(temp_saved_file_path, "wb") as fp:
            fp.write(img)


        col1, col2 = st.columns((1,1))
        
        with col1:
            enhance = st.toggle("Enhance image")
        with col2:
            predict = st.button("Predict")
        
        col3, col4 = st.columns((1, 1))
        
        with col3:
            st.image(img)

        if predict:
            label, prob = inference_pipeline.predict_image(temp_saved_file_path, enh=enhance, display=False)
            st.text(label)
            st.text(prob)

            if enhance:    
                with col4:
                    st.image(Image.open("./temp/temp.png"))




def main():
    st.title(constants.APP_TITLE)
    
    choice = st.sidebar.selectbox("Choose model", constants.MODELS)

    if choice == constants.MODELS[0]:
        view_handler(constants.MODELS[0])

    elif choice == constants.MODELS[1]:
        view_handler(constants.MODELS[1])

    elif choice == constants.MODELS[2]:
        view_handler(constants.MODELS[2])
    
    elif choice == constants.MODELS[3]:
        view_handler(constants.MODELS[3])
    
    elif choice == constants.MODELS[4]:
        view_handler(constants.MODELS[4])
    
    else:
        st.subheader("Hol' up. You should not be seeing this")

if __name__ == "__main__":
    os.chdir(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
    os.chdir("..")
    if not os.path.exists("temp"):
        os.mkdir("temp")
    main()
    