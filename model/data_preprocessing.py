import os
import shutil
import yaml
import cv2
import logging
from sklearn.model_selection import train_test_split
import albumentations as A

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def load_config(config_path='model/config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def copy_images(src_dir, dst_dir, images, logger):
    os.makedirs(dst_dir, exist_ok=True)
    for image_name in images:
        src_path = os.path.join(src_dir, image_name)
        dst_path = os.path.join(dst_dir, image_name)
        shutil.copy(src_path, dst_path)
    logger.info(f"Copied {len(images)} images to {dst_dir}")

def apply_augmentation_and_save(image_dir, images, dst_dir, transform, logger, augmentation_factor=2):
    os.makedirs(dst_dir, exist_ok=True)
    for image_name in images:
        image_path = os.path.join(image_dir, image_name)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if image is not None:
            for i in range(augmentation_factor):
                transformed = transform(image=image)
                transformed_image = transformed['image']
                new_image_name = f"{os.path.splitext(image_name)[0]}_aug_{i}{os.path.splitext(image_name)[1]}"
                cv2.imwrite(os.path.join(dst_dir, new_image_name), transformed_image)
    logger.info(f"Applied augmentation and saved {len(images) * augmentation_factor} images to {dst_dir}")

def create_dataset_structure(config, logger):
    data_dir = config['paths']['data_dir']
    processed_dir = config['paths']['processed_dir']
    test_size = config['preprocessing']['test_size']
    val_size = config['preprocessing']['val_size']
    random_state = config['preprocessing']['random_state']

    if os.path.exists(processed_dir):
        shutil.rmtree(processed_dir)
    logger.info("Removed existing processed directory.")

    os.makedirs(processed_dir, exist_ok=True)

    for subset in ['train', 'val', 'test']:
        os.makedirs(os.path.join(processed_dir, subset), exist_ok=True)

    labels = [label for label in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, label))]

    transform = A.Compose([
        A.RandomCrop(width=256, height=256, p=1),
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.2),
        A.Rotate(limit=15, p=0.5),
        A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=15, p=0.5),
        A.HueSaturationValue(p=0.3)
    ])

    for label in labels:
        images = os.listdir(os.path.join(data_dir, label))
        image_paths = [os.path.join(data_dir, label, img) for img in images]
        X_train, X_temp = train_test_split(image_paths, test_size=test_size + val_size, random_state=random_state)
        X_val, X_test = train_test_split(X_temp, test_size=test_size / (test_size + val_size), random_state=random_state)

        copy_images(os.path.join(data_dir, label), os.path.join(processed_dir, 'val', label), [os.path.basename(img) for img in X_val], logger)
        copy_images(os.path.join(data_dir, label), os.path.join(processed_dir, 'test', label), [os.path.basename(img) for img in X_test], logger)

        apply_augmentation_and_save(os.path.join(data_dir, label), [os.path.basename(img) for img in X_train], os.path.join(processed_dir, 'train', label), transform, logger)

if __name__ == "__main__":
    logger = setup_logging()
    config = load_config()
    create_dataset_structure(config, logger)
    logger.info("Dataset preparation completed successfully.")
