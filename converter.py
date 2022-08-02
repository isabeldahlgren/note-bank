import re
import os


def converter(latex_file):
    
    txt = str()
    with open(latex_file) as file:
        txt = file.read()

        # TODO: Add a for loop

        # Trimming document
        txt = txt[(txt.find('\\begin{document}') + 16):txt.find('\\end{document}')]

        # Creating titles
        txt = re.sub('\\\\section(\*)?{(.*)}', r'<h4 id="\2">\2<a id="hashtag" href="#\2">#</a></h4><p>', txt)
        txt = re.sub('\\\\subsection(\*)?{(.*)}', r'</p><h5 id="\2">\2<a id="hashtag" href="#\2">#</a></h5><p>', txt)

        # Creating theorem/definition cards
        txt = re.sub('\\\\begin\{theorem\}', '</p><div class="card"><div class="card-body"> &#128205 ', txt)
        txt = re.sub('\\\\begin\{definition\}', '</p><div class="card"><div class="card-body"> &#128273 ', txt)
        txt = re.sub('\\\\end\{(theorem|definition)\}', '</div></div><br><p>', txt)
        txt = re.sub('\[(.*)\]', r'<b>\1</b><br>', txt)

        # Creating block quotes
        txt = re.sub('\\\\somequote{(.*)}{(.*)}{(.*)}', r'''</p><figure>
        <blockquote class="blockquote">
            <p>\1</p>
        </blockquote>
        <figcaption class="blockquote-footer">
            \2, <cite title="Source Title">\3</cite>
        </figcaption>
        </figure><p>
        ''', txt)
        txt = re.sub('\\\\simplequote{(.*)}', r'''</p><figure><blockquote class="blockquote">
        <p>\1</p>
        </blockquote></figure><p>''', txt)

        # Support for enumerate/itemize
        txt = re.sub('\\\\begin{enumerate}', '<ol>', txt)
        txt = re.sub('\\\\end{enumerate}', '</ol>', txt)
        txt = re.sub('\\\\begin{itemize}', '<ul>', txt)
        txt = re.sub('\\\\end{itemize}', '</ul>', txt)
        txt = re.sub('\\\\item (.*)', r'<li>\1</li>', txt)

        return txt