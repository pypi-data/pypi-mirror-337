from enum import Enum, StrEnum


class YouTubeScopes(Enum):
    youtube_force_ssl = "https://www.googleapis.com/auth/youtube.force-ssl"
    youtube_readonly = "https://www.googleapis.com/auth/youtube.readonly"
    youtube_upload = "https://www.googleapis.com/auth/youtube.upload"
    youtube = "https://www.googleapis.com/auth/youtube"
    youtubepartner = "https://www.googleapis.com/auth/youtubepartner"


class GoogleCalendarScopes(Enum):
    calendar = "https://www.googleapis.com/auth/calendar"
    calendar_events = "https://www.googleapis.com/auth/calendar.events"
    calendar_settings_readonly = (
        "https://www.googleapis.com/auth/calendar.settings.readonly"
    )


class GoogleDriveScopes(Enum):
    metadata = "https://www.googleapis.com/auth/drive.metadata"
    files = "https://www.googleapis.com/auth/drive.file"
    drive = "https://www.googleapis.com/auth/drive"
    activity = "https://www.googleapis.com/auth/drive.activity"


class GMailScopes(StrEnum):
    send_emails = "https://www.googleapis.com/auth/gmail.addons.current.action.compose"
    action = "https://www.googleapis.com/auth/gmail.addons.current.message.action"
    message_metadata = (
        "https://www.googleapis.com/auth/gmail.addons.current.message.metadata"
    )
    message_readonly = (
        "https://www.googleapis.com/auth/gmail.addons.current.message.readonly"
    )
    labels = "https://www.googleapis.com/auth/gmail.labels"
    send = "https://www.googleapis.com/auth/gmail.send"
    readonly = "https://www.googleapis.com/auth/gmail.readonly"
    compose = "https://www.googleapis.com/auth/gmail.compose"
    insert = "https://www.googleapis.com/auth/gmail.insert"
    modify = "https://www.googleapis.com/auth/gmail.modify"
    metadata = "https://www.googleapis.com/auth/gmail.metadata"
    settings_basic = "https://www.googleapis.com/auth/gmail.settings.basic"
    settings_sharing = "https://www.googleapis.com/auth/gmail.settings.sharing"
    gmail = "https://mail.google.com/"
