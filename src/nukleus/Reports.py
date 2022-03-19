import json
import re


def report_parser(source: str, target):

    p_erc_err_drc = re.compile(r'^\*\* Found (.*) DRC violations \*\*$')
    p_nc_err = re.compile(r'^\*\* Found (.*) unconnected pads \*\*$')
    p_erc_err = re.compile(r'^ERC report \((.*)\)$')
    p_erc_violation = re.compile(r'^\[(.*)\]: (.*)$')

    p_erc_sheet = re.compile(r'^\*\*\*\*\* Sheet (.*)$')
    p_err_type = re.compile(r'^ErrType\((.*)\): (.*)$')
    p_err_entry = re.compile(r'^.*@\((.*) mm, (.*) mm\): (.*)$')

    act_list = []
    act_message = {}
    sheet_name = '/'

    lines = source.splitlines()
    for line in lines:
        if p_erc_err_drc.match(line):
            act_list = []
            target['drc'] = act_list

        elif p_nc_err.match(line):
            act_list = []
            target['unconnected'] = act_list

        elif p_erc_err.match(line):
            act_list = []
            target['erc'] = act_list

        elif p_erc_violation.match(line):
            err = p_erc_violation.match(line)
            if err:
                act_message = {'code': err.group(
                    1), 'sheet': sheet_name, 'message': err.group(2), 'con': []}
                act_list.append(act_message)

        elif p_erc_sheet.match(line):
            err = p_erc_sheet.match(line)
            if err:
                sheet_name = err.group(1)

        elif p_err_type.match(line):
            err = p_err_type.match(line)
            if err:
                act_message = {'code': err.group(
                    1), 'sheet': sheet_name, 'message': err.group(2), 'con': []}
                act_list.append(act_message)

        elif p_err_entry.match(line):
            err = p_err_entry.match(line)
            if err:
                act_message['con'].append(
                    {'x': err.group(1), 'y': err.group(2), 'message': err.group(3)})


def combine_reports(source):
    result = {}
    for s in source:
        with open(s) as f:
            reports = json.load(f)
            for name in reports:
                if name not in result:
                    result[name] = {'summary': {}}
                count_results(s, result[name]['summary'])
                for board in reports[name]:
                    if board not in result[name]:
                        result[name][board] = {}
                    for report in reports[name][board]:
                        result[name][board][report] = reports[name][board][report]
    return result


def count_results(source, results):
    with open(source) as file:
        reports = json.load(file)
        for name in reports:
            for board in reports[name]:
                if board == 'unit_test':
                    test = reports[name][board]['report']['summary']
                    results[board] = {'passed': test['passed'],
                                      'num_tests': test['num_tests']}
                else:
                    for report in reports[name][board]:
                        if report != 'bom':
                            if report not in results:
                                results[report] = len(
                                    reports[name][board][report])
                            else:
                                results[report] += len(reports[name]
                                                       [board][report])
    return results
