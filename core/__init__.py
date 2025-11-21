"""
智能检索系统核心模块
"""

from .search_engine import IntelligentSearchEngine, SearchResult
from .document_generator import DocumentGenerator

__all__ = ['IntelligentSearchEngine', 'SearchResult', 'DocumentGenerator']
__version__ = "1.0.0"