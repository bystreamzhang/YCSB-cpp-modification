import os
import argparse
import uuid

from struct import pack, unpack

def convert_to_ycsb(input_file, output_file, fields_size=100, fields_num=10):
    """
    将任意数据文件转换为 YCSB 格式，每个记录大小为 value_size 字节, 具体来说是 fields_num 个 fields_size 字节
    如果是1024B, 其中24B会是key, 实际value就是1000B, 10个field, 分别是100B
    """
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f_in, open(output_file, 'wb') as f_out:
        content = f_in.read().replace("\n", " ").replace("\r", " ")  # 移除换行符

        for i in range(0, len(content), fields_size * fields_num):
            data = bytearray()
            for j in range(0, fields_num):
                len_name = 6 # 先不考虑len大于10即有多位的情况了
                data.extend(pack('I', len_name))
                field_name = "field" + str(j)
                data.extend(field_name.encode('utf-8'))
                len_field = fields_size
                data.extend(pack('I', len_field))
                field_value = content[i + j * 100: i + j * 100 + 100]
                data.extend(field_value.encode('utf-8'))
            #print(data)
            #print("data:" + str(data))
            f_out.write(data)  # 写入 YCSB 记录 data, 不换行

    print(f"转换完成，输出文件: {output_file}")

if __name__ == "__main__":
    '''使用示例：
    python3 convert_to_ycsb.py --input /home/zwl/dataset/nci --output /home/zwl/datasets_ycsb/h1_nci.dat
    python3 convert_to_ycsb.py --input /home/zwl/dataset/webster --output /home/zwl/datasets_ycsb/m1_webster.dat
    python3 convert_to_ycsb.py --input /home/zwl/dataset/xml --output /home/zwl/datasets_ycsb/m2_xml.dat
    python3 convert_to_ycsb.py --input /home/zwl/dataset/osdb --output /home/zwl/datasets_ycsb/l1_osdb.dat
    python3 convert_to_ycsb.py --input /home/zwl/dataset/ooffice --output /home/zwl/datasets_ycsb/l2_ooffice.dat
    '''
    parser = argparse.ArgumentParser(description="Convert arbitrary data file to YCSB format")
    parser.add_argument("--input", type=str, required=True, help="Input data file")
    parser.add_argument("--output", type=str, required=True, help="Output YCSB file")
    parser.add_argument("--fields_size", type=int, default=100, help="Size of fields in bytes")
    parser.add_argument("--fields_num", type=int, default=10, help="Number of fields")

    args = parser.parse_args()
    convert_to_ycsb(args.input, args.output, args.fields_size, args.fields_num)
