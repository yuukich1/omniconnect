from enum import Enum


class ChatType(Enum):
    PRIVATE = 'private' # 1-1
    GROUP = 'group' 
    CHANNEL = 'channel' 
    SUPPORT = 'support'
    EXTERNAL = 'external'
    
class MemberRole(Enum):
    OWNER = 'owner'
    MEMBER = 'member'
    ADMIN = 'admin'