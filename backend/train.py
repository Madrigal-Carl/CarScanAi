import os
import warnings
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from tqdm import tqdm

from model import ResNet18

# ===========================
# CONFIG
# ===========================
DATA_DIR = "data"
SAVE_DIR = "models/car_brand_model.pth"
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001
IMG_SIZE = 224
VAL_SPLIT = 0.15
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
FREEZE_BASE = True  # initially freeze base layers

# ===========================
# WARNINGS
# ===========================
warnings.filterwarnings("ignore", category=UserWarning, module="PIL.Image")

# ===========================
# TRANSFORMS
# ===========================
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

# ===========================
# DATASET + SPLIT
# ===========================
dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
num_classes = len(dataset.classes)
total_size = len(dataset)
val_size = int(total_size * VAL_SPLIT)
train_size = total_size - val_size

train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

print(f"Total samples: {total_size}, Train: {train_size}, Val: {val_size}")
print(f"Classes: {dataset.classes}")

# ===========================
# MODEL
# ===========================
model = ResNet18(num_classes=num_classes, freeze_base=FREEZE_BASE).to(DEVICE)

# Only train the classifier first if base is frozen
if FREEZE_BASE:
    optimizer = optim.Adam(model.fc.parameters(), lr=LEARNING_RATE)
else:
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

criterion = nn.CrossEntropyLoss()

# ===========================
# FUNCTION: EVALUATE
# ===========================
def evaluate(model, loader):
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    return correct / total

# ===========================
# TRAIN LOOP
# ===========================
best_val_acc = 0.0

def train_epochs(model, loader, optimizer, epochs, desc_prefix="Epoch"):
    global best_val_acc
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for images, labels in tqdm(loader, desc=f"{desc_prefix} {epoch+1}/{epochs}"):
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        val_acc = evaluate(model, val_loader)
        print(f"{desc_prefix} {epoch+1}/{epochs} - "
              f"Train Loss: {total_loss/len(loader):.4f} - Val Acc: {val_acc:.4f}")

        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            os.makedirs(os.path.dirname(SAVE_DIR), exist_ok=True)
            torch.save({
                "model_state": model.state_dict(),
                "class_names": dataset.classes
            }, SAVE_DIR)
            print(f"Saved best model with Val Acc: {best_val_acc:.4f}")

# ===========================
# PHASE 1: TRAIN CLASSIFIER ONLY
# ===========================
if FREEZE_BASE:
    print("\nPhase 1: Training classifier only...")
    train_epochs(model, train_loader, optimizer, epochs=5, desc_prefix="Classifier Epoch")

# ===========================
# PHASE 2: TRAIN FULL MODEL
# ===========================
print("\nPhase 2: Training full model...")
# Unfreeze all layers
for param in model.parameters():
    param.requires_grad = True

optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
train_epochs(model, train_loader, optimizer, epochs=EPOCHS, desc_prefix="Full Model Epoch")

print(f"\nTraining finished! Best Val Acc: {best_val_acc:.4f}")
print(f"Model saved at {SAVE_DIR}")
