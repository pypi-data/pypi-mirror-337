from typing import Generator
from quentryanalytics.client import QuentryAnalyticsClient
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pydicom

class DicomFile:
    def __init__(self, filepath: str) -> None:
      self._filepath = filepath

    @property
    def name(self) -> str:
      return self._filepath.split("/")[-1]

    def to_pixel_matrix(self) -> np.ndarray:
      pixel_array = pydicom.dcmread(self._filepath).pixel_array
      normalized_pixel_array = pixel_array / np.max(pixel_array)
      inverted_pixel_array = np.ones(normalized_pixel_array.shape) - normalized_pixel_array
      return inverted_pixel_array
    
    def show(self) -> None:
      pixel_array = self.to_pixel_matrix()
      plt.title(self.name)
      plt.imshow(pixel_array, cmap=plt.cm.bone)
      plt.axis('off')
      plt.show()

class Series:
    __mock_patient_folder = "4th_Demo_Patient_30-Mar-2025_14_37"

    def __init__(self, client: QuentryAnalyticsClient, study: str, series: str) -> None:
      self._basepath = f'{client.s3_bucket_base_uri}/MockData/DownloadedQuentryFolder/{self.__mock_patient_folder}/{study}/{series}'
      self._client = client
      self._series = series
      self._study = study

    def get_images(self) -> Generator[DicomFile, None, None]:
      for path in self._client.list_dicom_files(self._basepath):
        yield DicomFile(self._client.download_file(path))

    def to_pixel_tensor(self) -> np.ndarray:
      firstimage = next(self.get_images())
      array_3d = np.stack([image.to_pixel_matrix() for image in self.get_images()
                            if image.to_pixel_matrix().shape == firstimage.to_pixel_matrix().shape
                          ]).T
      return array_3d

    def render_3d(self, pixel_value_cutoff: float=0.45, crop=(0,0,0,0,0,0)) -> None:
      array_3d = self.to_pixel_tensor()


      array_3d = array_3d[crop[0]:array_3d.shape[0]-crop[1],crop[2]:array_3d.shape[1]-crop[3], crop[4]:array_3d.shape[2]-crop[5]]
      X, Y, Z = np.argwhere(array_3d < pixel_value_cutoff).T
      width, depth, height = array_3d.shape

      fig = go.Figure(data=[go.Scatter3d(x=X, y=Y, z=Z,
                                          opacity=0.5,
                                          mode='markers',
                                          marker=dict(
                                              size=1.5,
                                              color=array_3d[X, Y, Z],
                                              colorscale='Greys'
                                          )
                                          )])

      long_dimension = max(width, depth)
      fig.update_layout(
              scene=dict(
                  xaxis=dict(title='',showticklabels=False,showgrid=False,zeroline=False),
                  yaxis=dict(title='',showticklabels=False,showgrid=False,zeroline=False),
                  zaxis=dict(title='',showticklabels=False,showgrid=False,zeroline=False),
                  aspectmode='manual',
                  aspectratio=dict(
                      x= min(2*array_3d.shape[0] / long_dimension, 1),
                      y= min(2*array_3d.shape[1] / long_dimension, 1),
                      z= min(2*array_3d.shape[2] / long_dimension, 1)
                      )
              ),
              width=800,
              height=800,
              margin=dict(r=20, b=10, l=10, t=10)
          )


      fig.show()