import requests
import datetime
import csv
import os

# function to add month to pass date date


def AddMonths(d, x):
    newmonth = (((d.month - 1) + x) % 12) + 1
    newyear = int(d.year + (((d.month - 1) + x) / 12))
    return datetime.date(newyear, newmonth, d.day)


headers = {"Authorization": "bearer TOKEN"}


# A simple function to use requests.post to make the API call. Note the json= section.
def run_query(query):
    # creating a request to graphql service and Authorization using the headers parameter
    request = requests.post('https://api.github.com/graphql',
                            json={'query': query}, headers=headers)
    # is status code is 200 will return the json data else will throw exception
    if request.status_code == 200:
        return request.json()
    else:
        print(request.json())
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))

# function to get last two years dates with an even difference of month from current date


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
    megadata = [["url", "stars", "forks"]]  # header for data
    # iterating over all urls
    for url in urls:
        # getting all org and repo name from urls
        org, repo = url.split('/')[-2], url.split('/')[-1]
        #  creating a graphql query to fetch star and fork data for every repo in a structure manner
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
    # creating file if not present
    os.makedirs('issue_data/', exist_ok=True)
    # writing data in csv file to store the response data
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
            #  creating a custom graphql query to fetch open and close issues count b/w each months
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
            # appending the fetch data in a list
            issue_data.append([url, d[0], d[1], result_open,
                               result_closed, result_open+result_closed])
        # creating file if not present
        os.makedirs('issue_data/', exist_ok=True)
        # creating dynamic files and appending data in respective files
        with open(f'issue_data/{org}-{repo}.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(issue_data[0])
            # write multiple rows
            writer.writerows(issue_data[1:])
        print(url, "done")
# issue data


# we can create a cron service to fetch data and retrive fresh data every day
get_all_forks_star()
get_all_issues()
