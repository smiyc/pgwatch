import yaml
import os

INPUT_FILE = "metrics.yaml"
OUTPUT_DIR = "cnpg_metrics"

def sanitize_filename(name):
    return name.replace(" ", "_").replace("/", "_")

def extract_sql(metric_data):
    sqls = metric_data.get("sqls", {})
    if isinstance(sqls, dict):
        for version in sorted(sqls.keys()):
            sql = sqls[version]
            if isinstance(sql, list):
                return "\n".join(sql)
            elif isinstance(sql, str):
                return sql
    return ""

def extract_init_sql(metric_data):
    init_sql = metric_data.get("init_sql")
    if isinstance(init_sql, list):
        return "\n".join(init_sql)
    elif isinstance(init_sql, str):
        return init_sql
    return None

def extract_gauges(metric_data):
    gauges = metric_data.get("gauges", [])
    if isinstance(gauges, list):
        return [{"name": g, "type": "gauge"} for g in gauges if g != "*"]
    return []

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(INPUT_FILE, "r") as f:
        data = yaml.safe_load(f)

    metrics = data.get("metrics", {})
    for name, metric_data in metrics.items():
        metric_yaml = {
            "query": extract_sql(metric_data),
            "metrics": extract_gauges(metric_data)
        }

        init_sql = extract_init_sql(metric_data)
        if init_sql:
            metric_yaml["init_sql"] = init_sql

        filename = os.path.join(OUTPUT_DIR, f"{sanitize_filename(name)}.yaml")
        with open(filename, "w") as out:
            yaml.dump(metric_yaml, out, sort_keys=False)
        print(f"Created: {filename}")

if __name__ == "__main__":
    main()
