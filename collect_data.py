import requests
import datetime
import csv
import os


def AddMonths(d, x):
    newmonth = (((d.month - 1) + x) % 12) + 1
    newyear = int(d.year + (((d.month - 1) + x) / 12))
    return datetime.date(newyear, newmonth, d.day)


headers = {"Authorization": "bearer TOKEN"}


# A simple function to use requests.post to make the API call. Note the json= section.
def run_query(query):
    request = requests.post('https://api.github.com/graphql',
                            json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        print(request.json())
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))


def get_month_last_two_years():
    all_date = []
    for i in range(-1, 23):
        all_date.append([str(AddMonths(datetime.datetime.now(), int(-i-1))),
                        str(AddMonths(datetime.datetime.now(), -i))])
    return all_date


urls = ["https://github.com/golang/go",
        "https://github.com/google/go-github",
        "https://github.com/angular/material",
        "https://github.com/angular/angular-cli",
        "https://github.com/sebholstein/angular-google-maps",
        "https://github.com/d3/d3",
        "https://github.com/facebook/react",
        "https://github.com/tensorflow/tensorflow",
        "https://github.com/keras-team/keras",
        "https://github.com/pallets/flask"]


# stars and forks data
def get_all_forks_star():
    megadata = [["url", "stars", "forks"]]
    for url in urls:
        org, repo = url.split('/')[-2], url.split('/')[-1]
        custom_query = f'owner: "{org}", name: "{repo}"'
        query_static_data = """{
                                repository("""+custom_query+""") {
                                    stargazers {
                                        totalCount
                                    }
                                    forks{
                                        totalCount
                                    }

                                }
                            }"""
        result = run_query(query_static_data)
        data = result['data']['repository']
        megadata.append([url, data['stargazers']['totalCount'],
                        data['forks']['totalCount']])
        print(data)
    os.makedirs('issue_data/', exist_ok=True)

    with open('issue_data/all_url_star_fork.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(megadata[0])
        # write multiple rows
        writer.writerows(megadata[1:])
# stars and forks data


# issue data

def get_all_issues():
    all_date = get_month_last_two_years()
    for url in urls:
        issue_data = [["url", "dateStart",
                       "dateEnd", "open", "closed", "total"]]

        org, repo = url.split('/')[-2], url.split('/')[-1]
        for d in all_date:
            custom_query_open_issues = f'org:{org} repo:{repo} is:open created:{d[0]}..{d[1]}'
            custom_query_closed_issues = f'org:{org} repo:{repo} is:closed created:{d[0]}..{d[1]}'
            query_open = '''{
                    search(query: "'''+custom_query_open_issues + '''", type: ISSUE) {
                        issueCount
                    }
                }'''
            query_closed = '''{
                    search(query: "'''+custom_query_closed_issues + '''", type: ISSUE) {
                        issueCount
                    }
                }'''

            result_open = run_query(query_open)['data']['search']['issueCount']
            result_closed = run_query(query_closed)[
                'data']['search']['issueCount']

            issue_data.append([url, d[0], d[1], result_open,
                               result_closed, result_open+result_closed])
        with open(f'issue_data/{org}-{repo}.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(issue_data[0])
            # write multiple rows
            writer.writerows(issue_data[1:])
        print(url, "done")
# issue data


get_all_forks_star()
get_all_issues()
