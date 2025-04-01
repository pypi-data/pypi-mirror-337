from finalsa.common.models import (SqsReponse)
from typing import Dict, List, Union, Optional
from uuid import uuid4
from abc import ABC, abstractmethod
from orjson import dumps
from finalsa.traceability import (
    get_correlation_id, get_trace_id, get_span_id,

)
from finalsa.traceability.functions import (
    ASYNC_CONTEXT_CORRELATION_ID,
    ASYNC_CONTEXT_TRACE_ID,
    ASYNC_CONTEXT_SPAN_ID,
)

class SqsService(ABC):

    @staticmethod
    def default_correlation_id():
        return str(uuid4())

    @abstractmethod
    def receive_messages(
            self,
            queue_url: str,
            max_number_of_messages: int = 1,
            wait_time_seconds: int = 1
    ) -> List[SqsReponse]:
        pass

    def send_message(
            self,
            queue_url: str,
            payload: Dict,
            message_attributes: Optional[Dict] = None,
    ) -> None:
        self.send_raw_message(queue_url, payload, message_attributes)

    def get_default_message_attrs(
        self,
    ) -> Dict:
        result = {
            ASYNC_CONTEXT_CORRELATION_ID: {'DataType': 'String', 'StringValue': get_correlation_id()},
            ASYNC_CONTEXT_TRACE_ID: {'DataType': 'String', 'StringValue': get_span_id()},
            ASYNC_CONTEXT_SPAN_ID: {'DataType': 'String', 'StringValue': get_trace_id()},
        }
        return result

    @abstractmethod
    def send_raw_message(
            self,
            queue_url: str,
            data: Union[Dict, str],
            message_attributes: Optional[Dict] = None,
    ) -> None:
        pass

    @staticmethod
    def __dump_payload__(payload: Union[Dict, str]) -> str:
        body = None
        if isinstance(payload, dict):
            body = dumps(payload)
            body = body.decode()
            return body
        return body

    @staticmethod
    def __parse_to_message__(
        payload: Union[Dict, str],
    ) -> Dict:
        if isinstance(payload, Dict):
            return payload
        return payload

    @abstractmethod
    def delete_message(self, queue_url: str, receipt_handle: str) -> None:
        pass

    @abstractmethod
    def get_queue_arn(self, queue_url: str) -> str:
        pass

    @abstractmethod
    def get_queue_attributes(self, queue_url: str, ) -> Dict:
        pass

    @abstractmethod
    def get_queue_url(self, queue_name: str) -> str:
        pass