import re


def converter(latex_files):
    res = str()
    txt = str()
    for tmp in latex_files:
        with open(tmp) as file:
            txt = file.read()

            # TODO: Add a for loop
            # TODO: Add support for enumerate

            # Trimming document
            txt = txt[(txt.find('\\begin{document}') + 16):txt.find('\\end{document}')]

            # Creating titles
            txt = re.sub('\\\\section(\*)?{(.*)}', r'<h3 id="\2"><a class="hashtag" href="#\2">#</a>\2</h3><p>', txt)
            txt = re.sub('\\\\subsection(\*)?{(.*)}', r'<h4 id="\2"><a class="hashtag" href="#\2">#</a>\2</h4><p>', txt)

            # Creating theorem/definition cards
            txt = re.sub('(\\\\begin{theorem})|(\\\\begin{definition})', '</p><div class="card"><div class="card-body">', txt)
            txt = re.sub('(\\\\end{theorem})|(\\\\end{definition})', '</div></div><p>', txt)
            txt = re.sub('\[(.*)\]', r'<b>\1</b><br>', txt)

            # Creating block quotes
            txt = re.sub('\\\\somequote{(.*)}{(.*)}{(.*)}', r'''<figure>
            <blockquote class="blockquote">
                <p>\1</p>
            </blockquote>
            <figcaption class="blockquote-footer">
                \2, <cite title="Source Title">\3</cite>
            </figcaption>
            </figure>
            ''', txt)

            # Adding to result and resetting txt
            res += f'\n\n{txt}'
            txt = ''

    return res