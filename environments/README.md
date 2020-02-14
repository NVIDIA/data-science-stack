# Data Science Stack Environments

## File Format

The file is part of the command used by the `data-science-stack` script to
generate pinned configurations.
The file should contain only the channels and packages, one per line.
Packages with version restictions should have double quotes around them.

    -c channel-1
    -c channel-2
    ...
    -c channel-n
    channel::package-1
    channel::package-2
    "channel::package-3==1.0.0"
    "channel::package-4<2.0"
    ...
    channel::package-n

See `data-science-stack.env` for an example.
