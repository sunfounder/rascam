Initialize the Environment
=============================

Initialize the environment before playing the Rascam. The 
methods are as follows.

1. Change directory to /home/pi.

.. code-block::

    cd /home/pi/

.. note::

    cd, short for change directory is to change from the 
    current path to the intended directory. Informally, 
    here is to go to the path /home/pi/.

2. Clone the repository from github.

.. code-block::

    git clone https://github.com/sunfounder/rascam.git

3. Enter the folder rascam

.. code-block::

    cd /home/pi/rascam

4. Start up the initialization function.

.. code-block::

    sudo python3 setup.py install
    
.. note::

    This process may take some time, please do not turn 
    off the power.

5. The message appears after the installation is complete.

.. image:: media/image0.png
    :align: center
    :width: 450

Type Y to reboot Raspberry Pi.