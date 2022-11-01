import gradio as gr

from myv_translit import lat2cyr, cyr2lat


def transliterator(input_text, direction_to_latn=1, joint_acute=True, not_first_e_with_hacek=False, not_soft_l_after_vowels=True):
    first_e_with_hacek = not not_first_e_with_hacek
    soft_l_after_vowels = not not_soft_l_after_vowels
    if direction_to_latn:
        result = cyr2lat(input_text, joint_acute=joint_acute, first_e_with_hacek=first_e_with_hacek, soft_l_after_vowels=soft_l_after_vowels)
    else:
        result = lat2cyr(input_text, joint_acute=joint_acute, first_e_with_hacek=first_e_with_hacek, soft_l_after_vowels=soft_l_after_vowels)
    return result


article = """
Это автоматический транслитератор между кириллицей и латиницей для эрянского языка.

В основе - алгоритм Михаила Потапова:
- https://github.com/potapoff271083/automatic_translation_latin_to_cyrillic
- http://valks.erzja.info/2020/04/30/эрзянский-алфавит/
"""

directions = ['lat -> кир', 'кир -> lat']


interface = gr.Interface(
    transliterator,
    [
        gr.Textbox(label="Text", lines=2, placeholder='text to transliterate'),
        gr.Radio(choices=directions, type="index", interactive=True, value=directions[0]),
        gr.Checkbox(value=True, label='L + ́  -> Ĺ'),
        gr.Checkbox(value=False, label='ěrzä -> erzä'),
        gr.Checkbox(value=False, label='peĺks -> pelks'),
    ],
    "text",
    title='Эрзянь транслитератор',
    article=article,
)


if __name__ == '__main__':
    interface.launch()
