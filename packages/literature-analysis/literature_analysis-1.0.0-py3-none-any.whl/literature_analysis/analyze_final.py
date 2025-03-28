import json
import sys
import argparse
from openai import OpenAI

def extract_json_from_text(text):
    """从文本中提取JSON内容"""
    try:
        # 查找第一个 { 和最后一个 } 的位置
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            json_str = text[start:end]
            return json.loads(json_str)
    except:
        pass
    return None

def analyze_literature_connections(json_file, api_key):
    """使用qwen-turbo分析文献关联"""
    try:
        # 读取JSON文件
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 创建输出文件名
        output_file = json_file.rsplit('.', 1)[0] + '_analysis.json'
        
        # 准备API调用
        client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        # 构建提示信息
        messages = [
            {
                "role": "system",
                "content": "你是一位资深生物医学科学家，请以全英文JSON格式输出分析结果。"
            },
            {
                "role": "user",
                "content": f"""请通读所有的文献信息，
                1. 把所有的文献分类为肿瘤，其他疾病，发育，免疫，转录调控，染色质调控，代谢，临床研究8个主题，进行匹配
                2. 将所有文献根据结论、模型和基因和通路，三个关键字段找出相互印证或矛盾的研究发现evidence_network
                3. 对所有文献进行全面总结，包括研究主题分布、主要发现、研究进展和未来方向

                请严格按照以下全英文JSON格式输出：
                {{
                    "research_groups": [
                        {{
                            "theme": "研究主题",
                            "papers": [
                                {{
                                    "title": "文章标题",
                                    "authors": "作者列表",
                                    "year": "年份",
                                    "journal": "期刊名称",
                                    "key_finding": "主要发现",
                                    "detailed_mechanism": "详细分子机制"
                                }}
                            ]
                        }}
                    ],
                    "evidence_network": [
                        {{
                            "type": "supporting/contradicting",
                            "papers": ["文章1标题", "文章2标题", "文章3标题"...],
                            "model_type": "使用的研究模型",
                            "mechanism": "涉及的分子机制",
                            "description": "详细的关系描述",
                            "implications": "研究意义和启示"
                        }}
                    ],
                    "overall_summary": {{
                        "research_distribution": "各研究主题的分布情况",
                        "major_findings": "主要研究发现概述",
                        "research_progress": "研究进展总结",
                        "future_directions": "未来研究方向建议",
                        "comprehensive_analysis": "全面分析总结"
                    }}
                }}

                文献内容：
                {json.dumps(data, ensure_ascii=False, indent=2)}
                """
            }
        ]

        print("正在调用API分析文献...")

        # 调用API
        completion = client.chat.completions.create(
            model="qwen2.5-7b-instruct-1m",
            messages=messages,
            temperature=0.1,
        )

        # 获取响应
        response_text = completion.choices[0].message.content
        print("已收到API响应，正在处理...")

        # 尝试解析响应
        analysis_result = extract_json_from_text(response_text)
        if analysis_result is None:
            print("无法解析API响应为JSON格式，原始响应：")
            print("-" * 80)
            print(response_text)
            print("-" * 80)
            raise ValueError("API响应格式错误")

        # 保存分析结果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        print(f"分析完成，结果已保存到 {output_file}")
        
        # 打印简要分析结果
        print("\n分析结果摘要：")
        print(f"找到 {len(analysis_result.get('research_groups', []))} 个研究主题组")
        print(f"找到 {len(analysis_result.get('evidence_network', []))} 个证据关系网络")
        
        # 打印总体分析
        if 'overall_summary' in analysis_result:
            print("\n总体分析：")
            print("-" * 80)
            print("\n研究主题分布：")
            print(analysis_result['overall_summary']['research_distribution'])
            print("\n主要研究发现：")
            print(analysis_result['overall_summary']['major_findings'])
            print("\n研究进展：")
            print(analysis_result['overall_summary']['research_progress'])
            print("\n未来研究方向：")
            print(analysis_result['overall_summary']['future_directions'])
            print("\n综合分析：")
            print(analysis_result['overall_summary']['comprehensive_analysis'])
            print("-" * 80)

    except Exception as e:
        print(f"处理过程中出错: {str(e)}")
        if 'response_text' in locals():
            print("\n原始API响应：")
            print("-" * 80)
            print(response_text)
            print("-" * 80)

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='使用qwen-turbo分析文献关联')
    parser.add_argument('input_file', help='输入的JSON文件路径')
    parser.add_argument('--api-key', required=True, help='DashScope API密钥')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 分析文献
    analyze_literature_connections(args.input_file, args.api_key)

if __name__ == "__main__":
    main()