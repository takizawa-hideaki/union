import tkinter as tk
from tkinter import scrolledtext
import re

class TextToHTMLConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to HTML Converter")

        self.date_label = tk.Label(root, text="Date (YYYY.MM.DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(root)
        self.date_entry.pack(pady=5)

        self.input_label = tk.Label(root, text="Input Text:")
        self.input_label.pack()
        self.input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
        self.input_text.pack(padx=10, pady=10)

        self.span_label = tk.Label(root, text="Span Text (Parts, comma-separated):")
        self.span_label.pack()
        self.span_entry = tk.Entry(root)
        self.span_entry.pack(pady=5)

        self.attention_label = tk.Label(root, text="Attention Text (Parts, comma-separated):")
        self.attention_label.pack()
        self.attention_entry = tk.Entry(root)
        self.attention_entry.pack(pady=5)

        self.convert_button = tk.Button(root, text="Convert to HTML", command=self.convert_to_html)
        self.convert_button.pack(pady=10)

        self.output_label = tk.Label(root, text="HTML Output:")
        self.output_label.pack()
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
        self.output_text.pack(padx=10, pady=10)

    def convert_to_html(self):
        date = self.date_entry.get().strip()
        span_input = self.span_entry.get().strip()
        attention_input = self.attention_entry.get().strip()
        input_text = self.input_text.get("1.0", tk.END).strip()
        articles = self.parse_articles(input_text)

        span_parts = self.parse_parts(span_input)
        attention_parts = self.parse_parts(attention_input)

        html_text = self.generate_html(articles, date, span_parts, attention_parts)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.INSERT, html_text)

    def parse_articles(self, input_text):
        articles = input_text.split('\n\n')
        cleaned_articles = [re.sub(r'^\d+\.\s*', '', article).strip() for article in articles]
        return cleaned_articles

    def parse_parts(self, parts_input):
        if not parts_input:
            return set()
        return set(map(int, parts_input.split(',')))

    def generate_html(self, articles, date, span_parts, attention_parts):
        html_header = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>お知らせ | PROFILE</title>
  <style>
    body {
      font-family: 'メイリオ', 'Meiryo', sans-serif;
    }
    .text_date {
      font-size: 0.9em;
      margin-bottom: 0.5em;
    }
    h1 {
      font-size: 1.5em;
      margin-bottom: 1em;
    }
    h2 {
      font-size: 1.2em;
      margin-top: 1em;
    }
    .text_content {
      font-size: 1em;
      margin-bottom: 3em;
    }
    .attention {
      color: #FF0000;
    }
    .blue{
      color: #0000FF;
    }
    footer {
      margin-top: 2em;
      font-size: 0.8em;
      text-align: center;
    }
  </style>
</head>
<body>
<main id="information">
<div class="wrapper">
<h1>お知らせ</h1>
'''

        html_footer = '''
</div>
</main>
</body>
</html>
'''

        html_body = ""
        for i, article in enumerate(articles):
            lines = article.split('\n')
            if len(lines) >= 2:
                title_line = lines[0].strip()
                content_lines = "<br>".join(line.strip() for line in lines[1:])

                part_number = i + 1
                span_html = f'<span class="blue">{title_line}</span>' if part_number in span_parts else title_line
                attention_html = f'<span class="attention">{span_html}</span>' if part_number in attention_parts else span_html

                html_body += f'''
<article id="part{part_number}">
  <p class="text_date"><time datetime="{date}">{date}</time></p>
  <h2>{attention_html}</h2>
  <p class="text_content">{content_lines}</p>
</article>
'''

        return html_header + html_body + html_footer

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToHTMLConverter(root)
    root.mainloop()
