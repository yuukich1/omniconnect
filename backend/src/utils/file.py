import os
import uuid

import aiofiles

from src.core.config import settings


async def save_file_to_disk( content: bytes, original_filename: str, owner_id: int) -> str:
    _, ext = os.path.splitext(original_filename)
    
    unique_suffix = uuid.uuid4().hex[:12]
    local_filename = f"user_{owner_id}_{unique_suffix}{ext}"
    
    local_path = os.path.join(settings.UPLOAD_DIR, local_filename)
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    async with aiofiles.open(local_path, "wb") as f:
        await f.write(content)
        
    return local_path