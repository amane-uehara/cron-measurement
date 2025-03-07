import datetime
import os.path
import pytz
import json
import sys
import gzip

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def fetch_json(config):
  creds = None
  savefile              = config["savefile"]
  token_json_path       = config["token_json_path"]
  credentials_json_path = config["credentials_json_path"]
  start_yyyymmddhhmmss  = config["start_yyyymmddhhmmss"]
  end_yyyymmddhhmmss    = config["end_yyyymmddhhmmss"]

  # 既にトークンファイルがあれば読み込む
  if os.path.exists(token_json_path):
    creds = Credentials.from_authorized_user_file(token_json_path, SCOPES)

  # 有効なクレデンシャルがない場合は、OAuthフローを実行
  # (既に token.json があるなら、通常ここはスキップされる)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(credentials_json_path, SCOPES)
      creds = flow.run_console()

  # 取得した認証情報を保存
  with open(token_json_path, "w") as token:
    token.write(creds.to_json())

  tz = pytz.timezone("Asia/Tokyo")
  start_time = datetime.datetime.strptime(start_yyyymmddhhmmss, "%Y%m%d%H%M%S").replace(tzinfo=tz)
  end_time = datetime.datetime.strptime(end_yyyymmddhhmmss, "%Y%m%d%H%M%S").replace(tzinfo=tz)

  ret = []
  # ここから Google Calendar API を利用
  try:
    service = build("calendar", "v3", credentials=creds)

    # カレンダーリストを取得
    calendar_list = service.calendarList().list().execute()
    for cal in calendar_list['items']:
      calendar_name = cal['summary']
      calendar_id   = cal['id']

      # イベント一覧を取得
      events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy="startTime"
      ).execute()

      events = events_result.get("items", [])

      for event in events:
        start   = event["start"].get("dateTime", event["start"].get("date"))
        end     = event["end"].get("dateTime", event["end"].get("date"))
        summary = event.get("summary", "")
        ret.append(
          {
            "calendar": calendar_name,
            "summary":  summary,
            "start":    start,
            "end":      end,
          }
        )

  except HttpError as error:
    print(f"An error occurred: {error}")
    ret.append({"calendar":"error", "summary":"error"})

  with gzip.open(savefile, mode='wt') as f:
    f.write(json.dumps(ret, indent=2, separators=(',',':'), ensure_ascii=False))

  sys.exit()


def key_list():
  return []


if __name__ == "__main__":
  data = fetch_json({})
