# WhatsApp YT Downloader API

WhatsApp YT Downloader API is a versatile tool designed to facilitate the management and downloading of YouTube videos programmatically via WhatsApp. It allows users to obtain download links for any YouTube video directly within the WhatsApp chat interface.

## Features

### 1. Get Download Links
- Get download links of any YouTube video using this API with your custom video link: `https://current-domain.com/downloadyt?urlyt={link}`
- Request should be GET. You can use a browser or other methods to make a request.

### 2. Automated Response
- Download the AutoResponder app from Play Store or App Store.
- Configure the app to connect to `http://current-domain.com` in the "Connect to Web Server" option.
- Start AutoResponder for WhatsApp to automatically respond to every message received on WhatsApp.
- Every message received on WhatsApp will get an auto response. If someone sends a YouTube video link, they will receive direct video and audio download links.

## Usage

1. Send a message containing the YouTube video link to the designated WhatsApp number.
2. Receive an automated response with download links for the video and audio formats.

## For Developers

### Dependencies
- aiohttp
- pytube
- wikipedia
- requests

### Development Setup
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Get inside of project dir `cd jufflers-bot`.
4. Run the application using `python server.py`.

### Additional Information
- Utilizes pytube Python library for downloading YouTube streams.
- Provides seamless integration with WhatsApp for easy access to download links.
- Enables users to automate the process of obtaining YouTube video download links via WhatsApp.
- This project is not maintained any more.

For any inquiries or issues, feel free to contact the developer on Telegram at https://t.me/juffler.
