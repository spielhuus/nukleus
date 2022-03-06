import re

def report_parser(source, target):

    p_erc_err_drc = re.compile('^\*\* Found (.*) DRC violations \*\*$')
    p_nc_err = re.compile('^\*\* Found (.*) unconnected pads \*\*$')
    p_erc_err = re.compile('^ERC report \((.*)\)$')
    p_erc_violation = re.compile('^\[(.*)\]: (.*)$')

    p_erc_sheet = re.compile('^\*\*\*\*\* Sheet (.*)$')
    p_err_type = re.compile('^ErrType\((.*)\): (.*)$')
    p_err_entry = re.compile('^.*@\((.*) mm, (.*) mm\): (.*)$')

    act_list = []
    act_message = {}
    sheet_name = '/'

    lines = source.readlines()
    for line in lines:

        if( p_erc_err_drc.match(line) ):
            act_list = []
            target['drc'] = act_list

        elif( p_nc_err.match(line) ):
            act_list = []
            target['unconnected'] = act_list

        elif( p_erc_err.match(line) ):
            act_list = []
            target['erc'] = act_list

        elif( p_erc_violation.match(line) ):
            err = p_erc_violation.match(line)
            act_message = {'code':err.group(1), 'sheet': sheet_name, 'message':err.group(2), 'con':[]}
            act_list.append(act_message)

        elif( p_erc_sheet.match(line) ):
            err = p_erc_sheet.match(line)
            sheet_name = err.group(1)

        elif( p_err_type.match(line) ):
            err = p_err_type.match(line)
            act_message = {'code':err.group(1), 'sheet': sheet_name, 'message':err.group(2), 'con':[]}
            act_list.append(act_message)

        elif( p_err_entry.match(line) ):
            err = p_err_entry.match(line)
            act_message['con'].append( {'x':err.group(1), 'y':err.group(2), 'message':err.group(3)})
