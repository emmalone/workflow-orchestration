#!/usr/bin/env python3
"""
Hugo Builder Worker
Executes Hugo build tasks and writes structured results.

Phase 1: Manual execution - processes one task then exits
Phase 2+: Continuous mode - watches for new tasks

Usage:
    python3 hugo_builder.py [task-file.md]

If no task file specified, processes first pending hugo-build task.
"""

import sys
import subprocess
import yaml
import time
from pathlib import Path
from datetime import datetime
import re


# Configuration
WORKFLOW_DIR = Path("/Users/mark/PycharmProjects/workflow")
TASKS_DIR = WORKFLOW_DIR / "tasks"
RESULTS_DIR = WORKFLOW_DIR / "results"


def log(message):
    """Simple logging with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def parse_task_file(task_path):
    """Parse task file with YAML frontmatter"""
    with open(task_path, 'r') as f:
        content = f.read()

    # Split frontmatter and body
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()
            return frontmatter, body

    raise ValueError("Invalid task file format - missing YAML frontmatter")


def execute_hugo_build(params):
    """Execute hugo build command with given parameters"""
    site_path = params.get('site_path')
    environment = params.get('environment', 'dev')
    base_url = params.get('base_url')
    minify = params.get('minify', True)
    clean = params.get('clean', True)

    # Build hugo command
    cmd = ['hugo']

    if base_url:
        cmd.extend(['--baseURL', base_url])

    if environment:
        cmd.extend(['--environment', environment])

    if minify:
        cmd.append('--minify')

    if clean:
        cmd.append('--cleanDestinationDir')

    log(f"Executing: {' '.join(cmd)}")
    log(f"Working directory: {site_path}")

    # Execute command
    start_time = time.time()
    result = subprocess.run(
        cmd,
        cwd=site_path,
        capture_output=True,
        text=True,
        timeout=120  # 2 minute timeout
    )
    duration = time.time() - start_time

    # Parse hugo output
    success = result.returncode == 0
    errors = parse_errors(result.stderr) if result.stderr else []
    warnings = parse_warnings(result.stdout) if result.stdout else []

    # Count files in public/ directory
    public_dir = Path(site_path) / 'public'
    file_count = count_files(public_dir) if public_dir.exists() else 0

    # Extract hugo version
    hugo_version = extract_hugo_version(result.stdout)

    # Extract pages generated
    pages_generated = extract_pages_count(result.stdout)

    return {
        'status': 'success' if success else 'failed',
        'duration_seconds': round(duration, 2),
        'outputs': {
            'build_success': success,
            'file_count': file_count,
            'errors': errors,
            'warnings': warnings,
            'hugo_version': hugo_version,
            'pages_generated': pages_generated
        },
        'build_log': result.stdout,
        'error_log': result.stderr,
        'returncode': result.returncode
    }


def parse_errors(stderr):
    """Extract errors from hugo stderr output"""
    errors = []
    for line in stderr.split('\n'):
        if 'ERROR' in line.upper() or 'FAIL' in line.upper():
            errors.append(line.strip())
    return errors


def parse_warnings(stdout):
    """Extract warnings from hugo stdout output"""
    warnings = []
    for line in stdout.split('\n'):
        if 'WARN' in line.upper():
            warnings.append(line.strip())
    return warnings


def extract_hugo_version(stdout):
    """Extract hugo version from output"""
    match = re.search(r'hugo v([\d.]+)', stdout, re.IGNORECASE)
    return match.group(1) if match else 'unknown'


def extract_pages_count(stdout):
    """Extract number of pages generated from output"""
    # Look for patterns like "Total in X ms" or page counts
    match = re.search(r'(\d+) pages?', stdout, re.IGNORECASE)
    return int(match.group(1)) if match else 0


def count_files(directory):
    """Count all files in directory recursively"""
    return sum(1 for _ in Path(directory).rglob('*') if _.is_file())


def write_result_file(task_id, task_type, result):
    """Write structured result file"""
    # Create results directory for today
    today = datetime.now().strftime("%Y-%m-%d")
    result_dir = RESULTS_DIR / today
    result_dir.mkdir(parents=True, exist_ok=True)

    # Result file path
    result_file = result_dir / f"{task_id}.result.md"

    # Build frontmatter
    frontmatter = {
        'task_id': task_id,
        'task_type': task_type,
        'status': result['status'],
        'completed_at': datetime.now().isoformat(),
        'duration_seconds': result['duration_seconds'],
        'worker_id': f"hugo-builder-{Path.home().name}",
        'outputs': result['outputs']
    }

    # Build body
    body = f"""## Build Summary
Build {'completed successfully' if result['status'] == 'success' else 'FAILED'}.

## Statistics
- Status: {result['status']}
- Duration: {result['duration_seconds']} seconds
- Files generated: {result['outputs']['file_count']}
- Pages: {result['outputs']['pages_generated']}
- Hugo version: {result['outputs']['hugo_version']}
- Errors: {len(result['outputs']['errors'])}
- Warnings: {len(result['outputs']['warnings'])}

## Build Output
```
{result['build_log'][:2000]}
```

## Errors
{"No errors" if not result['outputs']['errors'] else '\\n'.join('- ' + e for e in result['outputs']['errors'])}

## Warnings
{"No warnings" if not result['outputs']['warnings'] else '\\n'.join('- ' + w for w in result['outputs']['warnings'])}

## Next Steps
{"Ready for deployment." if result['status'] == 'success' and not result['outputs']['errors'] else "Review errors and fix before proceeding."}
"""

    # Write file
    content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n\n{body}"
    result_file.write_text(content)

    log(f"Result written to: {result_file}")
    return result_file


def process_task(task_file):
    """Process a single hugo-build task"""
    task_path = Path(task_file)

    if not task_path.exists():
        log(f"ERROR: Task file not found: {task_path}")
        return False

    log(f"Processing task: {task_path.name}")

    # Move to in-progress
    in_progress_path = TASKS_DIR / "in-progress" / task_path.name
    task_path.rename(in_progress_path)
    log(f"Moved to in-progress: {in_progress_path.name}")

    try:
        # Parse task
        task, body = parse_task_file(in_progress_path)
        task_id = task.get('task_id')
        task_type = task.get('task_type')
        params = task.get('params', {})

        log(f"Task ID: {task_id}")
        log(f"Task Type: {task_type}")
        log(f"Environment: {params.get('environment')}")

        # Execute build
        result = execute_hugo_build(params)

        # Write result file
        result_file = write_result_file(task_id, task_type, result)

        # Move to completed or failed
        if result['status'] == 'success':
            completed_path = TASKS_DIR / "completed" / task_path.name
            in_progress_path.rename(completed_path)
            log(f"SUCCESS: Task completed -> {completed_path.name}")
        else:
            failed_path = TASKS_DIR / "failed" / task_path.name
            in_progress_path.rename(failed_path)
            log(f"FAILED: Task failed -> {failed_path.name}")

        return result['status'] == 'success'

    except Exception as e:
        log(f"ERROR: Exception during task processing: {e}")
        # Move to failed
        failed_path = TASKS_DIR / "failed" / task_path.name
        in_progress_path.rename(failed_path)
        return False


def find_pending_hugo_build_task():
    """Find first pending hugo-build task"""
    pending_dir = TASKS_DIR / "pending"
    for task_file in pending_dir.glob("*hugo-build*.md"):
        return task_file
    return None


def main():
    """Main entry point"""
    log("Hugo Builder Worker starting...")

    # Determine task file
    if len(sys.argv) > 1:
        task_file = sys.argv[1]
    else:
        task_file = find_pending_hugo_build_task()
        if not task_file:
            log("No pending hugo-build tasks found")
            return

    # Process task
    success = process_task(task_file)

    if success:
        log("Worker completed successfully")
        sys.exit(0)
    else:
        log("Worker completed with errors")
        sys.exit(1)


if __name__ == '__main__':
    main()
