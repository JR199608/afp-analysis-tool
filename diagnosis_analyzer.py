import pandas as pd
from typing import List, Dict
from collections import defaultdict

class DiagnosisAnalyzer:
    def __init__(self):
        # 定义需要进行甲胎蛋白测定的疾病列表及其详细说明
        self.afp_related_diseases = {
            '肝脏疾病': {
                'diseases': ['肝癌', '原发性肝癌', '肝细胞癌', '肝硬化', '慢性肝炎', '病毒性肝炎', '重型肝炎'],
                'reason': '甲胎蛋白(AFP)是肝细胞癌的重要肿瘤标志物，对肝癌的诊断、疗效观察和预后判断有重要价值。在慢性肝病患者中，AFP水平升高提示肝癌风险增加'
            },
            '生殖系统肿瘤': {
                'diseases': ['睾丸癌', '卵巢癌', '生殖细胞瘤', '精原细胞瘤'],
                'reason': 'AFP是生殖细胞肿瘤的特异性标志物之一，可用于诊断和监测治疗效果。AFP水平与肿瘤负荷相关，可反映疾病进展和预后'
            },
            '胚胎性肿瘤': {
                'diseases': ['畸胎瘤', '胚胎性癌症', '卵黄囊瘤'],
                'reason': '胚胎性肿瘤常伴有AFP升高，其水平变化可反映肿瘤的生长情况和治疗效果。AFP是评估治疗反应和复发监测的重要指标'
            },
            '消化道肿瘤': {
                'diseases': ['胃癌', '胰腺癌', '结直肠癌'],
                'reason': '部分消化道肿瘤可出现AFP升高，可作为辅助诊断指标。同时需要排除肝转移的可能'
            },
            '妊娠相关': {
                'diseases': ['妊娠', '孕期检查', '胎儿筛查'],
                'reason': 'AFP是产前筛查的重要指标，可用于评估神经管畸形和染色体异常的风险。异常AFP水平提示需要进一步检查'
            },
            '其他可能相关': {
                'diseases': ['转移性肝癌', '肝占位', '腹腔肿瘤'],
                'reason': '当发现肝脏占位性病变或腹腔肿瘤时，AFP可协助鉴别诊断，特别是在判断肿瘤来源和性质方面有重要价值'
            }
        }
        
        # 创建疾病到类别的映射字典，提高查找效率
        self.disease_to_category = {}
        for category, info in self.afp_related_diseases.items():
            for disease in info['diseases']:
                self.disease_to_category[disease] = category
        
    def analyze_diagnosis(self, diagnosis: str) -> Dict:
        """
        分析单个诊断是否需要甲胎蛋白测定
        """
        result = {
            '是否合理': False,
            '原因': []
        }
        
        # 使用映射字典快速查找
        for disease, category in self.disease_to_category.items():
            if disease in diagnosis:
                result['是否合理'] = True
                detailed_reason = self.afp_related_diseases[category]['reason']
                result['原因'].append(f"诊断为{category}相关疾病（{diagnosis}）。{detailed_reason}")
                break
                
        if not result['是否合理']:
            result['原因'].append("当前诊断不属于甲胎蛋白测定的常规指征。AFP检测主要用于：1)肝细胞癌的筛查和监测；2)生殖细胞肿瘤的诊断和随访；3)胚胎性肿瘤的评估；4)妊娠期胎儿畸形筛查。当前诊断不符合上述情况。")
            
        return result

    def analyze_batch(self, diagnoses: List[str]) -> pd.DataFrame:
        """
        批量分析诊断数据
        """
        results = []
        for diagnosis in diagnoses:
            analysis = self.analyze_diagnosis(diagnosis)
            results.append({
                '出院诊断': diagnosis,
                '是否合理': '是' if analysis['是否合理'] else '否',
                '判断依据': '；'.join(analysis['原因'])
            })
        
        return pd.DataFrame(results)

def main():
    # 示例使用
    analyzer = DiagnosisAnalyzer()
    
    # 示例数据
    diagnoses = [
        "原发性肝癌",
        "高血压",
        "病毒性肝炎",
        "糖尿病",
        "胃癌"
    ]
    
    # 分析结果
    results_df = analyzer.analyze_batch(diagnoses)
    
    # 打印结果
    print("\n分析结果：")
    print(results_df.to_string(index=False))
    
    # 统计信息
    total_cases = len(results_df)
    reasonable_cases = len(results_df[results_df['是否合理'] == '是'])
    print(f"\n统计信息：")
    print(f"总病例数：{total_cases}")
    print(f"合理病例数：{reasonable_cases}")
    print(f"不合理病例数：{total_cases - reasonable_cases}")

if __name__ == "__main__":
    main() 