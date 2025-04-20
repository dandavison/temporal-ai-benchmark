import asyncio

from temporalio import workflow


@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self):
        print("wf run")
        await asyncio.Future()

    @workflow.update
    def update(self):
        print("wf update")
        pass
