import xlrd2
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import sys
import io


class ExcelQueryApp:
    def __init__(self, root):
        # 设置中文字体支持
        self.font = ('SimHei', 10)

        # 主窗口设置
        self.root = root
        self.root.title("Excel表格数据查询工具")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)

        # 保存Excel数据
        self.workbook = None
        self.Table0 = None
        self.Table1 = None
        self.current_file = ""

        # 创建UI
        self.create_widgets()

        # 重定向stdout到文本区域
        self.output_buffer = io.StringIO()
        sys.stdout = self.output_buffer

    def create_widgets(self):
        # 创建菜单栏
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="打开Excel文件", command=self.open_excel_file)
        filemenu.add_separator()
        filemenu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=filemenu)
        self.root.config(menu=menubar)

        # 文件操作区域 - 添加打开文件按钮和文件路径显示
        file_frame = ttk.LabelFrame(self.root, text="文件操作", padding="10")
        file_frame.pack(fill=tk.X, padx=10, pady=5)

        self.open_file_button = ttk.Button(file_frame, text="打开Excel文件", command=self.open_excel_file)
        self.open_file_button.pack(side=tk.LEFT, padx=5)

        # 文件路径显示区域
        self.file_path_var = tk.StringVar()
        self.file_path_var.set("未选择文件")
        self.file_path_label = ttk.Label(file_frame, textvariable=self.file_path_var, font=self.font, wraplength=600)
        self.file_path_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # 创建输入区域
        input_frame = ttk.LabelFrame(self.root, text="查询", padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(input_frame, text="方法名:", font=self.font).pack(side=tk.LEFT, padx=5)
        self.method_entry = ttk.Entry(input_frame, width=30, font=self.font)
        self.method_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.method_entry.bind("<Return>", lambda event: self.search_method())

        self.search_button = ttk.Button(input_frame, text="查询", command=self.search_method)
        self.search_button.pack(side=tk.LEFT, padx=5)
        self.search_button.config(state=tk.DISABLED)  # 初始禁用

        # 创建结果显示区域
        result_frame = ttk.LabelFrame(self.root, text="查询结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, font=self.font)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)

        # 创建状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("请先打开Excel文件")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def open_excel_file(self):
        # 打开文件选择对话框
        file = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[
                ("Excel files", "*.xls *.xlsx *.xlsm"),
                ("All files", "*.*")
            ]
        )

        if not file:
            return

        try:
            # 尝试打开Excel文件
            self.workbook = xlrd2.open_workbook(file)
            self.Table0 = self.workbook.sheet_by_name("1 服务定义")
            self.Table1 = self.workbook.sheet_by_name("2 数据类型定义")

            # 更新文件路径显示
            self.current_file = file
            self.file_path_var.set(file)

            # 更新状态栏和结果区域
            self.status_var.set(f"已打开文件: {file}")
            self.clear_result()
            self.print_to_gui(f"已成功打开Excel文件: {file}")
            self.print_to_gui("请在上方输入方法名进行查询")

            # 激活输入框和查询按钮
            self.method_entry.focus_set()
            self.search_button.config(state=tk.NORMAL)

        except xlrd2.XLRDError as e:
            if "Expected BOF record" in str(e):
                error_msg = f"错误：您选择的文件 '{file}' 不是有效的Excel文件，而是RTF格式或其他格式的文件。\n请选择正确的.xls或.xlsx文件。"
                messagebox.showerror("文件格式错误", error_msg)
            elif "No sheet named" in str(e):
                error_msg = f"错误：Excel文件中找不到指定的工作表。\n请确保文件包含'1 服务定义'和'2 数据类型定义'工作表。"
                messagebox.showerror("工作表不存在", error_msg)
            else:
                error_msg = f"Excel读取错误: {str(e)}"
                messagebox.showerror("Excel读取错误", error_msg)

            self.status_var.set("文件打开失败，请重试")
            self.workbook = None
            self.Table0 = None
            self.Table1 = None
            self.current_file = ""
            self.file_path_var.set("未选择文件")
        except Exception as e:
            error_msg = f"程序发生错误: {str(e)}"
            messagebox.showerror("程序错误", error_msg)

            self.status_var.set("文件打开失败，请重试")
            self.workbook = None
            self.Table0 = None
            self.Table1 = None
            self.current_file = ""
            self.file_path_var.set("未选择文件")

    def search_method(self):
        if not self.workbook:
            messagebox.showwarning("警告", "请先打开Excel文件")
            return

        methodname = self.method_entry.get().strip()
        if not methodname:
            messagebox.showwarning("警告", "请输入方法名")
            return

        # 清空之前的查询结果
        self.clear_result()
        self.print_to_gui(f"查询方法名: {methodname}")
        self.print_to_gui("=" * 60)

        # 执行查询
        self.search_by_methodname(methodname)

    def search_by_methodname(self, methodname):
        if not self.Table0 or not self.Table1:
            return

        length0 = self.Table0.nrows
        found = False

        for i in range(length0):
            row0 = self.Table0.row_values(i)
            if methodname == row0[7]:
                found = True
                brctype = row0[3]

                if (brctype == "Field") == False:
                    # 有两个需要查找，入参和出参
                    inputparameter = row0[12]
                    outputparameter = row0[13]

                    if inputparameter != "":
                        # 输出inputparameter数据类型的具体含义
                        self.print_to_gui("入参：")
                        self.select_by_datatype(inputparameter.split(':')[-1])
                    else:
                        self.print_to_gui("无入参！")

                    if outputparameter != "":
                        # 输出outputparameter数据类型的具体含义
                        self.print_to_gui("出参：")
                        self.select_by_datatype(outputparameter.split(':')[-1])
                    else:
                        self.print_to_gui("无出参！")
                else:
                    filedpropertydatatype = row0[5]
                    if filedpropertydatatype != "":
                        # 输出filedpropertydatatype的具体含义
                        self.print_to_gui("参数：")
                        self.select_by_datatype(filedpropertydatatype + "")
                    else:
                        self.print_to_gui("无参数！")

        if not found:
            self.print_to_gui(f"未找到方法名 '{methodname}'")

        self.print_to_gui("=" * 60)

    def select_by_datatype(self, datatypename):
        if not self.Table1:
            return

        flag = 0  # 标记数据长度字段是否为空
        flag_found = 0  # 标记是否找到该数据类型

        length = self.Table1.nrows
        datasizecount = 1

        for i in range(length):
            row = self.Table1.row_values(i)
            if datatypename == row[0]:
                flag_found = 1
                memberdatatypereference = row[9]

                if (row[2] == "Struct") == False:
                    # 数据类型不是结构体的情况
                    if row[10] == "":
                        flag = 1

                    if flag == 0:
                        if "uint" in row[10]:
                            datasize = int(int(row[10].replace("uint", "")) / 8)
                        elif "int" in row[10]:
                            datasize = int(int(row[10].replace("int", "")) / 8)
                        elif row[10] == "float":
                            datasize = 4
                        elif row[10] == "double":
                            datasize = 8
                        elif row[10] == "UTF-8":
                            datasize = 3

                        self.print_to_gui(f"是{row[2]}类型,占{datasize}字节,这是第{datasizecount}字节")
                        datasizecount = datasizecount + datasize
                    else:
                        self.print_to_gui(f"是{row[2]}类型,该数据的数据长度字段为空，需自行查看")

                    if ((row[19] == "") == False):
                        self.print_to_gui(row[19])
                    else:
                        self.print_to_gui(row[18])
                else:
                    # 数据类型是结构体的情况
                    self.print_to_gui(str(row[7:10]))

                    # 二级结构处理
                    for j in range(length):
                        row1 = self.Table1.row_values(j)
                        if memberdatatypereference == row1[0]:
                            memberdatatypereference1 = row1[9]
                            memberdatatype1 = row1[2]

                            if (memberdatatype1 == "Struct"):
                                # 三级结构处理
                                self.print_to_gui("\t" + str(row1[7:10]))
                                for k in range(length):
                                    row2 = self.Table1.row_values(k)
                                    if memberdatatypereference1 == row2[0]:
                                        if row2[10] == "":
                                            flag = 1
                                        if flag == 0:
                                            if "uint" in row2[10]:
                                                datasize = int(int(row2[10].replace("uint", "")) / 8)
                                            elif "int" in row2[10]:
                                                datasize = int(int(row2[10].replace("int", "")) / 8)
                                            elif row2[10] == "float":
                                                datasize = 4
                                            elif row2[10] == "double":
                                                datasize = 8
                                            elif row2[10] == "UTF-8":
                                                datasize = 3

                                            self.print_to_gui(
                                                f"\t是{row2[2]}类型,占{datasize}字节,这是第{datasizecount}字节")
                                            datasizecount = datasizecount + datasize
                                        else:
                                            self.print_to_gui(
                                                "\t是" + row2[2] + "类型,该数据的数据长度字段为空，需自行查看")

                                        if ((row2[19] == "") == False):
                                            self.print_to_gui("\t" + row2[19].replace("\n", "\n\t"))
                                        else:
                                            self.print_to_gui("\t" + row2[18].replace("\n", "\n\t"))
                            else:
                                # 二级非结构体处理
                                if row1[10] == "":
                                    flag = 1
                                if flag == 0:
                                    if "uint" in row1[10]:
                                        datasize = int(int(row1[10].replace("uint", "")) / 8)
                                    elif "int" in row1[10]:
                                        datasize = int(int(row1[10].replace("int", "")) / 8)
                                    elif row1[10] == "float":
                                        datasize = 4
                                    elif row1[10] == "double":
                                        datasize = 8
                                    elif row1[10] == "UTF-8":
                                        datasize = 3

                                    self.print_to_gui(f"是{row1[2]}类型,占{datasize}字节,这是第{datasizecount}字节")
                                    datasizecount = datasizecount + datasize
                                else:
                                    self.print_to_gui(f"是{row1[2]}类型,该数据的数据长度字段为空，需自行查看")

                                if ((row1[19] == "") == False):
                                    self.print_to_gui(row1[19])
                                else:
                                    self.print_to_gui(row1[18])

        if flag_found == 0:
            self.print_to_gui("没有找到该数据类型！")

    def print_to_gui(self, text):
        # 在文本区域显示内容
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.config(state=tk.DISABLED)
        # 自动滚动到底部
        self.result_text.see(tk.END)

    def clear_result(self):
        # 清空结果区域
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelQueryApp(root)
    root.mainloop()