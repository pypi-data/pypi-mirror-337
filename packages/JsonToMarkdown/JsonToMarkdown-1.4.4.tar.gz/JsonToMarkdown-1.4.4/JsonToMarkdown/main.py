#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import copy
from getopt import getopt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
import preprocess
import libsvg
import libmd
import cat as cat
import json_to_obs as jo

__version__ = 'v1.4.4'

class TranslateJson(object):
    def __init__(self, js_file, link_path, dir_type, output_md, output_gitbook, output_xmind, \
            save_dir, enable_hidden, reset_value_bin):
        self.js_file = js_file
        self.json_output_dir = os.path.join(link_path, '_json_output')
        self.save_dir = save_dir
        if save_dir:
            self.dirname = os.path.dirname(self.js_file).strip('./')
            self.link_path = os.path.join(link_path, '_json_output', self.dirname)
        else:
            self.link_path = os.path.join(link_path, '_json_output')
        self.dir_type = dir_type
        self.output_md = output_md
        self.output_gitbook = output_gitbook
        self.output_xmind = output_xmind
        self.enable_hidden = enable_hidden
        self.reset_value_bin = reset_value_bin

        ###################
        self.base_addr = ''
        self.group_addr = ''
        self.bit_num = 32
        self.tmp_path_dict = {}
        self.group_reg_dict = {}
        ###################


        self.gitbookpath = ''
        self.markdownpath = ''
        self.data = ''
        self.pre_leval = 0
        self.history_addrr = 0
        self.history_offset = 0
        self.history_base = -1
        self.history_group = {}
        self.group_set = []
        self.pre_group = ''
        self.all_reg_data = ''
        self.all_reg_tex_data = ''
        self.new_all_reg_list = []
        self.reg_data = '# 寄存器详细说明\n\n'
        self.path_addr_dict = {}
        self.max_len = ''
        self.reg_rst = '寄存器详细说明\n==============\n\n.. toctree::\n'
        self.reg_rst += '   :caption: Contents:\n\n'
        self.xmind_md = '# REG\n## register\n'

    def get_dpath(self, in_dict, pre_path = ''):
        path_list = []
        for k in in_dict:
            l1_path = os.path.join(pre_path, k)
            if isinstance(in_dict[k], list):
                for n,v in enumerate(in_dict[k]):
                    l2_path = os.path.join(l1_path, str(n))
                    if k == "registers":
                        if "Attribute" not in v or v["Attribute"] != "GROUP":
                            path_list.append(l2_path.strip("/"))
                    if k == "group_reg":
                        if "group_reg" not in v:
                            path_list.append(l2_path.strip("/"))
                    path_list.extend(self.get_dpath(v, l2_path))
        return path_list
    
    def get_delem(self, in_dict, dpath, key = ''):
        path = dpath.strip('/').split('/')
        msg = ''
        for i in path:
            if i.isdigit():
                msg += "["  + i + "]"
            else:
                msg += "[\'"  + i + "\']"
        if key != '':
            msg += "[\'"  + key + "\']"
        return eval("in_dict" + msg)
    
    def get_group_path(self, in_path):
        tmp = []
        for n,v in enumerate(in_path.split("/")):
            if v == "group_reg":
                tmp.append(n)
        path = []
        if tmp != []:
            for i in tmp:
                path.append("/".join(in_path.split("/")[:i]))
        return path

    def find_group_path(self, group, root_path):
        group_list = []
        group_list.append(root_path)
        for i in range(len(group['group_reg'])):
            path = root_path + "/group_reg/" + str(i)
            if 'group_reg' in group['group_reg'][i]:
                group_list.extend(self.find_group_path(group['group_reg'][i], path))
        return group_list
    
    def get_group_dict(self, dpath):
        group_dict = {}
        group = self.get_delem(self.js_dict, dpath)
        if 'depth' in group:
            depth = group['depth']
        else:
            depth = 1
        group_dict[dpath] = {"depth":depth, "num":0}
        for i in group['group_reg']:
            group_dict[dpath]['num'] += 1
        return group_dict
    
    def create_groupmsg(self):
        group_msg = {
                'step':'',
                'range':'',
                'group':[],
                }
        return group_msg

    def get_step_msg(self, dpath):
        msg_list = ["N","J","M","k","Z","I","D"]
        reg_list = self.group_reg_dict[dpath]
        name = reg_list[0]['name']
        start_addr = int(reg_list[0]['addr'], 16)
        tmp = name.split('||')
        step_msg = ''
        use_flag = 0
        for i in range(len(tmp)):
            n = tmp[i]
            if n.isdigit() and isinstance(eval(n), int):
                start = int(n)
                for r in reg_list:
                    count = int(r['name'].split('||')[i])
                    if count == start + 1:
                        end_addr = int(r['addr'], 16)
                        step_msg += "+" + msg_list[use_flag] + "*" + hex(end_addr - start_addr)
                        use_flag += 1
                        break
        return step_msg
                    
    
    def get_groupmsg(self, dpath):
        msg_list = ["N","J","M","k","Z","I","D"]
        group_path_list = self.get_group_path(dpath)
        group_path = group_path_list[0]
        group_end = group_path_list[-1]
        group = self.get_delem(self.js_dict, group_path)
        group_list = self.find_group_path(group, group_path)
        for n, path in enumerate(group_list):
            if path == group_end:
                end = n
        group_dict = {}
        for i in group_list:
            group_dict.update(self.get_group_dict(i))
        #print(group_dict)
        step_msg = ''
        scope_msg = ''
        total_msg = ''
        for j in range(len(group_list)):
            elen = len(group_list[j:])
            next_num = 0
            for i in range(elen):
                index = elen - i -1
                path = group_list[j + index]
                if index == 0:
                    if next_num == 0:
                        next_num = group_dict[path]['num']
                    else:
                        next_num = (group_dict[path]['num'] + next_num -1)
                elif i == 0:
                    next_num = group_dict[path]['depth'] * group_dict[path]['num']
                else:
                    next_num = group_dict[path]['depth'] * \
                            (group_dict[path]['num'] + next_num -1)
            step = next_num * (0x0004)
            #step_msg += "+" + msg_list[j] + "*" + hex(step)
            if total_msg == '':
                group_msg = self.create_groupmsg()
                total_msg = group_msg
            else:
                group_msg['group'].append(self.create_groupmsg())
                group_msg = group_msg['group'][0]
            group_msg['step'] = step
            group_msg['range'] = group_dict[path]['depth']
            scope_msg += " " + msg_list[j] + "的范围为0~" + str(group_dict[path]['depth']-1)
            if j == end:
                break
        step_msg = self.get_step_msg(dpath)
        return step_msg, scope_msg, total_msg

    def get_reserve_fields(self, fields, bit_num):
        bit_num = int(bit_num)
        re_map = [[0, bit_num -1]]
        re_fields = []
        hidden_map = []
        for f in fields:
            if self.enable_hidden:
                if 'hidden' in f and f['hidden'] == 'true':
                    hidden_map.append(f)
            index_range = f['range']
            scope = index_range.strip("[]").split(":")
            end = int(scope[0])
            start = int(scope[-1])
            for r in re_map:
                if r[0] <= start and r[-1] >= end:
                    re_map.remove(r)
                    if r[0] != start:
                        re_map.append([r[0], start - 1])
                    if r[-1] != end:
                        re_map.append([end + 1, r[-1]])
        for r in re_map:
            frange = "[" + str(r[-1]) + ":" + str(r[0]) + "]"
            re_fields.append({
                "name": "reserved",
                "range": frange,
                "reset_value": "0",
                })
        for h in hidden_map:
            reset_value = h['reset_value']
            if reset_value == '' or reset_value == 'None':
                reset_value = "0"
            reset_value = self.format_reset_value(reset_value, h['range'])
            re_fields.append({
                "name": "reserved",
                "range": h['range'],
                "reset_value": reset_value,
                "hidden": 'true',
                })
        #print(re_fields)
        return re_fields

    def add_reset(self, reset, index_range, value):
        scope = index_range.strip("[]").split(":")
        end = int(scope[0]) + 1
        start = int(scope[-1])
        if not value or value == 'None':
            pass
        elif int(value, 16) == 0:
            pass
        else:
            fill_list = list(bin(int(value, 16))[2:])
            for i in range(start, end):
                if fill_list != []:
                    reset[i] = fill_list.pop(-1)
                else:
                    break

    def get_reset(self, reset, bit_num):
        bit_num = int(bit_num)
        value = ''
        for i in range(bit_num):
            value += str(reset[bit_num -1 -i])
        tmp = hex(int(value, 2))[2:]
        #if tmp == '0':
        #    hex_value = "0x" + tmp
        #else:
        hex_value = "0x" + tmp.zfill(8)
        return hex_value

    def zero_fill(self, in_hex):
        new_hex = "0x" + in_hex[2:].zfill(self.max_len)
        return new_hex

    def relist_fields(self, fields):
        fields_len = len(fields)
        for i in range(fields_len):
            for j in range(i+1, fields_len):
                i_f = fields[i]
                i_index_range = i_f['range']
                i_scope = i_index_range.strip("[]").split(":")
                i_end = int(i_scope[0])
                i_start = int(i_scope[-1])
                j_f = fields[j]
                j_index_range = j_f['range']
                j_scope = j_index_range.strip("[]").split(":")
                j_end = int(j_scope[0])
                j_start = int(j_scope[-1])
                if i_end <= j_end:
                    fields[i], fields[j] = fields[j], fields[i]

    def create_md3(self, dpath, lm, bit_num = 32):
        update_fields = []
        ls = libsvg.LibSVG()
        reset = {}
        for k,v in enumerate("0"*bit_num):
            reset[k] = v
    
        is_group = 0
        register = self.get_delem(self.js_dict, dpath)
        name = self.get_delem(self.js_dict, dpath, key = 'RegName' )
        name = name.upper()
        #addr = self.get_addr(dpath)
        addr = self.zero_fill(self.path_addr_dict[dpath])
        if dpath.find("group_reg") >= 0:
            is_group = 1
            addr_msg, scope_msg, group_msg = self.get_groupmsg(dpath)
            addr = str(addr) + addr_msg + "(" + scope_msg + " )"
        #print(name, "(" + addr + ")")
    
        #if name.endswith("reserved"):
        if name.endswith("RESERVED"):
            return -1
    
        des = self.get_delem(self.js_dict, dpath, key = 'Description')
        #self.xmind_md += '### ' + name + '\n' + '> ' + des + '\n'
        self.xmind_md += '### ' + name + '\n'
        fields = self.get_delem(self.js_dict, dpath, key = 'Fields')
        for f in fields:
            if f['access'] in ['rw_fprotect_sec', 'rw_fprotect']:
                scope = f['range'].strip("[]").split(":")
                end = int(scope[0])
                start = int(scope[-1])

                high_end = (int)(end + bit_num/2)
                high_start = (int)(start + bit_num/2)
                if high_end == high_start:
                    high_range = "[" + str(high_end) + "]"
                else:
                    high_range = "[" + str(high_end) + ":" + str(high_start) + "]"
                update_field = {
                        **f,
                        'name': f['name'] + "_update",
                        'range': high_range,
                        'reset_value': '0',
                        'description': "每 bit 对应寄存寄存器 " + f['name'] + " 每一位是否更新; 0：不更新; 1：更新"
                    }
                update_fields.append(update_field)
        fields.extend(update_fields)
        for f in fields:
            if f['reset_value'] == '' or f['reset_value'] == 'None':
                f['reset_value'] = "0"
        reserve_fields = self.get_reserve_fields(fields, bit_num)
        if self.enable_hidden:
            new_fields = []
            for f in fields:
                if 'hidden' in f and f['hidden'] == 'true':
                    continue
                else:
                    new_fields.append(f)
            fields = new_fields
        fields.extend(reserve_fields)
        self.relist_fields(fields)

        for f in fields:
            table = ls.create_blank_form(bit_num, f['name'])
        for f in fields:
            ls.add_line(table, f['range'])
        for f in fields:
            ls.add_reset_value(table, f['range'], f['reset_value'], f['name'])
            self.add_reset(reset, f['range'], f['reset_value'])
        for f in fields:
            ls.add_name(table, f['range'], f['name'])
        hex_reset = self.get_reset(reset, bit_num)

        #ls.write_down(table)
        ls.indent(table)
        svg_data = ls.svg_transform(table)
        svg_name = name + ".svg"
        with open(svg_name, "w") as fd:
            fd.write(svg_data)
        #register_data = "![](" + svg_name + ")\n<br>"
        register_data = "![](" + svg_name + ")\n"

        line = lm.md_create_title_line(['位域','变量名', '属性', '默认值', '描述'])
        register_data += "\n\n" + line
        fields_len = len(fields)
        for i in range(fields_len):
            #f = fields[fields_len - i -1]
            f = fields[i]
            if f['name'] != 'reserved':
                #self.xmind_md += '* ' + f['name'] + '\n    * ' + f['description'] + '\n'
                self.add_xmind_md(f['name'], f['description'])
                formatted_reset_value = self.format_reset_value(f['reset_value'], f['range'])
                line = self.add_description_table(lm, [f['range'], f['name'], \
                        f['access'], formatted_reset_value, f['description']])
                register_data += line
            else:
                if 'hidden' in f and f['hidden'] == 'true':
                    line = self.add_description_table(lm, [f['range'], f['name'], \
                            '',f['reset_value'],''])
                else:
                    line = self.add_description_table(lm, [f['range'], f['name'], \
                            '','',''])
                register_data += line
    
        #table_title = 'Register:' + name + ' ('  + addr + ')'
        reg_addr_msg = '地址偏移 : '  + addr
        reg_hex_reset = '默认值 : ' + hex_reset
        register_data = "## " + name + "\n\n" + reg_addr_msg + '<br>' + \
                reg_hex_reset + '\n' + register_data
        if self.output_md:
            os.system("mv " + svg_name + " " + self.markdownpath)
            self.data += register_data +'\n'
        if self.output_gitbook:
            os.system("mv " + svg_name + " " + self.gitbookpath)
            #register_data += '\n<br>\n'
            register_data += '\n'
            self.reg_data += register_data + '\n'
            #print(self.reg_data)
            #sys.exit()
            self.reg_rst += '   ' + name + '.md\n'

            file_path = os.path.join(self.gitbookpath, name + '.md')
            #with open(file_path, 'w') as fd:
            #    fd.write(register_data)
            #    for i in range(fields_len):
            #        f = fields[i]
            #        fd.write('\n' + '### ' + f['name'])

    def add_xmind_md(self, name, des):
        self.xmind_md += '* ' + name + '\n'
        des = des.replace('：',':').replace('；',';')
        if re.findall(';[0-9]:|。[0-9]:', des):
            for tmp_des in re.split('[;。]', des):
                tmp_des = tmp_des.strip(' ')
                if not re.match('^[0-9]:', tmp_des):
                    self.xmind_md += '* > ' + tmp_des + '\n'
            for tmp_des in re.split('[;。]', des):
                tmp_des = tmp_des.strip(' ')
                if re.match('^[0-9]:', tmp_des):
                    self.xmind_md += '    * ' + tmp_des + '\n'
        else:
            for tmp_des in re.split('[。]', des)[1:]:
                self.xmind_md += '* > ' + tmp_des + '\n'
            tmp_des = re.split('[。]', des)[0]
            self.xmind_md += '    * ' + tmp_des + '\n'
    
    def add_description(self, name, des, access):
        des = des.replace("；", ";")
        dess = des.split(";")
        msg = ''
        if len(dess) == 1:
            line = "**" + name.upper() + "** **["+ access + "]** :&emsp;" + des.strip(" ")
        else:
            for i in dess:
                msg += "<br>&emsp;" + i.strip(" ")
            line = "**" + name.upper() + "** **[" + access + "]** :" + msg
        return line

    def add_description_table(self, lm, argv):
        line = lm.md_create_body_line2(argv)
        return line

    def check_file(self, file_name):
        if self.dir_type != "link":
            return
        if os.path.exists(os.path.join(self.json_output_dir, file_name)):
            add_cmd = "cat " + os.path.join(self.gitbookpath, file_name) + " >> " \
                    + os.path.join(self.json_output_dir, file_name)
            os.system(add_cmd)
        else:
            mv_cmd = "mv " + os.path.join(self.gitbookpath, file_name) + " " \
                    + os.path.join(self.json_output_dir, file_name)
            os.system(mv_cmd)

    def relist(self, in_list):
        new_list = []
        list_len = len(in_list)
        for i in range(list_len):
            for j in range(i, list_len):
                #print(in_list[j])
                if int(in_list[i]['addr'], 16) >= int(in_list[j]['addr'], 16):
                    in_list[i], in_list[j] = in_list[j], in_list[i]

    def create_all_reg_data(self, lm):
        for i in self.new_all_reg_list:
            if self.enable_hidden:
                if i['hidden'] == 'true':
                    continue
            self.all_reg_data += lm.md_create_body_line([i['name'], i['addr'], \
                    i['reset'], i['des']], self.output_md)
            self.all_reg_tex_data += lm.tex_create_body_line([i['name'], i['addr'], \
                    i['reset'], i['des']], self.gitbookpath)

    def get_gitlog(self):
        gitlog = ''
        gitlog += '# 最近修改:\n\n'
        gitlog += '|日期|作者|描述|commit_id|\n'
        gitlog += '|:---|:---|:---|:---|\n'
        json_dir = os.path.dirname(self.js_file)
        now_dir = os.getcwd()
        cmd = 'git log --pretty=format:"| %ad | %cn | %s | %h |" --date=short'
        os.chdir(json_dir)
        fd = os.popen(cmd)
        tmp = fd.readlines()
        if len(tmp) >= 1:
            for line in tmp:
                gitlog += line
        else:
            gitlog += '|暂无|暂无|暂无|暂无|\n'
        os.chdir(now_dir)
        with open(os.path.join(self.gitbookpath, 'gitlog.md'), 'w') as fc:
            fc.write(gitlog)
        return gitlog

    def parse_reg(self, in_dict, tpath = ''):
        # name
        name = in_dict['RegName']
        name = name.upper()

        # des
        des = ''
        if 'Description' in in_dict:
            des = in_dict['Description']

        # reset
        reset = {}
        for k,v in enumerate("0"*self.bit_num):
            reset[k] = v
        if 'Fields' in in_dict:
            for f in in_dict['Fields']:
                self.add_reset(reset, f['range'], f['reset_value'])
        hex_reset = self.get_reset(reset, self.bit_num)

        # addr
        if 'Offset' in in_dict:
            offset = int(in_dict['Offset'], 16)
            st_addr =  hex(self.base_addr + offset)
            self.history_addr = self.base_addr + offset
        elif 'Step' in in_dict:
            step = int(in_dict['Step'], 16)
            st_addr =  hex(self.history_addr + step)
            self.history_addr = self.history_addr + step

        # hidden
        hidden = 'false'
        if 'Hidden' in in_dict:
            hidden = in_dict['Hidden']

        self.new_all_reg_list.append({
            'name':name,
            'hidden':hidden,
            'addr':st_addr,
            'reset':hex_reset,
            'des':des,
            })
        #print(tpath, name, st_addr)
        if tpath not in self.tmp_path_dict:
            self.tmp_path_dict[tpath] = st_addr

    def parse_group_reg(self, group_hidden, in_dict, index = [], tpath = ''):
        # 组后缀
        if index != []:
            d = "||".join(index)

        # name
        name = in_dict['RegName'] + "||" + str(d)
        name = name.upper()

        # des
        des = ''
        if 'Description' in in_dict:
            des = in_dict['Description']

        # reset
        reset = {}
        for k,v in enumerate("0"*self.bit_num):
            reset[k] = v
        if 'Fields' in in_dict:
            for f in in_dict['Fields']:
                self.add_reset(reset, f['range'], f['reset_value'])
        hex_reset = self.get_reset(reset, self.bit_num)

        # addr
        if 'Offset' in in_dict:
            offset = int(in_dict['Offset'], 16)
            st_addr =  hex(self.group_offset + offset)
            self.history_addr = self.group_offset + offset
        elif 'Step' in in_dict:
            step = int(in_dict['Step'], 16)
            st_addr =  hex(self.history_addr + step)
            self.history_addr = self.history_addr + step

        # hidden
        hidden = 'false'
        if group_hidden == 'true':
            hidden = 'true'
        elif 'Hidden' in in_dict:
            hidden = in_dict['Hidden']

        self.new_all_reg_list.append({
            'name':name,
            'hidden':hidden,
            'addr':st_addr,
            'reset':hex_reset,
            'des':des,
            })
        #print(tpath, name, st_addr)
        if tpath not in self.group_reg_dict:
            self.group_reg_dict[tpath] = []
        self.group_reg_dict[tpath].append({
            "name":name,
            "addr":st_addr,
            })

        if tpath not in self.tmp_path_dict:
            self.tmp_path_dict[tpath] = st_addr

    def parse_group_group(self, group_hidden, in_dict, index = [], tpath = ''):
        depth = in_dict['depth']
        if 'Hidden' in in_dict and in_dict['Hidden'] == 'true':
            group_hidden = 'true'
        if "Offset" in in_dict:
            offset = int(in_dict['Offset'], 16)
            self.group_offset =  self.group_offset + offset
        elif "Step" in in_dict:
            step = int(in_dict['Step'], 16)
            self.group_offset =  self.history_addr + step
        for d in range(depth):
            if d >= 1:
                if 'Offset' in in_dict['group_reg'][0] and \
                        int(in_dict['group_reg'][0]['Offset'], 16) == 0:
                    self.group_offset =  self.history_addr + int(self.bit_num/8)
            for j in range(len(in_dict['group_reg'])):
                #print(g['RegName'])
                g = in_dict['group_reg'][j]
                tmp = copy.deepcopy(index)
                tmp.append(str(d))
                tmp_path = copy.deepcopy(tpath)
                if 'RegName' in g and 'group_reg' not in g:
                    self.parse_group_reg(group_hidden, g, tmp, tmp_path + '/group_reg/' + str(j))
                if 'RegName' in g and  'group_reg' in g:
                    self.parse_group_group(group_hidden, g, tmp, tmp_path + '/group_reg/' + str(j))

    def parse_group(self, in_dict, index = [], tpath = ''):
        depth = in_dict['depth']
        group_hidden = "false"
        if 'Hidden' in in_dict and in_dict['Hidden'] == 'true':
            group_hidden = 'true'
        if "Offset" in in_dict:
            offset = int(in_dict['Offset'], 16)
            self.group_offset =  self.base_addr + offset
        elif "Step" in in_dict:
            step = int(in_dict['Step'], 16)
            self.group_offset =  self.history_addr + step
        for d in range(depth):
            if d >= 1:
                if 'Offset' in in_dict['group_reg'][0] and \
                        int(in_dict['group_reg'][0]['Offset'], 16) == 0:
                    self.group_offset =  self.history_addr + int(self.bit_num/8)
            for j in range(len(in_dict['group_reg'])):
                g = in_dict['group_reg'][j]
                #print(g['RegName'])
                tmp = copy.deepcopy(index)
                tmp.append(str(d))
                tmp_path = copy.deepcopy(tpath)
                if 'RegName' in g and 'group_reg' not in g:
                    self.parse_group_reg(group_hidden, g, tmp, tmp_path + '/group_reg/' + str(j))
                if 'RegName' in g and  'group_reg' in g:
                    self.parse_group_group(group_hidden, g, tmp, tmp_path + '/group_reg/' + str(j))


    def parse_dict(self, in_dict, tpath = ''):
        if 'RegName' in in_dict and 'group_reg' not in in_dict:
            self.parse_reg(in_dict, tpath)
            return 0
        if 'RegName' in in_dict and  'group_reg' in in_dict:
            self.parse_group(in_dict, [], tpath)
            return 0
        if "base_addr" in in_dict:
            self.base_addr = int(in_dict['base_addr'], 16)
            self.history_addr = int(in_dict['base_addr'], 16) 
            self.bit_num = int(in_dict['d_width'])
        for k, v in in_dict.items():
            if isinstance(v, (str,int)):
                pass
                #print(k,v)
            else:
                pass
                #print(k,type(v))
            if isinstance(v, list):
                if not tpath:
                    tpath = k
                else:
                    tpath += '/' +k
                for j in range(len(v)):
                    tmp = copy.deepcopy(tpath)
                    t = v[j]
                    if isinstance(t, dict):
                        self.parse_dict(t, tmp+'/'+str(j))

    def get_addr(self, dpath):
        return self.tmp_path_dict[dpath]

    def relist(self, in_list):
        max_len = len(in_list[-1]['addr'][2:])
        new_list = []
        for i in in_list:
            if i['name'].startswith('RESERVED'):
                continue
            else:
                i['addr'] = self.zero_fill(i['addr'])
                new_list.append(i)
        self.new_all_reg_list = new_list

    def format_reset_value(self, reset_value, range_str):
        if not self.reset_value_bin:
            return reset_value
        scope = range_str.strip("[]").split(":")
        start = int(scope[-1])
        end = int(scope[0])
        bit_width = end - start + 1

        try:
            if reset_value.lower().startswith('0x'):
                value = int(reset_value, 16)
            elif reset_value.lower().startswith('0b'):
                value = int(reset_value, 2)
            else:
                value = int(reset_value)
        except ValueError:
            return reset_value

        # 生成二进制字符串
        bin_str = bin(value)[2:].zfill(bit_width)
        return f'0b{bin_str}'

    def main(self):
        file_msg = os.path.basename(self.js_file).split(".json")[0]
        self.file_msg = file_msg
        pp = preprocess.PreProcess()
        self.js_dict = pp.start(self.js_file)
        # 解析完json，获取所有寄存器和地址信息
        self.parse_dict(self.js_dict)
        #print(self.js_dict)
        #print(self.new_all_reg_list)
        #sys.exit()

        self.js_dpath = self.get_dpath(self.js_dict)
        lm = libmd.LibMarkdown()
        self.all_reg_data = lm.md_create_title_line(['名称', '地址', '初值', '描述'])
        self.all_reg_tex_data = lm.md_create_title_line(['名称', '地址', '初值', '描述'])
        if self.output_gitbook:
            if self.dir_type == "alone":
                self.gitbookpath = os.path.join("_json_output/gitbook/", file_msg)
                if not os.path.exists(self.gitbookpath):
                    os.system("mkdir -p " + self.gitbookpath)
                readme = os.path.join(self.gitbookpath, 'README.md')
                summary = os.path.join(self.gitbookpath, 'SUMMARY.md')
                if not os.path.exists(readme):
                    with open(readme, 'w') as fd:
                        fd.write("   ")
                with open(summary, 'w') as fd:
                    fd.write('# Summary \n\n')
                    fd.write('* [寄存器列表](all_register.md)\n')
                    for i in self.js_dpath:
                        self.path_addr_dict[i] = self.get_addr(i)
                    self.max_len = len(self.path_addr_dict[self.js_dpath[-1]][2:])
                    for i in range(int(len(self.js_dpath))):
                        name = self.get_delem(self.js_dict, self.js_dpath[i], key = 'RegName' )
                        name = name.upper()
                        if name != "RESERVED":
                            dpath = self.js_dpath[i]
                            fd.write('  * [' + name + ']('+ name + '.md)\n')
                            bit_num = self.get_delem(self.js_dict, dpath.split('registers')[0], \
                                    key = 'd_width')
                            self.create_md3(self.js_dpath[i], lm, bit_num)
                    self.relist(self.new_all_reg_list)
                    self.create_all_reg_data(lm)
                    with open(os.path.join(self.gitbookpath, 'all_register.md'), 'w') as fc:
                        fc.write("## 寄存器列表\n\n" + self.all_reg_data)
                print("\n\tcreate " + self.gitbookpath +" success") 
            elif self.dir_type == "link":
                self.gitbookpath = os.path.join(self.link_path, file_msg)
                if self.save_dir:
                    path_msg = os.path.join("_json_output/", self.dirname, str(file_msg))
                else:
                    path_msg = "_json_output/" + str(file_msg)
                if not os.path.exists(self.gitbookpath):
                    os.system("mkdir -p " + self.gitbookpath)
                readme = os.path.join(self.gitbookpath, 'README.md')
                summary = os.path.join(self.gitbookpath, 'SUMMARY.md')
                regrst = os.path.join(self.link_path, 'register.rst')
                if not os.path.exists(regrst):
                    with open(regrst, 'w') as fd:
                        fd.write("寄存器说明\n====================\n\n.. toctree::\n\n")
                        all_line = "   " + file_msg + "寄存器列表 <" + file_msg + "/all_register.md>\n" 
                        detail_line = "   " + file_msg + "寄存器详细说明 <" + file_msg + "/detail.md>\n" 
                        fd.write(all_line)
                        fd.write(detail_line)
                else:
                    with open(regrst, 'a') as fd:
                        all_line = "   " + file_msg + "寄存器列表 <" + file_msg + "/all_register.md>\n" 
                        detail_line = "   " + file_msg + "寄存器详细说明 <" + file_msg + "/detail.md>\n" 
                        fd.write(all_line)
                        fd.write(detail_line)
                if not os.path.exists(readme):
                    with open(readme, 'w') as fd:
                        fd.write("   ")
                with open(summary, 'w') as fd:
                    fd.write('# Summary \n\n')
                    reg_list_path = os.path.join(path_msg, "all_register.md") 
                    reg_detail_path = os.path.join(path_msg, "detail.md") 
                    fd.write('* [寄存器列表](' + reg_list_path + ')\n')
                    fd.write('* [寄存器详细说明](' + reg_detail_path + ')\n')
                    for i in self.js_dpath:
                        name = self.get_delem(self.js_dict, i, key = 'RegName' )
                        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        #print(name)
                        addr = self.get_addr(i)
                        self.path_addr_dict[i] = addr
                        name = self.get_delem(self.js_dict, i, key = 'RegName' )
                        #print(name, "(" + addr + ")")
                        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    self.max_len = len(self.path_addr_dict[self.js_dpath[-1]][2:])
                    for i in range(int(len(self.js_dpath))):
                        name = self.get_delem(self.js_dict, self.js_dpath[i], key = 'RegName' )
                        name = name.upper()
                        if name != "RESERVED":
                            dpath = self.js_dpath[i]
                            #md_path = os.path.join(path_msg, name + ".md")
                            #fd.write('  * [' + name + ']('+ md_path + ')\n')
                            bit_num = self.get_delem(self.js_dict, dpath.split('registers')[0], \
                                    key = 'd_width')
                            self.create_md3(self.js_dpath[i], lm, bit_num)
                    #print(111111111)
                    #sys.exit()
                    self.relist(self.new_all_reg_list)
                    self.create_all_reg_data(lm)
                    gitlog = ''
                    try:
                        gitlog = self.get_gitlog()
                    except:
                        pass
                    with open(os.path.join(self.gitbookpath, 'all_register.md'), 'w') as fc:
                        fc.write("# 寄存器列表\n\n" + self.all_reg_data)
                    #with open(os.path.join(self.gitbookpath, 'all_register_tex.md'), 'w') as fc:
                    #    fc.write("## 寄存器列表\n\n" + self.all_reg_tex_data)
                    with open(os.path.join(self.gitbookpath, 'detail.md'), 'w') as fc:
                        fc.write(self.reg_data)
                    #with open(os.path.join(self.gitbookpath, 'detail.rst'), 'w') as fc:
                    #    fc.write(self.reg_rst)
                #self.check_file('README.md')
                #self.check_file('SUMMARY.md')
                os.system('rm ' + readme)
                os.system('rm ' + summary)
                print("\n\tcreate " + self.gitbookpath +" success") 
        if self.output_md:
            #self.markdownpath = "./_json_output/" + file_msg
            self.markdownpath = os.path.join("./_json_output/markdwon/", file_msg)
            if not os.path.exists(self.markdownpath):
                os.system("mkdir -p " + self.markdownpath)
            md_file = os.path.join(self.markdownpath, file_msg + ".md")
            for i in self.js_dpath:
                self.path_addr_dict[i] = self.get_addr(i)
            self.max_len = len(self.path_addr_dict[self.js_dpath[-1]][2:])
            for i in self.js_dpath:
                bit_num = self.get_delem(self.js_dict, i.split('registers')[0], \
                        key = 'd_width')
                self.create_md3(i, lm, bit_num)
            self.relist(self.new_all_reg_list)
            self.create_all_reg_data(lm)
            self.data = "# 寄存器列表\n" + self.all_reg_data + "\n"\
                    + "# 寄存器详细说明\n" + self.data
            self.data = self.data.replace("\n#", "\n##")
            if self.output_xmind:
                md_file = file_msg + '.md'
                with open(md_file, 'w') as fd:
                    fd.write(self.xmind_md)
                    print("\n\tcreate " + md_file + " success") 
                    return
            with open(md_file, 'w') as fd:
                fd.write(self.data)
            print("\n\tcreate " + md_file + " success") 


def usage():
    """
    Usage:
        jsontomd -f json_file (-g) (-l remote_dir)
      exp
        jsontomd -f npu_register.json -g -l target_dir

    parameters:
        -f : 指定json文件
        -l : 指定生成目录, 把生成的gitbook目录,放到指定目录下
        -d : 加-d ,在生成目录中保留-f所指路径层级, 不加-d 只以json文件名创建目录
        -g : 加-g ,生成gitbook目录, 不加-g 生成单个markdown文件(加-l 默认加上了-g)
        -a : 加-a ,生成所有隐藏的寄存器， 默认不加, 隐藏寄存器不生成
    """
    print(usage.__doc__)

def main():
    if len(sys.argv) <= 1:
            usage()
            sys.exit()
    opts,args = getopt(sys.argv[1:],"f:l:gxhdvab")
    js_file = "demo.json"
    link_path = ''
    output_md = 1
    output_gitbook = 0
    output_xmind = 0
    enable_hidden = True
    reset_value_bin = False
    save_dir = 0
    dir_type = "alone"
    for k,v in opts:
        if k == "-f":
            js_file = v
        if k == "-d":
            save_dir = 1
        if k == "-l":
            link_path = v
            dir_type = "link"
            output_gitbook = 1
            output_md = 0
        if k == "-g":
            output_gitbook = 1
            output_md = 0
        if k == "-x":
            output_xmind = 1
        if k == "-a":
            enable_hidden = False
        if k == "-b":
            reset_value_bin = True
        if k == "-h":
            usage()
            sys.exit()
        if k == "-v":
            print(__version__)
            sys.exit()
    #print("opts:", opts, "args", args)
    tj = TranslateJson(js_file, link_path, dir_type, output_md, output_gitbook, output_xmind, \
            save_dir, enable_hidden, reset_value_bin)
    tj.main()

    #tjo = jo.TranslateJson(js_file, link_path, dir_type, output_md, output_gitbook, \
    #        output_xmind,save_dir)
    #tjo.main()
    #
    #cat.cat_md(link_path, tj.file_msg)

if __name__ == "__main__":
    main()

