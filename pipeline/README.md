## RoP Pipeline

1. Restructure data - copies all images into a single folder
2. Enhance images - enhances and stores all images in a new folder
3. Generate embeddings - generates .npy files for each image and is stored in a single folder
4. Create datasets - combines .npy files and labels into single .npy files
5. Train models - trains model on combined .npy files and saves model as .h5 file