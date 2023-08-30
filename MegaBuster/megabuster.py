#!/usr/bin/python3

from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace
from target import Target
import pytermgui as ptg


PALETTE_LIGHT = "#4d58ff"
PALETTE_MID = "#3c38a6"
PALETTE_DARK = "#4a0505"
PALETTE_DARKER = "#330202"


def _process_arguments(argv: list[str] | None = None) -> Namespace:
    """Processes command line arguments.
    Args:
        argv: A list of command line arguments, not including the binary path
            (sys.argv[0]).
    """

    parser = ArgumentParser(description="MegaBuster")

    return parser.parse_args(argv)


def _create_aliases() -> None:
    """Creates all the TIM aliases used by the application.

    Aliases should generally follow the following format:

        namespace.item

    For example, the title color of an app named "myapp" could be something like:

        myapp.title
    """

    ptg.tim.alias("app.text", "#cfc7b0")

    ptg.tim.alias("app.header", f"bold @{PALETTE_MID} #d9d2bd")
    ptg.tim.alias("app.header.fill", f"@{PALETTE_LIGHT}")

    ptg.tim.alias("app.title", f"bold {PALETTE_LIGHT}")
    ptg.tim.alias("app.button.label", f"bold @{PALETTE_DARK} app.text")
    ptg.tim.alias("app.button.highlight", "inverse app.button.label")

    ptg.tim.alias("app.footer", f"@{PALETTE_DARKER}")


def _configure_widgets() -> None:
    """Defines all the global widget configurations.

    Some example lines you could use here:

        ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
        ptg.Splitter.set_char("separator", " ")
        ptg.Button.styles.label = "myapp.button.label"
        ptg.Container.styles.border__corner = "myapp.border"
    """

    ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
    ptg.boxes.ROUNDED.set_chars_of(ptg.Container)

    ptg.Button.styles.label = "app.button.label"
    ptg.Button.styles.highlight = "app.button.highlight"
	
    ptg.Slider.styles.filled__cursor = PALETTE_MID
    ptg.Slider.styles.filled_selected = PALETTE_LIGHT

    ptg.Label.styles.value = "app.text"

    ptg.Window.styles.border__corner = "#C2B280"
    ptg.Container.styles.border__corner = PALETTE_DARK

    ptg.Splitter.set_char("separator", "")


def _define_layout() -> ptg.Layout:
    """Defines the application layout.

    Layouts work based on "slots" within them. Each slot can be given dimensions for
    both width and height. Integer values are interpreted to mean a static width, float
    values will be used to "scale" the relevant terminal dimension, and giving nothing
    will allow PTG to calculate the corrent dimension.
    """

    layout = ptg.Layout()

    # A header slot with a height of 1
    layout.add_slot("Header", height=1)
    layout.add_break()

    # A body slot that will fill the entire width, and the height is remaining
    layout.add_slot("Body")

    # A slot in the same row as body, using the full non-occupied height and
    # 20% of the terminal's width.
    layout.add_slot("Body right", width=0.2)

    layout.add_break()

    # A footer with a static height of 1
    layout.add_slot("Footer", height=1)

    return layout

def _target_window() -> ptg.Layout:
    """This will be the layout for the target window"""
    layout = ptg.Layout()
    layout.add_slot()

def _confirm_quit(manager: ptg.WindowManager) -> None:
    """Creates an "Are you sure you want to quit" modal window"""

    modal = ptg.Window(
        "[app.title]Are you sure you want to quit?",
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Yes", lambda *_: manager.stop()),
                ptg.Button("No", lambda *_: modal.close()),
            ),
        ),
    ).center()

    modal.select(1)
    manager.add(modal)

def _create_target(name, ip) -> Target:
    """Creates a Target with Target Class (via target.py)"""
    target = Target(name, ip)
    return target


def sidebar_target_window(manager: ptg.WindowManager, target) -> ptg.Window:
    """Creates the window for the target"""
    name =ptg.Window(
        target.get_name()
    )
    return name

def _add_target(manager: ptg.WindowManager) -> None:
    """Adds a new target to select"""
    name_input_field = ptg.InputField(
        prompt= "Input Name for Target"
    )

    ip_input_field = ptg.InputField(
            prompt="Input IP Address"
        )
    submit_button = ptg.Button().bind(ptg.keys.RETURN, lambda  *_: _create_target(name_input_field.value, ip_input_field.value))

    modal = ptg.Window(
        "[app.title]New Target:",
        "",

        name_input_field,
        ip_input_field,
        submit_button

    ).center()
    manager.add(modal)
    target = _create_target(name_input_field.value,ip_input_field.value)
    manager.add(sidebar_target_window(manager, target))

def main(argv: list[str] | None = None) -> None:
    """Runs the application."""

    _create_aliases()
    _configure_widgets()

    args = _process_arguments(argv)

    with ptg.WindowManager() as manager:
        manager.layout = _define_layout()

        header = ptg.Window(
            "[app.header] ZBuster - Enumeration Tool",
            box="EMPTY",
            is_persistant=True,
        )

        header.styles.fill = "app.header.fill"

        # Since header is the first defined slot, this will assign to the correct place
        manager.add(header)

        footer = ptg.Window(
            ptg.Button("Quit", lambda *_: _confirm_quit(manager)),
            box="EMPTY",
        )
        footer.styles.fill = "app.footer"

        # Since the second slot, body was not assigned to, we need to manually assign
        # to "footer"
        manager.add(footer, assign="footer")

        manager.add(
            ptg.Window("My sidebar"
                       ),
            assign="body_right",
        )

        manager.add(
            ptg.Window(
                ptg.Button("Test obj: Add new Target", lambda *_: _add_target(manager))
            ),
            assign="body_right"
        )



    ptg.tim.print(f"[{PALETTE_LIGHT}]Goodbye!")


if __name__ == "__main__":
    main(sys.argv[1:])
