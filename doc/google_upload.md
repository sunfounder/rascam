## Google Drive API
### step 1 download client configuration
Enter https://developers.google.com/drive/api/v3/quickstart/python ,Login account then click the (Enable the Drive API) button to open Google Drive API service.Select default option 'desktop app',Click (download client configuration) to download the file name credentials.json,This file is very important. For authentication, it should be placed in the same folder as the code.

### step 2 Verify Google account
The first time you upload a picture, you need to log in to Google account for verification, so you need to connect the screen and keyboard to run the command in raspberry pi 
```bash
python3 take_picture_and_upload.py
```
After running, it will pop out of the local browser to log in to Google account and follow the steps
