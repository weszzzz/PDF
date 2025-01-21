from pdf2image import convert_from_path
import os

def convert_pdf_to_images(pdf_path, output_base_dir=None, dpi=200):
    """
    将PDF文件转换为图片
    
    参数:
        pdf_path: PDF文件路径
        output_base_dir: 输出基础目录，如果为None则使用PDF所在目录
        dpi: 图片分辨率，默认200
    """
    # 获取PDF文件名（不含扩展名）
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # 如果没有指定输出基础目录，则使用PDF所在目录
    if output_base_dir is None:
        output_base_dir = os.path.dirname(pdf_path)
    
    # 在输出基础目录下创建以PDF文件名命名的子目录
    output_dir = os.path.join(output_base_dir, pdf_name)
    
    # 创建输出目录（如果不存在）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f'已创建输出目录: {output_dir}')
    
    try:
        # 指定 poppler 路径
        poppler_path = r"C:\Program Files\poppler\poppler-24.08.0\Library\bin"
        # 将PDF转换为图片
        images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
        
        # 保存每一页为单独的图片
        for i, image in enumerate(images):
            image_path = os.path.join(output_dir, f'page_{i+1}.png')
            image.save(image_path, 'PNG')
            print(f'已保存第 {i+1} 页到: {image_path}')
            
        print(f'转换完成！共转换 {len(images)} 页')
        print(f'所有图片已保存到目录: {output_dir}')
        
    except Exception as e:
        print(f'转换过程中出现错误: {str(e)}')

if __name__ == '__main__':
    # 示例使用
    pdf_path = input('请输入PDF文件路径: ')
    output_base_dir = input('请输入输出基础目录路径(直接回车则使用PDF所在目录): ')
    dpi = input('请输入图片分辨率(默认200，直接回车跳过): ')
    
    # 处理输出目录
    if not output_base_dir.strip():
        output_base_dir = None
        
    # 如果用户输入了DPI，则使用用户输入的值
    if dpi.strip():
        convert_pdf_to_images(pdf_path, output_base_dir, int(dpi))
    else:
        convert_pdf_to_images(pdf_path, output_base_dir) 