import os

from anylearn.config import AnylearnConfig
from anylearn.sdk import Auth

class LocalTaskFile:
    def __init__(
        self,
        os_info_file: str,
        project_info_file: str,
        task_info_file: str,
        task_stdout_log: str,
        task_stderr_log: str,
        task_agent_cache_file: str,
    ):
        self.OS_INFO_FILE = os_info_file
        self.PROJECT_INFO_FILE = project_info_file
        self.TASK_INFO_FILE = task_info_file
        self.TASK_STDOUT_LOG = task_stdout_log
        self.TASK_STDERR_LOG = task_stderr_log
        self.TASK_AGENT_CACHE_FILE = task_agent_cache_file

def get_local_task_file() -> LocalTaskFile:
    local_cache_path = os.path.join(os.getcwd(), "AnyctlLocalCache")
    if not os.path.exists(local_cache_path):
        os.makedirs(local_cache_path)
    os_info_file = os.path.join(local_cache_path, "OSinfo.yaml")
    project_info_file = os.path.join(local_cache_path, "Project.yaml")
    task_info_file = os.path.join(local_cache_path, "Task.yaml")
    task_stdout_log = os.path.join(local_cache_path, "train_output.log")
    task_stderr_log = os.path.join(local_cache_path, "train_err.log")
    task_agent_cache_file = os.path.join(local_cache_path, "agentCache.log")
    if not os.path.exists(task_agent_cache_file):
        with open(task_agent_cache_file, 'w') as f:
            f.write("0\n0\n0\n")
    return LocalTaskFile(
        os_info_file,
        project_info_file,
        task_info_file,
        task_stdout_log,
        task_stderr_log,
        task_agent_cache_file,
    )

def init_config(auth: Auth):
    AnylearnConfig.cluster_address = auth.host
    AnylearnConfig.username = auth.username
    AnylearnConfig.token = auth.access_token
    AnylearnConfig.user_id = auth.user_id

def init_sdk(auth: Auth):
    AnylearnConfig.init(
        cluster_address=auth.host,
        username=auth.username,
        password=auth.password,
        token=auth.access_token,
    )
