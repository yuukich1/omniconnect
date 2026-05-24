import os
import uuid

import aiofiles

from src.core.config import settings


async def save_file_to_disk(content: bytes, original_filename: str, owner_id: int, subfolder: str = "") -> str:
    _, ext = os.path.splitext(original_filename)
    unique_suffix = uuid.uuid4().hex[:12]
    local_filename = f"user_{owner_id}_{unique_suffix}{ext}"
    
    target_dir = os.path.join(settings.UPLOAD_DIR, subfolder)
    local_path = os.path.join(target_dir, local_filename)
    
    os.makedirs(target_dir, exist_ok=True)
    
    async with aiofiles.open(local_path, "wb") as f:
        await f.write(content)
        
    return os.path.join(subfolder, local_filename).replace("\\", "/")