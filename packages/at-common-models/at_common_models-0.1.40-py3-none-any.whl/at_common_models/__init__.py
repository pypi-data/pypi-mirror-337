# Import all models to register them with SQLAlchemy
from .system.cache import CacheModel
from .system.prompt import PromptModel
from .system.workflow import WorkflowModel
from .user.account import UserAccount
from .user.oauth import UserOAuth
from .user.subscription import UserSubscription
from .base import BaseModel
from .stock.company_profile import StockCompanyProfile
from .stock.entry import StockEntry
from .stock.similarity import StockSimilarity

# These imports will register all models with the Base.metadata
__all__ = [
    'BaseModel',
    'CacheModel',
    'PromptModel',
    'WorkflowModel',
    'UserAccount',
    'UserOAuth',
    'UserSubscription',
    'StockCompanyProfile',
    'StockEntry',
    'StockSimilarity'
]
