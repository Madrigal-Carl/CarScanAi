from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from predict import predict_image
import tempfile
import shutil

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # If deploying, replace "*" with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # --- 1. Save the uploaded file temporarily ---
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp:
            shutil.copyfileobj(file.file, temp)
            temp_path = temp.name

        # --- 2. Run prediction ---
        result = predict_image(temp_path)

        # --- 3. Error handling from the model ---
        if "error" in result:
            return JSONResponse(content={"error": result["error"]}, status_code=400)

        # --- 4. Return formatted result to frontend ---
        return {
            "predicted_class": result.get("predicted_class", "Unknown"),
            "confidence": float(result.get("confidence", 0)),
        }

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
