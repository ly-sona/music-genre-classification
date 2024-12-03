// src/pages/AboutModel.jsx
import React from 'react';

function AboutModel() {
  return (
    <div className="relative py-24 flex justify-center">
      <section className="relative w-full max-w-6xl p-8 md:p-14 backdrop-blur-lg bg-slate-950 rounded-lg md:rounded-2xl shadow-2xl z-20 border border-white/10 overflow-hidden">
        {/* Background Radial Gradient */}
        <div
          className="absolute top-0 left-0 z-[-2] h-full w-full bg-white 
            bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%, 
            rgba(120,119,198,0.3), rgba(255,255,255,0))]"
        ></div>

        {/* Heading */}
        <h2 className="text-3xl md:text-5xl font-extrabold text-purple-600 mb-8 drop-shadow-md text-center">
          About the Model
        </h2>

        {/* Content */}
        <div className="text-slate-500 space-y-6">
          {/* Data Preprocessing */}
          <div>
            <h3 className="text-2xl font-semibold text-purple-600">Data Preprocessing</h3>
            
            {/* What is a Spectrogram? */}
            <div className="mt-4">
              <h4 className="text-xl font-medium text-purple-500">What is a Spectrogram?</h4>
              <p className="mt-2">
                A spectrogram is a visual representation of the spectrum of frequencies in a sound as they vary with time.
                Imagine it as an image where one axis represents time, the other represents frequency, and the color or intensity represents the amplitude (loudness) of each frequency at each moment.
              </p>
            </div>

            {/* Why Spectrograms? */}
            <div className="mt-4">
              <h4 className="text-xl font-medium text-purple-500">Why Spectrograms?</h4>
              <p className="mt-2">
                Converting audio to spectrograms allows us to use image-based CNNs to analyze sound data.
              </p>
            </div>

            {/* Normalizing the Spectrogram */}
            <div className="mt-4">
              <h4 className="text-xl font-medium text-purple-500">Normalizing the Spectrogram</h4>
              
              {/* Why Normalize? */}
              <div className="mt-2">
                <h5 className="text-lg font-semibold text-purple-400">Why Normalize?</h5>
                <p className="mt-1">
                  Normalization ensures that the data has a consistent scale, which helps the neural network learn more effectively.
                  It reduces the impact of variations in loudness or recording quality.
                </p>
              </div>

              {/* How It Works */}
              <div className="mt-2">
                <h5 className="text-lg font-semibold text-purple-400">How It Works:</h5>
                <p className="mt-1">
                  The spectrogram values are scaled to a standard range (e.g., 0 to 1) using normalization techniques.
                </p>
              </div>
            </div>

            {/* Data Augmentation */}
            <div className="mt-4">
              <h4 className="text-xl font-medium text-purple-500">Data Augmentation</h4>
              
              {/* What is Data Augmentation? */}
              <div className="mt-2">
                <h5 className="text-lg font-semibold text-purple-400">What is Data Augmentation?</h5>
                <p className="mt-1">
                  Data Augmentation involves creating modified versions of the original data to increase the diversity of the dataset.
                  This helps the model generalize better to new, unseen data.
                </p>
              </div>

              {/* How It Works */}
              <div className="mt-2">
                <h5 className="text-lg font-semibold text-purple-400">How It Works:</h5>
                <ul className="list-disc list-inside mt-1 space-y-1">
                  <li><strong>Time Shifting:</strong> The audio waveform is slightly shifted in time, creating a new version of the audio without changing its content.</li>
                  <li><strong>Generating Augmented Spectrogram:</strong> A spectrogram is created from the augmented audio, providing additional training examples.</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Understanding Convolutional Neural Networks (CNNs) */}
          <div>
            <h3 className="text-2xl font-semibold text-purple-600">Understanding Convolutional Neural Networks (CNNs)</h3>
            
            {/* What are CNNs? */}
            <div className="mt-4">
              <h4 className="text-xl font-medium text-purple-500">What are CNNs?</h4>
              <p className="mt-2">
                Convolutional Neural Networks (CNNs) are a type of deep learning model primarily used for analyzing visual data.
                They are inspired by the human brain's visual cortex and are excellent at recognizing patterns and structures in images.
              </p>
            </div>

            {/* How Do CNNs Work? */}
            <div className="mt-4">
              <h4 className="text-xl font-medium text-purple-500">How Do CNNs Work?</h4>
              
              {/* Convolutional Layers */}
              <div className="mt-2">
                <h5 className="text-lg font-semibold text-purple-400">Convolutional Layers:</h5>
                <ul className="list-disc list-inside mt-1 space-y-1">
                  <li><strong>Filters/Kernels:</strong> Small matrices that slide over the input data to detect features like edges, textures, or more complex patterns.</li>
                  <li><strong>Feature Maps:</strong> The output after applying a filter, highlighting the presence of specific features in the input.</li>
                </ul>
              </div>

              {/* Pooling Layers */}
              <div className="mt-2">
                <h5 className="text-lg font-semibold text-purple-400">Pooling Layers:</h5>
                <ul className="list-disc list-inside mt-1 space-y-1">
                  <li><strong>Downsampling:</strong> Reduces the spatial dimensions (height and width) of the feature maps, decreasing computational load and helping the model focus on the most important features.</li>
                  <li><strong>Types:</strong> Common types include Max Pooling (selects the maximum value) and Average Pooling.</li>
                </ul>
              </div>

              {/* Activation Functions */}
              <div className="mt-2">
                <h5 className="text-lg font-semibold text-purple-400">Activation Functions:</h5>
                <ul className="list-disc list-inside mt-1 space-y-1">
                  <li>Introduce non-linearity to help the network learn complex patterns.</li>
                  <li>ReLU (Rectified Linear Unit) is a common activation function used in CNNs.</li>
                </ul>
              </div>

              {/* Fully Connected (Dense) Layers */}
              <div className="mt-2">
                <h5 className="text-lg font-semibold text-purple-400">Fully Connected (Dense) Layers:</h5>
                <ul className="list-disc list-inside mt-1 space-y-1">
                  <li>Neurons are fully connected to all neurons in the previous layer.</li>
                  <li>These layers perform the final classification based on the features extracted by the convolutional layers.</li>
                </ul>
              </div>
            </div>
          </div>

          {/* ResNet50 Architecture */}
          <div>
            <h3 className="text-2xl font-semibold text-purple-600">ResNet50 Architecture</h3>
            <p className="mt-4 text-slate-500">
              ResNet50 is a pre-trained CNN model with 50 layers, known for its deep architecture and use of residual connections.
              <br /><br />
              <strong>Residual Connections:</strong> Help in training very deep networks by allowing gradients to flow through the network more easily, preventing issues like vanishing gradients.
            </p>
          </div>

          {/* Why Use CNNs for Music Genre Classification? */}
          <div>
            <h3 className="text-2xl font-semibold text-purple-600">Why Use CNNs for Music Genre Classification?</h3>
            
            {/* Spectrograms as Images */}
            <div className="mt-4">
              <h4 className="text-xl font-medium text-purple-500">Spectrograms as Images</h4>
              <p className="mt-2">
                Spectrograms transform audio data into a 2D visual format.
                CNNs excel at processing and extracting features from 2D images, making them ideal for analyzing spectrograms.
              </p>
            </div>

            {/* Capturing Spatial Features */}
            <div className="mt-4">
              <h4 className="text-xl font-medium text-purple-500">Capturing Spatial Features</h4>
              
              <ul className="list-disc list-inside mt-2 space-y-1">
                <li><strong>Patterns in Spectrograms:</strong> Different music genres have distinct patterns in their frequency and time domains.</li>
                <li><strong>CNNs' Strength:</strong> They can automatically learn and identify these patterns, such as rhythm, harmony, and instrumentation, which are characteristic of specific genres.</li>
              </ul>
            </div>

            {/* Transfer Learning with Pre-Trained Models */}
            <div className="mt-4">
              <h4 className="text-xl font-medium text-purple-500">Transfer Learning with Pre-Trained Models</h4>
              
              {/* Description */}
              <p className="mt-2">
                Using a pre-trained model like ResNet50 leverages learned features from a vast image dataset (ImageNet), which can be beneficial even for spectrogram analysis.
              </p>

              {/* Benefits */}
              <div className="mt-2">
                <h5 className="text-lg font-semibold text-purple-400">Benefits:</h5>
                <ul className="list-disc list-inside mt-1 space-y-1">
                  <li><strong>Reduced Training Time:</strong> Less data and computational resources are needed.</li>
                  <li><strong>Improved Performance:</strong> Pre-trained models have already learned useful feature representations.</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default AboutModel;