import requests
import json
import xml.etree.ElementTree as ET
import time
import argparse

def count_chars(text):
    """计算文本的字符数（不计算空格和标点）"""
    # 移除空格和常见标点符号
    return len([char for char in text if char.strip() and not char in ',.;!?()[]{}'])

def split_articles(articles, chunk_size=5000):
    """按照字符数分割文章列表"""
    chunks = []
    current_chunk = []
    current_char_count = 0
    
    for article in articles:
        # 计算当前文章的字符数
        article_char_count = 0
        
        # 计算标题的字符数
        if article.get('title'):
            article_char_count += count_chars(article['title'])
            
        # 计算摘要的字符数
        if article.get('abstract'):
            article_char_count += count_chars(article['abstract'])
            
        # 计算其他文本字段的字符数
        for field in ['journal', 'first_author', 'last_author', 'year']:
            if article.get(field):
                article_char_count += count_chars(str(article[field]))
        
        # 如果当前块加上新文章会超出大小限制，开始新的块
        if current_char_count + article_char_count > chunk_size and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_char_count = 0
        
        current_chunk.append(article)
        current_char_count += article_char_count
    
    # 添加最后一个块
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def process_xml(xml_content):
    """处理XML内容，提取所需信息"""
    try:
        # 解析XML
        root = ET.fromstring(xml_content)
        
        # 存储所有文献信息
        articles = []
        for article in root.findall('.//PubmedArticle'):
            # 提取标题
            title = article.find('.//ArticleTitle')
            title_text = title.text if title is not None else ''
            
            # 提取发表年份
            pub_date = article.find('.//PubDate/Year')
            year = pub_date.text if pub_date is not None else ''
            
            # 提取期刊信息
            journal = article.find('.//Journal/Title')
            journal_text = journal.text if journal is not None else ''
            
            # 提取作者
            authors = article.findall('.//Author')
            first_author = ''
            last_author = ''
            if authors:
                # 第一作者
                first = authors[0]
                first_last_name = first.find('LastName')
                first_fore_name = first.find('ForeName')
                if first_last_name is not None and first_fore_name is not None:
                    first_author = f"{first_last_name.text} {first_fore_name.text}"
                
                # 最后作者
                last = authors[-1]
                last_last_name = last.find('LastName')
                last_fore_name = last.find('ForeName')
                if last_last_name is not None and last_fore_name is not None:
                    last_author = f"{last_last_name.text} {last_fore_name.text}"
            
            # 提取摘要
            abstract_texts = article.findall('.//AbstractText')
            abstract = ' '.join([text.text for text in abstract_texts if text.text]) if abstract_texts else ''
            
            # 创建文献对象
            article_info = {
                "title": title_text,
                "year": year,
                "journal": journal_text,
                "first_author": first_author,
                "last_author": last_author,
                "abstract": abstract
            }
            articles.append(article_info)
        
        if not articles:
            return {"error": "未找到文献信息"}
        
        # 将文献列表分组
        chunks = split_articles(articles)
        
        # 创建最终的输出格式
        output = {}
        for i, chunk in enumerate(chunks, 1):
            output[f"part_{i}"] = json.dumps(chunk, ensure_ascii=False)
        
        return {"result": output}
        
    except ET.ParseError as e:
        return {"error": f"XML解析错误: {str(e)}"}
    except Exception as e:
        return {"error": f"处理错误: {str(e)}"}

def pubmed_search_fetch(api_key, term, db, retmax=20):
    """执行PubMed搜索和获取"""
    try:
        # ESearch
        esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        esearch_params = {
            "db": db,
            "term": term,
            "retmax": retmax,
            "retmode": "json",
            "api_key": api_key
        }
        
        esearch_response = requests.get(esearch_url, params=esearch_params)
        esearch_response.raise_for_status()
        esearch_data = esearch_response.json()
        
        # 获取ID列表
        id_list = esearch_data['esearchresult']['idlist']
        if not id_list:
            return {"error": "未找到相关文献"}
            
        # 添加延时以符合NCBI的请求频率限制
        time.sleep(0.1)
        
        # EFetch
        efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        efetch_params = {
            "db": db,
            "id": ",".join(id_list),
            "retmode": "xml",
            "api_key": api_key
        }
        
        efetch_response = requests.get(efetch_url, params=efetch_params)
        efetch_response.raise_for_status()
        
        # 处理XML响应
        return process_xml(efetch_response.text)
        
    except requests.exceptions.RequestException as e:
        return {"error": f"API请求错误: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON解析错误: {str(e)}"}
    except Exception as e:
        return {"error": f"处理错误: {str(e)}"}

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='PubMed文献检索工具')
    parser.add_argument('--api-key', required=True, help='NCBI API密钥')
    parser.add_argument('--term', required=True, help='搜索词')
    parser.add_argument('--db', default='pubmed', help='数据库名称 (默认: pubmed)')
    parser.add_argument('--retmax', type=int, default=20, help='返回结果数量 (默认: 20)')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 执行搜索和获取
    result = pubmed_search_fetch(
        api_key=args.api_key,
        term=args.term,
        db=args.db,
        retmax=args.retmax
    )
    
    # 将结果保存到result1.json文件
    with open('result1.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到 result1.json")

if __name__ == "__main__":
    main()