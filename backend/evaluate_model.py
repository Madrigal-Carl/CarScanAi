import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

from model import ResNet18   # your model definition


# ===========================
# CONFIG
# ===========================
MODEL_PATH = "models/car_brand_model.pth"
DATA_DIR = "test"   
IMG_SIZE = 224
BATCH_SIZE = 16
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ===========================
# TRANSFORMS (same as training)
# ===========================
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])


# ===========================
# LOAD DATA
# ===========================
dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False)
class_names = dataset.classes


# ===========================
# LOAD MODEL
# ===========================
checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)

num_classes = len(checkpoint["class_names"])
model = ResNet18(num_classes=num_classes)
model.load_state_dict(checkpoint["model_state"])
model.to(DEVICE)
model.eval()


# ===========================
# EVALUATION LOOP
# ===========================
all_preds = []
all_labels = []

with torch.no_grad():
    for images, labels in loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)

        outputs = model(images)
        _, preds = torch.max(outputs, 1)

        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())


# ===========================
# METRICS
# ===========================
accuracy = np.mean(np.array(all_preds) == np.array(all_labels)) * 100

print("\n==============================")
print(f"✅ MODEL ACCURACY: {accuracy:.2f}%")
print("==============================\n")

print("📌 CLASSIFICATION REPORT:")
print(classification_report(all_labels, all_preds, target_names=class_names))

print("📌 CONFUSION MATRIX:")
print(confusion_matrix(all_labels, all_preds))
