from labtasker.client.core.api import ls_tasks


def get_counts(limit=100, extra_filter=None):
    extra_filter = extra_filter or {}
    status = ["pending", "running", "success", "failed", "cancelled"]
    results = {}
    for s in status:
        extra_filter["status"] = s
        cnt = len(ls_tasks(extra_filter=extra_filter, limit=limit).content)
        if cnt >= limit:
            results[s] = f">= {limit}"
        else:
            results[s] = cnt
    return results
