from typing import Dict
from datetime import datetime
from decimal import Decimal
from uuid import UUID


def parse_sns_message_attributes(attributes: Dict) -> Dict:
    message_attributes = {}
    if not attributes:
        return message_attributes
    for key, value in attributes.items():
        if value['Type'] == 'String':
            message_attributes[key] = value['Value']
        elif value['Type'] == 'Number':
            message_attributes[key] = int(value['Value'])
        elif value['Type'] == 'Binary':
            message_attributes[key] = bytes(value['Value'], 'utf-8')
    return message_attributes

def parse_sqs_message_attributes(attributes: Dict) -> Dict:
    message_attributes = {}
    if not attributes:
        return message_attributes
    for key, value in attributes.items():
        if value['DataType'] == 'String':
            message_attributes[key] = value['StringValue']
        elif value['DataType'] == 'Number':
            message_attributes[key] = int(value['StringValue'])
        elif value['DataType'] == 'Binary':
            message_attributes[key] = bytes(value['StringValue'], 'utf-8')
    return message_attributes

def to_sqs_message_attributes(attributes: Dict) -> Dict:
    att_dict = {}
    for key, value in attributes.items():
        if isinstance(value, str):
            att_dict[key] = {
                'DataType': 'String', 'StringValue': value}
        elif isinstance(value, Decimal):
            att_dict[key] = {
                'DataType': 'Number', 'StringValue': str(value)}
        elif isinstance(value, UUID):
            att_dict[key] = {
                'DataType': 'String', 'StringValue': str(value)}
        elif isinstance(value, datetime):
            att_dict[key] = {
                'DataType': 'String', 'StringValue': value.isoformat()}
        elif isinstance(value, int):
            att_dict[key] = {
                'DataType': 'Number', 'StringValue': str(value)}
        elif isinstance(value, bytes):
            att_dict[key] = {
                'DataType': 'Binary', 'BinaryValue': value}
    return att_dict



def to_sns_message_attributes(attributes: Dict) -> Dict:
    att_dict = {}
    for key, value in attributes.items():
        if isinstance(value, str):
            att_dict[key] = {
                'Type': 'String', 'Value': value}
        elif isinstance(value, Decimal):
            att_dict[key] = {
                'Type': 'Number', 'Value': str(value)}
        elif isinstance(value, UUID):
            att_dict[key] = {
                'Type': 'String', 'Value': str(value)}
        elif isinstance(value, datetime):
            att_dict[key] = {
                'Type': 'String', 'Value': value.isoformat()}
        elif isinstance(value, int):
            att_dict[key] = {
                'Type': 'Number', 'Value': str(value)}
        elif isinstance(value, bytes):
            att_dict[key] = {
                'Type': 'Binary', 'Value': value}
    return att_dict
