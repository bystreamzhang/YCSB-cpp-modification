#!/bin/bash

#DATASETS=("h1_nci")
DATASETS=("h1_nci" "m1_webster" "l1_osdb" "m2_xml"  "l2_ooffice")
#DATASETS=("h1_nci"  "m1_webster" "l1_osdb" "h2_hgdp" "m2_xml"  "l2_ooffice")
#WORKLOADS=("workloadd" "workloade" "workloadf")
#WORKLOADS=("workloada")
#ORKLOADS=("workloadc")
#WORKLOADS=("workloadd") # 有run阶段的insert操作
WORKLOADS=("workloada" "workloadb" "workloadc" "workloadd" "workloade" "workloadf")
#WORKLOADS=("workloada" "workloadb" "workloadc")

USR_PATH="/home/zwl"
DATASETS_PATH="/home/zwl/datasets_ycsb"
ZNS_DEV="nvme0n1"
ZNS_PATH=/dev/$ZNS_DEV

rm output.txt
exec > >(tee -a output.txt) 2>&1

for workload in "${WORKLOADS[@]}"; do
    for dataset in "${DATASETS[@]}"; do
    echo ""
    echo "============ Prepare Phase ============="
    echo "Testing : ${workload}, ${dataset}"

    # 检查数据文件是否存在
    if [ ! -f "${DATASETS_PATH}/${dataset}.dat" ]; then
        echo "Warning: ${DATASETS_PATH}/${dataset}.dat does not exist. Skipping..."
        echo "========================================"
        echo ""
        continue  # 文件不存在时跳过当前循环，进行下一个测试
    fi

    # 强制卸载设备（避免残留挂载）
    sudo umount $ZNS_PATH 2>/dev/null || true

    # 重置所有Zone为初始状态
    sudo blkzone reset $ZNS_PATH

    # zbd report $ZNS_PATH

    rm -rf ${USR_PATH}/ycsbtest

    echo deadline > /sys/class/block/nvme0n1/queue/scheduler

    ${USR_PATH}/rocksdb/plugin/zenfs/util/zenfs mkfs --zbd=$ZNS_DEV --aux_path=${USR_PATH}/ycsbtest

    echo "============== Load Phase =============="

    ./ycsb -load -db rocksdb -P workloads/${workload} -P rocksdb/rocksdb.properties -s \
    -p rocksdb.use_direct_io_for_flush_compaction=true \
    -p rocksdb.compression=no \
    -p rocksdb.datapath=${DATASETS_PATH}/${dataset}.dat

    echo "============== Run Phase ==============="

    ./ycsb -run -db rocksdb -P workloads/${workload} -P rocksdb/rocksdb.properties -s \
    -p rocksdb.use_direct_io_for_flush_compaction=true \
    -p rocksdb.compression=no \
    -p rocksdb.datapath=${DATASETS_PATH}/${dataset}.dat

    echo "========================================"
    echo ""
    done
done