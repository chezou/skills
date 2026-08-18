# <topic>

**Roles**: <asking role> = <which session> / <answering role> = <which session>

**Done when**: <answering role> appends a section containing `LGTM`. (Only a condition written here counts.)

**Subject**: PR <number> <URL> / HEAD `<commit>` / base `<branch>` — or the question to decide.

**Rules** (session-mailbox skill): this file is the only channel — never a new file, chat, or a messaging API.
Append at the end, never edit existing lines. Start each append with `## <role> <n>: <one-line summary>` and
put `Re: <role> <n>` (or `New`) on its first line. Re-count the other side's sections right before you write;
if the count grew, read those first and answer in one append. See `templates/example.md` for a worked round.
