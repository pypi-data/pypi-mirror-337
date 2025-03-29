# coding: gbk

# ͨ�����еķ�ʽ��ʵ��uiģ�����ѭ���ķ��룬�Ա�֤uiģ������ԣ��߼��ϱ��麯����ʽҪ����
# ���洦��ǰ̨���̣߳�mainloop����һ����̨�̣߳�ÿһ���¼�Դһ����̨�߳�
# ǰ̨���̣߳����棩��callbackֻ�ǽ������͵�q�оͷ����ˣ���������Դ������timer�������Ե�����һ���̣߳�Ҳ�ǽ����󷢵�q�Ͳ�����
# mainloop�Ǻ�̨�����̣߳����е������������Ŷ�ִ�У����̣߳�
#     ����callback��timer�����Ŷ�ִ�У�˭Ҳ���ܴ��˭�����Կ���ʡȥ��Դ�����ļ�������


import os
import time
import chardet
import queue
import traceback
import yaml
import threading
import tkinter as tk


def _yaml_load(fn, encoding=None, default=None):
    if default is None:
        default = dict()

    if os.path.exists(fn):
        bcontent = open(fn, "rb").read()
        if encoding is None:
            encoding = chardet.detect(bcontent)['encoding']
        yml = yaml.load(bcontent.decode(encoding), Loader=yaml.FullLoader)  # throw exception
        return default if yml is None else yml
    else:
        return default


class TkYzwMainUi:
    self = None  # ready mark

    def __init__(self, title=None, font='΢���ź� 9', icon_fn="", bg=None, geometry=None, topmost=False, layout=None, layout_encoding=None, mainq=None):
        """
        param mainq:
            �������գ�������һ��self.mainq�����ⲿ����
        param layout:
            str:  ������ַ������ͣ�������Ϊ�ļ�����������layout���Զ��������
            dict: layout�����ֵ�
        """
        self.root = tk.Tk()
        if mainq is None:
            self.mainq = queue.Queue()  # ����Ϣ����
        else:
            self.mainq = mainq

        self.title = title
        if title: self.root.title(title)
        self.root.option_add('*Font', font)  # '΢���ź� 9 bold'
        if bg: self.root.option_add('*Background', bg)  #  root["bg"] = bg
        if topmost: self.root.wm_attributes("-topmost", 1)
        if icon_fn and os.path.exists(icon_fn): self.root.iconbitmap(icon_fn)

        self.layout_fn = ""
        self.layout_encoding = layout_encoding
        if layout:
            self.root.protocol("WM_DELETE_WINDOW", self.do_exit)
            if isinstance(layout, str):
                self.layout_fn = layout
                self.layout = _yaml_load(self.layout_fn, layout_encoding)
            elif isinstance(layout, dict):
                self.layout = layout

            if geometry is None:
                geometry = self.layout.get("geometry", None)  #>  'geometry':'405x427+531+450'

        else:
            self.layout = dict()

        if geometry:
            self.root.geometry(geometry)

        self.after_ms = 0
        self.after_func = None
        self.after_id = None

        self.root_destroyed = False
        self.self = self  # ready

    def getall_uiv(self):
        d = dict()
        for mname in self.__dict__:
            if mname.startswith("uiv_"):
                mvalue = getattr(self, mname)
                d[mname[4:]] = mvalue.get()
        return d

    def after(self, ms:int, func):
        self.after_ms = ms
        self.after_func = func
        if ms == 0 or func is None:
            # ȡ��timer
            if self.after_id:
                self.root.after_cancel(self.after_id)
            self.after_ms = 0
            self.after_func = None
            self.after_id = None
        else:
            # ����timer
            self.after_id = self.root.after(ms, self.on_after)

    def on_after(self):
        self.after_func()
        self.after_id = self.root.after(self.after_ms, self.on_after)

    def on_root_destroy(self):
        pass

    def on_save_layout(self, f):
        # �����˳�ʱ,�Զ�����
        layout = self.layout.copy()
        layout.pop('geometry', None)
        for k,v in layout.items():
            print(f"{k}: {repr(v)}", file=f)

    def do_exit(self, *la, **ka):
        # *la, **ka to accept mainui_dispatch's calling convention
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        if self.layout_fn:
            with open(self.layout_fn, "w", encoding=self.layout_encoding) as f:
                print("geometry:", self.root.winfo_geometry(), file=f)
                self.on_save_layout(f)

        self.on_root_destroy()
        try:
            self.root.destroy()  # destory all widgets
        except RuntimeError:
            # main thread is not in main loop:
            pass
        self.root.quit()  # quit mainloop even if destroy() failed
        self.root_destroyed = True
        self.mainq.put(("exit", 0))

    def on_callback(self, callbackid, *la, **ka):
        self.mainq.put(("ui", callbackid, la, ka))

    # def run(self):
    #     if self.enable_on_idle:
    #         # ���ｫ����һ����ѭ�������߳�CPU 100%���������������
    #         while not self.root_destroyed:
    #             self.root.update_idletasks()  # ֻ������Ļ,������event��callback
    #             self.root.update()  # �����ܴ�callback�е���update
    #             self.on_idle()  # ִ���ڼ䣬���潫�ò�����Ӧ�����뾡���˳�
    #     else:
    #         self.root.mainloop()

    def run(self):
        self.root.mainloop()

    def mainui_dispatch(self, msga: tuple, ui_dispatcher:dict):
        callbackid, widget, la, ka = msga
        # print(f"mainui_dispatch id={callbackid} widget={widget} la={la} ka={ka}")
        func = ui_dispatcher.get(callbackid, None)
        if func is not None:
            func(widget, *la, **ka)


class TkYzwTimer(threading.Thread):
    def __init__(self, q:queue.Queue, tvsec:int, count:int=-1):
        super().__init__()
        self.daemon = True
        self.mainq = q
        self.tvsec = tvsec
        self.count = count

    def run(self):
        q = self.mainq
        while self.count != 0:
            self.count -= 1
            time.sleep(self.tvsec)
            q.put(("timer", self.tvsec))

    def exit(self):
        self.count = 0


class TkYzwMainUiApp:
    """
    ͨ��mainq���л��¼���������ʱ�������ص��������������
    idle_timers ����mainq����ʱ�Żᴥ���Ķ�ʱ�¼�
    ui�¼���on_ui_{callbackid}�д���
    �����¼� on_mainq
    """
    def __init__(self, mainui:TkYzwMainUi, tk_after=0, timers=None, enable_idle=None, idle_timers=None):
        """
        # param enable_idle��None or float
        #     mainq��idle�೤ʱ�䴥��on_idle
        #     ȱʡΪNone����������idle���ƣ�����������self.on_idle��Ҳ���ᱻ����
        # param idle_timers��None or list of float
        #     ���û�д�enable_idle�����Զ���enable_idle=0.01
        #     �����ö����ʱ����idle_timers=��ʱ��ʱ���б���λΪ�룬��������
        #     �ö�ʱ��������idle��lazy�жϣ����Բ���֤ʵʱ�ԣ�ϵͳû�¸ɵ�ʱ��Żᴥ����һֱæ��һֱ����������������enable_idle����
        #     Ҫʵ�־�ȷ�Ķ�ʱ���������й���һ���������̷߳��Ͷ�ʱ����Ϣ��q
        """
        if timers is None: timers = []

        self.mainui = mainui

        self.mainq = mainui.mainq
        threading.Thread(target=self.thproc_mainloop, args=(enable_idle, idle_timers), daemon=True).start()
        # self.ui_dispatcher = {
        #     "demo_bind": self.on_ui_demo_bind,
        #     "demo_command": self.on_ui_demo_command,
        #     "exit": self.on_ui_exit
        # }
        self.a_thrtimer = []
        for tvsec in timers: self.a_thrtimer.append(TkYzwTimer(self.mainq, tvsec))
        for x in self.a_thrtimer: x.start()
        if tk_after:
            mainui.after(tk_after, self.on_tk_after)

    def run(self):
        self.mainui.run()

    def on_ui_exit(self, *la, **ka):
        self.mainui.do_exit()

    def thproc_mainloop(self, enable_idle=None, idletimers=None):
        mainq = self.mainq

        if isinstance(idletimers, list) and len(idletimers) > 0:
            if enable_idle is None: enable_idle = 0.01
            t = time.time()
            a_timercycle = idletimers
            a_timerlast = [t] * len(idletimers)
        else:
            a_timercycle = []

        timeout = enable_idle if enable_idle else 1
        while not self.mainui.root_destroyed:
            btimeout = False
            try:
                msgtype, *argv = mainq.get(block=True, timeout=timeout)
            except queue.Empty:
                btimeout = True
            except:
                traceback.print_exc()
                continue

            try:
                if btimeout:
                    self.on_idle()

                    t = time.time()
                    for i, cycle in enumerate(a_timercycle):
                        if t - a_timerlast[i] > cycle:
                            a_timerlast[i] = t
                            self.on_idle_timer(cycle)
                    continue

                if msgtype == 'exit':
                    break
                elif msgtype == 'timer':
                    tvsec = argv[0]
                    self.on_mainq_timer(tvsec)
                elif msgtype == 'ui':
                    callbackid, la, ka = argv
                    # mainui.mainui_dispatch(argv[0], self.ui_dispatcher)
                    func = getattr(self, f"on_ui_{callbackid}")
                    if func: func(*la, **ka)  # self.on_ui_xxx
                else:
                    self.on_mainq(msgtype, *argv)
            except:
                traceback.print_exc()
                continue
        for x in self.a_thrtimer: x.exit()
        self.on_app_exit()

    def on_app_exit(self):
        pass

    def on_mainq(self, msgtype, *argv):
        print(f"on_mainq {msgtype} {argv}")

    def on_tk_after(self):
        # ע��, ������tk���߳���ִ��, ��mainq����һ���߳�, �о���, ���Բ�Ҫ�����߼�, ֻ�ܽ��н������
        print(f"on_tk_after")

    def on_mainq_timer(self, tvsec:float):
        print(f"on_mainq_timer {tvsec}")

    def on_idle_timer(self, cycle:float):
        # ע��һֱ��æʱ, ���ᱻ���ȵ�
        print(f"on_idle_timer {cycle}")

    def on_idle(self):
        # ��Ҫ�Ҹ�, ���ô�����Ƶ����
        pass


if __name__ == '__main__':

    def thproc_demo():
        while True:
            mainq.put(("demo", None))
            time.sleep(5)

    class MainUi(TkYzwMainUi):
        def __init__(self):
            super().__init__(title="mainui demo", geometry='800x500+200+200')
            fr = self.root
            w = tk.Label(fr, text="clickme", font="΢���ź� 28 bold");
            w.pack(side="top", fill="both", expand=1)
            w.bind("<Double-1>", lambda event: self.on_callback("demo_bind_double1", event))

            opm_list = ['Python', 'PHP', 'CPP', 'C', 'Java', 'JavaScript', 'VBScript']
            self.uiv_opm = tk.StringVar(value=opm_list[0])
            w = tk.OptionMenu(fr, self.uiv_opm, *opm_list, command=lambda v: self.on_callback("demo_command_option_menu", v))
            w.pack(side="top", padx=10, pady=5)
            self.uix_om = w

            w = tk.Button(fr, text="exit", fg="red",
                          command=lambda: self.on_callback("exit"))
            w.pack(side="top", padx=10, pady=5)

    class MainApp(TkYzwMainUiApp):
        def __init__(self, mainui:TkYzwMainUi, *la, **ka):

            # user init codes here

            super().__init__(mainui, *la, **ka)
            threading.Thread(target=thproc_demo, args=(), daemon=True).start()

        def on_ui_demo_bind_double1(self, event):
            print(f"on_ui_demo_bind_double1: event={event}")

        def on_ui_demo_command_option_menu(self, v):
            print(f"on_ui_demo_command_option_menu {v}")

        def on_mainq(self, msgtype, *argv):
            print(f"on_mainq {msgtype} {argv}")


    import threading
    import time

    mainui = MainUi()
    mainq = mainui.mainq
    mainapp = MainApp(mainui, timers=[1], tk_after=1000, idle_timers=[0.5, 3])
    mainapp.run()
    print("bye")