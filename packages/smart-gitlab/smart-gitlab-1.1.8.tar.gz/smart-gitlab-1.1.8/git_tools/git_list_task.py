# !/usr/bin/env python3
import curses
import datetime
import math
import os
import re
import sys
import time
from collections import namedtuple
from git_tools import gitlab_apis, sorted_key_utils
from git_tools.git_env import Env
from git_tools.sqlite_util import sqliteTool
from git_tools.table_column import TableColumns
from git_tools.toggle_util import Toggle
from textwrap import fill


def custom_sort(sorted_order, val):
    if sorted_order:
        if not sorted_order.__contains__(val):
            return 999
        return sorted_order.index(val)
    return 0


def get_tables_string(jobs, sorted_key):
    sort_order = sorted_key_utils.get_by_key(sorted_key)
    jobs = sorted(jobs, key=lambda x: custom_sort(sort_order, x.project_name))

    from prettytable import PrettyTable

    # 創建一個表格
    table = PrettyTable()
    table.field_names = [TableColumns.TagNo.value, TableColumns.TagId.value, TableColumns.Project.value,
                         TableColumns.Branch.value, TableColumns.SHA.value, TableColumns.Stage.value,
                         TableColumns.StageName.value,
                         TableColumns.Status.value, TableColumns.PipelineUrl.value, TableColumns.CreateTime.value]
    projects = list()

    toggle = Toggle()
    idx = 0
    for job in jobs:
        job.tag_id, allaw_none = toggle.toggle_by_tag(f'{job.tag_id}({job.pipeline_id})', job.tag_id)
        idx = idx if allaw_none else idx + 1
        if not allaw_none:
            projects.append(job.project_name)

        sha = job.hexsha if job.hexsha else "unknown"
        table.add_row([idx, job.tag_id, job.project_name, job.branch, fill(sha[:8],width=8), job.stage, job.name,
                       job.status, job.web_url,
                       datetime.datetime.fromtimestamp(job.create_time)])
    from collections import Counter
    counter = Counter(projects)
    duplicate = set([item for item, count in counter.items() if count > 1])
    return duplicate, table


Position = namedtuple("position", ["y", "x"])
warn_position = Position(0, 0)  # duplicate project & refresh time
info_position = Position(1, 0)  # usage
keyword_position = Position(2, 22)  # f:keyword
exclude_position = Position(3, 22)  # x: exclude
sort_position = Position(4, 22)  # s: sorted by
delete_position = Position(5, 22)  # d: delete by tag
export_position = Position(6, 22)  # o: export as html
log_position = Position(7, 0)  # log
text_position = Position(8, 0)  # text


def update_job_info(job_list):
    if len(job_list) == 0:
        return
    pipelines = set()
    for job in job_list:
        if job.pipeline_id not in pipelines:  # update once per pipeline
            # job.web_url
            from urllib.parse import urlparse
            jobs = gitlab_apis.query_jobs(domain=urlparse(job.web_url).hostname, project_id=job.project_id,
                                          pipeline_id=job.pipeline_id)
            pipelines.add(job.pipeline_id)
            for j in jobs:
                sqliteTool.update_job(job_id=j.job_id, status=j.status)


def get_color(value, green_pair, red_pair, white_pair):
    if value == 'success':
        return green_pair
    if value == 'failed':
        return red_pair
    return white_pair


def main(stdscr, job_name):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    green_pair = curses.color_pair(1)
    red_pair = curses.color_pair(3)
    white_pair = curses.color_pair(4)
    # content所在行
    page_num = 0
    table_header_len = 3  # 表头高度

    # 存储原始和过滤后的内容
    keyword = ""
    exclude = ""
    sorted_key = ""

    def print_title(duplicate):
        # info
        stdscr.addstr(info_position.y, info_position.x, "c: clear all conditions, ↑: page up, ↓: page down, q: quit, "
                                                        "other: refresh",
                      green_pair)
        # warn
        if duplicate and len(duplicate) > 0:
            stdscr.addstr(warn_position.y, warn_position.x, f"Duplicate project[{len(duplicate)}]: ", red_pair)
            for d in duplicate:
                stdscr.addstr(str(d) + " ", red_pair)

        stdscr.addstr(keyword_position.y, 0, "f: filter  keyword:", green_pair)
        stdscr.addstr(keyword_position.y, keyword_position.x, keyword, green_pair)

        stdscr.addstr(exclude_position.y, 0, "x: exclude keyword:", green_pair)
        stdscr.addstr(exclude_position.y, exclude_position.x, exclude, green_pair)

        stdscr.addstr(sort_position.y, 0, "s: sorted by:", green_pair)
        stdscr.addstr(sort_position.y, sort_position.x, sorted_key, green_pair)

        stdscr.addstr(delete_position.y, 0, "d: delete by tagid:", green_pair)

        stdscr.addstr(export_position.y, 0, "o: export to html:", green_pair)

    def print_row(screen_row, txt):
        pattern = r"(?P<left>.*?)(?P<value>(failed)|(success)|(running)|(skipped))(?P<right>.*)"
        # 换行了不处理
        txt = txt[0:min(max_x - 1, len(txt))]
        matches = re.search(pattern, txt)
        if matches:
            left = matches.group('left')
            value = matches.group('value')
            stdscr.addstr(screen_row, text_position.x, left)
            stdscr.addstr(value, get_color(value, green_pair, red_pair, white_pair))
            stdscr.addstr(matches.group('right'))
        else:
            stdscr.addstr(screen_row, text_position.x, txt)

    def print_content(table):
        text = table.get_string()
        text_arr = text.split("\n")
        for idx, row in enumerate(range(0, table_header_len)):
            print_row(text_position.y + idx, text_arr[row])

        content_arr = text_arr[table_header_len:]
        for idx, row in enumerate(range(page_num * page_size, (page_num + 1) * page_size)):
            if row > len(content_arr) - 1:
                return
            print_row(text_position.y + idx + table_header_len, content_arr[row])

    def filter_rows(table, keyword, exclude):
        def filter_keywords(table, keyword):
            filtered_size = 0
            if keyword:
                for idx, r in enumerate(table.rows):
                    if not any(keyword in str(item) for item in r):
                        table.del_row(idx - filtered_size)
                        filtered_size += 1

        def filter_exclude(table, exclude):
            filtered_size = 0
            if exclude:
                for idx, row in enumerate(table.rows):
                    if any(exclude in str(item) for item in row):
                        table.del_row(idx - filtered_size)
                        filtered_size += 1

        filter_keywords(table, keyword)
        filter_exclude(table, exclude)
        table.add_autoindex("ID")

    while True:
        # 初始化界面
        stdscr.clear()
        # 1s 刷新一次
        max_y, max_x = stdscr.getmaxyx()
        page_size = max_y - table_header_len - text_position.y
        jobs = sqliteTool.query_by_job_name(job_name)

        stdscr.addstr(warn_position.y, max_x - 80,
                      f'Task: {job_name} Refreshed At: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                      green_pair)

        duplicate, table = get_tables_string(jobs, sorted_key)

        filter_rows(table, keyword, exclude)
        page_total_num = math.ceil(len(table.rows) / page_size)
        stdscr.addstr(log_position.y, log_position.x,
                      f'page number: {page_num + 1}/{page_total_num}, total item: {len(table.rows)}', green_pair)

        # 根据标志位显示内容
        print_title(duplicate)
        print_content(table)

        stdscr.refresh()

        # 等待用户输入命令
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('f'):
            curses.echo()
            keyword = stdscr.getstr(keyword_position.y, keyword_position.x).decode('utf-8')
            curses.noecho()
            page_num = 0
        elif key == ord('x'):
            curses.echo()
            exclude = stdscr.getstr(exclude_position.y, exclude_position.x).decode('utf-8')
            curses.noecho()
            page_num = 0
        elif key == ord('s'):
            stdscr.addstr(sort_position.y, sort_position.x, "@1:lucy", white_pair)
            curses.echo()
            sorted_key = stdscr.getstr(sort_position.y, sort_position.x).decode('utf-8')
            curses.noecho()
            page_num = 0
        elif key == ord('d'):
            curses.echo()
            delete_tag = stdscr.getstr(delete_position.y, delete_position.x).decode('utf-8')
            if delete_tag and delete_tag in [j.tag_id for j in jobs]:
                sqliteTool.delete_by_tag(delete_tag)
            curses.noecho()
        elif key == ord('o'):
            stdscr.addstr(export_position.y, export_position.x, "export to html(conditions excluded) ,eg: /tmp/a.html",
                          white_pair)
            curses.echo()
            output_file = stdscr.getstr(export_position.y, export_position.x).decode('utf-8')
            dir_path = os.path.dirname(output_file)
            if not os.path.isdir(dir_path):
                stdscr.addstr(export_position.y, export_position.x, "file dir not exist", white_pair)
            else:
                with open(output_file, "w") as f:
                    table.del_column(TableColumns.CreateTime.value)
                    f.write(table.get_html_string())
                    os.system(f"open {os.path.abspath(f.name)}")
                stdscr.addstr(export_position.y, export_position.x, f"exported success: {output_file}", green_pair)
            curses.noecho()
        elif key == curses.KEY_UP and page_num > 0:
            page_num -= 1
        elif key == curses.KEY_DOWN and page_num < page_total_num - 1:
            page_num += 1
        elif key == ord('c'):  # clear condition
            keyword = ""
            exclude = ""
            page_num = 0


def run(job_name):
    while True:
        try:
            update_job_info(
                job_list=sqliteTool.query_by_job_name(job_name, except_status=['success', 'failed', 'canceled']))
            time.sleep(2)
        except Exception as e:
            print(e)


def task_command():
    import threading

    job_name = Env.get_task_name(sys.argv)
    thread = threading.Thread(target=run, args=[job_name])
    thread.start()
    curses.wrapper(main, job_name=job_name)
    thread.join()


if __name__ == "__main__":
    update_job_info(
        job_list=sqliteTool.query_by_job_name('Everyday-20241216', except_status=['success', 'failed', 'canceled']))

    # task_command()
