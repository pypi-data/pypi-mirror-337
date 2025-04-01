import re
from typing import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render
from mdit_py_plugins.amsmath import amsmath_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin


def update_mdit(mdit: MarkdownIt) -> None:
    mdit.use(dollarmath_plugin, double_inline=True, allow_blank_lines=True)
    mdit.use(amsmath_plugin)


def format_math_block_content(content):
    # strip and remove blank lines
    content = re.sub(r"\n+", "\n", content.strip(), re.DOTALL)

    #
    content = re.sub(r"\\(begin|end){align\*?}", r"\\\1{aligned}", content)

    # remove additional white spaces in the end of the line
    content = re.sub(r"\s+$", "", content)

    return f"\n{content}\n"


def _math_inline_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"${node.content}$"


def _math_block_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"$${format_math_block_content(node.content)}$$"


def _math_inline_double_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    # formats the inline doubles as math blocks
    return f"\n\n$${format_math_block_content(node.content.strip())}$$\n\n"


def _math_block_label_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"$${format_math_block_content(node.content)}$$ ({node.info})"


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
RENDERERS: Mapping[str, Render] = {
    "math_inline": _math_inline_renderer,
    "math_inline_double": _math_inline_double_renderer,
    "math_block_label": _math_block_label_renderer,
    "math_block": _math_block_renderer,
    "amsmath": _math_block_renderer,
}
