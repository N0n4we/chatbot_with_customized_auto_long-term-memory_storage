import os

class Memo:
    def __init__(self):
        self.events = None
        self.moodAndReasons = None
        self.relationship = None
        self.selfImage = None
        self.thoughts = None
        self.userCharacter = None
        self.userInfo = None

class Prompt:
    def __init__(self):
        self.eventsRevision = None
        self.memoCompress = None
        self.memoEnsemble = None
        self.moodRevision = None
        self.overthinking = None
        self.relationshipRevision = None
        self.selfImageRevision = None
        self.userCharacterRevision = None
        self.userInfoRevision = None
        self.whetherSearchDatabase = None  # Not in use

class Setting:
    def __init__(self):
        self.chatbotCharacter = None
        self.chatbotName = None
        self.userName = None  # Not in use

class DataAccess:
    def __init__(self, dataPath) -> None:
        self.memo = Memo()
        self.prompt = Prompt()
        self.setting = Setting()

        memoPath = os.path.join(dataPath, "memo")
        promptPath = os.path.join(dataPath, "prompt")
        settingPath = os.path.join(dataPath, "setting")

        # Read all files from the memo folder
        with open(os.path.join(memoPath, "Events"), mode='r', encoding="utf-8") as file:
            self.memo.events = file.read()
        with open(os.path.join(memoPath, "MoodAndReasons"), mode='r', encoding="utf-8") as file:
            self.memo.moodAndReasons = file.read()
        with open(os.path.join(memoPath, "Relationship"), mode='r', encoding="utf-8") as file:
            self.memo.relationship = file.read()
        with open(os.path.join(memoPath, "SelfImage"), mode='r', encoding="utf-8") as file:
            self.memo.selfImage = file.read()
        with open(os.path.join(memoPath, "Thoughts"), mode='r', encoding="utf-8") as file:
            self.memo.thoughts = file.read()
        with open(os.path.join(memoPath, "UserCharacter"), mode='r', encoding="utf-8") as file:
            self.memo.userCharacter = file.read()
        with open(os.path.join(memoPath, "UserInfo"), mode='r', encoding="utf-8") as file:
            self.memo.userInfo = file.read()

        # Read all files from the prompt folder
        with open(os.path.join(promptPath, "EventsRevision"), mode='r', encoding="utf-8") as file:
            self.prompt.eventsRevision = file.read()
        with open(os.path.join(promptPath, "MemoCompress"), mode='r', encoding="utf-8") as file:
            self.prompt.memoCompress = file.read()
        with open(os.path.join(promptPath, "MemoEnsemble"), mode='r', encoding="utf-8") as file:
            self.prompt.memoEnsemble = file.read()
        with open(os.path.join(promptPath, "MoodRevision"), mode='r', encoding="utf-8") as file:
            self.prompt.moodRevision = file.read()
        with open(os.path.join(promptPath, "Overthinking"), mode='r', encoding="utf-8") as file:
            self.prompt.overthinking = file.read()
        with open(os.path.join(promptPath, "RelationshipRevision"), mode='r', encoding="utf-8") as file:
            self.prompt.relationshipRevision = file.read()
        with open(os.path.join(promptPath, "SelfImageRevision"), mode='r', encoding="utf-8") as file:
            self.prompt.selfImageRevision = file.read()
        with open(os.path.join(promptPath, "UserCharacterRevision"), mode='r', encoding="utf-8") as file:
            self.prompt.userCharacterRevision = file.read()
        with open(os.path.join(promptPath, "UserInfoRevision"), mode='r', encoding="utf-8") as file:
            self.prompt.userInfoRevision = file.read()
        with open(os.path.join(promptPath, "WhetherSearchDatabase"), mode='r', encoding="utf-8") as file:
            self.prompt.whetherSearchDatabase = file.read()

        # Read all files from the setting folder
        with open(os.path.join(settingPath, "ChatbotCharacter"), mode='r', encoding="utf-8") as file:
            self.setting.chatbotCharacter = file.read()
        with open(os.path.join(settingPath, "ChatbotName"), mode='r', encoding="utf-8") as file:
            self.setting.chatbotName = file.read()
