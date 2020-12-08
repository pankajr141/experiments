import os
import io
import cv2
import streamlit as st
from datetime import datetime
import detect
import hashlib

def detect_face_mask(filename):
    print("Detect face mask . Input File ",filename)
    #Call Face model with input file and retrun output file name
    outputfile = filename #output file should be returned by model
    print("Detect face mask . Output File ", outputfile)
    return outputfile

def input_file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    filenames = list(filter(lambda x: x.lower().endswith('mp4') or x.lower().endswith('webm'), filenames))
    selected_filename = st.sidebar.selectbox('Select an processed video file (mp4/webm)', filenames)
    return os.path.join(folder_path, selected_filename)

@st.cache(allow_output_mutation=True)
def get_static_store():
    return {}

def main():
    static_store = get_static_store()

    global predictor
    cfg, predictor, _ = detect.load_models()
    st.title("Facemask and Social Distancing detector")
    st.set_option('deprecation.showfileUploaderEncoding', False)
    inputfilename = input_file_selector() # By default current folder is set is no folder path is provided
    # Here call model and provide input file and output should be filename
    # which should need to be played for face mask detection
    outputfilename = detect_face_mask(inputfilename)
    if st.button("Play video"):
        video_file = open(outputfilename, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

    st.title("Upload New video for processing")
    uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])
    if uploaded_file is not None:
        data = uploaded_file.read()
        checksum = hashlib.md5(data).hexdigest()

        if static_store.get(checksum, False):
            st.text("Already in processing queue or processed")
        else:
        
            static_store[checksum] = True

            g = io.BytesIO(data)  ## BytesIO Object
            temporary_location = "video_%s.mp4" % (datetime.now().strftime("%Y%m%d_%H%M%S"))
            with open(temporary_location, 'wb') as out:  ## Open temporary file as bytes
                out.write(g.read())  ## Read bytes into file
            out.close()
            st.text("uploaded %s to disk" % temporary_location)
            cmd = "python detect.py %s &" % temporary_location
            print(cmd)
            os.system(cmd)        
            st.text("video scheduled to be processed")

    st.title("Upload Image for instant detection")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg"])
    if uploaded_file is not None:
        #checksum = hashlib.md5(uploaded_file.read()).hexdigest()
        g = io.BytesIO(uploaded_file.read())  ## BytesIO Object
        temporary_location = "img_%s.jpg" % (datetime.now().strftime("%Y%m%d_%H%M%S"))
        with open(temporary_location, 'wb') as out:  ## Open temporary file as bytes
            out.write(g.read())  ## Read bytes into file
        out.close()
        st.text("uploaded %s to disk" % temporary_location)

        img = cv2.imread(temporary_location)
        outputs = detect.process_single_frame(0, img, predictor)
        imgs = list(detect.compute_final_frame([img], [outputs], 0, None))
        pimg = imgs[0]
        pimg = cv2.cvtColor(pimg, cv2.COLOR_BGR2RGB)
        st.image(pimg)

if __name__ == '__main__':
    main()


