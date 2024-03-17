import os
import random
import shutil


def get_image_label_pairs(images_root_dir, labels_root_dir):
    image_label_pairs = []

    for date_dir in os.listdir(images_root_dir):
        image_date_dir = os.path.join(images_root_dir, date_dir)
        label_date_dir = os.path.join(labels_root_dir, date_dir)
    
        if os.path.exists(label_date_dir):
            for image_file in os.listdir(image_date_dir):
                image_path = os.path.join(image_date_dir, image_file)
                label_file = os.path.join(label_date_dir, image_file[:-4] + '.txt')

                if os.path.exists(label_file):
                    image_label_pairs.append((image_path, label_file, date_dir))
        else:
            raise NotADirectoryError
    return image_label_pairs

def shuffle_and_split_data(image_label_pairs, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1, random_seed=42):
    random.seed(random_seed)
    random.shuffle(image_label_pairs)
    total_samples = len(image_label_pairs)
    train_samples = int(total_samples * train_ratio)
    val_samples = int(total_samples * val_ratio)
    return image_label_pairs[:train_samples], image_label_pairs[train_samples:train_samples + val_samples], image_label_pairs[train_samples + val_samples:]

def save_dataset(dataset, output_root_dir):
    for dataset_name, data in dataset.items():
        dataset_dir = os.path.join(output_root_dir, dataset_name)
        os.makedirs(os.path.join(dataset_dir, 'images'), exist_ok=True)
        os.makedirs(os.path.join(dataset_dir, 'labels'), exist_ok=True)
        
        for image_path, label_path, date in data:
            image_name = f"{date}_{os.path.basename(image_path)}"
            label_name = f"{date}_{os.path.basename(label_path)}"
            shutil.copy(image_path, os.path.join(dataset_dir, 'images', image_name))
            shutil.copy(label_path, os.path.join(dataset_dir, 'labels', label_name))

def save_datasets(images_root_dir, labels_root_dir, output_root_dir):
    image_label_pairs = get_image_label_pairs(images_root_dir, labels_root_dir)
    train_set, val_set, test_set = shuffle_and_split_data(image_label_pairs)    
    save_dataset({'train': train_set, 'val': val_set, 'test': test_set}, output_root_dir)

# # Example usage
images_dir = 'data/images'
yolo_dir = 'data/yolo_labels'
trainig_dir = 'yolo_training'

# image_label_pairs = get_image_label_pairs(images_root_directory, labels_root_directory)
# train_set, val_set, test_set = shuffle_and_split_data(image_label_pairs)

save_datasets(images_root_dir=images_dir, labels_root_dir=yolo_dir, output_root_dir=trainig_dir)
