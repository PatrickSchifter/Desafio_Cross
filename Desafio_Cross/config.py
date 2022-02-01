import requests
import time

list_temp = []
list_num = []
list_ignore = ['}', ']', '{"numbers":[', 'e-']
error = '{"error":"Simulated internal error"}'
page = 1
emp_return = '{"numbers":[]}'


def request(page):
    page = str(page)
    url = f'http://challenge.dienekes.com.br/api/numbers?page={page}'
    request = requests.get(url=url)
    return request.text


while True:
    info = request(page)
    if info == emp_return:
        break
    elif info == error:
        time.sleep(1)
        info = request(page)
        if info == emp_return:
            break
    else:
        # Clean
        info = info.split(',')
        for item in info:
            for to_ignore in list_ignore:
                item = item.replace(to_ignore, '')
            item = float(item)
            if page == 1:
                list_temp.append(item)
            else:
                # Organization in block
                step_ind = int(len(list_num) / 100)
                for ind in range(0, len(list_num) + step_ind, step_ind):
                    try:
                        if item < list_num[ind]:
                            if ind == 0:
                                list_num.insert(ind, item)
                            else:
                                for y in range(ind - 1, ind + 1):
                                    if item < list_num[y]:
                                        list_num.insert(y, item)
                                        break
                                    else:
                                        continue
                            break
                    except IndexError:
                        if item < list_num[-1]:
                            for y in range(len(list_num) - step_ind, len(list_num)):
                                try:
                                    if item < list_num[y]:
                                        list_num.insert(y, item)
                                        break
                                    else:
                                        continue
                                except IndexError:
                                    print(IndexError)
                                    continue
                            break
                        else:
                            list_num.append(item)
        if page == 1:
            # Organize the base
            for x in range(len(list_temp)):
                for y in range(len(list_temp)):
                    try:
                        if list_temp[y] < list_temp[y + 1]:
                            continue
                        else:
                            temp = list_temp[y]
                            list_temp[y] = list_temp[y + 1]
                            list_temp[y + 1] = temp
                    except IndexError:
                        continue
            list_num = list_temp
    page += 1
