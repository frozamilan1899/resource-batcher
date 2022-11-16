import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext

import constant
import batch_process
from log_redirect import StdoutRedirector

main_win = Tk()

srv_select_value = StringVar()
res_type_select_value = StringVar()
res_file_type_select_value = StringVar()
file_path_select_value = StringVar()


def srv_select(*args):
    global base_url
    base_url = constant.srv_env_dic[srv_select_value.get()]
    print("服务器基地址：" + base_url)


def res_type_select(*args):
    global resource_type
    resource_type = res_type_select_value.get()
    print("资源类型：" + resource_type)


def res_file_type_select(*args):
    global resource_file_type
    resource_file_type = res_file_type_select_value.get()
    print("资源文件类型：" + resource_file_type)


def choose_file_path():
    file_path = filedialog.askdirectory(initialdir=os.getcwd())
    if file_path != '':
        file_path_select_value.set(file_path)
        dir_lb = ttk.Label(main_win, text=str(file_path_select_value.get()), font=('楷体', 14), anchor='nw')
        dir_lb.place(x=320, y=160, anchor='nw')
        global batch_files_dir
        batch_files_dir = file_path_select_value.get()
        print("文件夹目录：" + batch_files_dir)
    else:
        print('choose no file.')


def isSet(v):
    try:
        type(eval(v))
    except:
        return 0
    return 1


def process():
    # 参数检查
    if isSet('base_url') and isSet('resource_type') and isSet('resource_file_type') and isSet('batch_files_dir'):
        # just do it
        print('==== 开始 =================================================================')
        ret = batch_process.get_res_data_and_upload_file(base_url, resource_type, resource_file_type, batch_files_dir)
        if ret == 0:
            messagebox.showinfo('处理结果', '处理完成')
        else:
            messagebox.showinfo('处理结果', '错误代码：' + ret)
    else:
        messagebox.showinfo('参数检查', '请选择参数')


def clear_log():
    myStd.text_space.delete(1.0, 'end')


def save_log():
    log_content = myStd.text_space.get(1.0, 'end')
    root_path = filedialog.askdirectory(initialdir=os.getcwd())
    import time
    filename = 'log_file_' + str(time.time()).split('.')[0] + '.txt'
    save_path = os.path.join(root_path, filename)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.writelines(log_content)
    messagebox.showinfo('处理结果', '保存完成:' + save_path)


def exit_program():
    # 退出程序
    main_win.destroy()


def init_client_window():
    # 初始化窗口
    main_win.title('资源管理--批处理程序')
    main_win.minsize(900, 600)
    main_win.maxsize(900, 600)
    main_win.geometry('550x350')
    main_win.configure(background='#eeeeee')

    # 操作按钮
    srv_choose_lb = ttk.Label(main_win, text="请选择服务器", anchor='e', font=('楷体', 14))
    srv_choose_lb.place(x=10, y=40, anchor='nw')
    srv_choose_cbx = ttk.Combobox(main_win, width=22, textvariable=srv_select_value)
    srv_choose_cbx.place(x=200, y=40, anchor='nw')
    srv_choose_cbx["values"] = constant.srv_names
    srv_choose_cbx.bind('<<ComboboxSelected>>', srv_select)

    # 操作按钮
    res_type_choose_lb = ttk.Label(main_win, text="请选择资源类型", font=('楷体', 14))
    res_type_choose_lb.place(x=10, y=80, anchor='nw')
    res_type_choose_cbx = ttk.Combobox(main_win, width=22, textvariable=res_type_select_value)
    res_type_choose_cbx.place(x=200, y=80, anchor='nw')
    res_type_choose_cbx["values"] = constant.res_types
    res_type_choose_cbx.bind('<<ComboboxSelected>>', res_type_select)

    # 操作按钮
    res_file_type_choose_lb = ttk.Label(main_win, text="请选择资源文件类型", font=('楷体', 14))
    res_file_type_choose_lb.place(x=10, y=120, anchor='nw')
    res_file_type_choose_cbx = ttk.Combobox(main_win, width=22, textvariable=res_file_type_select_value)
    res_file_type_choose_cbx.place(x=200, y=120, anchor='nw')
    res_file_type_choose_cbx["values"] = constant.res_file_types
    res_file_type_choose_cbx.bind('<<ComboboxSelected>>', res_file_type_select)

    # 操作按钮
    dir_choose_lb = ttk.Label(main_win, text="请选择文件夹", font=('楷体', 14))
    dir_choose_lb.place(x=10, y=160, anchor='nw')
    dir_choose_btn = ttk.Button(main_win, text='选择', width=8, command=choose_file_path)
    dir_choose_btn.place(x=200, y=160, anchor='nw')

    # 运行信息输出文本框
    info_text = scrolledtext.ScrolledText(main_win, relief="solid", width=120, height=16)
    info_text.place(x=20, y=200)

    # 退出
    quit_btn = ttk.Button(main_win, text='退出程序', width=10, command=exit_program)
    quit_btn.place(x=100, y=440, anchor='nw')

    # 执行
    exec_btn = ttk.Button(main_win, text='批处理执行', width=10, command=process)
    exec_btn.place(x=400, y=440, anchor='nw')

    # 清除
    save_btn = ttk.Button(main_win, text='清除日志', width=10, command=clear_log)
    save_btn.place(x=550, y=440, anchor='nw')

    # 保存
    save_btn = ttk.Button(main_win, text='保存日志', width=10, command=save_log)
    save_btn.place(x=700, y=440, anchor='nw')

    # 添加说明
    intro_lb = ttk.Label(main_win, text='注意：\n（1）在使用本程序前，请先将需要批处理的文件放入一个文件夹中。\n'
                                        '（2）程序会将文件夹中的文件一次性上传，请保证文件夹中是一类文件。\n'
                                        '（3）action、motion、emotion的文件类型为"默认类型"\n'
                                        '（4）发现问题可保存日志到文件，文件存储位置可自定义指定', font=('楷体', 12))
    intro_lb.place(x=10, y=500, anchor='nw')

    # 日志输出重定向
    global myStd
    myStd = StdoutRedirector(info_text)


if __name__ == '__main__':
    # 初始化程序UI界面
    init_client_window()
    # 进入消息循环
    main_win.mainloop()
