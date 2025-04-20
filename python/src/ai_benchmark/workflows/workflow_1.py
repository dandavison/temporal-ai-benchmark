import asyncio
from dataclasses import dataclass

from temporalio import workflow

@dataclass
class MyInput:
    name: str


@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self, input: MyInput):
        print("wf run")
        await asyncio.Future()

    @workflow.update
    def update(self):
        print("wf update")
        pass
