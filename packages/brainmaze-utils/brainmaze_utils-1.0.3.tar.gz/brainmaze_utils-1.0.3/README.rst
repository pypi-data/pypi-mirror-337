
BrainMaze: Brain Electrophysiology, Behavior and Dynamics Analysis Toolbox - Utils
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

This toolbox provides a generic tools for the BrainMaze package. This tool was separated from the BrainMaze toolbox to support a convenient and lightweight sharing of these tools across projects.

This project was originally developed as a part of the `BEhavioral STate Analysis Toolbox (BEST) <https://github.com/bnelair/best-toolbox>`_ project. However, the development has transferred to the BrainMaze project.


Documentation
"""""""""""""""

Documentation is available `here <https://bnelair.github.io/brainmaze_utils>`_.


Installation
"""""""""""""""""""""""""""

.. code-block:: bash

    pip install brainmaze-utils

How to contribute
"""""""""""""""""""""""""""
The project has 2 main protected branches *main* that contains official software releases and *dev* that contains the latest feature implementations shared with developers.
To implement a new feature a new branch should be created from the *dev* branch with name pattern of *developer_identifier/feature_name*.

After the feature is implemented, a pull request can be created to merge the feature branch into the *dev* branch with. Pull requests need to be reviewed by the code owners.
Drafting of new releases will be performed by the code owners in using pull request from *dev* to *main* and drafting a new release on GitHub.

New functions need to be implemented with Sphinx compatible docstrings. The documentation is automatically generated from the docstrings using Sphinx using make_docs.sh either calling its contents.
Documentation source is in docs_src/ and the generated documentation is in docs/. .doctrees is not shared in the repository.

Troubleshooting
''''''''''''''''''''''''''''''

If updating the docs web generated using sphinx, there might be a lot of changes resulting in a buffer hang up. Using SSH over HTTPS is preferred. If you are using HTTPS, you can increase the buffer size by running the following command:

.. code-block:: bash

    git config http.postBuffer 524288000


License
""""""""""""""""""

This software is licensed under BSD-3Clause license. For details see the `LICENSE <https://github.com/bnelair/brainmaze_utils/blob/master/LICENSE>`_ file in the root directory of this project.


Acknowledgment
"""""""""""""""""""""""""""
This code was developed and originally published for the first time with by (Mivalt 2022, and Sladky 2022).
We appreciate you citing these papers when utilizing this toolbox in further research work.

 | F. Mivalt et V. Kremen et al., “Electrical brain stimulation and continuous behavioral state tracking in ambulatory humans,” J. Neural Eng., vol. 19, no. 1, p. 016019, Feb. 2022, doi: 10.1088/1741-2552/ac4bfd.
 |
 | V. Sladky et al., “Distributed brain co-processor for tracking spikes, seizures and behaviour during electrical brain stimulation,” Brain Commun., vol. 4, no. 3, May 2022, doi: 10.1093/braincomms/fcac115.


