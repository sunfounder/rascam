Start On Boot 
=================

Modify crontab to make Rascam start the camera program 
on boot. Steps are:

1. Run the command.

.. code-block::

    sudo crontab -e

.. note::
    
    At the first time you execute the command, you need to select an editor and then choose nano.

2. Input the following content at the end of the file.

.. code-block::

    @reboot python3 /home/pi/rascam/example/take_picture.py 

.. note::
    
    This is the example of starting on boot (it can be 
    modified to others). If you want to cancel the “start 
    on boot”, back to the file and delete this line.

3. Then save and exit and you should see the message.

.. code-block::

    crontab: installing new crontab

4. Reboot.

.. code-block::

    sudo reboot