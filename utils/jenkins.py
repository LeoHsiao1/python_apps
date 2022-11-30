"""
- 用于管理 Jenkins 服务器
- 需要安装 pip install jenkinsapi
"""
import os
import re

from jenkinsapi.jenkins import Jenkins
import time


def build_jenkins_job(jk, job_name, params=None):
    """ Build a Jenkins Job, return the build object. """
    job = jk.get_job(job_name)
    last_number = job.get_last_build().get_number()
    jk.build_job(job_name, params)
    time_out = 10
    while 1:
        try:
            b = job.get_build(last_number + 1)
            return b
        except:
            if time_out:
                time.sleep(1)
                time_out -= 1
            else:
                raise

config_suffix = '.xml'

def export_job(job_pattern='.*', work_dir='.'):
    """ 导出 Jenkins 的 Job ，保存为 work_dir 目录下 XML 格式的配置文件 """
    for job_name in jk.keys():
        if not re.findall(job_pattern, job_name):
            continue
        config = jk.get_job(job_name).get_config()
        config_file = os.path.normpath(os.path.join(work_dir, job_name + config_suffix))
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config)
            print('已导出Job：', job_name)

def import_job(job_pattern='.*', work_dir='.'):
    """ 读取 work_dir 目录下的 Job 配置文件，导入 Jenkins
    - 为了允许 Job 配置文件包含非 ASCII 码字符，需要修改 jenkinsapi 源代码 job.py 中 update_config() 的定义代码，注释 config = str(config) 一行
    """
    for line in os.walk(work_dir, onerror=print):
        sub_dir,dir_list,file_list = line
        for file in file_list:
            if file[-len(config_suffix):] != config_suffix:
                continue
            # Jenkins 上创建的 Job ，可以位于 Folder 文件夹之下。因此这里的 job_name 是指 Job 的全名，等于 job_folder 加上 job_short_name
            # 从 sub_dir 的前缀中去掉 work_dir ，剩下的路径就是 job_folder
            job_folder = os.path.normpath(sub_dir).removeprefix(os.path.normpath(work_dir)).replace('\\', '/').removeprefix('/')
            job_short_name = file.removesuffix(config_suffix)
            job_name = job_folder + '/' + job_short_name
            # 读取 job 的配置文件
            if not re.findall(job_pattern, job_name):
                continue
            config_file = os.path.join(sub_dir, file)
            with open(config_file, 'r', encoding='utf-8') as f:
                config = f.read()
            # 导入 job 配置
            if jk.has_job(job_name):
                jk.get_job(job_name).update_config(config.encode('utf-8'))
            else:
                print('Jenkins不存在该Job，正在自动创建：', job_name)
                # 这里可以调用 jk.create_job(job_name, config.encode('utf-8')) 来创建 Job ，但是不支持创建在 folder 中的 Job ，因此调用更底层的 jk.requester
                jk.requester.post_xml_and_confirm_status(
                    '{}/job/{}/createItem'.format(jk.baseurl, job_folder),
                    data=config.encode('utf-8'),
                    params={'name': job_short_name}
                )
            print('已导入Job：', job_name)


if __name__ == '__main__':
    jk = Jenkins(baseurl='http://jenkins.test.com', username='***', password='***', timeout=10, useCrumb=True)

    # 测试构建 Job
    b = build_jenkins_job(jk, 'job1')
    while b.is_running():
        time.sleep(1)
    b = jk.get_job('job1').get_build(b.get_number())   # 重新获取 build 对象，否则 get_status() 不会刷新
    print(b.get_status())

    # 测试导出、导入
    export_job('DEV/.*', '.')
    import_job('DEV/.*', '.')
