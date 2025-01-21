import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pdf_to_image import convert_pdf_to_images
from PIL import Image, ImageOps
from color_convert import convert_colors, process_directory

class PDFConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF工具集")
        
        # 设置窗口大小和位置
        window_width = 600
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # 设置主题样式
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TLabel', padding=5)
        style.configure('TEntry', padding=5)
        style.configure('TNotebook', padding=5)
        
        # 创建标签页
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # PDF转图片标签页
        self.pdf_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.pdf_frame, text="PDF转图片")
        self.setup_pdf_tab()
        
        # 图片反转标签页
        self.invert_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.invert_frame, text="图片反转")
        self.setup_invert_tab()
        
        # 颜色转换标签页
        self.color_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.color_frame, text="颜色转换")
        self.setup_color_tab()
        
        # 图片合并PDF标签页
        self.merge_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.merge_frame, text="图片合并PDF")
        self.setup_merge_tab()
        
    def setup_pdf_tab(self):
        # PDF文件选择
        pdf_frame = ttk.Frame(self.pdf_frame)
        pdf_frame.pack(fill=tk.X, pady=10)
        
        self.pdf_path = tk.StringVar()
        ttk.Label(pdf_frame, text="PDF文件:").pack(side=tk.LEFT)
        self.pdf_entry = ttk.Entry(pdf_frame, textvariable=self.pdf_path, width=50)
        self.pdf_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(pdf_frame, text="浏览", command=self.select_pdf).pack(side=tk.LEFT)
        
        # 输出目录选择
        output_frame = ttk.Frame(self.pdf_frame)
        output_frame.pack(fill=tk.X, pady=10)
        
        self.output_path = tk.StringVar()
        ttk.Label(output_frame, text="输出目录:").pack(side=tk.LEFT)
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path, width=50)
        self.output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="浏览", command=self.select_output_dir).pack(side=tk.LEFT)
        
        # DPI设置
        dpi_frame = ttk.Frame(self.pdf_frame)
        dpi_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(dpi_frame, text="图片DPI:").pack(side=tk.LEFT)
        self.dpi_var = tk.StringVar(value="200")
        dpi_entry = ttk.Entry(dpi_frame, textvariable=self.dpi_var, width=10)
        dpi_entry.pack(side=tk.LEFT, padx=5)
        
        # 转换按钮
        convert_btn = ttk.Button(self.pdf_frame, text="开始转换", command=self.start_convert)
        convert_btn.pack(pady=20)
        
        # 状态显示
        self.pdf_status_var = tk.StringVar()
        status_label = ttk.Label(self.pdf_frame, textvariable=self.pdf_status_var, wraplength=500)
        status_label.pack(fill=tk.X, pady=10)
        
    def setup_invert_tab(self):
        # 输入目录选择
        input_frame = ttk.Frame(self.invert_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        self.invert_input_path = tk.StringVar()
        ttk.Label(input_frame, text="图片目录:").pack(side=tk.LEFT)
        self.invert_input_entry = ttk.Entry(input_frame, textvariable=self.invert_input_path, width=50)
        self.invert_input_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(input_frame, text="浏览", command=self.select_invert_input_dir).pack(side=tk.LEFT)
        
        # 输出目录选择
        output_frame = ttk.Frame(self.invert_frame)
        output_frame.pack(fill=tk.X, pady=10)
        
        self.invert_output_path = tk.StringVar()
        ttk.Label(output_frame, text="输出目录:").pack(side=tk.LEFT)
        self.invert_output_entry = ttk.Entry(output_frame, textvariable=self.invert_output_path, width=50)
        self.invert_output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="浏览", command=self.select_invert_output_dir).pack(side=tk.LEFT)
        
        # 反转按钮
        invert_btn = ttk.Button(self.invert_frame, text="开始反转", command=self.start_invert)
        invert_btn.pack(pady=20)
        
        # 状态显示
        self.invert_status_var = tk.StringVar()
        status_label = ttk.Label(self.invert_frame, textvariable=self.invert_status_var, wraplength=500)
        status_label.pack(fill=tk.X, pady=10)
        
    def setup_color_tab(self):
        # 输入选择框架
        input_frame = ttk.Frame(self.color_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        self.color_input_path = tk.StringVar()
        ttk.Label(input_frame, text="图片目录:").pack(side=tk.LEFT)
        self.color_input_entry = ttk.Entry(input_frame, textvariable=self.color_input_path, width=50)
        self.color_input_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(input_frame, text="浏览", command=self.select_color_input_dir).pack(side=tk.LEFT)
        
        # 输出目录选择
        output_frame = ttk.Frame(self.color_frame)
        output_frame.pack(fill=tk.X, pady=10)
        
        self.color_output_path = tk.StringVar()
        ttk.Label(output_frame, text="输出目录:").pack(side=tk.LEFT)
        self.color_output_entry = ttk.Entry(output_frame, textvariable=self.color_output_path, width=50)
        self.color_output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="浏览", command=self.select_color_output_dir).pack(side=tk.LEFT)
        
        # 颜色信息显示
        info_frame = ttk.Frame(self.color_frame)
        info_frame.pack(fill=tk.X, pady=10)
        ttk.Label(info_frame, text="白色 (255,255,255) → (255,223,63)").pack(pady=2)
        ttk.Label(info_frame, text="黑色 (0,0,0) → (31,77,120)").pack(pady=2)
        
        # 转换按钮
        convert_btn = ttk.Button(self.color_frame, text="开始转换", command=self.start_color_convert)
        convert_btn.pack(pady=20)
        
        # 状态显示
        self.color_status_var = tk.StringVar()
        status_label = ttk.Label(self.color_frame, textvariable=self.color_status_var, wraplength=500)
        status_label.pack(fill=tk.X, pady=10)
        
    def setup_merge_tab(self):
        # 输入目录选择
        input_frame = ttk.Frame(self.merge_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        self.merge_input_path = tk.StringVar()
        ttk.Label(input_frame, text="图片目录:").pack(side=tk.LEFT)
        self.merge_input_entry = ttk.Entry(input_frame, textvariable=self.merge_input_path, width=50)
        self.merge_input_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(input_frame, text="浏览", command=self.select_merge_input_dir).pack(side=tk.LEFT)
        
        # 输出PDF文件选择
        output_frame = ttk.Frame(self.merge_frame)
        output_frame.pack(fill=tk.X, pady=10)
        
        self.merge_output_path = tk.StringVar()
        ttk.Label(output_frame, text="输出PDF:").pack(side=tk.LEFT)
        self.merge_output_entry = ttk.Entry(output_frame, textvariable=self.merge_output_path, width=50)
        self.merge_output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="浏览", command=self.select_merge_output_file).pack(side=tk.LEFT)
        
        # 合并按钮
        merge_btn = ttk.Button(self.merge_frame, text="开始合并", command=self.start_merge)
        merge_btn.pack(pady=20)
        
        # 状态显示
        self.merge_status_var = tk.StringVar()
        status_label = ttk.Label(self.merge_frame, textvariable=self.merge_status_var, wraplength=500)
        status_label.pack(fill=tk.X, pady=10)
        
    def select_pdf(self):
        filename = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if filename:
            self.pdf_path.set(filename)
            # 自动设置输出目录为PDF所在目录
            self.output_path.set(os.path.dirname(filename))
    
    def select_output_dir(self):
        dirname = filedialog.askdirectory(title="选择输出目录")
        if dirname:
            self.output_path.set(dirname)
            
    def select_invert_input_dir(self):
        dirname = filedialog.askdirectory(title="选择图片目录")
        if dirname:
            self.invert_input_path.set(dirname)
            # 自动设置输出目录
            self.invert_output_path.set(os.path.join(dirname, "inverted"))
            
    def select_invert_output_dir(self):
        dirname = filedialog.askdirectory(title="选择输出目录")
        if dirname:
            self.invert_output_path.set(dirname)
    
    def select_color_input_dir(self):
        dirname = filedialog.askdirectory(title="选择图片目录")
        if dirname:
            self.color_input_path.set(dirname)
            # 自动设置输出目录
            self.color_output_path.set(os.path.join(dirname, "color_converted"))
            
    def select_color_output_dir(self):
        dirname = filedialog.askdirectory(title="选择输出目录")
        if dirname:
            self.color_output_path.set(dirname)
            
    def select_merge_input_dir(self):
        dirname = filedialog.askdirectory(title="选择图片目录")
        if dirname:
            self.merge_input_path.set(dirname)
            # 自动设置输出PDF文件路径
            self.merge_output_path.set(os.path.join(dirname, "merged.pdf"))
            
    def select_merge_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="保存PDF文件",
            defaultextension=".pdf",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if filename:
            self.merge_output_path.set(filename)
            
    def start_convert(self):
        pdf_path = self.pdf_path.get()
        output_dir = self.output_path.get()
        dpi = self.dpi_var.get()
        
        if not pdf_path:
            messagebox.showerror("错误", "请选择PDF文件！")
            return
            
        try:
            dpi = int(dpi) if dpi.strip() else 200
            self.pdf_status_var.set("正在转换中...")
            self.root.update()
            
            convert_pdf_to_images(pdf_path, output_dir, dpi)
            
            self.pdf_status_var.set("转换完成！")
            messagebox.showinfo("成功", "PDF转换完成！")
            
        except Exception as e:
            self.pdf_status_var.set(f"转换失败: {str(e)}")
            messagebox.showerror("错误", f"转换过程中出现错误：{str(e)}")
            
    def start_invert(self):
        input_dir = self.invert_input_path.get()
        output_dir = self.invert_output_path.get()
        
        if not input_dir:
            messagebox.showerror("错误", "请选择图片目录！")
            return
            
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        try:
            self.invert_status_var.set("正在处理图片...")
            self.root.update()
            
            # 支持的图片格式
            image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
            processed_count = 0
            
            for filename in os.listdir(input_dir):
                if filename.lower().endswith(image_extensions):
                    input_path = os.path.join(input_dir, filename)
                    output_path = os.path.join(output_dir, f"inverted_{filename}")
                    
                    # 打开图片并反转颜色
                    with Image.open(input_path) as img:
                        inverted_img = ImageOps.invert(img)
                        inverted_img.save(output_path)
                        processed_count += 1
                        
                    self.invert_status_var.set(f"已处理 {processed_count} 张图片...")
                    self.root.update()
            
            self.invert_status_var.set(f"处理完成！共处理 {processed_count} 张图片")
            messagebox.showinfo("成功", f"图片反转完成！共处理 {processed_count} 张图片")
            
        except Exception as e:
            self.invert_status_var.set(f"处理失败: {str(e)}")
            messagebox.showerror("错误", f"处理过程中出现错误：{str(e)}")
            
    def start_color_convert(self):
        input_path = self.color_input_path.get()
        output_path = self.color_output_path.get()
        
        if not input_path:
            messagebox.showerror("错误", "请选择输入目录！")
            return
            
        try:
            self.color_status_var.set("正在转换颜色...")
            self.root.update()
            
            # 处理整个目录
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            processed_count = process_directory(input_path, output_path)
            self.color_status_var.set(f"转换完成！共处理 {processed_count} 个文件")
            messagebox.showinfo("成功", f"目录中的图片颜色转换完成！共处理 {processed_count} 个文件")
                
        except Exception as e:
            self.color_status_var.set(f"转换失败: {str(e)}")
            messagebox.showerror("错误", f"转换过程中出现错误：{str(e)}")
            
    def start_merge(self):
        input_dir = self.merge_input_path.get()
        output_file = self.merge_output_path.get()
        
        if not input_dir:
            messagebox.showerror("错误", "请选择图片目录！")
            return
            
        if not output_file:
            messagebox.showerror("错误", "请选择输出PDF文件！")
            return
            
        try:
            self.merge_status_var.set("正在合并图片...")
            self.root.update()
            
            # 支持的图片格式
            image_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
            images = []
            first_image = None
            
            # 获取所有图片文件并按自然排序
            def natural_sort_key(s):
                import re
                # 将字符串中的数字转换为整数，用于自然排序
                return [int(text) if text.isdigit() else text.lower()
                        for text in re.split('([0-9]+)', s)]
            
            # 获取所有图片文件并按自然排序
            image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(image_extensions)]
            image_files.sort(key=natural_sort_key)
            
            for filename in image_files:
                input_path = os.path.join(input_dir, filename)
                img = Image.open(input_path)
                
                # 如果是PNG格式且有透明通道，转换为RGB
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                if first_image is None:
                    first_image = img
                else:
                    images.append(img)
                    
            if first_image:
                first_image.save(output_file, save_all=True, append_images=images)
                self.merge_status_var.set(f"合并完成！共处理 {len(images) + 1} 张图片")
                messagebox.showinfo("成功", f"图片合并完成！共处理 {len(images) + 1} 张图片")
            else:
                raise Exception("未找到任何图片文件")
                
        except Exception as e:
            self.merge_status_var.set(f"合并失败: {str(e)}")
            messagebox.showerror("错误", f"合并过程中出现错误：{str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = PDFConverterGUI(root)
    root.mainloop() 