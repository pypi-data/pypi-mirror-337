# 标准库导入
import argparse
import sys
import os
import json
import xml.etree.ElementTree as ET
import time
import asyncio
from typing import Optional, List, Dict, Any

# 第三方库导入
try:
    import requests
    import aiohttp
    from openai import OpenAI, AsyncOpenAI
    import pandas as pd
    import openpyxl
    from openpyxl.styles import Alignment, Font
    from openpyxl.utils import get_column_letter
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
except ImportError as e:
    print(f"错误：缺少必要的依赖包 - {str(e)}")
    print("请使用以下命令安装所需依赖：")
    print("pip install requests aiohttp openai pandas openpyxl reportlab")
    sys.exit(1)

# 导入本地模块
try:
    from literature_analysis.search import pubmed_search_fetch
    from literature_analysis.analyze import analyze_literature_connections
    from literature_analysis.process import process_results
    from literature_analysis.analyze_final import analyze_results
    from literature_analysis.visualize import create_pdf_report
except ImportError as e:
    print(f"错误：无法导入本地模块 - {str(e)}")
    print("请确保所有必要的脚本文件都在正确的位置")
    sys.exit(1)

def check_dependencies():
    """检查必要的依赖是否已安装"""
    required_packages = {
        'requests': requests,
        'aiohttp': aiohttp,
        'openai': OpenAI,
        'pandas': pd,
        'openpyxl': openpyxl,
        'reportlab': SimpleDocTemplate
    }
    
    missing_packages = []
    for package, module in required_packages.items():
        if module is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("缺少必要的依赖包，请安装以下包：")
        print("pip install " + " ".join(missing_packages))
        sys.exit(1)

class LiteratureProcessor:
    def __init__(self):
        self.search_result: Optional[str] = None      # search.py的输出
        self.qwen_result: Optional[str] = None        # analyze.py的输出
        self.processed_result: Optional[str] = None    # process.py的输出
        self.analysis_result: Optional[str] = None     # analyze_final.py的输出

    def search(self, ncbi_key: str, term: str, db: str = 'pubmed', retmax: int = 20):
        """执行PubMed检索"""
        try:
            self.search_result = 'result1.json'
            result = pubmed_search_fetch(ncbi_key, term, db, retmax)
            
            with open(self.search_result, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"检索完成，结果保存至 {self.search_result}")
            return True
        except Exception as e:
            print(f"检索出错: {str(e)}")
            return False

    def analyze_with_qwen(self, dashscope_key: str, input_file: str):
        """使用qwen-turbo分析"""
        try:
            self.qwen_result = input_file.rsplit('.', 1)[0] + '_analysis.json'
            analyze_literature_connections(input_file, dashscope_key)
            
            print(f"qwen-turbo分析完成，结果保存至 {self.qwen_result}")
            return True
        except Exception as e:
            print(f"qwen-turbo分析出错: {str(e)}")
            return False

    def process_result(self, input_file: str):
        """处理分析结果"""
        try:
            self.processed_result = input_file.rsplit('.', 1)[0] + '_processed.json'
            process_results(input_file)
            
            print(f"结果处理完成，输出保存至 {self.processed_result}")
            return True
        except Exception as e:
            print(f"处理结果出错: {str(e)}")
            return False

    def analyze_final(self, dashscope_key: str, input_file: str):
        """分析结果"""
        try:
            self.analysis_result = input_file.rsplit('.', 1)[0] + '_final.json'
            analyze_results(input_file, dashscope_key)
            
            print(f"结果分析完成，输出保存至 {self.analysis_result}")
            return True
        except Exception as e:
            print(f"分析结果出错: {str(e)}")
            return False

    def visualize(self, input_file: str):
        """可视化结果"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            create_pdf_report(data)
            print("可视化完成，PDF报告已生成")
            return True
        except Exception as e:
            print(f"可视化出错: {str(e)}")
            return False

def setup_argparse():
    """设置命令行参数解析"""
    parser = argparse.ArgumentParser(description='文献分析工具集')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # search.py - 检索命令
    parser_search = subparsers.add_parser('search', help='执行PubMed检索')
    parser_search.add_argument('--ncbi-key', required=True, help='NCBI API密钥')
    parser_search.add_argument('--term', required=True, help='搜索词')
    parser_search.add_argument('--db', default='pubmed', help='数据库名称')
    parser_search.add_argument('--retmax', type=int, default=20, help='返回结果数量')
    
    # analyze.py - qwen-turbo分析命令
    parser_qwen = subparsers.add_parser('analyze', help='使用qwen-turbo分析')
    parser_qwen.add_argument('--dashscope-key', required=True, help='DashScope API密钥')
    parser_qwen.add_argument('input_file', help='输入文件路径')
    
    # process.py - 处理结果命令
    parser_process = subparsers.add_parser('process', help='处理分析结果')
    parser_process.add_argument('input_file', help='输入文件路径')
    
    # analyze_final.py - 分析结果命令
    parser_analyze = subparsers.add_parser('analyze-final', help='分析结果')
    parser_analyze.add_argument('--dashscope-key', required=True, help='DashScope API密钥')
    parser_analyze.add_argument('input_file', help='输入文件路径')
    
    # visualize.py - 可视化命令
    parser_visualize = subparsers.add_parser('visualize', help='可视化结果')
    parser_visualize.add_argument('input_file', help='输入文件路径')
    
    # 执行完整流程命令
    parser_all = subparsers.add_parser('run-all', help='执行完整分析流程')
    parser_all.add_argument('--ncbi-key', required=True, help='NCBI API密钥')
    parser_all.add_argument('--dashscope-key', required=True, help='DashScope API密钥')
    parser_all.add_argument('--term', required=True, help='搜索词')
    parser_all.add_argument('--db', default='pubmed', help='数据库名称')
    parser_all.add_argument('--retmax', type=int, default=20, help='返回结果数量')
    
    return parser

def main():
    # 检查依赖
    check_dependencies()
    
    # 设置参数解析器
    parser = setup_argparse()
    args = parser.parse_args()
    
    # 创建处理器实例
    processor = LiteratureProcessor()
    
    try:
        if args.command == 'search':
            processor.search(args.ncbi_key, args.term, args.db, args.retmax)
        
        elif args.command == 'analyze':
            processor.analyze_with_qwen(args.dashscope_key, args.input_file)
        
        elif args.command == 'process':
            processor.process_result(args.input_file)
        
        elif args.command == 'analyze-final':
            processor.analyze_final(args.dashscope_key, args.input_file)
        
        elif args.command == 'visualize':
            processor.visualize(args.input_file)
        
        elif args.command == 'run-all':
            # 执行完整流程
            if processor.search(args.ncbi_key, args.term, args.db, args.retmax):
                if processor.analyze_with_qwen(args.dashscope_key, processor.search_result):
                    if processor.process_result(processor.qwen_result):
                        if processor.analyze_final(args.dashscope_key, processor.qwen_result):
                            processor.visualize(processor.analysis_result)
        
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"执行过程中出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()