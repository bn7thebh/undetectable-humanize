"""Submit once and retrieve resumably; no third-party Python dependencies."""
import argparse
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

BASE = 'https://humanize.undetectable.ai'

def credential():
    key = os.environ.get('UNDETECTABLE_API_KEY', '').strip()
    if not key and os.name == 'nt':
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as registry:
                key = winreg.QueryValueEx(registry, 'UNDETECTABLE_API_KEY')[0].strip()
        except FileNotFoundError:
            pass
    if not key:
        raise ValueError('Configure UNDETECTABLE_API_KEY locally before using the API.')
    return key

def request(endpoint, payload, key):
    req = urllib.request.Request(BASE + endpoint, data=json.dumps(payload).encode('utf-8'),
        headers={'apikey': key, 'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        raise ValueError(f'API HTTP {exc.code}; check credentials, credits, parameters, or service status.') from None
    except (urllib.error.URLError, TimeoutError):
        raise ValueError('API connection failed or timed out. Do not automatically resubmit.') from None
    if not isinstance(result, dict) or result.get('error'):
        raise ValueError('API returned an error or unexpected response.')
    return result

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    submit = sub.add_parser('submit')
    submit.add_argument('--input', required=True, type=Path)
    submit.add_argument('--job', required=True, type=Path)
    submit.add_argument('--readability', choices=['High School', 'University', 'Doctorate', 'Journalist', 'Marketing'], default='High School')
    submit.add_argument('--purpose', choices=['General Writing', 'Essay', 'Article', 'Marketing Material', 'Story', 'Cover Letter', 'Report', 'Business Material', 'Legal Material'], default='General Writing')
    submit.add_argument('--strength', choices=['Quality', 'Balanced', 'More Human'], default='Balanced')
    submit.add_argument('--model', choices=['v2', 'v11', 'v11sr'], default='v2')
    fetch = sub.add_parser('fetch')
    fetch.add_argument('--job', required=True, type=Path)
    fetch.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(argv)
    if args.command == 'submit':
        content = args.input.read_text(encoding='utf-8-sig')
        if len(content.strip()) < 50:
            raise ValueError('Input must contain at least 50 characters.')
        key = credential()
        payload = {k: getattr(args, k) for k in ('readability', 'purpose', 'strength', 'model')}
        payload['content'] = content
        # Exclusive reservation prevents accidental duplicate charge after uncertain failure.
        with args.job.open('x', encoding='utf-8') as handle:
            json.dump({'state': 'submission_uncertain', 'message': 'Do not resubmit automatically.'}, handle)
        result = request('/submit', payload, key)
        if not isinstance(result.get('id'), str) or not result['id']:
            raise ValueError('No job ID returned. Submission state is uncertain; do not resubmit.')
        args.job.write_text(json.dumps({'id': result['id'], 'state': 'submitted'}), encoding='utf-8')
        print('Submitted; job ID saved. Retrieve using fetch.')
        return 0
    if args.output.exists():
        raise ValueError('Output already exists; choose a new output path.')
    job = json.loads(args.job.read_text(encoding='utf-8'))
    if not isinstance(job.get('id'), str) or not job['id']:
        raise ValueError('No resumable job ID. Reconcile the uncertain submission with the service.')
    result = request('/document', {'id': job['id']}, credential())
    status = str(result.get('status', '')).lower()
    if status in ('error', 'failed', 'cancelled'):
        raise ValueError('Humanization job failed or was cancelled.')
    output = result.get('output')
    if not isinstance(output, str) or not output.strip() or status in ('pending', 'processing', 'queued'):
        print('Pending; fetch this same job again in 5–10 seconds.')
        return 3
    with args.output.open('x', encoding='utf-8', newline='') as handle:
        handle.write(output)
    print('API output saved.')
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print(str(exc) if isinstance(exc, ValueError) else 'Local file operation failed; check paths and permissions.', file=sys.stderr)
        sys.exit(1)
