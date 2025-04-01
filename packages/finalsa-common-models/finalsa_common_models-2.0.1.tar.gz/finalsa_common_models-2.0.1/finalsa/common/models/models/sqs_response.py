from typing import Dict, Optional, Union
from pydantic import BaseModel
from orjson import loads
from .functions import parse_sqs_message_attributes, parse_sns_message_attributes


class SqsReponse(BaseModel):
    message_id: str
    receipt_handle: str
    md5_of_body: str
    body: str
    attributes: Optional[Dict] = {}
    topic: Optional[str] = ""
    md5_of_message_attributes: Optional[str] = ""
    message_attributes: Optional[Dict] = {}

    @staticmethod
    def __is_sns_message__(content: Dict) -> bool:
        return 'Type' in content and content['Type'] == 'Notification'

    def parse_from_sns(self) -> Dict:
        payload = loads(self.body)
        if self.__is_sns_message__(payload):
            return self.__parse_from_sns__(payload)
        raise ValueError('The message is not a SNS message')

    def __parse_from_sns__(self, payload: Dict) -> Union[str, Dict]:
        self.topic = str(payload['TopicArn'].split(':')[-1]).lower()
        self.message_attributes = parse_sns_message_attributes(
            payload.get('MessageAttributes', {}))
        try:
            return loads(payload['Message'])
        except Exception:
            return payload['Message']

    def parse(self) -> Optional[Dict]:
        content = loads(self.body)
        if self.__is_sns_message__(content):
            content = self.__parse_from_sns__(content)
        return content

    def get_payload(self) -> Union[str, Dict]:
        try:
            content = loads(self.body)
        except Exception:
            return self.body
        if self.__is_sns_message__(content):
            content = self.__parse_from_sns__(content)
            return content
        return loads(self.body)

    @classmethod
    def from_boto_response(cls, response: Dict):
        return cls(
            message_id=response['MessageId'],
            receipt_handle=response['ReceiptHandle'],
            md5_of_body=response.get('MD5OfBody', ""),
            body=response['Body'],
            attributes=response['Attributes'],
            md5_of_message_attributes=response.get(
                'MD5OfMessageAttributes', ''),
            message_attributes=parse_sqs_message_attributes(
                response.get('MessageAttributes', {}))
        )
