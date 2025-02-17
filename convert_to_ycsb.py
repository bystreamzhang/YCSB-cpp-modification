import os
import argparse
import uuid

def convert_to_ycsb(input_file, output_file, record_size=1024):
    """
    将任意数据文件转换为 YCSB 格式，每个记录大小为 record_size 字节。
    """
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        content = f_in.read().replace("\n", " ").replace("\r", " ")  # 移除换行符
        record_id = 0
        for i in range(0, len(content), record_size):
            data = content[i:i + record_size]
            key = f"key_{record_id}"  # 生成唯一 key
            f_out.write(f"{key} {data}\n")  # 按行写入 YCSB 记录
            record_id += 1

    print(f"转换完成，输出文件: {output_file}")

if __name__ == "__main__":
    '''使用示例：
    python3 convert_to_ycsb.py --input /home/zwl/dataset/nci --output /home/zwl/datasets_ycsb/h1_nci.dat
    python3 convert_to_ycsb.py --input /home/zwl/dataset/xml --output /home/zwl/datasets_ycsb/m2_xml.dat
    '''
    parser = argparse.ArgumentParser(description="Convert arbitrary data file to YCSB format")
    parser.add_argument("--input", type=str, required=True, help="Input data file")
    parser.add_argument("--output", type=str, required=True, help="Output YCSB file")
    parser.add_argument("--record_size", type=int, default=1024, help="Size of each YCSB record in bytes")

    args = parser.parse_args()
    convert_to_ycsb(args.input, args.output, args.record_size)
