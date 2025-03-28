import json
import argparse
import os
import asyncio
import aiohttp
from openai import AsyncOpenAI
from typing import List, Dict, Any

async def process_part_with_llm(part_content: List[Dict], client: AsyncOpenAI, part_key: str, max_retries: int = 3) -> List[Dict]:
    """异步处理一个part中的所有文章，包含重试机制"""
    print(f"\n开始处理 {part_key}，包含 {len(part_content)} 篇文章...")
    
    for retry in range(max_retries):
        try:
            # 准备所有文章的信息
            articles_info = []
            for idx, article in enumerate(part_content, 1):
                article_info = {
                    "id": idx,
                    "title": article["title"],
                    "abstract": article["abstract"],
                    "authors": {
                        "first": article["first_author"],
                        "last": article["last_author"]
                    },
                    "publication": {
                        "year": article["year"],
                        "journal": article["journal"]
                    }
                }
                articles_info.append(article_info)
            
            # 构建提示信息
            articles_text = ""
            for article in articles_info:
                articles_text += f"\n文章{article['id']}:\n标题：{article['title']}\n摘要：{article['abstract']}\n"

            print(f"{part_key} 正在发送请求到API...")

            messages = [
                {
                    "role": "system",
                    "content": "你是一名资深的生物医学家"
                },
                {
                    "role": "user",
                    "content": f"""请分析以下{len(articles_info)}篇文献，对每篇文献提取关键结论、研究的基因和通路、研究模型。

{articles_text}

请以全英文JSON格式输出，格式如下：
{{
    "articles": [
        {{
            "id": 文章编号,
            "conclusion": "研究的主要结论",
            "genes_pathways": ["相关基因", "相关通路"],
            "research_model": "使用的研究模型"
        }},
        // ... 其他文章
    ]
}}
"""
                }
            ]

            # 异步调用API，增加超时时间
            try:
                completion = await asyncio.wait_for(
                    client.chat.completions.create(
                        model="qwen-turbo",
                        messages=messages,
                        temperature=0.1,
                        max_tokens=8192
                    ),
                    timeout=180
                )
                
                print(f"{part_key} 收到API响应...")
                response_text = completion.choices[0].message.content

            except asyncio.TimeoutError:
                print(f"{part_key} 请求超时（{180}秒）")
                if retry < max_retries - 1:
                    print(f"{part_key} 将在5秒后进行第 {retry + 2}/{max_retries} 次重试")
                    await asyncio.sleep(5)
                    continue
                return []

            # 解析JSON响应
            try:
                # 打印原始响应用于调试
                print(f"{part_key} 原始响应: {response_text[:200]}...")
                
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    llm_result = json.loads(json_str)
                    
                    if 'articles' not in llm_result:
                        print(f"{part_key} 响应中缺少 'articles' 字段")
                        raise json.JSONDecodeError("Missing 'articles' field", json_str, 0)
                else:
                    raise json.JSONDecodeError("No JSON found in response", response_text, 0)

                # 合并结果
                final_results = []
                for article_info in articles_info:
                    article_id = article_info['id']
                    llm_article = next((a for a in llm_result['articles'] if a['id'] == article_id), None)
                    if llm_article:
                        final_result = {
                            "title": article_info["title"],
                            "authors": article_info["authors"],
                            "publication": article_info["publication"],
                            "conclusion": llm_article.get("conclusion", ""),
                            "genes_pathways": llm_article.get("genes_pathways", []),
                            "research_model": llm_article.get("research_model", "")
                        }
                        final_results.append(final_result)
                    else:
                        print(f"{part_key} 警告: 未找到文章ID {article_id} 的分析结果")

                print(f"成功处理 {part_key} 中的 {len(final_results)}/{len(articles_info)} 篇文章")
                return final_results

            except json.JSONDecodeError as e:
                print(f"{part_key} JSON解析失败: {str(e)}")
                print(f"{part_key} 完整响应: {response_text}")
                if retry < max_retries - 1:
                    print(f"{part_key} 将在5秒后进行第 {retry + 2}/{max_retries} 次重试")
                    await asyncio.sleep(5)
                    continue
                return []
                
        except Exception as e:
            print(f"{part_key} 处理错误: {str(e)}")
            print(f"{part_key} 错误类型: {type(e).__name__}")
            if retry < max_retries - 1:
                print(f"{part_key} 将在5秒后进行第 {retry + 2}/{max_retries} 次重试")
                await asyncio.sleep(5)
                continue
            return []

    print(f"{part_key} 处理完成")
    return []

async def process_all_parts(data: Dict, client: AsyncOpenAI) -> List[Dict]:
    """并行处理所有parts，限制并发数"""
    # 创建信号量限制并发数
    semaphore = asyncio.Semaphore(3)  # 限制最多3个并发请求

    async def process_with_semaphore(part_content, part_key):
        async with semaphore:
            return await process_part_with_llm(part_content, client, part_key)

    tasks = []
    for part_key, part_value in data['result'].items():
        try:
            part_content = json.loads(part_value)
            if isinstance(part_content, list):
                print(f"创建任务: {part_key} ({len(part_content)} 篇文章)")
                task = asyncio.create_task(process_with_semaphore(part_content, part_key))
                tasks.append(task)
            else:
                print(f"警告: {part_key} 的内容不是列表格式")
        except json.JSONDecodeError as e:
            print(f"警告: {part_key} 内容解析失败: {str(e)}")
            continue

    # 并行执行所有任务
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 合并所有结果
    all_results = []
    for result in results:
        if isinstance(result, list):
            all_results.extend(result)
        else:
            print(f"警告: 任务执行出错 - {result}")

    return all_results

async def main_async():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='并行处理PubMed搜索结果并使用qwen-turbo模型进行分析')
    parser.add_argument('input_file', help='PubMed搜索结果文件路径')
    parser.add_argument('--api-key', required=True, help='DashScope API密钥')
    
    args = parser.parse_args()
    
    # 初始化异步OpenAI客户端
    client = AsyncOpenAI(
        api_key=args.api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    try:
        # 读取输入文件
        with open(args.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'result' not in data:
            raise ValueError("输入文件格式错误：缺少'result'字段")

        print("开始并行处理所有parts...")
        all_results = await process_all_parts(data, client)

        # 保存结果
        output = {
            "total_count": len(all_results),
            "articles": all_results
        }

        output_file = 'processed_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"处理完成，共处理 {len(all_results)} 篇文献")
        print(f"结果已保存到 {output_file}")

    except Exception as e:
        print(f"处理失败: {str(e)}")

def main():
    """入口函数"""
    asyncio.run(main_async())

if __name__ == "__main__":
    main()