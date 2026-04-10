
screen main_menu():

    on "show" action SetVariable("parallax_active", True)
    on "replace" action SetVariable("parallax_active", True)
    on "hide" action [
        SetVariable("parallax_active", False),
        SetVariable("parallax_x", 0.5),
        SetVariable("parallax_y", 0.5),
        SetVariable("interpolated_x", 0.5),
        SetVariable("interpolated_y", 0.5),
        SetVariable("smooth_x", 0.0),
        SetVariable("smooth_y", 0.0)
    ]
    on "replaced" action [
        SetVariable("parallax_active", False),
        SetVariable("parallax_x", 0.5),
        SetVariable("parallax_y", 0.5),
        SetVariable("interpolated_x", 0.5),
        SetVariable("interpolated_y", 0.5),
        SetVariable("smooth_x", 0.0),
        SetVariable("smooth_y", 0.0)
    ]

    tag menu
    modal True

    add Transform(ParallaxLayer("gui/zhopa2.png", depth=0, zoom=1.5), alpha=1.0)
    add Transform(ParallaxLayer("gui/zhopa3.png", depth=0, zoom=1.5), alpha=0.2)
    add ParallaxLayer("gui/zhopa2.png", depth=90, zoom=1.05)
    add Transform(ParallaxLayer("gui/kassir6.png", depth=180, anchor=(0.5, 0.5), zoom=1.05), alpha=0.1)
    add Transform(ParallaxLayer("gui/kassir6.png", depth=150, anchor=(0.5, 0.5), zoom=1.05), alpha=0.2)
    add Transform(ParallaxLayer("gui/kassir6.png", depth=90, anchor=(0.5, 0.5), zoom=1.05), alpha=0.4)
    add Transform(ParallaxLayer("gui/kassir6.png", depth=120, anchor=(0.5, 0.5), zoom=1.05), alpha=0.3)
    add ParallaxLayer("gui/zhopa.png", depth=60, zoom=1.05)
    add Transform(ParallaxLayer("gui/zhopa3.png", depth=60, zoom=1.1), alpha=0.2)
    add Transform(ParallaxLayer("gui/Bullshit.png", depth=40, anchor=(0.5, 0.52), zoom=1.2), alpha=0.2)
    add Transform(ParallaxLayer("gui/Bullshit.png", depth=10, anchor=(0.5, 0.52), zoom=1.2), alpha=1.0)
    add Transform(ParallaxLayer("gui/bullshit2.png", depth=0, zoom=1.5), alpha=0.2)
    add Transform(ParallaxLayer("dust_blend2", depth=50), blend="add", alpha=0.2)

    if renpy.variant("pc") or renpy.variant("web"): 

    mousearea:
        area (0, 0, config.screen_width, config.screen_height)

    if renpy.android:
        timer 0.016 repeat True action Function(interpolate_parallax)
        
    else:
        timer 0.016 repeat True action [
            Function(update_mouse_parallax),
            Function(interpolate_parallax)
        ]
