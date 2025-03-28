"""This module contains the `generation` decorator and related utilities for tracing."""

from __future__ import annotations

import os
import json
import inspect
from types import MappingProxyType
from typing import (
    Any,
    Generic,
    Literal,
    TypeVar,
    Protocol,
    ParamSpec,
    TypeAlias,
    overload,
)
from contextlib import contextmanager
from contextvars import ContextVar
from collections.abc import Callable, Coroutine, Generator

from pydantic import BaseModel
from opentelemetry.trace import format_span_id, get_tracer_provider
from opentelemetry.util.types import AttributeValue
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from .spans import Span
from ._utils import (
    Closure,
    call_safely,
    fn_is_async,
    jsonable_encoder,
    inspect_arguments,
    get_qualified_name,
)
from .sandbox import SandboxRunner, SubprocessSandboxRunner
from .._client import Lilypad, AsyncLilypad
from .exceptions import RemoteFunctionError
from .._exceptions import NotFoundError
from ._utils.settings import get_settings
from ..types.ee.projects import Label, EvaluationType, annotation_create_params

_P = ParamSpec("_P")
_R = TypeVar("_R")
_R_CO = TypeVar("_R_CO", covariant=True)
_T = TypeVar("_T")


TRACE_TYPE = "trace"


class Annotation(BaseModel):
    data: dict[str, Any] | None

    label: Label | None

    reasoning: str | None

    type: EvaluationType | None


class _TraceBase(Generic[_T]):
    """
    Base class for the Trace wrapper.
    """

    def __init__(self, response: _T, span_id: int, function_uuid: str) -> None:
        self.response: _T = response
        self.function_uuid: str = function_uuid
        self.formated_span_id: str = format_span_id(span_id)

    def _create_body(
        self, project_id: str, span_uuid: str, annotation: Annotation | list[Annotation]
    ) -> list[annotation_create_params.Body]:
        if not isinstance(annotation, list):
            annotation = [annotation]
        return [
            annotation_create_params.Body(
                data=annotation.data,
                function_uuid=self.function_uuid,
                span_uuid=span_uuid,
                label=annotation.label,
                reasoning=annotation.reasoning,
                type=annotation.type,
                project_uuid=project_id,
            )
            for annotation in annotation
        ]


class Trace(_TraceBase[_T]):
    """
    A simple trace wrapper that holds the original function's response and allows annotating the trace.
    """

    def _get_span_uuid(self, client: Lilypad) -> str | None:
        response = client.projects.functions.spans.list(
            project_uuid=get_settings().project_id, function_uuid=self.function_uuid
        )
        for span in response:
            if span.span_id == self.formated_span_id:
                return span.uuid
        return None

    def annotate(self, annotation: Annotation | list[Annotation]) -> None:
        """
        Annotate the trace with the given annotation.
        """
        settings = get_settings()
        lilypad_client = Lilypad(api_key=settings.api_key)
        body = self._create_body(settings.project_id, self._get_span_uuid(lilypad_client), annotation)
        lilypad_client.ee.projects.annotations.create(project_uuid=settings.project_id, body=body)


class AsyncTrace(_TraceBase[_T]):
    """
    A simple trace wrapper that holds the original function's response and allows annotating the trace.
    """

    async def _get_span_uuid(self, client: AsyncLilypad) -> str | None:
        response = await client.projects.functions.spans.list(
            project_uuid=get_settings().project_id, function_uuid=self.function_uuid
        )
        for span in response:
            if span.span_id == self.formated_span_id:
                return span.uuid
        return None

    async def annotate(self, annotation: Annotation | list[Annotation]) -> None:
        """
        Annotate the trace with the given annotation.
        """
        settings = get_settings()
        lilypad_client = AsyncLilypad(api_key=settings.api_key)
        body = self._create_body(settings.project_id, await self._get_span_uuid(lilypad_client), annotation)
        await lilypad_client.ee.projects.annotations.create(project_uuid=settings.project_id, body=body)


def _get_batch_span_processor() -> BatchSpanProcessor | None:
    """Get the BatchSpanProcessor from the current TracerProvider.

    Retrieve the BatchSpanProcessor from the current TracerProvider dynamically.
    This avoids using a global variable by inspecting the provider's _active_span_processors.
    """
    tracer_provider = get_tracer_provider()
    processor = getattr(tracer_provider, "_active_span_processor", None)
    if not processor:
        return None
    _span_processors = getattr(processor, "_span_processors", None)
    if _span_processors:
        for processor in _span_processors:
            if isinstance(processor, BatchSpanProcessor):
                return processor
    return None


# Type definitions for decorator registry
FunctionInfo: TypeAlias = tuple[str, str, int, str]  # (file_path, function_name, line_number, module_name)
DecoratorRegistry: TypeAlias = dict[str, list[FunctionInfo]]

# Globals for decorator registry
_RECORDING_ENABLED: bool = False
_DECORATOR_REGISTRY: DecoratorRegistry = {}  # Maps decorator names to lists of function info


def enable_recording() -> None:
    """Enable recording of decorated functions."""
    global _RECORDING_ENABLED
    _RECORDING_ENABLED = True


def disable_recording() -> None:
    """Disable recording of decorated functions."""
    global _RECORDING_ENABLED
    _RECORDING_ENABLED = False


def clear_registry() -> None:
    """Clear the registry of decorated functions."""
    global _DECORATOR_REGISTRY
    _DECORATOR_REGISTRY = {}


def register_decorated_function(decorator_name: str, fn: Callable[..., Any]) -> None:
    """Register a function that has been decorated.

    Args:
        decorator_name: The name of the decorator
        fn: The decorated function
    """
    if not _RECORDING_ENABLED:
        return

    try:
        # Get function information
        file_path: str = inspect.getfile(fn)
        abs_path: str = os.path.abspath(file_path)
        lineno: int = inspect.getsourcelines(fn)[1]
        # Use Closure.from_fn to get the wrapped function name
        function_name: str = Closure.from_fn(fn).name
        module_name: str = fn.__module__

        # Add to registry
        if decorator_name not in _DECORATOR_REGISTRY:
            _DECORATOR_REGISTRY[decorator_name] = []

        # Store (file_path, function_name, line_number, module_name)
        _DECORATOR_REGISTRY[decorator_name].append((abs_path, function_name, lineno, module_name))
    except (TypeError, OSError):
        # Handle cases where inspect might fail (e.g., built-in functions)
        pass


def get_decorated_functions(decorator_name: str | None = None) -> DecoratorRegistry:
    """Get information about registered decorated functions.

    Args:
        decorator_name: Optional name of decorator to filter by

    Returns:
        Dictionary mapping decorator names to lists of function information tuples
    """
    if decorator_name:
        return {decorator_name: _DECORATOR_REGISTRY.get(decorator_name, [])}
    return _DECORATOR_REGISTRY.copy()


class SyncVersionedFunction(Protocol[_P, _R_CO]):
    """Protocol for the `VersionedFunction` decorator return type."""

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _R_CO:
        """Protocol for the `VersionFunction` decorator return type."""
        ...

    def version(
        self,
        forced_version: int,
        sandbox_runner: SandboxRunner | None = None,
    ) -> Callable[_P, _R_CO]:
        """Protocol for the `VersionFunction` decorator return type."""
        ...

    def remote(
        self,
        sandbox_runner: SandboxRunner | None = None,
    ) -> _R_CO:
        """Protocol for the `VersionFunction` decorator return type."""
        ...


class AsyncVersionedFunction(Protocol[_P, _R_CO]):
    """Protocol for the `VersionFunction` decorator return type."""

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> Coroutine[Any, Any, _R_CO]:
        """Protocol for the `VersionFunction` decorator return type."""
        ...

    def version(
        self,
        forced_version: int,
        sandbox_runner: SandboxRunner | None = None,
    ) -> Coroutine[Any, Any, Callable[_P, Coroutine[Any, Any, _R_CO]]]:
        """Protocol for the `VersionFunction` decorator return type."""
        ...

    def remote(
        self,
        sandbox_runner: SandboxRunner | None = None,
    ) -> Coroutine[Any, Any, _R_CO]:
        """Protocol for the `VersionFunction` decorator return type."""
        ...


class TraceDecoratedFunctionWithContext(Protocol[_P, _R]):
    """Protocol for the `VersioningDecorator` decorator return type."""

    def __call__(self, trace_ctx: Span, *args: _P.args, **kwargs: _P.kwargs) -> _R: ...


class TraceDecorator(Protocol):
    """Protocol for the `VersioningDecorator` decorator return type."""

    @overload
    def __call__(
        self, fn: TraceDecoratedFunctionWithContext[_P, Coroutine[Any, Any, _R]]
    ) -> Callable[_P, Coroutine[Any, Any, _R]]: ...

    @overload
    def __call__(self, fn: TraceDecoratedFunctionWithContext[_P, _R]) -> Callable[_P, _R]: ...

    @overload
    def __call__(self, fn: Callable[_P, Coroutine[Any, Any, _R]]) -> Callable[_P, Coroutine[Any, Any, _R]]: ...

    @overload
    def __call__(self, fn: Callable[_P, _R]) -> Callable[_P, _R]: ...

    def __call__(
        self,
        fn: TraceDecoratedFunctionWithContext[_P, Coroutine[Any, Any, _R]]
        | TraceDecoratedFunctionWithContext[_P, _R]
        | Callable[_P, _R]
        | Callable[_P, Coroutine[Any, Any, _R]],
    ) -> Callable[_P, _R] | Callable[_P, Coroutine[Any, Any, _R]]:
        """Protocol `call` definition for `VersioningDecorator` decorator return type."""
        ...


class WrappedTraceDecorator(Protocol):
    """Protocol for the `WrappedTraceDecorator` decorator return type."""

    @overload
    def __call__(
        self, fn: TraceDecoratedFunctionWithContext[_P, Coroutine[Any, Any, _R]]
    ) -> Callable[_P, Coroutine[Any, Any, Trace[_R]]]: ...

    @overload
    def __call__(self, fn: TraceDecoratedFunctionWithContext[_P, _R]) -> Callable[_P, Trace[_R]]: ...

    @overload
    def __call__(self, fn: Callable[_P, Coroutine[Any, Any, _R]]) -> Callable[_P, Coroutine[Any, Any, Trace[_R]]]: ...

    @overload
    def __call__(self, fn: Callable[_P, _R]) -> Callable[_P, Trace[_R]]: ...

    def __call__(
        self,
        fn: TraceDecoratedFunctionWithContext[_P, Coroutine[Any, Any, _R]]
        | TraceDecoratedFunctionWithContext[_P, _R]
        | Callable[_P, _R]
        | Callable[_P, Coroutine[Any, Any, _R]],
    ) -> Callable[_P, Trace[_R]] | Callable[_P, Coroutine[Any, Any, Trace[_R]]]:
        """Protocol `call` definition for `VersioningDecorator` decorator return type."""
        ...


class VersionedFunctionTraceDecorator(Protocol):
    """Protocol for the `VersionedFunction` decorator return type."""

    @overload
    def __call__(
        self, fn: TraceDecoratedFunctionWithContext[_P, Coroutine[Any, Any, _R]]
    ) -> AsyncVersionedFunction[_P, _R]: ...

    @overload
    def __call__(self, fn: TraceDecoratedFunctionWithContext[_P, _R]) -> SyncVersionedFunction[_P, _R]: ...

    @overload
    def __call__(self, fn: Callable[_P, Coroutine[Any, Any, _R]]) -> AsyncVersionedFunction[_P, _R]: ...

    @overload
    def __call__(self, fn: Callable[_P, _R]) -> SyncVersionedFunction[_P, _R]: ...

    def __call__(
        self,
        fn: TraceDecoratedFunctionWithContext[_P, Coroutine[Any, Any, _R]]
        | TraceDecoratedFunctionWithContext[_P, _R]
        | Callable[_P, _R]
        | Callable[_P, Coroutine[Any, Any, _R]],
    ) -> AsyncVersionedFunction[_P, _R] | SyncVersionedFunction[_P, _R]:
        """Protocol `call` definition for `VersionedFunction` decorator return type."""
        ...


class WrappedVersionedFunctionTraceDecorator(Protocol):
    """Protocol for the `WrappedVersionedFunctionTraceDecorator` decorator return type."""

    @overload
    def __call__(
        self, fn: TraceDecoratedFunctionWithContext[_P, Coroutine[Any, Any, _R]]
    ) -> AsyncVersionedFunction[_P, Trace[_R]]: ...

    @overload
    def __call__(self, fn: TraceDecoratedFunctionWithContext[_P, _R]) -> SyncVersionedFunction[_P, Trace[_R]]: ...

    @overload
    def __call__(self, fn: Callable[_P, Coroutine[Any, Any, _R]]) -> AsyncVersionedFunction[_P, Trace[_R]]: ...

    @overload
    def __call__(self, fn: Callable[_P, _R]) -> SyncVersionedFunction[_P, Trace[_R]]: ...

    def __call__(
        self,
        fn: TraceDecoratedFunctionWithContext[_P, Coroutine[Any, Any, _R]]
        | TraceDecoratedFunctionWithContext[_P, _R]
        | Callable[_P, _R]
        | Callable[_P, Coroutine[Any, Any, _R]],
    ) -> AsyncVersionedFunction[_P, Trace[_R]] | SyncVersionedFunction[_P, Trace[_R]]:
        """Protocol `call` definition for `VersionedFunction` decorator return type."""
        ...


_TraceAttribute: TypeAlias = dict[str, AttributeValue]


class _ResultHolder:
    """A class to hold the result of a function call."""

    def __init__(self) -> None:
        self.result = None

    def set_result(self, result: Any) -> None:
        """Set the result attribute."""
        self.result: Any = result


_trace_context: ContextVar[MappingProxyType] = ContextVar("_trace_context", default=MappingProxyType({}))


def _get_trace_context() -> dict[str, Any]:
    return dict(_trace_context.get())


def _set_trace_context(trace_ctx: dict[str, Any]) -> None:
    _trace_context.set(MappingProxyType(trace_ctx.copy()))


@contextmanager
def _set_span_attributes(
    trace_type: str, span: Span, span_attribute: _TraceAttribute, is_async: bool
) -> Generator[_ResultHolder, None, None]:
    """Set the attributes on the span."""
    settings = get_settings()
    span_attribute["lilypad.project_uuid"] = settings.project_id if settings.project_id else ""
    span_attribute["lilypad.type"] = trace_type
    span_attribute["lilypad.is_async"] = is_async
    span.opentelemetry_span.set_attributes(span_attribute)
    result_holder = _ResultHolder()
    yield result_holder
    original_output = result_holder.result
    output_for_span = original_output.model_dump() if isinstance(original_output, BaseModel) else original_output
    span.opentelemetry_span.set_attribute(f"lilypad.{trace_type}.output", str(output_for_span))


def _construct_trace_attributes(
    arg_types: dict[str, str],
    arg_values: dict[str, Any],
) -> dict[str, AttributeValue]:
    jsonable_arg_values = {}
    for arg_name, arg_value in arg_values.items():
        try:
            serialized_arg_value = jsonable_encoder(arg_value)
        except ValueError:
            serialized_arg_value = "could not serialize"
        jsonable_arg_values[arg_name] = serialized_arg_value
    return {
        "lilypad.trace.arg_types": json.dumps(arg_types),
        "lilypad.trace.arg_values": json.dumps(jsonable_arg_values),
    }


@overload
def trace(versioning: None = None, mode: None = None) -> TraceDecorator: ...


@overload
def trace(versioning: Literal["automatic"], mode: None = None) -> VersionedFunctionTraceDecorator: ...


@overload
def trace(versioning: None, mode: Literal["wrap"]) -> WrappedTraceDecorator: ...


@overload
def trace(versioning: Literal["automatic"], mode: Literal["wrap"]) -> WrappedVersionedFunctionTraceDecorator: ...


def trace(
    versioning: Literal["automatic"] | None = None, mode: Literal["wrap"] | None = None
) -> TraceDecorator | VersionedFunctionTraceDecorator:
    """The tracing LLM generations.

    The decorated function will trace and log automatically.
    If mode="wrap" is set, the function will return a Trace[_R] object with a 'response' property containing the original function's response and an 'annotate' method.
    """

    @overload
    def decorator(
        fn: TraceDecoratedFunctionWithContext[_P, Coroutine[Any, Any, _R]],
    ) -> Callable[_P, Coroutine[Any, Any, _R]]: ...

    @overload
    def decorator(fn: TraceDecoratedFunctionWithContext[_P, _R]) -> Callable[_P, _R]: ...

    @overload
    def decorator(fn: Callable[_P, Coroutine[Any, Any, _R]]) -> Callable[_P, Coroutine[Any, Any, _R]]: ...

    @overload
    def decorator(fn: Callable[_P, _R]) -> Callable[_P, _R]: ...

    def decorator(
        fn: TraceDecoratedFunctionWithContext[_P, Coroutine[Any, Any, _R]]
        | TraceDecoratedFunctionWithContext[_P, _R]
        | Callable[_P, _R]
        | Callable[_P, Coroutine[Any, Any, _R]],
    ) -> Callable[_P, _R] | Callable[_P, Coroutine[Any, Any, _R]]:
        if _RECORDING_ENABLED and versioning == "automatic":
            register_decorated_function("lilypad.lib.trace", fn)

        signature = inspect.signature(fn)
        closure = Closure.from_fn(fn)

        if fn_is_async(fn):

            @call_safely(fn)
            async def inner_async(*args: _P.args, **kwargs: _P.kwargs) -> _R:
                bound_args = signature.bind_partial(*args, **kwargs)

                with Span(get_qualified_name(fn)) as span:
                    if "trace_ctx" not in bound_args.arguments and "trace_ctx" in signature.parameters:
                        args = tuple((span, *args))
                    arg_types, arg_values = inspect_arguments(fn, *args, **kwargs)
                    arg_values.pop("trace_ctx", None)
                    arg_types, arg_values = inspect_arguments(fn, *args, **kwargs)
                    trace_attribute = _construct_trace_attributes(
                        arg_types=arg_types,
                        arg_values=arg_values,
                    )
                    settings = get_settings()
                    async_lilypad_client = AsyncLilypad(api_key=settings.api_key)

                    try:
                        function = await async_lilypad_client.projects.functions.retrieve_by_hash(
                            project_uuid=settings.project_id, function_hash=closure.hash
                        )
                    except NotFoundError:
                        function = await async_lilypad_client.projects.functions.create(
                            path_project_uuid=settings.project_id,
                            code=closure.code,
                            hash=closure.hash,
                            name=closure.name,
                            signature=closure.signature,
                            arg_types=arg_types,
                            dependencies=closure.dependencies,
                            is_versioned=True,
                        )
                    with _set_span_attributes(TRACE_TYPE, span, trace_attribute, is_async=True) as result_holder:
                        output = await fn(*args, **kwargs)
                        result_holder.set_result(output)
                    span_id = span.span_id
                    _set_trace_context({"span_id": span_id, "function_uuid": function.uuid})
                if mode == "wrap":
                    return AsyncTrace(response=output, span_id=span_id, function_uuid=function.uuid)
                return output  # pyright: ignore [reportReturnType]

            if versioning is None:
                return inner_async

            async def _specific_function_version_async(
                forced_version: int,
                sandbox: SandboxRunner | None = None,
            ) -> Callable[_P, _R]:
                settings = get_settings()
                async_lilypad_client = AsyncLilypad(api_key=settings.api_key)

                try:
                    versioned_function = await async_lilypad_client.projects.functions.name.retrieve_by_version(
                        version_num=forced_version,
                        project_uuid=settings.project_id,
                        function_name=closure.name,
                    )
                    versioned_function_closure = Closure(
                        name=versioned_function.name,
                        code=versioned_function.code,
                        signature=versioned_function.signature,
                        hash=versioned_function.hash,
                        dependencies={k: v.model_dump() for k, v in versioned_function.dependencies.items()}
                        if versioned_function.dependencies is not None
                        else {},
                    )
                except Exception as e:
                    raise RemoteFunctionError(f"Failed to retrieve function {fn.__name__}: {e}")

                if sandbox is None:
                    sandbox = SubprocessSandboxRunner(os.environ.copy())

                @call_safely(fn)  # pyright: ignore [reportArgumentType]
                def _inner_async(*args: _P.args, **kwargs: _P.kwargs) -> _R:
                    return sandbox.execute_function(
                        versioned_function_closure,
                        *args,
                        extra_result={"trace_context": "_get_trace_context()"},
                        extra_imports=["from lilypad.lib.trace import _get_trace_context"],
                        **kwargs,
                    )

                return _inner_async

            inner_async.version = _specific_function_version_async  # pyright: ignore [reportAttributeAccessIssue, reportFunctionMemberAccess]

            async def _deployed_version_async(
                *args: _P.args, sandbox: SandboxRunner | None = None, **kwargs: _P.kwargs
            ) -> _R:
                settings = get_settings()
                async_lilypad_client = AsyncLilypad(api_key=settings.api_key)

                try:
                    deployed_function = await async_lilypad_client.projects.functions.name.retrieve_deployed(
                        project_uuid=settings.project_id,
                        function_name=closure.name,
                    )
                    deployed_function_closure = Closure(
                        name=deployed_function.name,
                        code=deployed_function.code,
                        signature=deployed_function.signature,
                        hash=deployed_function.hash,
                        dependencies={k: v.model_dump() for k, v in deployed_function.dependencies.items()}
                        if deployed_function.dependencies is not None
                        else {},
                    )
                except Exception as e:
                    raise RemoteFunctionError(f"Failed to retrieve function {fn.__name__}: {e}")

                if sandbox is None:
                    sandbox = SubprocessSandboxRunner(os.environ.copy())

                result = sandbox.execute_function(
                    deployed_function_closure,
                    *args,
                    extra_result={"trace_context": "_get_trace_context()"},
                    extra_imports=["from lilypad.lib.trace import _get_trace_context"],
                    **kwargs,
                )
                if mode == "wrap":
                    return AsyncTrace(
                        response=result["result"],
                        span_id=result["trace_context"]["span_id"],
                        function_uuid=result["trace_context"]["function_uuid"],
                    )
                return result["result"]

            inner_async.remote = _deployed_version_async
            return inner_async
        else:

            @call_safely(fn)
            def inner(*args: _P.args, **kwargs: _P.kwargs) -> _R:
                bound_args = signature.bind_partial(*args, **kwargs)
                with Span(get_qualified_name(fn)) as span:
                    if "trace_ctx" not in bound_args.arguments and "trace_ctx" in signature.parameters:
                        args = tuple((span, *args))
                    arg_types, arg_values = inspect_arguments(fn, *args, **kwargs)
                    arg_values.pop("trace_ctx", None)
                    trace_attribute = _construct_trace_attributes(
                        arg_types=arg_types,
                        arg_values=arg_values,
                    )
                    settings = get_settings()
                    lilypad_client = Lilypad(api_key=settings.api_key)
                    try:
                        function = lilypad_client.projects.functions.retrieve_by_hash(
                            project_uuid=settings.project_id, function_hash=closure.hash
                        )
                    except NotFoundError:
                        function = lilypad_client.projects.functions.create(
                            path_project_uuid=settings.project_id,
                            code=closure.code,
                            hash=closure.hash,
                            name=closure.name,
                            signature=closure.signature,
                            arg_types=arg_types,
                            dependencies=closure.dependencies,
                            is_versioned=True,
                        )

                    with _set_span_attributes(TRACE_TYPE, span, trace_attribute, is_async=False) as result_holder:
                        output = fn(*args, **kwargs)
                        result_holder.set_result(output)
                    span_id = span.span_id
                    _set_trace_context({"span_id": span_id, "function_uuid": function.uuid})
                if mode == "wrap":
                    return Trace(response=output, span_id=span_id, function_uuid=function.uuid)
                return output  # pyright: ignore [reportReturnType]

            if versioning is None:
                return inner  # pyright: ignore [reportReturnType]

            def _specific_function_version(
                forced_version: int,
                sandbox: SandboxRunner | None = None,
            ) -> Callable[_P, _R]:
                settings = get_settings()
                lilypad_client = Lilypad(api_key=settings.api_key)

                try:
                    versioned_function = lilypad_client.projects.functions.name.retrieve_by_version(
                        version_num=forced_version,
                        project_uuid=settings.project_id,
                        function_name=closure.name,
                    )
                    versioned_function_closure = Closure(
                        name=versioned_function.name,
                        code=versioned_function.code,
                        signature=versioned_function.signature,
                        hash=versioned_function.hash,
                        dependencies={k: v.model_dump() for k, v in versioned_function.dependencies.items()}
                        if versioned_function.dependencies is not None
                        else {},
                    )
                except Exception as e:
                    raise RemoteFunctionError(f"Failed to retrieve function {fn.__name__}: {e}")

                if sandbox is None:
                    sandbox = SubprocessSandboxRunner(os.environ.copy())

                @call_safely(fn)  # pyright: ignore [reportArgumentType]
                def _inner(*args: _P.args, **kwargs: _P.kwargs) -> _R:
                    return sandbox.execute_function(
                        versioned_function_closure,
                        *args,
                        extra_result={"trace_context": "_get_trace_context()"},
                        extra_imports=["from lilypad.lib.trace import _get_trace_context"],
                        **kwargs,
                    )

                return _inner

            inner.version = _specific_function_version  # pyright: ignore [reportAttributeAccessIssue, reportFunctionMemberAccess]

            def _deployed_version(*args: _P.args, sandbox: SandboxRunner | None = None, **kwargs: _P.kwargs) -> _R:
                settings = get_settings()
                lilypad_client = Lilypad(api_key=settings.api_key)

                try:
                    deployed_function = lilypad_client.projects.functions.name.retrieve_deployed(
                        project_uuid=settings.project_id,
                        function_name=closure.name,
                    )
                    deployed_function_closure = Closure(
                        name=deployed_function.name,
                        code=deployed_function.code,
                        signature=deployed_function.signature,
                        hash=deployed_function.hash,
                        dependencies={k: v.model_dump() for k, v in deployed_function.dependencies.items()}
                        if deployed_function.dependencies is not None
                        else {},
                    )
                except Exception as e:
                    raise RemoteFunctionError(f"Failed to retrieve function {fn.__name__}: {e}")

                if sandbox is None:
                    sandbox = SubprocessSandboxRunner(os.environ.copy())

                result = sandbox.execute_function(
                    deployed_function_closure,
                    *args,
                    extra_result={"trace_context": "_get_trace_context()"},
                    extra_imports=["from lilypad.lib.trace import _get_trace_context"],
                    **kwargs,
                )
                if mode == "wrap":
                    return Trace(
                        response=result["result"],
                        span_id=result["trace_context"]["span_id"],
                        function_uuid=result["trace_context"]["function_uuid"],
                    )
                return result["result"]

            inner.remote = _deployed_version
            return inner

    return decorator
