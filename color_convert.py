import os
from PIL import Image
import numpy as np

def convert_colors(image_path, output_path=None):
    """
    修改图片颜色
    将白色(255,255,255)转换为(255,223,63)
    将黑色(0,0,0)转换为(31,77,120)
    
    参数:
        image_path: 输入图片路径
        output_path: 输出图片路径，如果为None则覆盖原图片
    """
    # 如果没有指定输出路径，则覆盖原图片
    if output_path is None:
        output_path = image_path
        
    try:
        # 打开图片
        img = Image.open(image_path)
        # 转换为RGB模式
        img = img.convert('RGB')
        # 转换为numpy数组
        img_array = np.array(img)
        
        # 创建白色和黑色的掩码
        white_mask = (img_array == [255, 255, 255]).all(axis=2)
        black_mask = (img_array == [0, 0, 0]).all(axis=2)
        
        # 替换颜色
        img_array[white_mask] = [255, 223, 63]  # 将白色替换为指定颜色
        img_array[black_mask] = [31, 77, 120]   # 将黑色替换为指定颜色
        
        # 转换回PIL图片
        new_img = Image.fromarray(img_array)
        # 保存图片
        new_img.save(output_path)
        print(f'颜色转换完成，已保存到: {output_path}')
        
    except Exception as e:
        print(f'处理图片时出现错误: {str(e)}')

def process_directory(input_dir, output_dir=None):
    """
    处理整个目录中的图片
    
    参数:
        input_dir: 输入目录路径
        output_dir: 输出目录路径，如果为None则在原目录创建color_converted子目录
    """
    # 如果没有指定输出目录，则在输入目录下创建color_converted子目录
    if output_dir is None:
        output_dir = os.path.join(input_dir, 'color_converted')
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f'已创建输出目录: {output_dir}')
    
    # 获取输出目录的绝对路径，用于后续过滤
    output_dir_abs = os.path.abspath(output_dir)
    
    # 递归处理目录中的所有PNG文件
    processed_count = 0
    for root, dirs, files in os.walk(input_dir):
        # 过滤掉输出目录
        if os.path.abspath(root).startswith(output_dir_abs):
            continue
            
        # 计算相对路径，用于在输出目录中创建相同的目录结构
        rel_path = os.path.relpath(root, input_dir)
        
        # 创建对应的输出子目录
        if rel_path != '.':
            current_output_dir = os.path.join(output_dir, rel_path)
            if not os.path.exists(current_output_dir):
                os.makedirs(current_output_dir)
        else:
            current_output_dir = output_dir
        
        # 处理当前目录中的所有PNG文件
        for file in files:
            if file.lower().endswith('.png'):
                input_path = os.path.join(root, file)
                output_path = os.path.join(current_output_dir, file)
                convert_colors(input_path, output_path)
                processed_count += 1
                print(f'已处理: {processed_count} 个文件')
    
    print(f'处理完成！共处理 {processed_count} 个文件')
    return processed_count

if __name__ == '__main__':
    # 示例使用
    choice = input('请选择处理模式 (1: 单个文件, 2: 整个目录): ')
    
    if choice == '1':
        image_path = input('请输入图片路径: ')
        output_path = input('请输入输出路径(直接回车则覆盖原图片): ')
        if not output_path.strip():
            output_path = None
        convert_colors(image_path, output_path)
    elif choice == '2':
        input_dir = input('请输入图片目录路径: ')
        output_dir = input('请输入输出目录路径(直接回车则在原目录创建color_converted子目录): ')
        if not output_dir.strip():
            output_dir = None
        process_directory(input_dir, output_dir)
    else:
        print('无效的选择') 