Check Photos
=================

Samba helps when you share and other devices access 
your photo album. Steps:

1. Run the command to set up Samba service.

.. code-block::

    sudo apt-get update
    sudo apt-get install samba samba-common-bin

2. Configure Samba typing.

.. code-block::

    sudo nano /etc/samba/smb.conf

.. note::
    
    Press ctrl+o to save what you modify in nano editor, ctrl+x to to exit.

Input the following content at the end of the file:

.. code-block::

    [share] 
    path = /home/pi/Pictures/rascam_picture_file #This is your album path.
    valid users = pi 
    browseable = yes 
    public = yes 
    writable = yes 

3. Restart Samba service.

.. code-block::

    sudo service smbd restart


4. Add sharing account.

.. code-block::

    sudo smbpasswd -a pi

.. note::
    
    A sharing account \"pi\" is created and you need to set your passcode.
