import asyncio
import uuid

from ai_benchmark import git
from ai_benchmark.workflows import workflow_1
from temporalio.client import (
    Client,
    WithStartWorkflowOperation,
    WorkflowUpdateStage,
)
from temporalio.common import WorkflowIDConflictPolicy
from temporalio.worker import Worker

TASK_QUEUE = "tq"


async def main():
    WORKFLOW_ID = str(uuid.uuid4())
    client = await Client.connect("localhost:7233")

    # Execute WFT 1 with previous version of workflow code
    git.assert_workspace_clean()
    git.checkout("HEAD~1", workflow_1.__file__)
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[workflow_1.MyWorkflow],
        max_cached_workflows=0,
        max_concurrent_workflow_task_polls=1,
    )
    start_op = WithStartWorkflowOperation(
        workflow_1.MyWorkflow.run,
        id=WORKFLOW_ID,
        task_queue=TASK_QUEUE,
        id_conflict_policy=WorkflowIDConflictPolicy.FAIL,
    )
    asyncio.create_task(worker.run())
    await client.start_update_with_start_workflow(
        workflow_1.MyWorkflow.update,
        start_workflow_operation=start_op,
        wait_for_stage=WorkflowUpdateStage.COMPLETED,
    )
    wf_handle = await start_op.workflow_handle()

    # Switch to new version of workflow code and execute WFT 2
    git.stash_changes()
    await wf_handle.execute_update(workflow_1.MyWorkflow.update)


if __name__ == "__main__":
    asyncio.run(main())
