"""
AutoDiag Pro - Professional Automotive Diagnostic Tool
Main package initialization
"""

__version__ = "1.0.0"
__author__ = "AutoDiag Pro Team"
__description__ = "Professional automotive diagnostic tool for OBD/ELM interfaces"

from core.diagnostic import (
    Language,
    VehicleType,
    Manufacturer,
    DiagnosticTroubleCode,
    LiveDataParameter,
    VehicleInfo,
    DiagnosticSession,
)

__all__ = [
    'Language',
    'VehicleType',
    'Manufacturer',
    'DiagnosticTroubleCode',
    'LiveDataParameter',
    'VehicleInfo',
    'DiagnosticSession',
]
