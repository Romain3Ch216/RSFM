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
   * Select and apply an anomaly detection method for forest monitoring.


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

.. toctree::
   :caption: Tutorials
   :maxdepth: 1

   tutorials/basics_radiative_transfer_modeling/basics_radiative_transfer_modeling.ipynb
   tutorials/leaf_traits_inversion/leaf_traits_inversion.ipynb

Evaluation
----------

In groups of two or three, you will design and implement a data processing pipeline to detect tree dieback.
You will select and implement an anomaly detection method calibrated on a given geographic area, and assess the
performance of the method on other geographic areas.