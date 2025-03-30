"""
vBones - 간단한 Hello World 패키지
"""
try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0"  # 개발 환경에서 기본값