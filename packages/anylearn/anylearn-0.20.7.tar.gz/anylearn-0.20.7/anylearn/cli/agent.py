import time
import os
from threading import Thread

from rich import print

from anylearn.cli import LocalTaskFile, get_local_task_file
from anylearn.interfaces import TrainTask

l_error_cache = 0
c_error_cache = 0
l_output_cache = 0
c_output_cache = 0
l_resourceCache = 0
c_resourceCache = 0


def update_stdout(
    train_task: TrainTask,
    local_task_file: LocalTaskFile,
    subprocess_train,
):
    output_log_path = local_task_file.TASK_STDOUT_LOG
    agent_cache_path = local_task_file.TASK_AGENT_CACHE_FILE
    while subprocess_train.poll() is None:
        if not os.path.exists(output_log_path):
            # train_output.log文件不存在！继续循环
            time.sleep(1)
            continue

        # 获取本地agent缓存
        try:
            with open(agent_cache_path, 'r') as f:
                l_resource_cache = int(f.readline())
                l_output_cache = int(f.readline())
        except (FileNotFoundError, ValueError) as e:
            print(f"[red]读取 agent 缓存失败-stdout: {e}[/red]")
            time.sleep(1)
            continue

        # TODO 获取云端agent缓存
        c_output_cache = l_output_cache
        try:
            # 获取云端缓存中
            res = train_task.get_local_task_catch()
            if res:
                if res['output_cache_pointer']:
                    c_output_cache = res['output_cache_pointer']
        except Exception as e:
            print('[red]云端缓存获取失败: [/red]', e)

        # 获取文件大小
        p_output_cache = os.path.getsize(output_log_path)

        # 检查文件指针错误并确定读取范围
        if p_output_cache < l_output_cache:
            print("[red]agent output read: 文件指针错误！[/red]")
            time.sleep(1)
            continue
        elif p_output_cache == l_output_cache:
            if l_output_cache < c_output_cache:
                print("[red]agent output read: 文件指针错误！[/red]")
                time.sleep(1)
                continue
            elif l_output_cache == c_output_cache:
                # 文件无更新
                time.sleep(1)
                continue
            else:
                p_start = c_output_cache
                p_end = l_output_cache
        else:
            if l_output_cache < c_output_cache:
                print("[red]agent output read: 文件指针错误！[/red]")
                time.sleep(1)
                continue
            elif l_output_cache == c_output_cache:
                p_start = l_output_cache
                p_end = p_output_cache
            else:
                p_start = c_output_cache
                p_end = p_output_cache

        # 读取并处理新日志内容
        try:
            with open(output_log_path, 'r') as f:
                f.seek(p_start)
                outputInfo = f.read(p_end - p_start)
                l_output_cache = f.tell()
                if outputInfo:
                    try:
                        # 日志上传中
                        res = train_task.upload_logs(outputInfo)
                        if res:
                            # 日志上传成功 更新云端缓存中
                            res = train_task.upload_local_task_catch('output_cache_pointer', l_output_cache)
                    except Exception as e:
                        print('[red]Log upload failed: [/red]', e)
        except IOError as e:
            print(f'[red]读取输出日志失败: {e}[/red]')
            time.sleep(1)
            continue
        # 更新本地缓存
        try:
            with open(agent_cache_path, 'r+') as f:
                l_resource_cache = int(f.readline())
                f.readline()
                l_error_cache = int(f.readline())
                f.seek(0)
                f.write(f"{str(l_resource_cache)}\n{str(l_output_cache)}\n{str(l_error_cache)}")
        except IOError as e:
            print(f'[red]本地缓存更新失败: {e}[/red]')
            continue
        time.sleep(2)


def update_err(
    train_task: TrainTask,
    local_task_file: LocalTaskFile,
    subprocess_train,
):
    error_path = local_task_file.TASK_STDERR_LOG
    agent_cache_path = local_task_file.TASK_AGENT_CACHE_FILE
    while subprocess_train.poll() is None:
        if not os.path.exists(error_path):
            # train_err.log文件不存在！继续循环
            time.sleep(1)
            continue

        # 获取本地agent缓存
        try:
            with open(agent_cache_path, 'r') as f:
                l_resource_cache = int(f.readline())
                l_output_cache = int(f.readline())
                l_error_cache = int(f.readline())
        except (FileNotFoundError, ValueError) as e:
            print(f"[red]读取 agent 缓存失败-err: {e}[/red]")
            time.sleep(1)
            continue

        # TODO 获取云端agent缓存
        c_error_cache = l_error_cache
        try:
            # 获取云端缓存中
            res = train_task.get_local_task_catch()
            if res:
                if res['error_cache_pointer']:
                    c_error_cache = res['error_cache_pointer']
        except Exception as e:
            print('[red]云端缓存获取失败: [/red]', e)

        # 获取文件末尾指针
        p_error_cache = os.path.getsize(error_path)

        # 检查文件指针错误并确定读取范围
        if p_error_cache < l_error_cache:
            print("[red]agent output read: 文件指针错误！[/red]")
            time.sleep(1)
            continue
        elif p_error_cache == l_error_cache:
            if l_error_cache < c_error_cache:
                print("[red]agent output read: [文件指针错误！[/red]")
                time.sleep(1)
                continue
            elif l_error_cache == c_error_cache:
                # 文件无更新
                time.sleep(1)
                continue
            else:
                p_start = c_error_cache
                p_end = l_error_cache
        else:  
            if l_error_cache < c_error_cache:
                print("[red]agent output read: 文件指针错误！[/red]")
                time.sleep(1)
                continue
            elif l_error_cache == c_error_cache:
                p_start = l_error_cache
                p_end = p_error_cache
            else:
                p_start = c_error_cache
                p_end = p_error_cache
        # 读取并处理新日志内容
        try:
            with open(error_path, 'r') as f:
                f.seek(p_start)
                err_info = f.read(p_end - p_start)
                l_error_cache = f.tell()
                if err_info:
                    print("[green]agent read[/green] err_info: ", err_info)
                    try:
                        # 日志上传中
                        res = train_task.upload_logs(err_info)
                        if res:
                            # 日志上传成功 更新云端缓存中
                            res = train_task.upload_local_task_catch('error_cache_pointer', l_error_cache)
                    except Exception as e:
                        print('[red]Log upload failed: [/red]', e)
        except IOError as e:
            print(f'[red]读取输出日志失败: {e}[/red]')
            time.sleep(1)
            continue
        # 更新本地缓存
        try:
            with open(agent_cache_path, 'r+') as f:
                l_resource_cache = int(f.readline())
                l_output_cache = int(f.readline())
                f.seek(0)
                f.write(f"{str(l_resource_cache)}\n{str(l_output_cache)}\n{str(l_error_cache)}")
        except IOError as e:
            print(f'[red]本地缓存更新失败: {e}[/red]')
            continue
        time.sleep(2)


def init_agent(train_task: TrainTask, subprocess_train):
    print("[blue]正在初始化日志同步...[/blue]")
    local_task_file = get_local_task_file()
    p_stdout = Thread(target=update_stdout, args=(train_task, local_task_file, subprocess_train))
    p_err = Thread(target=update_err, args=(train_task, local_task_file, subprocess_train))
    p_stdout.start()
    p_err.start()
    # #TODO 心跳机制
    while subprocess_train.poll() is None:
        try:
            train_task.heartbeat()
        except Exception as e:
            print('===[red]HeartBeat failed: [/red]', e)
        time.sleep(3)
    p_stdout.join()
    p_err.join()
    return
