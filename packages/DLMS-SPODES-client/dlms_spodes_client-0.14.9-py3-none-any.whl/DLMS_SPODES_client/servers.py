from dataclasses import dataclass, field
from typing import Optional, Any
from threading import Thread, Event
from functools import cached_property
import asyncio
from itertools import chain
from DLMSCommunicationProfile.osi import OSI
from .logger import LogLevel as logL
from .client import Client, Errors, cdt
from . import task


# todo: join with StructResult.Result
@dataclass(eq=False)
class SessionResult:
    client: Client
    complete: bool = False
    """complete exchange"""
    errors: Errors = field(default_factory=Errors)  # todo: remove in future, replace to <err>
    value: Optional[Any] = field(init=False)
    """response if available"""
    err: Optional[list[Exception]] = field(init=False)

    async def session(self, t: task.ExTask):
        self.client.lock.acquire(timeout=10)  # 10 second, todo: keep parameter anywhere
        assert self.client.media is not None, F"media is absense"  # try media open
        res = await t.run(self.client)
        self.value, self.err = res
        self.client.lock.release()
        self.complete = True
        self.errors = self.client.errors
        # media close
        if not self.client.lock.locked():
            self.client.lock.acquire(timeout=1)
            if self.client.media.is_open():
                self.client.log(logL.DEB, F"close communication channel: {self.client.media}")
                await self.client.media.close()
            else:
                self.client.log(logL.WARN, F"communication channel: {self.client.media} already closed")
            self.client.lock.release()
            self.client.level = OSI.NONE
        else:
            """opened media use in other session"""

    def __hash__(self):
        return hash(self.client)


class Results:
    __non_complete: set[SessionResult]
    __complete: set[SessionResult]
    name: str
    tsk: task.ExTask

    def __init__(self, clients: tuple[Client],
                 tsk: task.ExTask,
                 name: str = None):
        self.__non_complete = {SessionResult(c) for c in clients}
        self.__complete = set()
        self.tsk = tsk
        self.name = name
        """common operation name"""

    @cached_property
    def res(self) -> set[SessionResult]:
        return self.__non_complete | self.__complete

    def __getitem__(self, item) -> SessionResult:
        return tuple(self.res)[item]

    @cached_property
    def clients(self) -> set[Client]:
        return {res.client for res in self.res}

    @property
    def ok_results(self) -> set[SessionResult]:
        """without errors exchange clients"""
        return {res for res in self.__complete if res.err is None}

    @cached_property
    def nok_results(self) -> set[SessionResult]:
        """ With errors exchange clients """
        return self.res.difference(self.ok_results)

    def pop(self) -> set[SessionResult]:
        """get and move complete session"""
        to_move = {res for res in self.__non_complete if res.complete}
        self.__complete |= to_move
        self.__non_complete -= to_move
        return to_move

    def is_complete(self) -> bool:
        """check all complete sessions. call <pop> before"""
        return len(self.__non_complete) == 0


class TransactionServer:
    __t: Thread
    results: Results

    def __init__(self,
                 clients: list[Client] | tuple[Client],
                 tsk: task.ExTask,
                 name: str = None,
                 abort_timeout: int = 1):
        self.results = Results(clients, tsk, name)
        # self._tg = None
        self.__stop = Event()
        self.__t = Thread(
            target=self.__start_coro,
            args=(self.results, abort_timeout))

    def start(self):
        self.__t.start()

    def abort(self):
        self.__stop.set()

    def __start_coro(self, results, abort_timeout):
        asyncio.run(self.coro_loop(results, abort_timeout))

    async def coro_loop(self, results: Results, abort_timeout: int):
        async def check_stop(tg: asyncio.TaskGroup):
            while True:
                await asyncio.sleep(abort_timeout)
                if results.is_complete():
                    break
                elif self.__stop.is_set():
                    tg._abort()
                    break

        async with asyncio.TaskGroup() as tg:
            for res in results:
                # tg.create_task(
                    # coro=session(
                    #     c=res.client,
                    #     t=results.tsk,
                    #     result=res))
                tg.create_task(res.session(results.tsk))
            tg.create_task(
                coro=check_stop(tg),
                name="wait abort task")


async def session(c: Client,  # todo: move to Result as method
                  t: task.ExTask,
                  result: SessionResult):
    if not result:  # if not use TransActionServer
        result = SessionResult(c)
    c.lock.acquire(timeout=10)  # 10 second, todo: keep parameter anywhere
    # try media open
    assert c.media is not None, F"media is absense"
    result.value = await t.run(c)
    c.lock.release()
    result.complete = True
    result.errors = c.errors
    # media close
    if not c.lock.locked():
        c.lock.acquire(timeout=1)
        if c.media.is_open():
            await c.media.close()
            c.log(logL.DEB, F'Close communication channel: {c.media}')
        c.lock.release()
        c.level = OSI.NONE
    else:
        """opened media use in other session"""
    return result
