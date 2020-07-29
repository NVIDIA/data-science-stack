# Custom Data Science Stack Environments

The default environment includes many commonly used libraries and is meant
to get users started quickly.
It is expected that users will create their own environments with additional
libraries, and slim down to only the libraries needed.

To create a fully pinned environment suitable for development, testing,
CI/CD, and for production a stable environment must be produced.

1. Create an `environments/FOO.env` file with the libraries wanted.
1. Run `data-science-stack pin FOO`
1. Examine the pinned.yaml file produced and copy to the environments:
1. `cp pinned.yaml environments/FOO.yaml`

Once pinned the environment can be used and shared without concerns
that library versions will change over time.

## Problems while pinning

Satisfying the constraings in your .env file may not be possible, in which
case the pin command will fail.

To make this (very common) problem easier to solve, the command to generate
the environment is printed right before the attempt to solve is made. Adding
an extra `-v` or `-vv` to the command will print more debug information,
including what constraints cannot be satisfied.

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
