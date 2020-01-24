class ClimateArgumentError(TypeError):
    """Invalid Argument Given To Command"""
    pass

class ClimateConversionError(TypeError):
    """Invalid Data Given So Could Not Be Converted To Desired Datatype"""
    pass

class ClimateImportError(ImportError):
    """Could Not Access Module"""
    pass


