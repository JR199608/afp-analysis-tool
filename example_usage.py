from diagnosis_analyzer import DiagnosisAnalyzer
import pandas as pd
import time
import os

def process_excel_data(input_file: str, diagnosis_column: str = '出院诊断'):
    # 创建分析器实例
    analyzer = DiagnosisAnalyzer()
    
    print(f"开始读取数据文件: {input_file}")
    start_time = time.time()
    
    try:
        # 读取Excel文件
        df = pd.read_excel(input_file)
        
        # 打印列名，帮助调试
        print("\n文件包含的列名：")
        print(df.columns.tolist())
        
        # 确保诊断列存在
        if diagnosis_column not in df.columns:
            raise ValueError(f"未找到列 '{diagnosis_column}'，请检查Excel文件")
        
        # 获取诊断数据
        diagnoses = df[diagnosis_column].tolist()
        total_records = len(diagnoses)
        print(f"\n成功读取 {total_records} 条记录")
        
        # 分批处理数据
        batch_size = 1000
        results = []
        
        for i in range(0, total_records, batch_size):
            batch = diagnoses[i:i + batch_size]
            batch_results = analyzer.analyze_batch(batch)
            results.append(batch_results)
            print(f"已处理 {min(i + batch_size, total_records)}/{total_records} 条记录")
        
        # 合并所有结果
        results_df = pd.concat(results, ignore_index=True)
        
        # 合并原始数据和分析结果
        df['甲胎蛋白测定是否合理'] = results_df['是否合理']
        df['判断依据'] = results_df['判断依据']
        
        # 打印结果统计
        print("\n=== 统计信息 ===")
        total_cases = len(results_df)
        reasonable_cases = len(results_df[results_df['是否合理'] == '是'])
        print(f"总病例数：{total_cases}")
        print(f"合理病例数：{reasonable_cases}")
        print(f"不合理病例数：{total_cases - reasonable_cases}")
        print(f"合理比例：{(reasonable_cases/total_cases*100):.2f}%")
        
        # 打印一些示例结果
        print("\n=== 部分分析结果示例 ===")
        sample_size = min(5, total_cases)
        print("\n合理案例示例：")
        reasonable_samples = df[df['甲胎蛋白测定是否合理'] == '是'].head(sample_size)
        for _, row in reasonable_samples.iterrows():
            print(f"诊断：{row['出院诊断']}")
            print(f"判断依据：{row['判断依据']}\n")
            
        print("\n不合理案例示例：")
        unreasonable_samples = df[df['甲胎蛋白测定是否合理'] == '否'].head(sample_size)
        for _, row in unreasonable_samples.iterrows():
            print(f"诊断：{row['出院诊断']}")
            print(f"判断依据：{row['判断依据']}\n")
        
        # 保存结果到Excel
        output_file = 'afp_analysis_result.xlsx'
        # 如果文件已存在，先删除
        if os.path.exists(output_file):
            os.remove(output_file)
        df.to_excel(output_file, index=False)
        print(f"\n结果已保存到 '{output_file}'")
        
        # 打印处理时间
        end_time = time.time()
        processing_time = end_time - start_time
        print(f"\n总处理时间：{processing_time:.2f} 秒")
        print(f"平均每条记录处理时间：{processing_time/total_records:.4f} 秒")
        
    except Exception as e:
        print(f"处理过程中出现错误：{str(e)}")
        print("错误详细信息：")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    # 使用工作簿4.xlsx
    input_file = "工作簿4.xlsx"
    process_excel_data(input_file) 