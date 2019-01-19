import re, requests, sys


def boj_crawl(name):

    url = f'https://www.acmicpc.net/status?problem_id=&user_id={name}&language_id=-1&result_id=-1'
    resp = requests.get(url)
    if resp.status_code == 200:
        pattern = re.compile(
            r'<td><a href="/problem/(?P<prob_num>\d+)" * title="(?P<year>\d+)년 (?P<month>\d+)월 (?P<day>\d+)일 (?P<hour>\d+)시'
        )

        html = resp.text
        data = pattern.findall(html)
        sub_code = re.compile(r'id = "solution-(?P<submission_code>\d+)"')
        last_sub = int((sub_code).findall(html)[-1])-1
        print(data)


    # #    list of how many problems they solved
    #
    # while (data[-1] < 일주일 전):
    #     url = f'https://www.acmicpc.net/status?user_id={name}&top={last_sub}'
    #     resp = requests.get(url)
    #     if resp.status_code == 200:
    #         pattern = re.compile(
    #             r'title="(?P<year>\d+)년 (?P<month>\d+)월 (?P<day>\d+)일 (?P<hour>\d+)시'
    #         )
    #
    #         html = resp.text
    #         data += pattern.findall(html)
    #
    #         last_sub = re.compile(r'id = "solution-(?P<submission_code>\d+)"').findall(html)[-1]
    #
    #
    # # for date in data :
    # #     if date[0]=='year' & date[1]=='' :
    # #         points[0]+=1
    #
    #
    #
    #
    # print('\n'.join(map(lambda x: str(x), data)))
    # print(len(data))
    #
    #

        # print('\n'.join(map(lambda x: str(x), data)))
        # print(len(data))

if __name__ == '__main__':
    name = sys.argv
    print(name[1])
    boj_crawl(name[1])
