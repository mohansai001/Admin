from fastapi import APIRouter, HTTPException
from vida.database.database import db_dependency
from vida.utils.crud_ops import AgentsOps as ao, AgentTaskOps as ato, AgentRunOps as aro, AgentMetricsOps as amo, DashboardOps as do
from vida.models.requests.Agents_table_requests import AgentCreateRequest, AgentUpdateRequest
from vida.models.requests.Agent_Task_requests import AgentTaskDetailsCreateRequest, AgentTaskDetailsUpdateRequest
from vida.models.requests.Agent_Run_request import AgentRunCreateRequest, AgentRunUpdateRequest
from vida.models.requests.Agent_Metrics_requests import AgentMetricsCreateRequest, AgentMetricsUpdateRequest

router = APIRouter()

# ── Dashboard ─────────────────────────────────────────────────────────────────
@router.get("/dashboard/summary")
async def get_dashboard_summary(db: db_dependency):
    return do().get_summary(db)

@router.get("/dashboard/task-breakdown")
async def get_task_breakdown(db: db_dependency):
    return do().get_agent_task_status_breakdown(db)

@router.get("/dashboard/run-breakdown")
async def get_run_breakdown(db: db_dependency):
    return do().get_agent_run_status_breakdown(db)

@router.get("/dashboard/token-usage")
async def get_token_usage_summary(db: db_dependency):
    return do().get_token_usage_summary(db)


# ── Agents ────────────────────────────────────────────────────────────────────
@router.get("/agents/with-metrics")
async def get_all_agents_with_metrics(db: db_dependency):
    return ao().get_all_agents_with_metrics(db)

@router.get("/agents")
async def get_agents(db: db_dependency):
    return ao().get_agents(db)

@router.post("/agents")
async def add_agent(details: AgentCreateRequest, db: db_dependency):
    return ao().add_agent(db, details)

@router.patch("/agents/{agent_id}")
async def update_agent(agent_id: int, details: AgentUpdateRequest, db: db_dependency):
    result = ao().update_agent(db, agent_id, details)
    if not result:
        raise HTTPException(status_code=404, detail="Agent not found")
    return result

@router.get("/agents/{agent_id}/with-metrics")
async def get_agent_with_metrics(agent_id: int, db: db_dependency):
    agent = ao().get_agent_with_metrics(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.get("/agents/{agent_id}/run-stats")
async def get_agent_run_stats(agent_id: int, db: db_dependency):
    return aro().get_run_duration_stats(db, agent_id)

# ── Tasks ─────────────────────────────────────────────────────────────────────
@router.get("/tasks/paginated")
async def get_tasks_paginated(db: db_dependency, offset: int = 0, limit: int = 50):
    return ato().get_tasks_paginated(db, offset, limit)

@router.get("/tasks/status/{status}")
async def get_tasks_by_status(status: str, db: db_dependency):
    return ato().get_tasks_by_status(db, status)

@router.get("/tasks/agent/{agent_id}")
async def get_agent_tasks(agent_id: int, db: db_dependency):
    return ato().get_agent_tasks_by_agent_id(db, agent_id)

@router.get("/tasks/range/{from_task_id}/{to_task_id}")
async def get_tasks_in_range(from_task_id: int, to_task_id: int, db: db_dependency):
    return ato().get_agent_tasks(db, from_task_id, to_task_id)

@router.get("/tasks")
async def get_all_tasks(db: db_dependency):
    return ato().get_all_tasks(db)

@router.post("/tasks")
async def add_task(task: AgentTaskDetailsCreateRequest, db: db_dependency):
    return ato().add_task(db, task)

@router.patch("/tasks/{task_id}")
async def update_task(task_id: int, task: AgentTaskDetailsUpdateRequest, db: db_dependency):
    result = ato().update_task(db, task_id, task)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: db_dependency):
    result = ato().delete_task(db, task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

@router.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int, db: db_dependency):
    task = ato().get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# ── Runs ──────────────────────────────────────────────────────────────────────
@router.get("/runs/paginated")
async def get_runs_paginated(db: db_dependency, offset: int = 0, limit: int = 50):
    return aro().get_runs_paginated(db, offset, limit)

@router.get("/runs/status/{status}")
async def get_runs_by_status(status: str, db: db_dependency):
    return aro().get_runs_by_status(db, status)

@router.get("/runs/recent/{limit}")
async def get_recent_runs(limit: int, db: db_dependency):
    return aro().get_recent_runs(db, limit)

@router.get("/runs/task/{task_id}")
async def get_runs_by_task(task_id: int, db: db_dependency):
    return aro().get_run_by_task_id(db, task_id)

@router.get("/runs/agent/{agent_id}")
async def get_runs_by_agent(agent_id: int, db: db_dependency):
    return aro().get_run_by_agent_id(db, agent_id)

@router.get("/runs/range/{from_run_id}/{to_run_id}")
async def get_runs_in_range(from_run_id: int, to_run_id: int, db: db_dependency):
    return aro().get_runs(db, from_run_id, to_run_id)

@router.get("/runs")
async def get_all_runs(db: db_dependency):
    return aro().get_all_runs(db)

@router.post("/runs")
async def add_run(run: AgentRunCreateRequest, db: db_dependency):
    return aro().add_run(db, run)

@router.patch("/runs/{run_id}")
async def update_run(run_id: int, run: AgentRunUpdateRequest, db: db_dependency):
    result = aro().update_run(db, run_id, run)
    if not result:
        raise HTTPException(status_code=404, detail="Run not found")
    return result

@router.delete("/runs/{run_id}")
async def delete_run(run_id: int, db: db_dependency):
    result = aro().delete_run(db, run_id)
    if not result:
        raise HTTPException(status_code=404, detail="Run not found")
    return result

@router.get("/runs/{run_id}")
async def get_run_by_id(run_id: int, db: db_dependency):
    run = aro().get_run_by_id(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

# ── Metrics ───────────────────────────────────────────────────────────────────
@router.get("/metrics")
async def get_all_metrics(db: db_dependency):
    return amo().get_all_metrics(db)

@router.post("/metrics")
async def add_metrics(details: AgentMetricsCreateRequest, db: db_dependency):
    return amo().add_metrics(db, details)

@router.patch("/metrics/{agent_id}")
async def update_metrics(agent_id: int, details: AgentMetricsUpdateRequest, db: db_dependency):
    result = amo().update_metrics(db, agent_id, details)
    if not result:
        raise HTTPException(status_code=404, detail="Metrics not found")
    return result

@router.delete("/metrics/{agent_id}")
async def delete_metrics(agent_id: int, db: db_dependency):
    result = amo().delete_metrics(db, agent_id)
    if not result:
        raise HTTPException(status_code=404, detail="Metrics not found")
    return result

@router.get("/metrics/{agent_id}")
async def get_metrics_by_agent(agent_id: int, db: db_dependency):
    metrics = amo().get_metrics_by_agent_id(db, agent_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="Metrics not found")
    return metrics
