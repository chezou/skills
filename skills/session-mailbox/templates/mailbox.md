# <topic>

**Roles**: <asking role> = <which session> / <answering role> = <which session>

**Done when**: <answering role> appends a section containing `LGTM`. (Only a condition written here counts.)

**Subject**: PR <number> <URL> / HEAD `<commit>` / base `<branch>` — or the question to decide.

**Rules** (session-mailbox skill): this file is the only channel — never a new file, chat, or a messaging API.
Write with `mailbox.py append <this file> --role <you> --re '<their role> <n>' --summary '<one line>'
--body-file -`; it numbers your section, appends at the end, and refuses a reply to a section the other side
has already moved past. Never edit existing lines. See `templates/example.md` for a worked round.
