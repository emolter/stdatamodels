from .reference import ReferenceFileModel

__all__ = ["PictureFrameModel"]


class PictureFrameModel(ReferenceFileModel):
    """
    A data model for 2D thermal picture frame reference files.

    Attributes
    ----------
    data : numpy float32 array
        Picture frame rate data.
    """

    schema_url = "http://stsci.edu/schemas/jwst_datamodel/pictureframe.schema"
