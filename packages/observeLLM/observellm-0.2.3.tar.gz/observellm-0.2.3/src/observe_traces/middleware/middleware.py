import uuid
from typing import Optional, Dict, Any

from fastapi import Request

from observe_traces.config.context_util import (
    langfuse_context,
    request_context,
    tracer_context,
    request_metadata_context,
)


async def set_request_context(
    request: Request, call_next, metadata: Optional[Dict[str, Any]] = None
):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    if request_context.get() is None:
        token = request_context.set(request_id)

    # Set metadata if provided
    metadata_token = None
    if metadata is not None:
        metadata_token = request_metadata_context.set(metadata)

    try:
        response = await call_next(request)
    finally:
        request_context.reset(token)
        if metadata_token is not None:
            request_metadata_context.reset(metadata_token)

    response.headers["X-Request-ID"] = request_id
    return response


async def create_unified_trace(request: Request, call_next):
    try:
        trace_id = request.headers.get("X-Request-ID", None)
        langfuse_client = langfuse_context.get()

        token = None

        if not trace_id:
            trace = langfuse_client.trace(
                id=request_context.get(),
                name=request_context.get(),
                metadata=request_metadata_context.get(),
            )

            token = tracer_context.set(trace)

            trace_id = trace.id

        else:
            trace = langfuse_client.trace(id=trace_id)

        request.state.trace_id = trace_id

        response = await call_next(request)

        response.headers["X-Trace-ID"] = trace_id
    finally:
        tracer_context.reset(token)

    return response
