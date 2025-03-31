from __future__ import annotations

from asyncio import Lock, PriorityQueue, Queue, TaskGroup, run, sleep, timeout
from dataclasses import dataclass, field
from gc import collect
from itertools import chain
from re import search
from typing import TYPE_CHECKING, Self, override

from hypothesis import Phase, given, settings
from hypothesis.strategies import (
    DataObject,
    data,
    floats,
    integers,
    just,
    lists,
    none,
    permutations,
    sampled_from,
)
from pytest import mark, raises

from utilities.asyncio import (
    AsyncLoopingService,
    AsyncService,
    AsyncServiceError,
    BoundedTaskGroup,
    ExceptionProcessor,
    QueueProcessor,
    UniquePriorityQueue,
    UniqueQueue,
    get_items,
    get_items_nowait,
    sleep_dur,
    stream_command,
    timeout_dur,
)
from utilities.datetime import MILLISECOND, datetime_duration_to_timedelta
from utilities.hypothesis import settings_with_reduced_examples, text_ascii
from utilities.iterables import one, unique_everseen
from utilities.pytest import skipif_windows
from utilities.timer import Timer

if TYPE_CHECKING:
    from utilities.types import Duration


class TestAsyncLoopingService:
    @mark.flaky
    async def test_main(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncLoopingService):
            counter: int = 0

            @override
            async def _run(self) -> None:
                self.counter += 1
                await sleep(0.01)

        service = Example()
        assert service.counter == 0

        await service.start()
        await sleep(0.2)
        assert 10 <= service.counter <= 30


class TestAsyncService:
    async def test_start_and_stop(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncService):
            running: bool = False

            @override
            async def _start_core(self) -> None:
                self.running = True

            @override
            async def _stop_core(self) -> None:
                self.running = False

        service = Example()
        for _ in range(2):
            assert not service.running
            assert service._task is None

            for _ in range(2):
                await service.start()
                await sleep(0.01)
                assert service.running
                assert service._task is not None

            for _ in range(2):
                await service.stop()
                await sleep(0.01)
                assert not service.running
                assert service._task is None

    async def test_await_with_task(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncService):
            running: bool = False

            @override
            async def _start_core(self) -> None:
                self.running = True

            @override
            async def _stop_core(self) -> None:
                self.running = False

        service = Example()
        assert not service.running
        await service.start()
        assert await service is None
        assert service.running

    async def test_await_without_task(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncService):
            running: bool = False

            @override
            async def _start_core(self) -> None:
                self.running = True

            @override
            async def _stop_core(self) -> None:
                self.running = False

        service = Example()
        with raises(AsyncServiceError, match=".* is not running"):
            await service

    async def test_call_direct(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncService):
            running: bool = False

            @override
            async def _start_core(self) -> None:
                self.running = True

            @override
            async def _stop_core(self) -> None:
                self.running = False

        service = Example()
        assert not service.running
        assert await service() is None
        assert service.running

    async def test_call_in_task_group(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncService):
            running: bool = False

            @override
            async def _start_core(self) -> None:
                self.running = True

            @override
            async def _stop_core(self) -> None:
                self.running = False

        service = Example()
        assert not service.running
        async with TaskGroup() as tg:
            _ = tg.create_task(service())
        assert service.running

    async def test_context_manager(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncService):
            running: bool = False

            @override
            async def _start_core(self) -> None:
                self.running = True

            @override
            async def _stop_core(self) -> None:
                self.running = False

        service = Example()
        for _ in range(2):
            assert not service.running

            async with service:
                await sleep(0.01)
                assert service.running

            await sleep(0.01)
            assert not service.running

    async def test_del_with_task(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncService):
            running: bool = False

            @override
            async def _start_core(self) -> None:
                self.running = True

            @override
            async def _stop_core(self) -> None:
                self.running = False

        service = Example()
        assert service._task is None

        await service.start()
        await sleep(0.01)
        assert service._task is not None

        del service
        _ = collect()

    async def test_del_with_task_equal_to_none(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncService):
            running: bool = False

            @override
            async def _start_core(self) -> None:
                self.running = True

            @override
            async def _stop_core(self) -> None:
                self.running = False

        service = Example()
        assert service._task is None

        del service
        _ = collect()

    async def test_del_without_task_attribute(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncService):
            x: int

            @override
            async def _start_core(self) -> None:
                self.running = True

            @override
            async def _stop_core(self) -> None:
                self.running = False

        with raises(TypeError, match="missing 1 required keyword-only argument: 'x'"):
            _ = Example()  # pyright: ignore[reportCallIssue]

    async def test_extra_context_managers(self) -> None:
        @dataclass(kw_only=True)
        class Inner(AsyncService):
            running: bool = False

            @override
            async def _start_core(self) -> None:
                self.running = True

            @override
            async def _stop_core(self) -> None:
                self.running = False

        @dataclass(kw_only=True)
        class Outer(AsyncService):
            running: bool = False
            inner: Inner = field(default_factory=Inner, init=False, repr=False)

            @override
            async def __aenter__(self) -> Self:
                _ = await self._stack.enter_async_context(self.inner)
                return await super().__aenter__()

            @override
            async def _start_core(self) -> None:
                self.running = True

            @override
            async def _stop_core(self) -> None:
                self.running = False

        outer = Outer()
        for _ in range(2):
            assert not outer.running
            assert not outer.inner.running

            async with outer:
                await sleep(0.01)
                assert outer.running
                assert outer.inner.running

            await sleep(0.01)
            assert not outer.running
            assert not outer.inner.running

    async def test_new(self) -> None:
        @dataclass(kw_only=True)
        class Example(AsyncService):
            running: bool = False

            @override
            async def _start_core(self) -> None:
                self.running = True

            @override
            async def _stop_core(self) -> None:
                self.running = False

        service = await Example.new()
        await sleep(0.01)
        assert service.running

    def test_repr(self) -> None:
        class Example(AsyncService):
            @override
            async def _start_core(self) -> None:
                await sleep(0.01)

            @override
            async def _stop_core(self) -> None:
                await sleep(0.01)

        service = Example()
        result = repr(service)
        expected = "TestAsyncService.test_repr.<locals>.Example()"
        assert result == expected


class TestBoundedTaskGroup:
    async def test_with(self) -> None:
        with Timer() as timer:
            async with BoundedTaskGroup(max_tasks=2) as tg:
                for _ in range(10):
                    _ = tg.create_task(sleep(0.01))
        assert timer >= 0.05

    async def test_without(self) -> None:
        with Timer() as timer:
            async with BoundedTaskGroup() as tg:
                for _ in range(10):
                    _ = tg.create_task(sleep(0.01))
        assert timer <= 0.05


class TestExceptionProcessor:
    async def test_main(self) -> None:
        processor = ExceptionProcessor()

        class CustomError(Exception): ...

        async def yield_tasks() -> None:
            await sleep(0.01)
            processor.enqueue(CustomError)

        with raises(ExceptionGroup) as exc_info:  # noqa: PT012
            async with TaskGroup() as tg:
                _ = tg.create_task(processor())
                _ = tg.create_task(yield_tasks())

        assert len(exc_info.value.exceptions) == 1
        exception = one(exc_info.value.exceptions)
        assert isinstance(exception, CustomError)


class TestGetItems:
    @given(
        xs=lists(integers(), min_size=1),
        max_size=integers(1, 10) | none(),
        lock=just(Lock()) | none(),
    )
    async def test_put_then_get(
        self, *, xs: list[int], max_size: int | None, lock: Lock | None
    ) -> None:
        queue: Queue[int] = Queue()
        for x in xs:
            await queue.put(x)
        result = await get_items(queue, max_size=max_size, lock=lock)
        if max_size is None:
            assert result == xs
        else:
            assert result == xs[:max_size]

    @given(
        xs=lists(integers(), min_size=1),
        max_size=integers(1, 10) | none(),
        lock=just(Lock()) | none(),
    )
    async def test_get_then_put(
        self, *, xs: list[int], max_size: int | None, lock: Lock | None
    ) -> None:
        queue: Queue[int] = Queue()

        async def put() -> None:
            await sleep(0.01)
            for x in xs:
                await queue.put(x)

        async with TaskGroup() as tg:
            task = tg.create_task(get_items(queue, max_size=max_size, lock=lock))
            _ = tg.create_task(put())
        result = task.result()
        if max_size is None:
            assert result == xs
        else:
            assert result == xs[:max_size]

    async def test_empty(self) -> None:
        queue: Queue[int] = Queue()
        with raises(TimeoutError):  # noqa: PT012
            async with timeout(0.01), TaskGroup() as tg:
                _ = tg.create_task(get_items(queue))
                _ = tg.create_task(sleep(0.02))


class TestGetItemsNoWait:
    @given(
        xs=lists(integers(), min_size=1),
        max_size=integers(1, 10) | none(),
        lock=just(Lock()) | none(),
    )
    async def test_main(
        self, *, xs: list[int], max_size: int | None, lock: Lock | None
    ) -> None:
        queue: Queue[int] = Queue()
        for x in xs:
            await queue.put(x)
        result = await get_items_nowait(queue, max_size=max_size, lock=lock)
        if max_size is None:
            assert result == xs
        else:
            assert result == xs[:max_size]


class TestQueueProcessor:
    @given(n=integers(1, 10))
    async def test_one_processor_slow_tasks(self, *, n: int) -> None:
        @dataclass(kw_only=True)
        class Example(QueueProcessor[int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, item: int, /) -> None:
                self.output.add(item)

        processor = Example()

        async def yield_tasks() -> None:
            await processor.start()
            await sleep(0.01)
            for i in range(n):
                processor.enqueue(i)
                await sleep(0.01)
            await sleep(0.01)

        async with TaskGroup() as tg:
            _ = tg.create_task(yield_tasks())
            _ = tg.create_task(processor.run_until_empty())
        assert len(processor.output) == n
        await processor.stop()

    @given(n=integers(1, 10))
    async def test_one_processor_slow_run(self, *, n: int) -> None:
        @dataclass(kw_only=True)
        class Example(QueueProcessor[int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, item: int, /) -> None:
                self.output.add(item)
                await sleep(0.01)

        processor = Example()
        processor.enqueue(*range(n))
        async with TaskGroup() as tg:
            _ = tg.create_task(processor.run_until_empty())
        assert len(processor.output) == n
        await processor.stop()

    @given(n=integers(1, 10))
    async def test_one_processor_continually_adding(self, *, n: int) -> None:
        @dataclass(kw_only=True)
        class Example(QueueProcessor[int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, item: int, /) -> None:
                self.output.add(item)

        processor = Example()
        await processor.start()
        for i in range(n):
            processor.enqueue(i)
            await sleep(0.01)
        assert len(processor.output) == n

    @given(n=integers(0, 10))
    async def test_two_processors(self, *, n: int) -> None:
        @dataclass(kw_only=True)
        class First(QueueProcessor[int]):
            second: Second
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, item: int, /) -> None:
                self.second.enqueue(item)
                self.output.add(item)

        @dataclass(kw_only=True)
        class Second(QueueProcessor[int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, item: int, /) -> None:
                self.output.add(item)

        second = await Second.new()
        first = await First.new(second=second)

        async def yield_tasks() -> None:
            first.enqueue(*range(n))
            await first.run_until_empty()

        async with TaskGroup() as tg:
            _ = tg.create_task(yield_tasks())

        assert len(first.output) == n
        assert len(second.output) == n

    @given(n=integers(0, 10), duration=floats(0.0, 0.2))
    @settings_with_reduced_examples()
    async def test_cancellation(self, *, n: int, duration: float) -> None:
        @dataclass(kw_only=True)
        class Example(QueueProcessor[int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, item: int, /) -> None:
                self.output.add(item)
                await sleep(0.01)

        processor = Example()
        await processor.start()
        processor.enqueue(*range(n))
        async with timeout_dur(duration=duration):
            await processor
        assert processor.output == set(range(n))

    async def test_empty(self) -> None:
        class Example(QueueProcessor[int]):
            @override
            async def _process_item(self, item: int, /) -> None:
                _ = item

        processor = Example()
        assert processor.empty()
        processor.enqueue(0)
        assert not processor.empty()

    @given(n=integers(0, 10))
    async def test_get_items_nowait(self, *, n: int) -> None:
        @dataclass(kw_only=True)
        class Example(QueueProcessor[int]):
            output: set[int] = field(default_factory=set)

            @override
            async def _process_item(self, _: int, /) -> None:
                items = await self._get_items_nowait()
                self.output.add(len(items))

        processor = Example()
        processor.enqueue(*range(n + 1))
        await processor._run()
        result = one(processor.output)
        assert result == n

    @given(n=integers(0, 10))
    async def test_len(self, *, n: int) -> None:
        class Example(QueueProcessor[int]):
            @override
            async def _process_item(self, item: int) -> None:
                _ = item

        processor = Example()
        assert len(processor) == 0
        processor.enqueue(*range(n))
        assert len(processor) == n

    @given(data=data(), texts=lists(text_ascii(min_size=1), min_size=1))
    async def test_priority_queue(self, *, data: DataObject, texts: list[str]) -> None:
        @dataclass(kw_only=True)
        class Example(QueueProcessor[tuple[int, str]]):
            output: set[str] = field(default_factory=set)

            @override
            async def _process_item(self, item: tuple[int, str]) -> None:
                _, text = item
                self.output.add(text)

        processor = Example(queue_type=PriorityQueue)
        items = data.draw(permutations(list(enumerate(texts))))
        processor.enqueue(*items)
        await processor._run()
        result = one(processor.output)
        assert result == texts[0]


class TestUniquePriorityQueue:
    @given(data=data(), texts=lists(text_ascii(min_size=1), min_size=1, unique=True))
    async def test_main(self, *, data: DataObject, texts: list[str]) -> None:
        items = list(enumerate(texts))
        extra = data.draw(lists(sampled_from(items)))
        items_use = data.draw(permutations(list(chain(items, extra))))
        queue: UniquePriorityQueue[int, str] = UniquePriorityQueue()
        assert queue._set == set()
        for item in items_use:
            await queue.put(item)
        assert queue._set == set(texts)
        result = await get_items(queue)
        assert result == items
        assert queue._set == set()


class TestUniqueQueue:
    @given(x=lists(integers(), min_size=1))
    async def test_main(self, *, x: list[int]) -> None:
        queue: UniqueQueue[int] = UniqueQueue()
        assert queue._set == set()
        for x_i in x:
            await queue.put(x_i)
        assert queue._set == set(x)
        result = await get_items(queue)
        expected = list(unique_everseen(x))
        assert result == expected
        assert queue._set == set()


class TestSleepDur:
    @given(duration=sampled_from([0.1, 10 * MILLISECOND]))
    @mark.flaky
    @settings(phases={Phase.generate})
    async def test_main(self, *, duration: Duration) -> None:
        with Timer() as timer:
            await sleep_dur(duration=duration)
        assert timer >= datetime_duration_to_timedelta(duration / 2)

    async def test_none(self) -> None:
        with Timer() as timer:
            await sleep_dur()
        assert timer <= 0.01


class TestStreamCommand:
    @skipif_windows
    async def test_main(self) -> None:
        output = await stream_command(
            'echo "stdout message" && sleep 0.1 && echo "stderr message" >&2'
        )
        await sleep(0.01)
        assert output.return_code == 0
        assert output.stdout == "stdout message\n"
        assert output.stderr == "stderr message\n"

    @skipif_windows
    async def test_error(self) -> None:
        output = await stream_command("this-is-an-error")
        await sleep(0.01)
        assert output.return_code == 127
        assert output.stdout == ""
        assert search(
            r"^/bin/sh: (1: )?this-is-an-error: (command )?not found$", output.stderr
        )


class TestTimeoutDur:
    @given(duration=sampled_from([0.01, 5 * MILLISECOND]))
    @mark.flaky
    @settings(phases={Phase.generate})
    async def test_main(self, *, duration: Duration) -> None:
        with raises(TimeoutError):
            async with timeout_dur(duration=duration):
                await sleep_dur(duration=2 * duration)

    @mark.flaky
    async def test_custom_error(self) -> None:
        class CustomError(Exception): ...

        with raises(CustomError):
            async with timeout_dur(duration=0.05, error=CustomError):
                await sleep_dur(duration=0.1)


if __name__ == "__main__":
    _ = run(
        stream_command('echo "stdout message" && sleep 2 && echo "stderr message" >&2')
    )
