from typing import List
import boto3
import awswrangler as wr
import pandas as pd
import warnings
import re
import enum
import os

class Sheet(enum.Enum):
        Patients="Patients"
        Baseline="Baseline"
        FollowUpDetails="Follow-Up Details"
        SurgicalResection="Surgical Resection"
        Objects="Objects"
        Diagnosis="Diagnosis"
        Correlations="Correlations"

class QuentryAnalyticsClient:
    __mockDataBucketPath = "MockData"
    __downloadFolder = "/tmp"

    @property
    def s3_bucket_base_uri(self) -> str:
        return f"s3://{self._bucket_name}"

    def __init__(self, use_mock_data=True, auth_token: str=None) -> None:
        self._bucket_name = "poc-data-for-google-colab"
        self._use_mock_data = use_mock_data
        self.__authenticateAwsSession(auth_token or self.getGoogleColabSecretAuthToken())

    def __authenticateAwsSession(self, auth_token):
        try:
            self._boto3_session = boto3.Session(
                aws_access_key_id=auth_token.split(";")[0],
                aws_secret_access_key=auth_token.split(";")[1]
            )
            sts = self._boto3_session.client('sts')
            caller_identity = sts.get_caller_identity()
            print(f"logged in as: {caller_identity['Arn']}")
        except:
            raise Exception("There was an error with your auth token.")
    

    def getGoogleColabSecretAuthToken(self) -> str:
        try: 
            from google.colab import userdata
            return userdata.get('QUENTRY_DATA_KEY')
        except userdata.SecretNotFoundError:
            print("Your QUENTRY_DATA_KEY colab secret was not found.")
            raise

    def getDataFrame(self, sheet: Sheet) -> pd.DataFrame:
        if self._use_mock_data:
            filename = f"{self.__mockDataBucketPath}/ExportedAnalyticsData.xlsx"
        else:
            warnings.showwarning("Currently only mock data is supported. Using mock data.")
            filename = f"{self.__mockDataBucketPath}/ExportedAnalyticsData.xlsx"

        file_url = f"s3://{self._bucket_name}/{filename}"
        warnings.filterwarnings('ignore', category=UserWarning, module=re.escape('openpyxl.styles.stylesheet'))
        return wr.s3.read_excel(file_url, sheet_name=sheet.value, boto3_session=self._boto3_session)
    
    def list_dicom_files(self, s3_uri: str) -> List[str]:
        return [path for path in wr.s3.list_objects(s3_uri, boto3_session=self._boto3_session)]
            
    def download_file(self, s3_uri: str) -> str:
      localfilepath = f"{self.__downloadFolder}/{s3_uri.split('//')[-1]}"
      if not os.path.exists(localfilepath):
        wr.s3.download(s3_uri, localfilepath, boto3_session=self._boto3_session)
      return localfilepath