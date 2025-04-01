import asyncio
import os
import sys
from warnings import warn

from IPython import get_ipython

# Use a global variable here because some calls to IPython will actually case an
# interpreter to be created.  This file needs to be imported BEFORE that
# happens.
running_as_notebook = (
    "COLAB_TESTING" not in os.environ
    and get_ipython()
    and hasattr(get_ipython(), "kernel")
)


def pyplot_is_interactive():
    # import needs to happen after the backend is set.
    import matplotlib.pyplot as plt
    from matplotlib.rcsetup import interactive_bk

    return plt.get_backend() in interactive_bk


def SetupMatplotlibBackend(wishlist=["notebook"]):
    """
    Helper to support multiple workflows:
        1) nominal -- running locally w/ jupyter notebook
        2) unit tests (no ipython, backend is template)
        3) binder -- does have notebook backend
        4) colab -- claims to have notebook, but it doesn't work
    Puts the matplotlib backend into notebook mode, if possible,
    otherwise falls back to inline mode.
    Returns True iff the final backend is interactive.
    """
    # To find available backends, one can access the lists:
    # matplotlib.rcsetup.interactive_bk
    # matplotlib.rcsetup.non_interactive_bk
    # matplotlib.rcsetup.all_backends
    if running_as_notebook:
        ipython = get_ipython()
        # Short-circuit for google colab.
        if "google.colab" in sys.modules:
            ipython.run_line_magic("matplotlib", "inline")
            return False
        # TODO: Find a way to detect vscode, and use inline instead of notebook
        for backend in wishlist:
            try:
                ipython.run_line_magic("matplotlib", backend)
                return pyplot_is_interactive()
            except KeyError:
                continue
        ipython.run_line_magic("matplotlib", "inline")
    return False


# Deprecate/remove everything below this line:


def AdvanceToAndVisualize(*args, **kwargs):
    raise Exception("AdvanceToAndVisualize() has moved to underactuated.pyplot_utils.")


def setup_matplotlib_backend(**kwargs):
    SetupMatplotlibBackend(**kwargs)


# Inspired by https://github.com/Kirill888/jupyter-ui-poll but there *must* be a
# better way. Ideas:
#  - provide init() and cleanup() methods that could be called to pull out and
#    replace the irrelevant events just once (instead of on every time step).
#    E.g. init(), simulator.AdvanceTo(10), cleanup().
#  - whitelist widget events and only process them (instead of black-listing the
#    execute_request).
#  - do I actually need asyncio?  can I just write the events back?
#
# But I'll wait to see how much we use this before spending too much time on it.
# BTW,
# https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Asynchronous.html  # noqa
# describes the problem but does not offer a solution.
def update_widgets(num_ui_events_to_process=1):
    shell = get_ipython()
    # Ok to do nothing if running from console
    if shell is None:
        return
    kernel = shell.kernel
    events = []
    kernel.shell_handlers["execute_request"] = lambda *e: events.append(e)
    current_parent = (kernel._parent_ident, kernel._parent_header)

    for _ in range(num_ui_events_to_process):
        # ensure stdout still happens in the same cell
        kernel.set_parent(*current_parent)
        kernel.do_one_iteration()
        kernel.set_parent(*current_parent)

    kernel.shell_handlers["execute_request"] = kernel.execute_request

    def _replay_events(shell, events):
        kernel = shell.kernel
        sys.stdout.flush()
        sys.stderr.flush()
        for stream, ident, parent in events:
            kernel.set_parent(ident, parent)
            if kernel._aborting:
                kernel._send_abort_reply(stream, parent, ident)
            else:
                kernel.execute_request(stream, ident, parent)

    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.call_soon(lambda: _replay_events(shell, events))
    else:
        warn(
            "Automatic execution of scheduled cells only works with "
            "asyncio-based ipython"
        )
