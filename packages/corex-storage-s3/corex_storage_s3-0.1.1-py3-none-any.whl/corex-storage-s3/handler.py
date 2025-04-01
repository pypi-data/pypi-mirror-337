import boto3
import json
import re
import threading
from typing import List, Callable, Any, Optional
from corex.interfaces.storage import StorageInterface

class S3Handler(StorageInterface):
    def __init__(self, bucket_name: str, region_name: str = 'us-east-1', sqs_queue_url: Optional[str] = None):
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.sqs_client = boto3.client('sqs', region_name=region_name) if sqs_queue_url else None
        self.bucket_name = bucket_name
        self.sqs_queue_url = sqs_queue_url
        self.event_listeners = {}  # key: (path, event), value: list of callbacks
        self._stop_watching = False
        self._watch_thread = None

    def save(self, source: str, destination: str) -> None:
        self.s3_client.upload_file(source, self.bucket_name, destination)
        self._trigger_event(destination, 'create')

    def delete(self, file_path: str) -> None:
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_path)
        self._trigger_event(file_path, 'delete')

    def list_files(self, directory: str) -> List[str]:
        file_list = []
        paginator = self.s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=self.bucket_name, Prefix=directory):
            if 'Contents' in page:
                for obj in page['Contents']:
                    file_list.append(obj['Key'])
        return file_list

    def search(self, directory: str, pattern: str, recursive: bool = True) -> List[str]:
        files = self.list_files(directory)
        regex = re.compile(pattern)
        return [f for f in files if regex.search(f)]

    def create_bucket(self, bucket_name: str) -> None:
        self.s3_client.create_bucket(Bucket=bucket_name)

    def delete_bucket(self, bucket_name: str) -> None:
        self.s3_client.delete_bucket(Bucket=bucket_name)

    def list_buckets(self) -> List[str]:
        response = self.s3_client.list_buckets()
        return [bucket['Name'] for bucket in response.get('Buckets', [])]

    def add_event_listener(self, path: str, event: str, callback: Callable[[str, str], Any]) -> None:
        key = (path, event)
        if key not in self.event_listeners:
            self.event_listeners[key] = []
        self.event_listeners[key].append(callback)

    def remove_event_listener(self, path: str, event: str, callback: Callable[[str, str], Any]) -> None:
        key = (path, event)
        if key in self.event_listeners and callback in self.event_listeners[key]:
            self.event_listeners[key].remove(callback)
            if not self.event_listeners[key]:
                del self.event_listeners[key]

    def watch(self, path: str) -> None:
        if self.sqs_queue_url and self.sqs_client:
            self._stop_watching = False
            self._watch_thread = threading.Thread(target=self._poll_sqs, args=(path,), daemon=True)
            self._watch_thread.start()
        else:
            print(f"Watching {path} for events (dummy implementation)")

    def stop_watch(self) -> None:
        self._stop_watching = True
        if self._watch_thread:
            self._watch_thread.join()

    def _poll_sqs(self, path: str) -> None:
        while not self._stop_watching:
            try:
                response = self.sqs_client.receive_message(
                    QueueUrl=self.sqs_queue_url,
                    MaxNumberOfMessages=10,
                    WaitTimeSeconds=20
                )
                messages = response.get("Messages", [])
                for message in messages:
                    body = json.loads(message.get("Body", "{}"))
                    records = body.get("Records", [])
                    for record in records:
                        s3_info = record.get("s3", {})
                        object_info = s3_info.get("object", {})
                        key = object_info.get("key", "")
                        event_name = record.get("eventName", "")
                        if "ObjectCreated" in event_name:
                            event_type = "create"
                        elif "ObjectRemoved" in event_name:
                            event_type = "delete"
                        else:
                            event_type = "modify"
                        self._trigger_event(key, event_type)
                    receipt_handle = message.get("ReceiptHandle")
                    if receipt_handle:
                        self.sqs_client.delete_message(QueueUrl=self.sqs_queue_url, ReceiptHandle=receipt_handle)
            except Exception:
                continue

    def _trigger_event(self, file_path: str, event: str) -> None:
        key = (file_path, event)
        listeners = self.event_listeners.get(key, [])
        for callback in listeners:
            try:
                callback(event, file_path)
            except Exception:
                pass
