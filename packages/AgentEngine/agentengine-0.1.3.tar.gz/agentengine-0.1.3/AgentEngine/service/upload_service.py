import os
import asyncio
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import aiofiles
from pathlib import Path

# 配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
MAX_CONCURRENT_UPLOADS = 5

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录
upload_dir = Path(UPLOAD_FOLDER)
upload_dir.mkdir(exist_ok=True)

# 并发控制
upload_semaphore = asyncio.Semaphore(MAX_CONCURRENT_UPLOADS)

def allowed_file(filename: str) -> bool:
    return True
    # return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def save_upload_file(file: UploadFile, upload_path: Path) -> bool:
    try:
        async with aiofiles.open(upload_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        return True
    except Exception as e:
        print(f"Error saving file {file.filename}: {str(e)}")
        return False

@app.post("/upload")
async def upload_files(file: List[UploadFile] = File(..., alias="file")):
    if not file:
        raise HTTPException(status_code=400, detail="No files in the request")
    
    uploaded_filenames = []
    errors = []
    
    async with upload_semaphore:
        for f in file:
            if not f:
                continue
                
            if not allowed_file(f.filename):
                errors.append(f"File type not allowed: {f.filename}")
                continue
            
            # 安全处理文件名
            safe_filename = os.path.basename(f.filename)
            upload_path = upload_dir / safe_filename
            
            # 保存文件
            if await save_upload_file(f, upload_path):
                uploaded_filenames.append(safe_filename)
            else:
                errors.append(f"Failed to save file: {f.filename}")
    
    if uploaded_filenames:
        return JSONResponse(
            status_code=201,
            content={
                "message": "Files uploaded successfully",
                "uploaded_files": uploaded_filenames
            }
        )
    else:
        print(f"Errors: {errors}")
        return JSONResponse(
            status_code=400,
            content={
                "error": "No valid files uploaded",
                "errors": errors
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3020)
