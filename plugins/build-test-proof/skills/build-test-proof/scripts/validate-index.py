#!/usr/bin/env python3
"""Validate evidence references and declared coverage; never run tests or infer passes."""
import argparse
import json
from pathlib import Path
import sys

STATUSES = {'passed', 'failed', 'blocked', 'not_checked'}
def validate(index_path):
    data = json.loads(index_path.read_text(encoding='utf-8'))
    root = index_path.parent.resolve()
    errors = []
    def require(condition, message):
        if not condition: errors.append(message)
    def nonempty(value): return isinstance(value, str) and bool(value.strip())
    def contained(relative, label, directory=False):
        if not nonempty(relative) or Path(relative).is_absolute():
            errors.append(f'{label}: expected a relative path'); return None
        resolved = (root / relative).resolve()
        if not resolved.is_relative_to(root):
            errors.append(f'{label}: path escapes index directory'); return None
        if not (resolved.is_dir() if directory else resolved.is_file()):
            errors.append(f'{label}: referenced path does not exist'); return None
        if not directory and resolved.stat().st_size == 0:
            errors.append(f'{label}: artifact is empty'); return None
        return resolved
    require(isinstance(data, dict), 'Index must be a JSON object')
    if not isinstance(data, dict): return errors
    require(data.get('schema_version') == 1, 'schema_version must be 1')
    for key in ['task', 'run_id', 'source_revision', 'checked_at']:
        require(nonempty(data.get(key)), f'{key}: required observed value')
    activation = data.get('skill_activation', {})
    require(isinstance(activation, dict), 'skill_activation must be an object')
    if isinstance(activation, dict):
        require(activation.get('mode') in {'catalog_explicit','catalog_implicit','manual_file','unavailable'}, 'skill_activation.mode invalid')
        require(nonempty(activation.get('evidence')), 'skill_activation.evidence required')
    env = data.get('environment', {})
    require(isinstance(env, dict), 'environment must be an object')
    if isinstance(env, dict):
        for key in ['url', 'browser', 'viewport']:
            require(nonempty(env.get(key)), f'environment.{key} required')
    selected = contained(data.get('selected_run'), 'selected_run', directory=True)
    require(selected is None or selected != root, 'selected_run must select a distinct run directory, not the whole task root')
    def artifact(value, label):
        resolved = contained(value, label)
        if resolved and selected and not resolved.is_relative_to(selected):
            errors.append(f'{label}: artifact belongs outside selected_run')
        return resolved
    scenarios = data.get('scenarios')
    require(isinstance(scenarios,list) and bool(scenarios), 'scenarios must be a nonempty list')
    seen=set()
    for i, scenario in enumerate(scenarios if isinstance(scenarios,list) else []):
        label=f'scenarios[{i}]'
        if not isinstance(scenario,dict): errors.append(f'{label}: must be an object'); continue
        sid=scenario.get('id')
        require(nonempty(sid) and sid not in seen, f'{label}.id required and unique')
        if isinstance(sid,str): seen.add(sid)
        status=scenario.get('status')
        require(status in STATUSES, f'{label}.status invalid')
        for key in ['title','actions','expected','observed']:
            require(nonempty(scenario.get(key)), f'{label}.{key} required')
        for key in ['visual_change','long_flow']:
            require(isinstance(scenario.get(key),bool), f'{label}.{key} must be boolean')
        shots=scenario.get('screenshots',[])
        require(isinstance(shots,list), f'{label}.screenshots must be a list')
        if scenario.get('visual_change') and status=='passed':
            require(isinstance(shots,list) and bool(shots),f'{label}: passed visual change needs fresh screenshots')
        for j,shot in enumerate(shots if isinstance(shots,list) else []):
            if not isinstance(shot,dict): errors.append(f'{label}.screenshots[{j}]: must be object'); continue
            artifact(shot.get('path'),f'{label}.screenshots[{j}].path')
            require(shot.get('reviewed') is True,f'{label}.screenshots[{j}]: must be visually reviewed')
        video=scenario.get('video')
        if scenario.get('long_flow') and status=='passed':
            require(isinstance(video,dict),f'{label}: passed long flow needs actual video or use blocked/failed for that coverage')
        if video is not None:
            if not isinstance(video,dict): errors.append(f'{label}.video: must be object')
            else:
                artifact(video.get('path'),f'{label}.video.path')
                require(video.get('actual_flow') is True,f'{label}.video: a trace/montage is not actual-flow video')
                require(video.get('decoded') is True and video.get('reviewed') is True,f'{label}.video: decode and visual review declarations required')
                require(nonempty(video.get('coverage')),f'{label}.video.coverage required')
        if status in {'blocked','not_checked'}:
            require(nonempty(scenario.get('limitation')),f'{label}.limitation required')
        require(isinstance(scenario.get('server_result_required',False),bool),f'{label}.server_result_required must be boolean')
        result=scenario.get('server_result')
        if scenario.get('server_result_required') is True:
            require(isinstance(result,dict),f'{label}.server_result required')
            if isinstance(result,dict):
                require(result.get('status') in STATUSES,f'{label}.server_result.status invalid')
                require(nonempty(result.get('observed')),f'{label}.server_result.observed required')
                if status=='passed': require(result.get('status')=='passed',f'{label}: UI pass cannot override server-result failure')
                if result.get('status')=='passed':
                    output=result.get('artifacts',[])
                    require(isinstance(output,list) and bool(output),f'{label}: passed server result needs artifact/readback receipt')
                    for j,value in enumerate(output if isinstance(output,list) else []): artifact(value,f'{label}.server_result.artifacts[{j}]')
    require(isinstance(data.get('unchecked'),list),'unchecked must be a list (empty if none)')
    return errors

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('index',type=Path)
    args=parser.parse_args()
    try: errors=validate(args.index.resolve())
    except (OSError,ValueError,TypeError) as error: errors=[str(error)]
    print(json.dumps({'status':'invalid' if errors else 'valid','errors':errors,'scope':'Structural evidence checks only; declarations are not proof that tests passed.'},ensure_ascii=False,indent=2))
    return 2 if errors else 0
if __name__=='__main__': sys.exit(main())
