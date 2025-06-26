import pyvisual as pv


def create_page_1_ui(window,ui):
    """
    Create and return UI elements for Page 1.
    :param container: The page widget for Page 1.
    :return: Dictionary of UI elements.
    """
    ui_page = {}
    ui_page["Text_0"] = pv.PvText(container=window, x=308, y=614, width=383,
        height=29, idle_color=(144, 80, 178, 0), text='Computing Optical Flow for video...', is_visible=True,
        text_alignment='left', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=22,
        font_color=(51, 106, 255, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    ui_page["optical_flow_video"] = pv.PvOpencvVideo(container=window, x=149, y=203, width=700,
        height=393, video_path=None, scale=1, corner_radius=10,
        auto_start=False, flip_v=False, flip_h=False, rotate=0,
        border_color=(0, 0, 0, 1), border_hover_color=None, border_thickness=0, border_style="solid",
        is_visible=True, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Text_2"] = pv.PvText(container=window, x=16, y=37, width=69,
        height=43, idle_color=(144, 80, 178, 0), text='CPU', is_visible=True,
        text_alignment='left', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=30,
        font_color=(51, 106, 255, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=1, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    ui_page["cpu_button"] = pv.PvButton(container=window, x=102, y=40, width=40,
        height=40, text='', font='assets/fonts/Lexend/Lexend.ttf', font_size=16,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(1, 130, 255, 1), hover_color=None,
        clicked_color=None, border_color=(100, 100, 100, 1), border_hover_color=None, border_thickness=0,
        corner_radius=25, border_style="solid", box_shadow=None, box_shadow_hover=None,
        icon_path='assets/icons/01c4df648a.svg', icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1.2, paddings=(2, 0, 3, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    ui_page["Text_4"] = pv.PvText(container=window, x=165, y=39, width=69,
        height=43, idle_color=(144, 80, 178, 0), text='GPU', is_visible=True,
        text_alignment='left', paddings=(0, 0, 0, 0), font='assets/fonts/Poppins/Poppins.ttf', font_size=30,
        font_color=(51, 106, 255, 1), bold=False, italic=False, underline=False,
        strikethrough=False, opacity=0.3, border_color=None, corner_radius=0,
        on_hover=None, on_click=None, on_release=None, tag=None)

    ui_page["gpu_button"] = pv.PvButton(container=window, x=102, y=40, width=40,
        height=40, text='', font='assets/fonts/Lexend/Lexend.ttf', font_size=16,
        font_color=(255, 255, 255, 1), font_color_hover=None, bold=False, italic=False,
        underline=False, strikethrough=False, idle_color=(1, 130, 255, 1), hover_color=None,
        clicked_color=None, border_color=(100, 100, 100, 1), border_hover_color=None, border_thickness=0,
        corner_radius=25, border_style="solid", box_shadow=None, box_shadow_hover=None,
        icon_path='assets/icons/0fafcba000.svg', icon_position='left', icon_color=(255, 255, 255, 1), icon_color_hover=None,
        icon_spacing=0, icon_scale=1.2, paddings=(2, 0, 0, 0), is_visible=True,
        is_disabled=False, opacity=1, on_hover=None, on_click=None,
        on_release=None, tag=None)

    return ui_page
