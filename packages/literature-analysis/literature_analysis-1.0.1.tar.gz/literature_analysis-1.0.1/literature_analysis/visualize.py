import json
import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_pdf_report(data, output_file="literature_analysis.pdf"):
    """创建PDF报告"""
    try:
        # A4页面尺寸（单位：点）
        doc = SimpleDocTemplate(
            output_file,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            spaceBefore=20,
            textColor=colors.HexColor('#2E5090')
        )
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=10,
            textColor=colors.HexColor('#4A6BA5')
        )
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            spaceBefore=6,
            spaceAfter=6
        )
        
        story = []
        
        # 添加标题
        story.append(Paragraph("Literature Analysis Report", title_style))
        story.append(Spacer(1, 20))
        
        # 添加总体分析
        story.append(Paragraph("Overall Summary", heading_style))
        
        # 研究分布
        story.append(Paragraph("Research Distribution:", subheading_style))
        story.append(Paragraph(data['overall_summary']['research_distribution'], normal_style))
        story.append(Spacer(1, 10))
        
        # 主要发现
        story.append(Paragraph("Major Findings:", subheading_style))
        story.append(Paragraph(data['overall_summary']['major_findings'], normal_style))
        story.append(Spacer(1, 10))
        
        # 研究进展
        story.append(Paragraph("Research Progress:", subheading_style))
        story.append(Paragraph(data['overall_summary']['research_progress'], normal_style))
        story.append(Spacer(1, 10))
        
        # 未来方向
        story.append(Paragraph("Future Directions:", subheading_style))
        story.append(Paragraph(data['overall_summary']['future_directions'], normal_style))
        story.append(Spacer(1, 10))
        
        # 综合分析
        story.append(Paragraph("Comprehensive Analysis:", subheading_style))
        story.append(Paragraph(data['overall_summary']['comprehensive_analysis'], normal_style))
        
        # 添加分页符
        story.append(PageBreak())
        
        # 添加研究主题详细内容
        story.append(Paragraph("Research Themes Detail", heading_style))
        for theme in data['research_groups']:
            story.append(Paragraph(f"<b>{theme['theme']}</b>", subheading_style))
            for paper in theme['papers']:
                paper_text = (f"• <b>Authors:</b> {paper.get('authors', '')}<br/>"
                            f"<b>Year:</b> {paper.get('year', '')}<br/>"
                            f"<b>Title:</b> {paper.get('title', '')}<br/>"
                            f"<b>Journal:</b> {paper.get('journal', '')}<br/>"
                            f"<b>Key Finding:</b> {paper.get('key_finding', '')}<br/>"
                            f"<b>Mechanism:</b> {paper.get('detailed_mechanism', '')}")
                story.append(Paragraph(paper_text, normal_style))
                story.append(Spacer(1, 10))
            story.append(Spacer(1, 15))
        
        # 添加分页符
        story.append(PageBreak())
        
        # 添加证据网络
        story.append(Paragraph("Evidence Network", heading_style))
        for evidence in data['evidence_network']:
            # 证据类型
            evidence_type = "Supporting" if evidence['type'] == 'supporting' else "Contradicting"
            story.append(Paragraph(f"<b>{evidence_type} Evidence:</b>", subheading_style))
            
            # 相关论文
            story.append(Paragraph("<b>Related Papers:</b>", normal_style))
            for paper in evidence['papers']:
                story.append(Paragraph(f"• {paper}", normal_style))
            
            # 研究模型
            story.append(Paragraph(f"<b>Model Type:</b> {evidence['model_type']}", normal_style))
            
            # 分子机制
            story.append(Paragraph(f"<b>Mechanism:</b> {evidence['mechanism']}", normal_style))
            
            # 详细描述
            story.append(Paragraph(f"<b>Description:</b> {evidence['description']}", normal_style))
            
            # 研究意义
            story.append(Paragraph(f"<b>Implications:</b> {evidence['implications']}", normal_style))
            
            story.append(Spacer(1, 15))
        
        # 生成PDF
        doc.build(story)
        
        print(f"PDF report has been generated: {output_file}")
        
    except Exception as e:
        print(f"Error during PDF creation: {str(e)}")
        raise e

def main():
    if len(sys.argv) != 2:
        print("Usage: python visualize_analysis.py analysis_result.json")
        sys.exit(1)
    
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("Generating PDF report...")
        create_pdf_report(data)
        
        print("Complete!")
        print("- Analysis report saved as literature_analysis.pdf")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e

if __name__ == "__main__":
    main()