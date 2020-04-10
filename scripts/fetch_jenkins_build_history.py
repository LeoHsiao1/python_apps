"""
该脚本用于抓取 Jenkins 的历史构建信息，保存为一个 xlsx 表格。
用法：
pip install jenkinsapi openpyxl
python fetch_jenkins_build_history.py
"""
import jenkinsapi
import openpyxl


def get_build_history(jk) -> list:
    for job_name in jk.keys():
        job = jk.get_job(job_name)
        number = job.get_next_build_number()
        if number == 1:
            continue
        # for n in range(1, number):
        for n in range(1, 2):
            try:
                b = job.get_build(n)
            except jenkinsapi.custom_exceptions.NotFound:
                continue
            info = {
                'job_name': job_name,
                # 'job_url': job.url,
                'number': n,
                'node': b.get_slave() or 'master',
                'timestamp': b.get_timestamp().strftime("%Y/%m/%d-%H:%M:%S"),
                'duration': round(b.get_duration().total_seconds()),
                'status': b.get_status(),
                'cause': b.get_causes()[0].get('shortDescription').replace('Started by ', '')
            }
            yield info


jk = jenkinsapi.jenkins.Jenkins("http://10.0.0.1:8080", username='admin', password='******')
build_history = get_build_history(jk)

wb = openpyxl.Workbook(write_only=True)
ws = wb.create_sheet('构建历史')
ws.append(['任务名', '构建编号', '所在节点', '开始时间', '耗时', '状态', '启动者'])
for i in build_history:
    ws.append([i['job_name'], i['number'], i['node'],
               i['timestamp'], i['duration'], i['status'], i['cause']])
    print('fetched ', i['job_name'], '\t#', i['number'])
wb.save("Jenkins构建历史.xlsx")
wb.close()
