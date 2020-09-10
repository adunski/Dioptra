
import os
import shlex
import subprocess
from subprocess import CompletedProcess
from tempfile import TemporaryDirectory
from typing import List, Optional

import rq




def run_mlflow_task(
    workflow_uri: str,
    entry_point: str,
    conda_env: str = "base",
    entry_point_kwargs: Optional[str] = None,
) -> CompletedProcess:
    cmd: List[str] = [
        "/usr/local/bin/run-mlflow-job.sh",
        "--s3-workflow",
        workflow_uri,
        "--entry-point",
        entry_point,
        "--conda-env",
        conda_env,
    ]

    env = os.environ.copy()
    rq_job: Optional[rq.job.Job] = rq.get_current_job()

    if rq_job is not None:
        env["AI_RQ_JOB_ID"] = rq_job.get_id()

    if entry_point_kwargs is not None:
        cmd.extend(shlex.split(entry_point_kwargs))

    with TemporaryDirectory(dir=os.getenv("AI_WORKDIR")) as tmpdir:
        p = subprocess.run(args=cmd, cwd=tmpdir, env=env)

    if p.returncode > 0:
        return p

    return p
