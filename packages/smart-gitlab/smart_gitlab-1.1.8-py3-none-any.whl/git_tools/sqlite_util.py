import os
import re
import sqlite3
import time

from git_tools.job_dto import job_dto


class SqliteUtil:
    def __init__(self, db_file):
        self.base_dir = os.path.expanduser('~/.sqlite')
        self.db_file = os.path.join(self.base_dir, db_file)
        self.__init_database__()

    def get_connection(self):
        conn = sqlite3.connect(self.db_file)
        return conn

    def __init_database__(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        if os.path.exists(self.db_file):
            return
        print("Begin init databases...")
        conn = self.get_connection()
        conn.cursor().execute('''CREATE TABLE deploy_task (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         job_id TEXT NOT NULL, 
                         project_id TEXT NOT NULL,
                         project_name TEXT NOT NULL,
                         pipeline_id TEXT NOT NULL,
                         job_name TEXT NOT NULL,
                         branch TEXT NULL,
                         hexsha TEXT NULL,
                         name TEXT NOT NULL,
                         tag_id TEXT NOT NULL,
                         stage TEXT NOT NULL,
                         status TEXT NOT NULL, 
                         web_url TEXT NOT NULL, 
                         create_time int 
                         );
                         ''')
        conn.commit()
        conn.close()
        print("Done init databases.")

    def insert_job(self, job_id, project_id, project_name, pipeline_id, job_name, name, stage, status, refer, web_url,
                   create_time=int(time.time()),branch='Unknown',hexsha="Unknow"):
        web_url = re.sub('http://13.229.25.115','https://codelab001.xyz',web_url)
        sql = f"INSERT INTO deploy_task (job_id,project_id,project_name,pipeline_id,job_name,branch,hexsha,tag_id, name, stage, " \
              f"status, web_url,create_time ) values " \
              f"('{job_id}','{project_id}','{project_name}','{pipeline_id}','{job_name}','{branch}','{hexsha}','{refer}','{name}','{stage}','{status}','{web_url}',{create_time})"
        conn = self.get_connection()
        conn.cursor().execute(sql)

        conn.commit()
        conn.close()

    def delete_by_tag(self, tag_id):
        sql = f"delete from deploy_task where tag_id = '{tag_id}'"
        conn = self.get_connection()
        conn.cursor().execute(sql)
        conn.commit()
        conn.close()

    def query_by_job_name(self, job_name, except_status=[]) -> list:

        status_condition = ''
        if except_status:
            for s in except_status:
                status_condition += f" and status != '{s}'"

        sql = f"select job_id,project_id,project_name,pipeline_id,job_name,branch,hexsha,tag_id, stage, name, status, web_url," \
              f"create_time from deploy_task " \
              f"where job_name = '{job_name}' {status_condition} order by create_time asc, job_id asc"
        conn = self.get_connection()

        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        lists = list()
        for r in results:
            job_id, project_id, project_name, pipeline_id, job_name, branch,hexsha,tag_id, stage, name, status, web_url, create_time = r
            job = job_dto(job_id=job_id,branch=branch,hexsha=hexsha, project_id=project_id, project_name=project_name, pipeline_id=pipeline_id,
                          job_name=job_name, tag_id=tag_id, name=name, stage=stage, status=status, web_url=web_url,
                          create_time=create_time)
            if 'rollback' in job.name:
                continue
            if 'crypto-engine-' in job.name:
                continue
            if 'crypto-service-' in job.name:
                continue
            # if 'engine-' in job.name and job.project_name == 'tkl-search-service':
            #     continue
            lists.append(job)
        return lists

    def update_job(self, job_id, status):
        sql = f"update deploy_task " \
              f"set status = '{status}' where job_id = '{job_id}'"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()


# singleton
sqliteTool = SqliteUtil('git_deploy.db')

if __name__ == '__main__':
    web_url = 'http://13.229.25.115/lucky/libs/tkl-pom/-/pipelines/1902'
    web = re.sub('http://13.229.25.115', 'https://codelab001.xyz', web_url)
    print(web)
