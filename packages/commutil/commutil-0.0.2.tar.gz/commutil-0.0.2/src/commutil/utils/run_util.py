from typing import Callable, Dict, Optional, List, Union, Any
from functools import partial
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Pool
import subprocess
from .debug_util import dbg


def run_cmd(cmd, verbose=False, shell=True):
    if verbose:
        # dbg(cmd, head="Run $")
        print(f"Run $ {cmd}")
    process = subprocess.Popen(cmd, shell=shell)
    process.wait()


def multi_wrapper(cmd_list, choice="thread", n=2, **kwargs):
    run_cmd_wrapper = partial(run_cmd, **kwargs)

    if choice in ["thread", "t", "th", "T", "threads"]:
        with ThreadPoolExecutor(max_workers=n) as executor:
            futures = [executor.submit(run_cmd_wrapper, cmd) for cmd in cmd_list]
            for future in futures:
                future.result()
    elif choice in ["process", "p", "pro", "P", "processes"]:
        with ProcessPoolExecutor(max_workers=n) as executor:
            futures = [executor.submit(run_cmd_wrapper, cmd) for cmd in cmd_list]
            for future in futures:
                future.result()
    elif choice in ["pool", "po", "poo", "Pool"]:
        with Pool(processes=n) as pool:
            pool.map(run_cmd_wrapper, cmd_list)

    else:
        raise ValueError("Invalid choice")


def run_cmd_list(cmd_list: List[str], logger: Optional[Callable] = None, n: int = 1, **kwargs):
    if n == 1:
        for cmd in cmd_list:
            if logger:
                logger.info(f"Stream $ {cmd}")
            else:
                # dbg(cmd, head="Stream $")
                print(f"Stream $ {cmd}")
            run_cmd(cmd, **kwargs)
    else:
        if logger:
            for cmd in cmd_list:
                logger.info(f"Batch $ {cmd}")
        else:
            for cmd in cmd_list:
                # dbg(cmd, head="Batch $")
                print(f"Batch $ {cmd}")
            # pass
        multi_wrapper(cmd_list=cmd_list, n=n, **kwargs)


class CommandGenerator:
    def __init__(self, script="python run.py", **kwargs):
        self.script = script
        zip_params = {k: list(v) for k, v in kwargs.items() if isinstance(v, zip)}
        normal_params = {k: v for k, v in kwargs.items() if not isinstance(v, zip)}

        self._original_kwargs = {"normal_params": normal_params, "zip_params": zip_params}
        self._filter_conditions = {k: None for params_dict in self._original_kwargs.values() for k in params_dict}
        self.config_list = self._gen_config_list(self._original_kwargs)

    def _handle_normal_params(self, params) -> List[Dict]:
        if not params:
            return [{}]

        lengths = {k: len(v) if isinstance(v, (list, tuple)) else 1 for k, v in params.items()}
        from itertools import product
        indices = product(*[range(lengths[k]) for k in params])

        return [{k: params[k][i] if isinstance(params[k], (list, tuple)) else params[k]
                 for k, i in zip(params, idx)} for idx in indices]

    def _merge_zip_params(self, base_configs: List[Dict], zip_params: Dict) -> List[Dict]:
        zip_len = len(next(iter(zip_params.values())))
        if not base_configs:
            base_configs = [{}]

        return [{**base, **{k: v[i][0] for k, v in zip_params.items()}}
                for base in base_configs
                for i in range(zip_len)]

    def _gen_config_list(self, kwargs) -> List[Dict]:
        normal_params = kwargs["normal_params"]
        zip_params = kwargs["zip_params"]

        config_list = self._handle_normal_params(normal_params)
        if zip_params:
            config_list = self._merge_zip_params(config_list, zip_params)
        return config_list

    def filter(self, **kwargs) -> 'CommandGenerator':
        for key, value in kwargs.items():
            if key not in self._filter_conditions:
                raise KeyError(f"Filter key '{key}' not found")
            self._filter_conditions[key] = (value if callable(value) or value is None
                                            else ([value] if not isinstance(value, (list, tuple))
                                                  else value))
        return self

    def _apply_filters(self, config: Dict[str, Any]) -> bool:
        for key, condition in self._filter_conditions.items():
            if condition is None or key not in config:
                continue
            value = config[key]
            if callable(condition):
                try:
                    if not condition(value):
                        return False
                except Exception as e:
                    raise ValueError(f"Filter function error for '{key}': {e}")
            elif value not in condition:
                return False
        return True

    def _format_cmd(self, config):
        cmd = self.script
        for k, v in config.items():
            if isinstance(v, bool):
                cmd += f" --{k}" if v else ""
            else:
                if isinstance(v, str):
                    cmd += f" --{k} \"{v}\""
                else:
                    cmd += f" --{k} {v}"
        return cmd.strip()

    def add(self, **kwargs) -> 'CommandGenerator':
        for k, v in kwargs.items():
            if isinstance(v, zip):
                self._original_kwargs["zip_params"][k] = list(v)
            else:
                self._original_kwargs["normal_params"][k] = v
            self._filter_conditions.update({k: None for k in kwargs})
        self.config_list = self._gen_config_list(self._original_kwargs)
        return self

    def rm(self, *keys) -> 'CommandGenerator':
        for k in keys:
            if k in self._original_kwargs["normal_params"]:
                self._original_kwargs["normal_params"].pop(k, None)
            elif k in self._original_kwargs["zip_params"]:
                self._original_kwargs["zip_params"].pop(k, None)
            self._filter_conditions.pop(k, None)
        self.config_list = self._gen_config_list(self._original_kwargs)
        return self

    def reset(self) -> 'CommandGenerator':
        self._filter_conditions = {k: None for k in self._original_kwargs}
        return self

    def gen(self) -> List[str]:
        return [self._format_cmd(config)
                for config in self.config_list
                if self._apply_filters(config)]

