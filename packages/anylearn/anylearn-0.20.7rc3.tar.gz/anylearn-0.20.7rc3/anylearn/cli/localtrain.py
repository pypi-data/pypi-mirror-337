from multiprocessing import Process
import os
from pathlib import Path
from requests import HTTPError
from rich import print
from threading import Thread
import platform
import shlex
import socket
import subprocess
import time

import typer

try:
    from ruamel.yaml import YAML
except ImportError:
    from ruamel_yaml import YAML

from anylearn.applications.utils import generate_random_name
from anylearn.cli._utils import HostOption
from anylearn.sdk.auth import authenticate
from anylearn.sdk.context import init
from anylearn.applications import sync_algorithm
from anylearn.utils.cmd import cmd_error
from anylearn.utils.errors import (
    AnylearnRequiredLocalCommitException,
)
from anylearn.cli import(
    get_local_task_file,
    init_config,
)
from anylearn.sdk import (
    Project as SDKProject,
)
from anylearn.interfaces import (
    Project,
    TrainTask,
)
from anylearn.cli.agent import init_agent


app = typer.Typer()


def _get_or_create_default_project():
    try:
        return Project.get_my_default_project()
    except:
        return Project.create_my_default_project()


@app.command()
def run(host: str = HostOption):
    config_path = os.path.join(os.getcwd(), "config.yaml")
    host_port = host
    project_name = ""
    algorithm_name = ""
    entrypoint = ""
    algorithm_local_dir = ""
    dataset_local_dir = ""
    if os.path.exists(config_path):
        config_path = Path(config_path)
        yaml = YAML()
        config = yaml.load(config_path)
        if config:
            if 'host_port' in config:
                host_port = config['host_port']
            if 'project_name' in config:
                project_name = config['project_name']
            if 'algorithm_name' in config:
                algorithm_name = config['algorithm_name']
            if 'entrypoint' in config:
                entrypoint = config['entrypoint']
            if 'algorithm_local_dir' in config:
                algorithm_local_dir = config['algorithm_local_dir']
            if 'dataset_local_dir' in config:
                dataset_local_dir = config['dataset_local_dir'] or ""
    init(host_port)
    auth = authenticate(host_port)
    if not auth:
        raise typer.Abort()
    init_config(auth)
    submit_project_name = typer.prompt("Project name", default=project_name)
    submit_task_name = typer.prompt("Train task name", default=generate_random_name())
    submit_algorithm_local_dir = typer.prompt("Algorithm local dir", default=algorithm_local_dir)
    submit_algorithm_name = typer.prompt("Algorithm cloud name", default=algorithm_name)
    submit_dataset_local_dir = typer.prompt("Dataset local dir", default=dataset_local_dir)
    submit_entrypoint = typer.prompt("Train entrypoint", default=entrypoint)

    # Project
    print("[blue]正在检查项目信息... [/blue]")
    if submit_project_name:
        try:
            project = SDKProject.from_full_name(submit_project_name)
            project = Project(id=project.id, load_detail=True) # TODO: unify tag in .sdk module then unify project models by SDKProject
        except HTTPError as e:
            status_code = e.response.status_code
            cmd_error(
                f"Error fetching project {submit_project_name}, "
                f"status code {status_code}."
            )
            raise
    else:
        project = _get_or_create_default_project()

    # Algorithm
    print("[blue]正在上传算法... [/blue]")
    try:
        algo, _ = sync_algorithm(
            name=submit_algorithm_name,
            dir_path=submit_algorithm_local_dir,
            force=True,
        )
    except AnylearnRequiredLocalCommitException:
        # Notify possible usage of algorithm_force_update=True
        raise AnylearnRequiredLocalCommitException(
            "Local algorithm code has uncommitted changes. "
            "Please commit your changes or "
            "specify `algorithm_force_update=True` "
            "to let Anylearn make an auto-commit."
    )
    print("[blue]正在创建训练任务... [/blue]")

    os_name = platform.system()
    os_version = platform.version()
    username = os.getlogin()
    device_name = socket.gethostname()

    description = f"""系统版本： {os_name} {os_version}
    用户名： {username}
    设备名称： {device_name}"""
    if submit_dataset_local_dir:
        description += f"\nDataset: {submit_dataset_local_dir}"

    train_task = TrainTask(
        name=submit_task_name,
        description=description,
        creator_id=auth.user_id,
        project_id=project.id,
        algorithm_id=algo.id,
        state=0,
        entrypoint=submit_entrypoint,
        train_params="{}",
        is_local=True,
    )
    train_task.save()
    train_task.get_detail()
    print(train_task)

    # 保存训练任务信息到本地
    TrainTaskInfo = {
        "TaskName": submit_task_name,
        "TaskAlgorithm": submit_algorithm_name,
        "TaskAlgorithmId": algo.id,
        "ProjectId": project.id,
        "CreatorId": auth.user_id,
        "TaskId": train_task.id,
        "Entrypoint": submit_entrypoint,
        "TrainParams": "{}",
    }
    local_task_file = get_local_task_file()
    with open(local_task_file.TASK_INFO_FILE, 'w') as f:
        yaml.dump(TrainTaskInfo, f)
    print("[blue]训练任务创建完成且已就绪 [/blue]")

    print("[blue]正在启动训练任务... [/blue]")
    train_task.update_state(state=1)
    #  TODO: 启动训练任务
    p_train = Process(target=local_train(train_task))
    p_train.start()
    p_train.join()


def local_train(train_task: TrainTask):
    # 采用管道方式通信，该进程中定期从管道读取并写入文件（缺点是可能会有频繁的开关文件操作，比较耗时）
    if not train_task.entrypoint:
        raise Exception("Entrypoint is None")
    cmd = shlex.split(train_task.entrypoint)
    p_train = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    local_task_file = get_local_task_file()
    p_stdout = Thread(target=print_stdout_stderr, args=(p_train, local_task_file.TASK_STDOUT_LOG, 'stdout'))
    p_err = Thread(target=print_stdout_stderr, args=(p_train, local_task_file.TASK_STDERR_LOG, 'stderr'))
    p_stdout.start()
    p_err.start()
    init_agent(train_task, p_train)
    state_code = p_train.wait()
    if state_code == 0:
        train_task.update_state(state=2)
        tip = "Task finished with code 0"
        print(tip)
        train_task.upload_logs(tip)
    else:
        train_task.update_state(state=-2)
        tip = f"Task failed with code {str(state_code)}"
        print(tip)
        train_task.upload_logs(tip)
    p_stdout.join()
    p_err.join()
    print("任务结束！")


def print_stdout_stderr(p_train: subprocess.Popen, file_path: str, flag: str):
    while p_train.poll() is None:
        # 逐行读取子进程的标准输出
        if flag == 'stdout':
            line = p_train.stdout.readline()
        elif flag == 'stderr':
            line = p_train.stderr.readline()
        std_log = line.decode('utf-8')
        print(f"{flag}:", std_log, end='')
        with open(file_path, 'a') as f_output:
            f_output.write(std_log)
        time.sleep(3)
