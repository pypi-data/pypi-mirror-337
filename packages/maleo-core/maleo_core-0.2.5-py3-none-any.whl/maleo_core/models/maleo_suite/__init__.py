# This file serves all MaleoSuite's models

from .maleo_shared import MaleoSharedModels

class MaleoSuiteModels:
    MaleoShared = MaleoSharedModels

__all__ = ["MaleoSuiteModels", "MaleoSharedModels"]