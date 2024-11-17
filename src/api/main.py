import os
from pathlib import Path
from fastapi import FastAPI
from dotenv import load_dotenv
from prompty.tracer import trace
from prompty.core import PromptyStream, AsyncPromptyStream
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from fastapi import FastAPI, File, UploadFile
from evaluate.evaluators import evaluate_image

from orchestrator import Task, create
from telemetry import setup_telemetry

base = Path(__file__).resolve().parent

load_dotenv()
app = FastAPI()

code_space = os.getenv("CODESPACE_NAME")
app_insights = os.getenv("APPINSIGHTS_CONNECTIONSTRING")

if code_space: 
    origin_8000= f"https://{code_space}-8000.app.github.dev"
    origin_5173 = f"https://{code_space}-5173.app.github.dev"
    ingestion_endpoint = app_insights.split(';')[1].split('=')[1]
    
    origins = [origin_8000, origin_5173, os.getenv("API_SERVICE_ACA_URI"), os.getenv("WEB_SERVICE_ACA_URI"), ingestion_endpoint]
else:
    origins = [
        o.strip()
        for o in Path(Path(__file__).parent / "origins.txt").read_text().splitlines()
    ]
    origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_telemetry(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/article")
@trace
async def create_article(task: Task):
    return StreamingResponse(
        PromptyStream(
            "create_article", create(task.research, task.products, task.assignment)
        ),
        media_type="text/event-stream",
    )

@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):

    base = Path(__file__).resolve().parents[1]

    # Set the directory for the stored image
    image_dir = os.path.join(base, 'web/public')
    print(image_dir)

    # Initialize the image path (note the filetype should be png)
    file_path  = os.path.join(image_dir, file.filename)
    # UPLOAD_DIRECTORY = Path(base / "images")

    # Construct the file path where the image will be saved
    # file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    
    # Save the image to the specified path
    with open(file_path, "wb") as image:
        content = await file.read()
        image.write(content)

    project_scope = {
        "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],   
        "resource_group_name": os.environ["AZURE_RESOURCE_GROUP"],
        "project_name": os.environ["AZURE_AI_PROJECT_NAME"],        
    }

    from evaluate.evaluate import evaluate_image

    result = evaluate_image(project_scope, file_path)

    if len(result) > 0:
        # Return the filename and location
        return JSONResponse({"filename": file.filename, 
                             "location": file_path,
                            "message": f'''
                            ❌This image contains the following harmful/protected content {result}. 
                            We do not recommend including it in the blog!❌''',
                            "safety": ""
                            })
    else:
        # Return the filename and location
        return JSONResponse({"filename": file.filename, 
            "location": file_path,
            "message":"This image is safe to include in the blog ✅",
            "safety": "Yes this is safe"
            })


# TODO: fix open telemetry so it doesn't slow app so much
FastAPIInstrumentor.instrument_app(app)
