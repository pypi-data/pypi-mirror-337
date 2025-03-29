# coding: utf-8

import sys
import time
import tkinter as tk
import tkinter.ttk as ttk
#import bisect
from sortedcontainers import SortedList
from collections import defaultdict


if sys.platform == 'win32':
    import win32clipboard
    import win32con

    def clip_copy(msg):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_TEXT, msg.encode("gbk"))
        win32clipboard.CloseClipboard()
else:
    def clip_copy(msg):
        pass


def list_get(a:list, i:int, default:any):
    if i < 0 or i >= len(a):
        return default
    else:
        return a[i]


class TkYzwFrameTree(tk.Frame):
    def __init__(self, master, column_list, width_list:list=None, command=None, on_select=None, heading_command=None, scroll="", dnd="", **kw):
        """
        推荐格式: column_list = [("tag", 120), ("desc,w", "100,w+"), ...("抬头列名,抬头列anchor", "列宽,内容行anchor")] 分别对应column=['#0', 'c1', 'c2', ...]  #0是树节点
               或早期格式: column_list = ["tag", "desc,w", ..."列名,列名anchor"] width_list=[120, "100,w+", ..."列宽,内容行anchor"]
               抬头列anchor表示heading行的每一列的anchor, 不写表示默认center
               ("tag", 120)表示这一列的抬头写tag,居中对齐, 列宽120, 下面的内容行居中对齐
               ("desc,w", "100,w+")表示这一列抬头写desc,左对齐, 列宽100, 下面的内容行左对齐
        command: 双击某个单元格时调用，同时on_select也会被调用
        on_select: 选择时调用(单击某行单选, 按shift片选, 按ctrl多选)
        heading_command： 单击抬头时调用
        dnd: drag and drop模式 "move"或""
        kw:
            show缺省, 既显示抬头又树
            show="tree" 只显示树, 无抬头栏；
            show="headings" 只显示抬头  # 无抬头无法拉伸单列的列宽
        """

        self.cb_command = command
        self.cb_on_select = on_select
        kw2 = kw.copy()
        kw2.pop("show", None)
        super().__init__(master, **kw2)
        self.master = master
        fr = self

        self.all_user_defined_iids = set()
        self.d_piid_a_sortkey = defaultdict(SortedList)  # 父节点iid -> 子节点的sorted_key列表
        self.d_iid_seq = defaultdict(int)

        if isinstance(column_list[0], tuple):
            a = [x[0] for x in column_list]
            width_list = [x[1] for x in column_list]
            column_list = a

        # column_list[0] 对应树节点column="#0", 不需要命名, 剩下的是list列, 依次命名为"c1", "c2", ...
        tree = ttk.Treeview(fr, columns=["c%d" % (i + 1) for i in range(len(column_list)-1)], **kw)
        self.wx = tree  #type: ttk.Treeview

        # 配置抬头行 column_list
        style = ttk.Style()
        style.configure("Treeview", foreground='black', font="微软雅黑 10")  #  highlightthickness=0, bd=0
        style.configure("Treeview.Heading", foreground='black', font="微软雅黑 11 bold")

        ANCHORS = ('n', 's', 'w', 'e', 'nw', 'sw', 'ne', 'se', 'ns', 'ew', 'nsew', 'center')

        for i, c in enumerate(column_list):
            a = c.rsplit(",", maxsplit=1)  # a> [text, anchor]
            if len(a) > 1 and a[1] in ANCHORS:
                # 指定了anchor, 并且anchor合法
                text = a[0]
                anchor = a[1]
            else:
                # 没有指定anchor, 或者指定的anchor非法
                text = c
                anchor = 'center'

            # column_list[0]代表#0, 所以需要区别对待:
            column = '#0' if i == 0 else "c%d"%i
            if heading_command is not None:
                tree.heading(column, text=text, anchor=anchor, command=lambda x=text: heading_command(x))
            else:
                tree.heading(column, text=text, anchor=anchor)

        # 配置内容行width_list
        for i, width in enumerate(width_list): # tk.W
            #> "50:100,w+"  # "<minwidth>:<width>, <anchor><stretch>"
            minwidth = 1
            stretch = 0
            anchor = "center"
            if type(width) is str:
                if width.endswith("+"):
                    stretch = 1
                    width=width[:-1]
                a = width.rsplit(",", maxsplit=1)
                if len(a) > 1 and a[1] in ANCHORS:
                    width = a[0]
                    anchor = a[1]
                a = width.split(":", maxsplit=1)
                if len(a) > 1:
                    minwidth = int(a[0])
                    width = a[1]
                width = int(width)
            column = '#0' if i == 0 else "c%d"%i
            tree.column(column, minwidth=minwidth, width=width, stretch=stretch, anchor=anchor)

        #tree.tag_configure('h1', font="微软雅黑 12 bold", foreground='red')
        tree.tag_configure('h1', font="微软雅黑 12 bold")
        tree.tag_configure('h2', font="微软雅黑 11")
        tree.tag_configure('h3', font="微软雅黑 10")
        tree.tag_configure('blue', foreground='blue')
        tree.tag_configure('red', foreground='red')
        tree.tag_configure('green', foreground='green')
        tree.tag_configure('grey', foreground='grey')

        tree.bind("<Double-1>", self._on_tree_double1)      # double click
        # tree.bind("<ButtonRelease-1>", self.on_tree_release1)  # single click, 不能使用<Button-1>,会取到鼠标点击前的状态
        # tree.bind("<<TreeviewSelect>>", self.on_tree_select)  # 一定能取到selection, 不会"index out of range"
        tree.bind("<<TreeviewSelect>>", self.__on_tree_select)

        fr.columnconfigure(0, weight=1)
        fr.rowconfigure(0, weight=1)
        tree.grid(row=0, column=0, sticky="nsew")

        # 卷滚条
        if 'y' in scroll:
            ysb = ttk.Scrollbar(fr, orient='vertical', command=tree.yview)
            tree.configure(yscroll=ysb.set)
            ysb.grid(row=0, column=1, sticky='ns')

        if 'x' in scroll:
            xsb = ttk.Scrollbar(fr, orient='horizontal', command=tree.xview)
            tree.configure(xscroll=xsb.set)
            xsb.grid(row=1, column=0, sticky='ew')

        if dnd:
            tree.bind("<ButtonPress-1>", self.on_dnd_enter, add='+')
            tree.bind("<ButtonRelease-1>", self.on_dnd_leave, add='+')
            tree.bind("<B1-Motion>", self.on_dnd_move, add='+')
            tree.bind("<Shift-ButtonPress-1>", self.on_dnd_enter_block, add='+')
            # tree.bind("<Shift-ButtonRelease-1>", self.on_dnd_leave_block, add='+')

        #fr.bind("<F1>", self.on_F1)
        #fr.bind("<F3>", self.on_F3)
        #fr.bind("<Control-c>", self.on_COPY)

        self.bind("x", self.on_key_x)
        self.bind("X", self.on_key_X)
        self.bind("<Control-c>", self.on_key_ctrl_c)
        self.bind("<Control-a>", self.on_key_ctrl_a)

    def on_dnd_enter_block(self, event):
        tv = event.widget
        select = [tv.index(s) for s in tv.selection()]
        select.append(tv.index(tv.identify_row(event.y)))
        select.sort()
        for i in range(select[0], select[-1] + 1, 1):
            tv.selection_add(tv.get_children()[i])

    def on_dnd_enter(self, event):
        tv = event.widget
        if tv.identify_row(event.y) not in tv.selection():
            tv.selection_set(tv.identify_row(event.y))

    def on_dnd_leave(self, event):
        tv = event.widget
        if tv.identify_row(event.y) in tv.selection():
            tv.selection_set(tv.identify_row(event.y))

    def on_dnd_move(self, event):
        tv = event.widget

        # 取目标位置
        iid = tv.identify_row(event.y)
        if not iid: return
        parent = tv.parent(iid)  # 目标父节点
        moveto = tv.index(iid)   # 目标兄弟节点的排行, 从0开始编号

        # 移动源到目标位置
        for s in tv.selection():
            # 源和目标的父节点不同, 不允许移动
            if tv.parent(s) != parent:
                continue
            if s == iid:
                continue
            tv.move(s, parent, moveto)

    def bind(self, sequence, func):
        self.wx.bind(sequence, func)

    def on_key_X(self, _):
        self.do_clear()

    def on_key_x(self, _):
        self.do_deltree_selected()

    def on_key_ctrl_c(self, _):
        a = self.wx.selection()
        a_msg = []
        for iid in a:
            text = self.wx.item(iid, 'text')
            values = self.wx.item(iid, 'values')
            a_msg.append("%s: %s" % (text, ','.join(values)))
        clip_copy('\n'.join(a_msg))

    def on_key_ctrl_a(self, _):
        a_iid = self.iter_children("")
        self.wx.selection_set(a_iid)

    def __on_tree_select(self, event):
        if self.cb_on_select:
            iids = self.wx.selection()  # type: tuple
            if iids: self.cb_on_select(iids[0], event)

    def _on_tree_double1(self, event):
        if self.cb_command:
            iids = self.wx.selection()  # type: tuple
            if iids: self.cb_command(iids[0], event)

    def dump_selection(self):
        print("dump_selection:")
        iids = self.wx.selection()  # type: tuple  # 刚启动时,未选择任何东西,返回空tuple
        for i, iid in enumerate(iids):
            parent = self.wx.parent(iid)
            index = self.wx.index(iid)  # 兄弟节点排行
            print(f'  [{i}] iid={iid} text={self.wx.item(iid, "text")} parent={parent} index={index}')

    # def iter_children(self, iid:str):
    #     print("iter_children", iid)
    #     yield iid
    #     a = self.ui_tree.get_children(iid)
    #     for x in a:
    #         print("iter_children for", x)
    #         self.iter_children(x)

    def iter_children(self, iid="", a=[]):
        """ 返回iid下的所有子节点，如果iid为空，则返回所有节点 """
        try:
            children = self.wx.get_children(iid)
        except:
            return a
        a.append(iid)
        for x in children:
            self.iter_children(x, a)
        return a

    def get_all_children(self, item=""):
        children = self.wx.get_children(item)
        for child in children:
            children += self.get_all_children(child)
        return children

    def on_tree_release1(self, event):
        print('on_tree_release1(%r):' % event)  #> <ButtonRelease event state=Control|Mod1|Button1 num=1 x=199 y=176>
        self.dump_selection()

    def on_tree_select(self, event):
        print('on_tree_select(%r):' % event)  #> <VirtualEvent event x=0 y=0>
        self.dump_selection()

    def do_clear(self):
        for i in self.wx.get_children():
            # 遍历第一级子节点即可
            self.wx.delete(i)  # 包含其子节点
        self.all_user_defined_iids = set()
        self.d_piid_a_sortkey = defaultdict(SortedList)  # 为实现sorted_key排序插入

    def delete(self, iid:str):
        if iid in self.all_user_defined_iids:
            self.all_user_defined_iids.discard(iid)

        try:
            self.wx.delete(iid)
        except:
            pass

    def do_deltree(self, iid:str, keepself=False):
        for i in self.iter_children(iid):
            if i in self.all_user_defined_iids:
                self.all_user_defined_iids.discard(i)

        if keepself:
            # 删除子节点, 保留自身
            for i in self.iter_children(iid):
                if i != iid:
                    try:
                        self.wx.delete(i)
                    except:
                        pass
        else:
            # 删除本身及其子节点
            try:
                self.wx.delete(iid)
            except:
                pass

    def do_deltree_selected(self):
        for iid in self.wx.selection():  # tuple
            self.do_deltree(iid)

    def insert(self, parent, index="end", sorted_key=None, reversed=False, **kw):
        """  添加一个树节点, 可以使用kv对描述, 左侧k=iid(显示为text), 右侧v=value, 每个节点的iid是唯一的,不可以重复
        除了第一个参数parent,建议都采用key传入
        :param parent: ""=top_level or 父iid
        :param index: 0, 1, ..., "end",  # index="sorted" changed to sorted_key=<iid>
        :param iid: 子iid, 不一定按照easy规范的路径格式, 不指定iid则不加入iids_user_defined(不参与去重,系统保证不重), 所以也无须"存在变修改"逻辑
        :param text: 显示在树节点上的文本, text不能为None,否则会乱报错
        :param values(value也可以): 指定节点右栏显示的值, str或者tuple(多列的值), 如果是str,只取第一个词,所以最好还是传入tuple=(str,)
        :param tags(tag也可以): 类似css的属性,str或tuple(同时指定多个tag)
        :param sorted_key: 每个兄弟节点,都用一个字符串代表自己,字符串的排序,作为兄弟节点的排序依据
        :param reversed: bool, 指定sorted_key是否倒序

        e.g.
            .insert("xxx/yyy", iid="xxx/yyy/zzz", text="zzz", index="end", value="msg")
            .insert("xxx/yyy", iid="xxx/yyy/zzz", text="zzz", index="end", values=("msg",))
            .insert("xxx/yyy", text="zzz1", value="msg1", sorted_key="zzz1", reversed=True)  # 使用sorted_key, 忽略index, 且一般没必要指定iid(不加入
            .insert("xxx/yyy", text="zzz3", value="msg3", sorted_key="zzz3", reversed=True)
            .insert("xxx/yyy", text="zzz2", value="msg2", sorted_key="zzz2", reversed=True)
        """
        iid_user_defined = kw.get("iid", None)  # 如果指定了自定义的iid,将被存放到cache
        if iid_user_defined and iid_user_defined in self.all_user_defined_iids:
            # values = kw.get("values", ())
            # if values: self.wx.item(iid_user_defined, values=values)
            try:
                del kw['iid']
                del kw['sorted_key']
                del kw['reversed']
            except:
                pass
            self.wx.item(iid_user_defined, **kw)  # 如果已经存在,则放弃插入,直接修改原节点
            return iid_user_defined

        # if 'sorted_key' in kw:
        #     sorted_key = kw['sorted_key']
        #     del kw['sorted_key']
        # else:
        #     sorted_key = None
        #
        # if 'reversed' in kw:
        #     reversed_ = kw['reversed']
        #     del kw['reversed']
        # else:
        #     reversed_ = False

        try:
            if sorted_key is not None:
                a_sortkey = self.d_piid_a_sortkey[parent]     # type: SortedList # 取所有兄弟的sorted_key
                index = a_sortkey.bisect_right(sorted_key)  # 覆盖传入的index参数
                if reversed: index = len(a_sortkey) - index
            else:
                a_sortkey = None

            # print("wx.insert(parent=%s, iid=%r)"%(parent, iid_user_defined), kw)
            iid = self.wx.insert(parent, index, **kw)
            # 插入成功,没有引发异常
            if a_sortkey is not None:
                a_sortkey.add(sorted_key)
            if iid_user_defined is not None:
                self.all_user_defined_iids.add(iid)
            return iid
        except tk.TclError as e:
            #> e.args[0] 'Item xxx already exists'
            if "already exists" in e.args[0]:
                # 应该不会进入到这里, 用户指定的iid已经被iids_user_defined过滤掉了
                return iid_user_defined
            raise

    def easy_path(self, path_in:str, index="end", sorted_key=None, reversed=False):
        """ easy系列使用路径格式来规范节点的iid """
        path_exists = ""
        path_to_make_reversed = [path_in]
        while True:
            # print("---", path_to_make_reversed)
            path = path_to_make_reversed[-1]
            if path in self.all_user_defined_iids:
                path_exists = path
                path_to_make_reversed.pop()
                break

            a = path.rsplit("/", maxsplit=1)
            if len(a) == 1: break
            path_to_make_reversed[-1:] = a[::-1]

        for x in path_to_make_reversed[::-1]:
            path_new = path_exists + '/' + x if path_exists else x
            path_exists = self.insert(path_exists, iid=path_new, text=x, open=True, index=index, sorted_key=sorted_key, reversed=reversed)
            self.all_user_defined_iids.add(path_new)

    def easy_item(self, path:str, index="end", sorted_key=None, reversed=False, **kw):
        """ 设置指定路径的节点
            easy_item(path, values=((c1, 1, ""))

        easy系列使用路径格式来规范节点的iid
        与easy_insert相比,这个无法插入匿名节点
        """
        if not path: return
        if path not in self.all_user_defined_iids:
            self.easy_path(path, index, sorted_key=sorted_key, reversed=reversed)
        self.wx.item(path, **kw)

    def easy_set(self, path:str, index="end", sorted_key=None, reversed=False, column=None, value=None, **kw):
        """ 设置指定路径的节点

        easy系列使用路径格式来规范节点的iid
        与easy_insert相比,这个无法插入匿名节点
        """
        if not path: return
        if path not in self.all_user_defined_iids:
            self.easy_path(path, index, sorted_key=sorted_key, reversed=reversed)
        self.wx.set(path, column=column, value=value)

    def easy_insert(self, path:str, _iid:str=None, index="end", sorted_key=None, reversed=False, **kw):
        """ 在指定父路径插入子节点, 允许使用sorted_key排序(此时忽略index)
                匿名节点: _iid=None text=节点显示名
                命名节点: iid="path/_iid", text显示名缺省为_iid,也可以另行指定

            _iid 节点名, 不指定时为匿名节点(该节点由系统自动分配一个不符合路径规范的iid,不参与去重处理)
            text 显示在节点上的文本,对于命名节点,缺省与节点名一致
            iid  节点路径,使用分隔符/连接所有节点名, iid=path/_iid

        :param path: 类似父目录路径(iid), 不存在的所有上级节点自动创建
        :param _iid: 一般不指定, _iid类似文件名(或子目录名), 新创建的节点路径为iid=path/_iid,
                     不指定iid则不加入iids_user_defined(不参与去重,系统保证不重)
        :param text: 显示在树节点上的文本
        :param values(value也可以): 指定节点右栏显示的值, str或者tuple(多列的值),如果是str,只取第一个词,所以最好还是传入tuple=(str,)
        :param tags(tag也可以): 类似css的属性,str或tuple(同时指定多个tag)
        :param sorted_key: 用于节点排序的key, 兄弟节点也必须使用sorted_key插入
        :param reversed: bool 指定sorted_key是否倒序
        :param open: bool 折叠状态
        :return: 新创建的文件(或子目录)的完整路径(iid)

        e.g.
            .easy_insert("xxx/yyy", "zzz", value="msg", index="end", tags="h1")
              ==.easy_item("xxx/yyy/zzz",  value="msg", index="end", tags="h1")
            .easy_insert("xxx/yyy",        text="node1", value="msg1", sorted_key="key1", reversed=True)
        """
        if path and path not in self.all_user_defined_iids:
            self.easy_path(path, index, sorted_key=sorted_key, reversed=reversed)
        if _iid is not None:
            kw['iid'] = path + '/' + _iid if path else _iid
            if 'text' not in kw:
                kw['text'] = _iid
        return self.insert(path, index, sorted_key=sorted_key, reversed=reversed, **kw)

    def process_special_text(self, iid_parent, text):
        """节点上显示的文本"""
        if text == '<ts>':
            text = time.strftime("%H:%M:%S")
        elif text == '<seq>':
            self.d_iid_seq[iid_parent] += 1
            text = str(self.d_iid_seq[iid_parent])
        return  text

    def treecmd(self, cmd:str, rootpath="", rootpath_=""):
        """ 允许指定一个顶级rootpath
            rootpath_是rootpath加上目录分隔符/, 这个冗余仅仅是为了性能优化 """

        # t title            # 设置root节点显示的文本
        # X                  # clear all
        # xaaa/bbb           # deltree aaa/bbb

        # rxxx/yyy msg       # 更改路径xxx/yyy的msg, 如果不存在,则插入
        # Rxxx/yyy msg       # R,r的区别在于r在头部插入,R在尾部插入,其他用法相同

        # ixxx yyy:text msg  # 在路径xxx下面插入子节点yyy, 冒号后面为节点上显示的文本(可缺省使用yyy)
        # Ixxx yyy:text msg  # I, i的区别在于i在头部插入,I在尾部插入,其他用法相同
        # ixxx yyy      msg  # 在路径xxx下面插入子节点yyy, 节点上显示的文本为yyy
        # ixxx :text    msg  # 在路径xxx下面插入匿名节点(系统自动提供), 冒号后面为节点上显示的文本
        # ixxx :<ts>    msg  # 在路径xxx下面插入匿名节点(系统自动提供), 节点上显示时间戳

        # zxxx/yyy 0         # folder close 取名vim的z功能
        # zxxx/yyy 1         # folder open
        # txxx/yyy tag1 tag2 tag3 ...  # h1,h2,h3,red,green,blue,grey

        # 高级命令:
        # `<exec_source_code>  # 直接调用self.<exec_source_code>
        # `easy_inert(path, _iid, index=0...)

        if not cmd: return True
        if rootpath:
            if not rootpath_:
                rootpath_ = rootpath + '/'
        action, cmda = cmd[0], cmd[1:]

        if action == 'r':
            # rxxx/yyy msg       # 更改路径xxx/yyy的msg, 如果不存在,则插入
            a = cmda.split(maxsplit=1)  # iid, msg
            relpath = a[0]
            if relpath == '.':
                self.easy_item(rootpath, values=(list_get(a, 1, ""),))
            else:
                self.easy_item(rootpath_ + relpath, values=(list_get(a, 1, ""),))

        elif action == 'R':
            # Rxxx/yyy msg       # R,r的区别在于r在头部插入,R在尾部插入,其他用法相同
            a = cmda.split(maxsplit=1)  # iid, msg
            self.easy_item(rootpath_ + a[0], index="end", values=(list_get(a, 1, ""),))

        elif action == 'z':
            # fold
            a = cmda.split(maxsplit=1)  # iid, bopen
            try:
                bopen = eval(a[1])
            except:
                bopen = True
            self.easy_item(rootpath_ + a[0], open=bopen)

        elif action == 't':
            # tag
            a = cmda.split()  # iid, tags...
            tag=a[1:]
            self.easy_item(rootpath_ + a[0], tags=tag)

        elif action == 'i':
            a = cmda.split(maxsplit=2)  # iid_parent iid_new:text msg
            iid_parent = rootpath_ + a[0] if a[0] != '.' else rootpath
            iid_text = list_get(a, 1, "").split(":")
            _iid = list_get(iid_text, 0, "")
            text = list_get(iid_text, 1, "")
            text = self.process_special_text(iid_parent, text)
            if not text: text = _iid
            if not _iid: _iid = None
            values = (list_get(a, 2, ""),)
            self.easy_insert(iid_parent, index=0, _iid=_iid, text=text, values=values)
        elif action == 'I':
            a = cmda.split(maxsplit=2)  # iid_parent iid_new:text msg
            iid_parent = rootpath_ + a[0] if a[0] != '.' else rootpath
            iid_text = list_get(a, 1, "").split(":")
            _iid = list_get(iid_text, 0, "")
            text = list_get(iid_text, 1, "")
            sorted_key = list_get(iid_text, 2, None)
            text = self.process_special_text(iid_parent, text)
            if not text: text = _iid
            if not _iid: _iid = None
            values = (list_get(a, 2, ""),)
            self.easy_insert(iid_parent, index="end", _iid=_iid, text=text, values=values, sorted_key=sorted_key)
        elif action == 'X':
            self.do_clear()
        elif action == 'x':
            keepself = cmda.endswith("/")
            if keepself:
                cmda = cmda[:-1]
            if cmda == '.':
                self.do_deltree(rootpath, keepself=keepself)
            else:
                self.do_deltree(rootpath_ + cmda, keepself=keepself)
        elif action == '`':
            try:
                exec("self." + cmda)
            except:
                pass
        else:
            return False  # fail to parse cmd

        return True  # succ


class FrameTaskTree(TkYzwFrameTree):
    def __init__(self, master, column_list:list, width_list:list, scroll="xy", **ak):
        super().__init__(master, column_list, width_list, scroll, **ak)

        # column_list = ["task", "bs", "报价", "数量", "行情", "盈亏", "动作"]
        # width_list =  [120,     100,   60,      60,   120,   80,      80]

        for i in ['当前任务', '已完成任务']:
            self.insert('', 'end', text=i, open=True, iid=i, tags="h1")

        # self.wx.bind("<Delete>", self.on_key_delete)
        self.wx.bind("<Key>", self.on_key_)

    def task_add(self, iid_task:str, text_task:str, values:tuple):
        self.insert("当前任务", 0, text=text_task, iid=iid_task, open=True, tags="dir", values=values)

    def task_delete(self, iid_task):
        self.wx.delete(iid_task)

    def task_done(self, iid_task):
        self.wx.move(iid_task, "已完成任务", 0)

    def leg_add(self, iid_task:str, iid_leg:str, text_leg:str):
        self.insert(iid_task, 0, text=text_leg, iid=iid_leg, open=False, tags="dir")

    def item_update(self, iid:str, values:tuple):
        self.wx.item(iid, values=values)

    def column_update(self, iid:str, column:str, value:str):
        self.wx.set(iid, column=column, value=value)

    def on_key_(self, e):
        w = self.master.focus_get()
        if w != self.wx: return

        items = w.selection()  # type: tuple
        self.on_key(e, items)

    def on_key(self, e, items):
        print("on_key:", e.char, items)


if __name__ == '__main__':
    import time

    class Ui:  # 把UI相关的控件及其变量都封装在一起
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("tk_listview demo")
            self.root.geometry('800x500+200+200') # yscroll=True时需要设，否则窗口很小
            fr = tk.Frame(self.root)
            self.uiv_iid = tk.IntVar(value=1)
            tk.Entry(fr, width=4, textvariable=self.uiv_iid).pack(side="left")
            tk.Button(fr, text="easy", command=self.on_btn_easy, bg="#d0e0d0").pack(side="left")
            tk.Button(fr, text="添加", command=self.on_btn_insert, bg="#d0e0d0").pack(side="left")
            tk.Button(fr, text="GO", command=self.on_btn_go, bg="#d0e0d0").pack(side="left")
            tk.Button(fr, text="清空", command=self.on_btn_clear, bg="#d0e0d0").pack(side="left")
            tk.Button(fr, text="退出", command=self.root.destroy, bg="#d0e0d0").pack(side="left")
            fr.pack(side="top")

            # column_list = ["tag", "时间", "来源", "分类", "信息,w"]
            # width_list = [120, 100, 100, "50:100,w", "100,w+"]
            # 建议使用column_list的新格式, 每一项为(column, width), 其中column/width都可以有anchor,前者表示各title的anchor, 后者表示row中各列的anchor
            column_list = [("tag,w", "120,w"), ("时间", 100), ("来源", 100), ("分类","50:100,w"), ("信息,w", "100,w+")]

            ui_tree = TkYzwFrameTree(self.root, column_list, scroll="xy", height=10, on_select=self.on_select, command=self.on_command, heading_command=self.on_heading, dnd="move")
            # show="tree" 无抬头栏(无法拖拽列宽)；  show="headings" 有抬头
            self.ui_tree = ui_tree
            # ui_tree.wx.column('#0', stretch="no", minwidth=10, width=10)

            self.tree_branches = ["当前任务", "已完成任务", 'sorted', 'logs']  # '成交e', '委托op', '成交op',

            for i in ["状态"] + self.tree_branches:
                self.ui_tree.insert('', 'end', text=i, open=True, iid=i, tags="h1")

            v = ["时间x", "x来源", "分类", "信息,w"]
            self.ui_tree.insert('状态', 'end', text='无连接', open=True, iid='连接状态', value=v)
            # self.ui_tree.insert('状态', 'end', text='交易状态：STOPPED', open=True, iid='交易状态')
            self.ui_tree.insert('状态', 'end', text='现货挂: 0', open=False, iid='现货挂')
            self.ui_tree.insert('状态', 'end', text='现货成: 0', open=False, iid='现货成')
            self.ui_tree.insert('状态', 'end', text='期权放: 0', open=False, iid='期权放')

            # ui_tree.wx.heading('c4', text='信息', anchor='w')   使用,w后缀实现
            # ui_tree.wx.column('c4', width=100, stretch=1, anchor='w')  使用,w+后缀实现

            ui_tree.pack(side="top", fill="both", expand=1)

        def on_btn_easy(self):
            wx = self.ui_tree
            wx.easy_insert("", _iid='a', values=('a',), tags="h1")
            wx.easy_insert("", _iid='A', values=('A',), tags=["h1", "red"])
            wx.easy_insert("a/b/c", _iid='d', values=('abcd',), sorted_key='')
            wx.easy_insert("a/b/c", _iid='d', values=('ABCD',), sorted_key='')  # 修改已存在的path
            wx.easy_insert("1/2/3/4", _iid='5', values=('12345',))
            wx.easy_insert("a/b/c", text='x', values=('x',), sorted_key='x')
            wx.easy_insert("a/b/c", text='y', values=('y',), sorted_key='y')
            wx.easy_insert("a/b/c", text='z', values=('z',), sorted_key='z')
            wx.easy_item("a/b/c", tags="red")
            wx.easy_item("a/b", tags="blue")

        def on_btn_insert(self):
            a = self.ui_tree.wx.selection()  # type: tuple
            parent = "" if not a else a[0]
            iid = self.uiv_iid.get()
            t = time.strftime("%H%M%S")
            v = (t, iid, "x%d"%iid, "row%d"%iid )
            if parent == 'sorted':
                self.ui_tree.insert(parent, 0, values=v, text=iid, iid="myiid%d"%iid, sorted_key=iid, reversed=True)
            else:
                self.ui_tree.insert(parent, 0, values=v, text=iid, iid="myiid%d"%iid)
            self.uiv_iid.set(iid+1)

        def on_btn_go(self):
            tree = self.ui_tree.wx
            print("selected:")
            for i, item in enumerate(tree.selection()):
                print("    [%d]"%i, item, tree.item(item, "values"))

        def on_btn_clear(self):
            self.ui_tree.do_clear()

        def on_heading(self, col:str):
            print("on_heading %s"%col)

        def on_select(self, iid:str, event):
            self.ui_tree.dump_selection()

        def on_command(self, iid:str, event):
            tree = self.ui_tree.wx
            print("on_command ", tree.item(iid, "values")) # tuple
            rowiid = tree.identify_row(event.y)  # > iid I001 I002 I003 ...
            column = tree.identify_column(event.x)  # > #1 #2 #3 ...
            # treeview也相当于一张表格(不包含headings)
            rowindex = tree.index(rowiid) #> 0表示第一行，不包含headings
            colindex = int(column[1:]) #> 0表示第一列#0
            print("    row=[%d]%s"%(rowindex,rowiid), "col=[%d]%s"%(colindex,column), tree.set(rowiid))

            print("   ---", tree.set(rowiid, "%d" % colindex))
            if colindex > 0:
                # 设置点中的单元格
                tree.set(rowiid, "c%d"%colindex, value="xxx")
            else:
                # 第一列#0不能被设置
                #tree.set(rowiid, "#0", value="xxx")
                pass


    ui = Ui()
    ui.root.mainloop()

