"""Placeholder package for keyed-extras sponsorware.

This is NOT the real package! Visit https://dougmercer.github.io/keyed/extras/ for more info.
"""

import sys
import warnings

WARNING_MESSAGE = """
=================================================================
WARNING: This is NOT the real keyed-extras package!
=================================================================

You have installed the placeholder package for keyed-extras.
The real package is only available to sponsors.

To access the real keyed-extras package:
1. Become a sponsor at: https://dougmercer.github.io/keyed/extras/
2. Follow the installation instructions to configure pip with 
   the correct `--extra-index-url`.

=================================================================
"""

# Print the warning and also raise a warning
print(WARNING_MESSAGE, file=sys.stderr)
warnings.warn(WARNING_MESSAGE, UserWarning)

# Create stub function that will be imported when people try to use common functions from the package
def not_available(*args, **kwargs):
    """Function that raises an error when any functionality is attempted to be used."""
    raise ImportError(
        "This functionality requires the full keyed-extras package. "
        "Please visit https://dougmercer.github.io/keyed/extras/ "
        "to become a sponsor and gain access."
    )

# Simulate the expected exports from the real package
# List these based on what would be in the real package
post_process_tokens = not_available
FreeHandContext = not_available
Editor = not_available
# Add any other expected exports from your real package

# Don't expose anything else
__all__ = ["post_process_tokens", "FreeHandContext", "Editor"]
