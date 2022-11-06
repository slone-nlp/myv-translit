import gradio as gr

from myv_translit import lat2cyr, cyr2lat, detect_script

DIRECTIONS = ['lat -> кир', 'кир -> lat']


def transliterator(input_text, direction, joint_acute=True, not_first_e_with_hacek=False, not_soft_l_after_vowels=True):
    first_e_with_hacek = not not_first_e_with_hacek
    soft_l_after_vowels = not not_soft_l_after_vowels
    if direction is None:
        code = detect_script(input_text)
        direction = DIRECTIONS[int(code != 'lat')]
    if direction == DIRECTIONS[1]:
        result = cyr2lat(input_text, joint_acute=joint_acute, first_e_with_hacek=first_e_with_hacek, soft_l_after_vowels=soft_l_after_vowels)
    else:
        result = lat2cyr(input_text, joint_acute=joint_acute, first_e_with_hacek=first_e_with_hacek, soft_l_after_vowels=soft_l_after_vowels)
    return result


article = """
Это автоматический транслитератор между кириллицей и латиницей для эрзянского языка.

В основе - алгоритм Михаила Потапова:
- https://github.com/potapoff271083/automatic_translation_latin_to_cyrillic
- http://valks.erzja.info/2020/04/30/эрзянский-алфавит/
"""


interface = gr.Interface(
    transliterator,
    [
        gr.Textbox(label="Текст", lines=2, placeholder='text to transliterate'),
        gr.Radio(choices=DIRECTIONS, type="value", interactive=True, label='Направление'),
        gr.Checkbox(value=True, label='L + ́  -> Ĺ'),
        gr.Checkbox(value=False, label='ěrzä -> erzä'),
        gr.Checkbox(value=False, label='peĺks -> pelks'),
    ],
    "text",
    title='Эрзянь транслитератор <-> Ěrzäń transliterator',
    article=article,
)


if __name__ == '__main__':
    interface.launch(server_name="0.0.0.0")
