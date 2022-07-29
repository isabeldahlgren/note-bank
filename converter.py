import re
import os


def converter(latex_files):
    res = str()
    txt = str()
    for tmp in latex_files:
        with open(tmp) as file:
            txt = file.read()

            # TODO: Add a for loop

            # Trimming document
            txt = txt[(txt.find('\\begin{document}') + 16):txt.find('\\end{document}')]

            # Creating titles
            txt = re.sub('\\\\section(\*)?{(.*)}', r'<h3 id="\2"><a class="hashtag" href="#\2">#</a>\2</h3><p>', txt)
            txt = re.sub('\\\\subsection(\*)?{(.*)}', r'</p><h4 id="\2"><a class="hashtag" href="#\2">#</a>\2</h4><p>', txt)

            # Creating theorem/definition cards
            txt = re.sub('\\\\begin\{(theorem|definition)\}', '</p><div class="card"><div class="card-body">', txt)
            txt = re.sub('\\\\end\{(theorem|definition)\}', '</div></div><br><p>', txt)
            txt = re.sub('\[(.*)\]', r'<b>\1</b>', txt)

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

            txt = re.sub('\\\\begin{enumerate}', '<ol>', txt)
            txt = re.sub('\\\\end{enumerate}', '</ol>', txt)
            txt = re.sub('\\\\begin{itemize}', '<ul>', txt)
            txt = re.sub('\\\\end{itemize}', '</ul>', txt)
            txt = re.sub('\\\\item (.*)', r'<li>\1</li>', txt)

            # Adding to result and resetting txt
            res += f'\n\n{txt}'
            txt = ''

    return res