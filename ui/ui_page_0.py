import pyvisual as pv


def create_page_0_ui(window,ui):
    """
    Create and return UI elements for Page 0.
    :param container: The page widget for Page 0.
    :return: Dictionary of UI elements.
    """
    ui_page = {}
    ui_page["file_selector"] = pv.PvFileDialog(container=window, x=322, y=260, width=356,
        height=280, text='Select a file to get started.', font='assets/fonts/Poppins/Poppins.ttf', font_size=16,
        font_color=(171, 171, 171, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(56, 182, 255, 0), hover_color=None,
        clicked_color=None, border_color=(1, 134, 255, 1), border_hover_color=None, border_thickness=3,
        corner_radius=15, border_style="dashed", box_shadow=None, box_shadow_hover=None,
        icon_path='assets/icons/a660281630.svg', icon_position='left', icon_color=(1, 134, 255, 1), icon_color_hover=None,
        icon_spacing=22, icon_scale=1.2, paddings=(0, 0, 0, 0), enable_drag_drop=True,
        dialog_mode="open", files_filter="All Files (*.*);;Images (*.png *.jpg *.gif)", is_visible=True, is_disabled=False,
        opacity=1, on_hover=None, on_click=None, on_release=None,
        tag=None)

    ui_page["Text_1"] = pv.PvText(container=window, x=351, y=-4, width=297,
        height=114, idle_color=(144, 80, 178, 0), text='AutoPoint', is_visible=True,
        text_alignment='left', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=60,
        font_color=(51, 106, 255, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    ui_page["cpu_text"] = pv.PvText(container=window, x=13, y=29, width=84,
        height=48, idle_color=(144, 80, 178, 0), text='CPU', is_visible=True,
        text_alignment='left', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=35,
        font_color=(51, 106, 255, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    ui_page["gpu_button"] = pv.PvButton(container=window, x=104, y=33, width=40,
        height=40, text='', font='assets/fonts/Lexend/Lexend.ttf', font_size=16,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(1, 130, 255, 1), hover_color=None,
        clicked_color=None, border_color=(100, 100, 100, 1), border_hover_color=None, border_thickness=0,
        corner_radius=25, border_style="solid", box_shadow=None, box_shadow_hover=None,
        icon_path='assets/icons/0fafcba000.svg', icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1.2, paddings=(2, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["gpu_text"] = pv.PvText(container=window, x=160, y=29, width=74,
        height=47, idle_color=(144, 80, 178, 0), text='GPU', is_visible=True,
        text_alignment='left', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=35,
        font_color=(51, 106, 255, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=0.3, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    ui_page["cpu_button"] = pv.PvButton(container=window, x=104, y=33, width=40,
        height=40, text='', font='assets/fonts/Lexend/Lexend.ttf', font_size=16,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(1, 130, 255, 1), hover_color=None,
        clicked_color=None, border_color=(100, 100, 100, 1), border_hover_color=None, border_thickness=0,
        corner_radius=25, border_style="solid", box_shadow=None, box_shadow_hover=None,
        icon_path='assets/icons/01c4df648a.svg', icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1.2, paddings=(2, 0, 3, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    return ui_page
