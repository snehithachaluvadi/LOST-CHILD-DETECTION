##  Finding Lost Child Through Structural Similarity Using ML Approach

This project proposes a solution that uses machine learning techniques, specifically structural similarity and facial recognition, to detect and identify missing children in real-time. By analysing images or video frames captured from surveillance cameras or public spaces, the system can compare the captured faces with known images of missing children. It will provide instant alerts with crucial details like location, photograph, and the time of the incident, enhancing the speed of detection and increasing the chances of safely locating the child.

## STRUCTUTAL SIMILARITY
A perceptual metric used to measure the similarity between two images. It is particularly useful in machine learning tasks involving image processing, computer vision, and image quality assessment. Unlike pixel-wise metrics like Mean Squared Error (MSE) or Peak Signal-to-Noise Ratio (PSNR), SSIM focuses on structural information, which is more aligned with human visual perception.

## FACIAL RECOGNITION
The face_recognition library provides methods to detect faces within images or
video frames. It utilizes pre-trained face detection models based on Histogram
of Oriented Gradients (HOG) and Convolutional Neural Networks (CNN). This
library captures the landmarks of the face (like distance between the eyes, lips,
distance of nose etc..). These landmarks are crucial for tasks like aligning faces,
measuring facial features, and improving face recognition accuracy. It utilizes a
deep learning-based face recognition model trained on a large dataset of faces.
This model extracts unique facial features, often referred to as face
embeddings, which represent each face in a high-dimensional space. By
comparing these embeddings, the library can determine whether two faces
belong to the same person or not.
