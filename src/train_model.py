import os
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint  # Corrected import
from data_generator import create_data_generators
from model import create_cnn_model
import matplotlib.pyplot as plt

def main():
    # 1. Define paths and parameters
    TRAIN_DIR = 'data/train'
    VAL_DIR = 'data/validation'
    BATCH_SIZE = 32
    IMG_HEIGHT = 224
    IMG_WIDTH = 224
    NUM_CLASSES = 10  # Update based on your dataset
    EPOCHS = 50
    MODEL_SAVE_DIR = 'models'
    os.makedirs(MODEL_SAVE_DIR, exist_ok=True)

    # 2. Create data generators
    train_generator, val_generator = create_data_generators(
        train_dir=TRAIN_DIR,
        val_dir=VAL_DIR,
        img_height=IMG_HEIGHT,
        img_width=IMG_WIDTH,
        batch_size=BATCH_SIZE
    )

    # 3. Create and compile the model
    model = create_cnn_model(input_shape=(IMG_HEIGHT, IMG_WIDTH, 3), num_classes=NUM_CLASSES)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # 4. Set up callbacks
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    checkpoint_path = os.path.join(MODEL_SAVE_DIR, 'best_model.h5')
    model_checkpoint = ModelCheckpoint(
        filepath=checkpoint_path,
        monitor='val_loss',
        save_best_only=True
    )

    # 5. Train the model
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        callbacks=[early_stop, model_checkpoint]
    )

    # 6. Save the final model
    final_model_path = os.path.join(MODEL_SAVE_DIR, 'music_genre_cnn_final.h5')
    model.save(final_model_path)
    print(f"Final model saved to {final_model_path}")

    # 7. Plot training history
    plot_training_history(history, MODEL_SAVE_DIR)

def plot_training_history(history, save_dir):
    # Plot accuracy
    plt.figure(figsize=(8, 6))
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Accuracy over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig(os.path.join(save_dir, 'accuracy.png'))
    plt.close()

    # Plot loss
    plt.figure(figsize=(8, 6))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Loss over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig(os.path.join(save_dir, 'loss.png'))
    plt.close()

if __name__ == "__main__":
    main()
