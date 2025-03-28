from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTText, LTChar, LTTextLine


class pdfToool():
    def __init__(self):
        pass

    @staticmethod
    def create_pdf_objects(fp):
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        return parser, doc, interpreter, device

    @staticmethod
    def custom_sort_key(item):
        # 提取 "-" 前后的数字，并将其转换为整数
        page, line = map(int, item.split('-'))
        # 返回一个元组，其中第一个元素是升序排序的页码，第二个元素是降序排序的行号
        return page, -line

    @staticmethod
    def comparison(page_num, datas, data):
        # 遍历datas字典中的每个项
        for k, lines in datas.items():
            page, line = map(int, k.split('-'))
            # 检查页码是否匹配以及行号是否在指定范围内
            if page_num == page and -5 <= data - line < 5:
                return True, k
        return False, None

    def get_pdf_data(self, file_path):
        line_dict = {}
        lines = []
        with open(file_path, 'rb') as fp:  # 使用with语句自动管理文件
            parser, doc, interpreter, device = self.create_pdf_objects(fp)
            page_num = 1  # 初始化页数
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
                layout = device.get_result()
                current_lines = []  # 存储当前页的文本行
                for element in layout:
                    if isinstance(element, LTTextBox) or isinstance(element, LTTextLine):
                        # 正确迭代 LTTextBox 或 LTTextLine 对象
                        for line in element:
                            if isinstance(line, LTTextLine):
                                line_key = f"{str(page_num)}-{str(int(line.bbox[3]))}"
                                if line_key not in line_dict:
                                    line_dict[line_key] = []
                                    lines.append(line_key)
                                current_lines.append((line_key, line))

                # 代表文本行的(x0, y0, x1, y1)坐标，其中x0和y0是左下角的坐标，x1和y1是右上角的坐标
                sorted_text_lines = sorted(current_lines, key=lambda x: (-x[1].bbox[3], x[1].bbox[2]))

                for line_key, line in sorted_text_lines:
                    found, key = self.comparison(page_num, line_dict, int(line.bbox[3]))
                    if found:
                        line_dict[key].append([line.get_text().strip(), line])
                    else:
                        line_dict[line_key].append([line.get_text().strip(), line])

                page_num += 1

            # 根据自定义排序规则对lines进行排序
            sorted_lines = sorted(lines, key=self.custom_sort_key)

            output = [
                [[lin[0], lin[1].bbox[0], lin[1].bbox[1], lin[1].bbox[2], lin[1].bbox[3]] for lin in sorted_items]
                for line_key in sorted_lines
                if line_dict.get(line_key)  # 使用get避免key不存在时抛出异常
                for sorted_items in (sorted(line_dict[line_key], key=lambda x: x[1].bbox[2]),)
            ]
            return output, page_num - 1


pdfTooolObj = pdfToool()

if __name__ == '__main__':
    filePath = r"d:\SHAE66842600.pdf"
    data = pdfTooolObj.get_pdf_data(filePath)
    print(data)
