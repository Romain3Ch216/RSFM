Remote Sensing for Forest Monitoring @ AgroParisTech - 2026 ATHENS week
=======================================================================

Welcome to the lectures and tutorials on **Remote Sensing for Forest Monitoring** organized at **AgroParisTech**
as part of the **2026 ATHENS week** (https://athensnetwork.eu/athens-programme.html).
It is under construction, and we expect some bugs and issues. 
Feel free to send feedback at romain dot thoreau at agroparistech dot fr.


Learning Objectives
-------------------

The course will cover theoretical concepts of **remote sensing using optical imagery** ranging from the
visible to the short-wavelength infrared (0.4 µm–2.5 µm) with a focus on the **practical processing of
satellite images to detect tree dieback** caused by bark beetle infestations.

By the end of the week, you will be able to:
   * Select optical remote sensing data suitable for a given application,
   * Process optical satellite images using specialized Python libraries,
   * Design and implement a data processing pipeline to automatically detect tree dieback.


Schedule (First edition, 2026)
----------------------------------------

+---------------------------+----------------+--------------------------------------------------------------------------+
| **Date**                  |                | **Lectures / Tutorials**                                                 |
+===========================+================+==========================================================================+
| Monday, 16. Nov 2026      | 08:30–11:45    | Introduction to remote sensing and radiative transfer modeling           |
+---------------------------+----------------+--------------------------------------------------------------------------+
|                           | 13:30–16:45    | Practical work                                                           |
+---------------------------+----------------+--------------------------------------------------------------------------+
| Tuesday, 17. Nov 2026     | 08:30–11:45    | Leaf traits inversion from satellites images - practical work            |
+---------------------------+----------------+--------------------------------------------------------------------------+
|                           | 13:30–16:45    | Satellite image co-registration - practical work                         |
+---------------------------+----------------+--------------------------------------------------------------------------+
| Wednesday, 18. Nov 2026   | 08:30–11:45    | Anomaly detection for forest monitoring - start of the projects          |
+---------------------------+----------------+--------------------------------------------------------------------------+
|                           | 13:30–16:45    | Group work outside class                                                 |
+---------------------------+----------------+--------------------------------------------------------------------------+
| Thursday, 19. Nov 2026    | 08:30–11:45    | Project in class                                                         |
+---------------------------+----------------+--------------------------------------------------------------------------+
|                           | 13:30–16:45    | Group work outside class                                                 |
+---------------------------+----------------+--------------------------------------------------------------------------+
| Friday, 20. Nov 2026      | 08:30–11:45    | Project in class                                                         |
+---------------------------+----------------+--------------------------------------------------------------------------+
|                           | 13:30–16:45    | Team presentation of the projects                                        |
+---------------------------+----------------+--------------------------------------------------------------------------+
Lectures
----------

- `Introduction to remote sensing and radiative transfer modeling <https://raw.githubusercontent.com/Romain3Ch216/RSFM/main/docs/lectures/introduction_optical_remote_sensing/intro.pdf>`_
- `Tree dieback detection from multispectral satellite image time series <https://raw.githubusercontent.com/Romain3Ch216/RSFM/main/docs/lectures/tree_dieback_detection/tree_dieback_detection.pdf>`_

.. toctree::
   :caption: Tutorials
   :maxdepth: 1

   tutorials/basics_radiative_transfer_modeling/basics_radiative_transfer_modeling.ipynb
   tutorials/leaf_traits_inversion/leaf_traits_inversion.ipynb

The material for the tutorials is available here: https://fichiers.numerique.gouv.fr/explorer/items/c34458d1-a27c-459f-ab82-e4abfb75281d

Evaluation
----------

In groups of two or three, you will design and implement a data processing pipeline to detect tree dieback caused by bark beetle infestations.
On the last day, you will present to the class the methodological choices underlying your anomaly detection pipeline.

Python installation
-------------------


1. **Install Miniconda (all platforms)**

Download and install Miniconda: https://www.anaconda.com/docs/getting-started/installation

- **Windows:** run the ``.exe`` installer. During installation, it is recommended to check "Add Miniconda3 to my PATH environment variable" (otherwise, always launch conda from the **Anaconda Prompt (miniconda3)** from the Start menu).
- **macOS:** run the ``.pkg`` installer, or use the shell installer in a terminal (``bash Miniconda3-latest-MacOSX-x86_64.sh`` for Intel, ``Miniconda3-latest-MacOSX-arm64.sh`` for Apple Silicon).
- **Linux:** run the shell installer (``bash Miniconda3-latest-Linux-x86_64.sh``), then restart your terminal.

After installation, open:

- **Windows:** the *Anaconda Prompt (miniconda3)* (or a terminal if you added conda to PATH).
- **macOS / Linux:** your terminal (Terminal.app on macOS).

2. **Create a virtual environment**

In your terminal, run:

.. code-block:: bash

   conda create -n ucathens python=3.14.8


See the conda environments guide for further details: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html.

3. **Download the requirements.txt**

Download the file ``requirements.txt`` in the `project` folder at https://fichiers.numerique.gouv.fr/explorer/items/c34458d1-a27c-459f-ab82-e4abfb75281d and place it in your project folder.

4. **Go to your project folder**

.. code-block:: bash

   cd path/to/project

- **Windows:** in ``cmd`` use backslashes (``cd C:\Users\you\project``); in PowerShell or Anaconda Prompt both ``/`` and ``\`` work.
- **macOS / Linux:** ``cd /Users/you/project`` (macOS) or ``cd /home/you/project`` (Linux).

Tip: you can type ``cd `` then drag and drop the folder into the terminal window (works on Windows, macOS and Linux).

5. **Install the dependencies**

Still in your terminal, run:

.. code-block:: bash

   conda activate ucathens
   pip install -r requirements.txt

- **Windows:** if ``conda activate`` is not recognized, first run ``conda init``, close and reopen the Anaconda Prompt, then try again.
- **macOS / Linux:** if ``conda activate`` is not recognized, first run ``conda init`` (or ``source ~/miniconda3/bin/activate``), close and reopen the terminal, then try again.

Your terminal should now show ``(ucathens)`` before the command line, confirming the environment is active.
