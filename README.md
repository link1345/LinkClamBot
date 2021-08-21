# LinkClamBot
A DiscordBot for managing a game's clans, with features such as recording participation time in voice channels, voting, and teaming.

Features include :
	VoiceChennel Monitoring

	MemberList (GoogleSheet)


# Download 

```
git clone https://github.com/link1345/LinkClamBot.git
```

# Config Setting

sample-\*.py と付くファイルの中に

「 **** Configure to your environment. **** 」

という表記がある欄を、自分の環境に合わせて記入。

その後、sample-\*.pyと言う名前を、\*.pyに変更し保存。

# RUN 

```
docker-compose up --build
```

# Bot Command

全て、最初にボットの表示名(DisplayName)から始まります。

例：hogeBotという名前のボットなら、「hogeBot,help」という形になります。

## VoiceChennel Monitoring

### (BotName)、ログ取得したい

csvかjson(raw)形式でのボイスチャンネル監視データが取得できます。

### (BotName)、自分の参加時間は？
自分が、１か月間ボイスチャンネルの参加時間が取得できます。

## MemberList (GoogleSheet)

### (BotName)、自分の名簿情報を変更する

自分のGoogleSheetの名簿の情報を変更できます。

### (BotName)、名簿の置き場所を教えて

名簿のURLを教えてくれます。

### (BotName)、上位権限で名簿情報を変更する

他のユーザーをの名簿情報を変更できます。

### (BotName)、名簿整合性チェック

名簿に登録されているdiscord情報の更新が行えます。

※ このコマンドは、名簿の情報に、問題がある際の使用を前提としています。


# Description is CommandSetting.py 

## "channelID"

Botが対応するテキストチャンネルを指定します。

## "role"
Botが対応するロールを指定します。
