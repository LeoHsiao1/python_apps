"""
Used to communicate with the Jenkins server.
Installation required: pip install jenkinsapi
"""
from jenkinsapi.jenkins import Jenkins
import time


def build_jenkins_job(jk, jobname, params=None):
    """ Build a Jenkins Job, return the build object. """
    job = jk.get_job(jobname)
    last_number = job.get_last_build().get_number()
    jk.build_job(jobname, params)
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


if __name__ == '__main__':
    jk = Jenkins(baseurl='http://jenkins.test.com')
    b = build_jenkins_job(jk, 'job1')

    while b.is_running():
        time.sleep(1)
    b = jk.get_job('job1').get_build(b.get_number())   # 重新获取build对象，否则get_status()不会刷新
    print(b.get_status())
