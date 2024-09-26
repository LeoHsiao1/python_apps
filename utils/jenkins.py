"""
- 该脚本用于导出、导入 Jenkins 的 Pipeline 脚本
- 需要安装 pip3 install jenkinsapi==0.3.13
"""

import os
import re

config_suffix = '.xml'  # 导出到本机的配置文件的后缀名

def convert_escape_characters_in_xml(text):
    """ XML 格式的文本中有一些转义字符，需要转换成 utf-8 字符，方便阅读。比如 &gt; 要转换成 > """
    # 转换单引号、双引号
    text = text.replace('&apos;', "'").replace('&quot;', '"')
    # 如果 text 中没有用到 HTML 元素标记，则转换小于号、大于号
    if '&lt;/' not in text:
        text = text.replace('&lt;', "<").replace('&gt;', '>')
    # & 字符总是不支持转换，导入 Jenkins 时会报 XML 格式错误
    # text = text.replace('&amp;', '&')
    return text

def removeprefix(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    else:
        return string[:]

def removesuffix(string, suffix):
    if suffix and string.endswith(suffix):
        return string[:-len(suffix)]
    else:
        return string[:]

def export_job(job_pattern='.*', work_dir='.'):
    """ 导出 Jenkins 的 Job ，保存为 work_dir 目录下 XML 格式的配置文件 """
    for job_name in jk.keys():
        if not re.findall(job_pattern, job_name):
            continue
        # 从 Jenkins 获取 Job 的配置，为 XML 格式的文本
        config = jk.get_job(job_name).get_config()
        config = convert_escape_characters_in_xml(config)
        config_file = os.path.normpath(os.path.join(work_dir, job_name + config_suffix))
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config)
            print('已导出Job：', job_name)

def import_job(job_pattern='.*', work_dir='.'):
    """ 读取 work_dir 目录下的 Job 配置文件，导入 Jenkins
    - 为了允许 Job 配置文件包含非 ASCII 码字符，需要修改 jenkinsapi 源代码 job.py 中 update_config() 的定义代码，将 data=config 改为 data=config.encode('utf-8')
    """
    for line in os.walk(work_dir, onerror=print):
        sub_dir,dir_list,file_list = line
        for file in file_list:
            if file[-len(config_suffix):] != config_suffix:
                continue
            # Jenkins 上创建的 Job ，可以位于 Folder 文件夹之下。因此这里的 job_name 是指 Job 的全名，等于 job_folder 加上 job_short_name
            # 从 sub_dir 的前缀中去掉 work_dir ，剩下的路径就是 job_folder
            _job_folder = removeprefix(os.path.normpath(sub_dir), os.path.normpath(work_dir))
            job_folder  = removeprefix(_job_folder.replace('\\', '/'), '/')
            job_short_name = removesuffix(file, config_suffix)
            job_name = job_folder + '/' + job_short_name
            # 读取 job 的配置文件
            if not re.findall(job_pattern, job_name):
                continue
            config_file = os.path.join(sub_dir, file)
            with open(config_file, 'r', encoding='utf-8') as f:
                config = f.read()
            # 导入 job 配置
            if jk.has_job(job_name):
                jk.get_job(job_name).update_config(config)
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
    from jenkinsapi.jenkins import Jenkins
    jk = Jenkins('https://jenkins.test.com/',
             username=os.environ.get('JENKINS_USERNAME', '???'),
             password=os.environ.get('JENKINS_PASSWORD', '???'),
             timeout=30,
             use_crumb=True)
    jk.requester.max_retries = 3
    jk.requester.timeout = 50

    work_dir    = os.environ.get('WORK_DIR', 'jobs')
    action      = os.environ.get('ACTION', 'export')
    job_pattern = os.environ.get('JOB_PATTERN', '.*')
    if action == 'export':
        export_job(job_pattern, work_dir)
    elif action == 'import':
        import_job(job_pattern, work_dir)


# 示例：
# export_job('.*', work_dir)
