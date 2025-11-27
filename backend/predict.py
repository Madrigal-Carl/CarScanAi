import torch
from torchvision import transforms
from PIL import Image
import os

from model import ResNet18

# ===========================
# CONFIG
# ===========================
MODEL_PATH = "models/car_brand_model.pth"
IMG_SIZE = 224
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ===========================
# LOAD MODEL
# ===========================
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

    checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)

    class_names = checkpoint["class_names"]
    num_classes = len(class_names)

    model = ResNet18(num_classes=num_classes)
    model.load_state_dict(checkpoint["model_state"])
    model.to(DEVICE)
    model.eval()

    return model, class_names


model, class_names = load_model()

# ===========================
# TRANSFORM IMAGE (same as training)
# ===========================
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

# ===========================
# PREDICTION FUNCTION
# ===========================
def predict_image(image_path: str):
    """
    Predicts the car brand of an uploaded image.
    Returns:
        {
            "predicted_class": str,
            "confidence": float
        }
    """
    if not os.path.exists(image_path):
        return {"error": f"File not found: {image_path}"}

    try:
        image = Image.open(image_path).convert("RGB")
    except:
        return {"error": "Invalid or corrupted image file."}

    img_tensor = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(img_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        conf, predicted_idx = torch.max(probabilities, 1)

    predicted_class = class_names[predicted_idx.item()]
    confidence = round(conf.item() * 100, 2)

    return {
        "predicted_class": predicted_class,
        "confidence": confidence
    }


# ===========================
# OPTIONAL: RUN DIRECTLY
# ===========================
if __name__ == "__main__":
    test_image = input("Enter path to image: ")
    result = predict_image(test_image)
    print(result)
