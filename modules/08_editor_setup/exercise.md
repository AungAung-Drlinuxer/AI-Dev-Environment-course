# Module 08 — Editor Setup · Exercise များ

Exercise တိုင်းတွင် **လိုအပ်ချက်**၊ **လုပ်ရမည့် အဆင့်** နှင့် **အောင်မြင်မှု စစ်နည်း** ပါသည်။
အဖြေ ကို မကြည့်မီ ကိုယ်တိုင် လုပ်ပါ။ Lab ကို `python3 modules/08_editor_setup/lab.py` ဖြင့်
run ၍ မိမိ အဖြေနှင့် နှိုင်းယှဉ်နိုင်သည်။

## Exercise 1 — settings.json ကို စစ်ဆေးခြင်း

**လိုအပ်ချက်** — VS Code ၏ `settings.json` ကို parse လုပ်၍ AI အလုပ်အတွက် မဖြစ်မနေ လိုအပ်သည့် key
၅ ခု ပါ/မပါ နှင့် တန်ဖိုး မှန်/မမှန် ကို ဆုံးဖြတ်သည့် function တစ်ခု ရေးပါ။

**အဆင့်**

1. temporary directory တစ်ခု ဖန်တီးပြီး `settings.json` ဖိုင် တစ်ခု ရေးပါ။ ဖိုင်ထဲတွင် ဤ key များ
   ပါရမည် — `python.analysis.typeCheckingMode`၊ `editor.formatOnSave`၊ `editor.rulers`၊
   `notebook.output.scrolling`၊ `files.autoSave`။
2. `json.load` ဖြင့် ဖိုင် ကို ပြန်ဖတ်ပါ။
3. Key တစ်ခုချင်းစီအတွက် `[OK]`၊ `[MISSING]` သို့မဟုတ် `[MISMATCH]` လိုင်း ရိုက်ထုတ်ပါ။
4. ချို့နေသည့် key ရှိလျှင် `assert` ဖြင့် ရပ်ပါ။
5. `[OK] exercise_1 — settings.json key ၅ ခုကို စစ်ဆေးပြီးပါပြီ` လိုင်း ရိုက်ထုတ်ပါ။

**အောင်မြင်မှု စစ်နည်း** — `editor.rulers` သည် `[88, 120]` ဖြစ်ရမည်။ `editor.formatOnSave` သည်
`true` ဖြစ်ရမည်။ Key တစ်ခုကို ဖျက်ပြီး ပြန် run လျှင် `[MISSING]` လိုင်း ထွက်ရမည်။

## Exercise 2 — Extension စာရင်း နှိုင်းယှဉ်ခြင်း

**လိုအပ်ချက်** — လိုအပ်သည့် extension ID ၈ ခုကို `code --list-extensions` output နှင့် နှိုင်းယှဉ်၍
ချို့နေသည့် အရာ နှင့် ပိုနေသည့် အရာ ကို ခွဲထုတ်ပါ။

**အဆင့်**

1. `code --list-extensions` ကို တစ်ကြိမ် run ၍ output ကို ဖိုင် တစ်ခုထဲ သိမ်းပါ။
   (Lab တွင် ထို output ကို စာသား စာရင်း အဖြစ် တုပထားသည်။)
2. လိုအပ်သည့် ID စာရင်းကို အစဉ်လိုက် သတ်မှတ်ပါ — `ms-python.python`၊
   `ms-python.vscode-pylance`၊ `ms-toolsai.jupyter`၊ `eamodio.gitlens`၊
   `ms-vscode-remote.remote-ssh`၊ `ms-python.debugpy`၊ `ms-python.black-formatter`၊
   `charliermarsh.ruff`။
3. Installed စာရင်းကို `sorted()` လုပ်ပြီး ID တိုင်းအတွက် `required` သို့မဟုတ် `extra` ဟု မှတ်ပါ။
4. ချို့နေသည့် ID တိုင်းအတွက် `code --install-extension <id>` လိုင်း ထုတ်ပါ။
5. `[OK] exercise_2 — extension စာရင်း ၈ ခုကို နှိုင်းယှဉ်ပြီးပါပြီ` လိုင်း ရိုက်ထုတ်ပါ။

**အောင်မြင်မှု စစ်နည်း** — လိုအပ် ၈ ခုနှင့် installed အရေအတွက် ကို ပေါင်းလျှင် missing အရေအတွက်
ကို ကိုက်ရမည်။ `ms-python.debugpy` ကို ဖျက်ထားလျှင် missing စာရင်းထဲတွင် တွေ့ရမည်။

## Exercise 3 — Remote SSH host entry တည်ဆောက်ခြင်း

**လိုအပ်ချက်** — Alias၊ hostname၊ user နှင့် key လမ်းကြောင်း ပါသည့် `~/.ssh/config` host entry
တစ်ခုကို spec(dictionary)မှ တည်ဆောက်ပါ။

**အဆင့်**

1. `alias`၊ `hostname`၊ `user`၊ `identity_file`၊ `forward_agent` ပါသည့် dictionary တစ်ခု သတ်မှတ်ပါ။
2. အောက်ပါ ပုံစံအတိုင်း လိုင်း များ တည်ဆောက်ပါ —

   ```
   Host <alias>
       HostName <hostname>
       User <user>
       IdentityFile <identity_file>
       ForwardAgent <forward_agent>
   ```

3. လိုင်း တိုင်း ပါ/မပါ ကို `assert` ဖြင့် စစ်ပါ။
4. လိုင်း အရေအတွက် ၅ ဖြစ်ရမည်။
5. `[OK] exercise_3 — SSH host entry လိုင်း ၅ လိုင်း တည်ဆောက်ပြီးပါပြီ` လိုင်း ရိုက်ထုတ်ပါ။

**အောင်မြင်မှု စစ်နည်း** — တည်ဆောက်ထားသည့် စာသားကို `ssh <alias>` ဖြင့် စမ်းနိုင်သည်။
ဤ machine တွင် remote host အစစ် မရှိလျှင် `ssh -G <alias>` ဖြင့် ဖတ်လာသည့် တန်ဖိုး များကို
စစ်နိုင်သည်။

## Exercise 4 — Format-on-save မူဝါဒ

**လိုအပ်ချက်** — Language တစ်ခုချင်းစီအတွက် format-on-save ဖွင့်/ပိတ် နှင့် အသုံးပြုမည့် formatter
ကို ဆုံးဖြတ်သည့် function တစ်ခု ရေးပါ။

**အဆင့်**

1. Language စာရင်း သတ်မှတ်ပါ — `python`၊ `jsonc`၊ `markdown`၊ `dockerfile`၊ မသိသည့် language တစ်ခု။
2. `python` အတွက် `formatOnSave` ဖွင့်၍ `ms-python.black-formatter` ကို သတ်မှတ်ပါ။
3. `jsonc` နှင့် `markdown` အတွက် ပိတ်ထားပါ — comment ပါသည့် ဖိုင် နှင့် စာသား ဖိုင် ကို ကိုယ်တိုင်
   စီစဉ်သင့်သည်။
4. မသိသည့် language အတွက် ပိတ်ထား၍ `version အလိုက် ပြန်စစ်ရန် လိုသည်` ဟု မှတ်ပါ။
5. ဆုံးဖြတ်ချက် တိုင်းကို လိုင်း တစ်လိုင်းစီ ရိုက်ထုတ်ပြီး
   `[OK] exercise_4 — format-on-save မူဝါဒ ၅ မျိုးအတွက် ဆုံးဖြတ်ပြီးပါပြီ` လိုင်း ရိုက်ထုတ်ပါ။

**အောင်မြင်မှု စစ်နည်း** — VS Code တွင် Python ဖိုင် တစ်ခု ဖွင့်၍ နေရာ ပိုထည့်ပြီး သိမ်းပါ။ Black သည်
ထို လိုင်း ကို ပြန်ပြင်ရမည်။ မပြင်လျှင် `editor.formatOnSave` နှင့်
`[python]` scope setting ကို စစ်ပါ။

## Exercise 5 — Editor ရွေးချယ်မှု ဇယား

**လိုအပ်ချက်** — VS Code၊ Cursor၊ Windsurf နှင့် Neovim ကို လိုအပ်ချက် စာရင်း တစ်ခုနှင့်
နှိုင်းယှဉ်၍ အမှတ်ပေး အဆင့်သတ်ပါ။

**အဆင့်**

1. လိုအပ်ချက် နှင့် အလေးချိန် သတ်မှတ်ပါ — `remote_ssh_editing` ၃၊ `vscode_settings_compat` ၂၊
   `jupyter_support` ၂၊ `free_no_subscription` ၂၊ `builtin_ai_completion` ၁။
2. Editor တိုင်းအတွက် လိုအပ်ချက် တိုင်း ဖြည့်ဆည်း/မဖြည့်ဆည်း ကို boolean အဖြစ် သတ်မှတ်ပါ။
3. အမှတ် ပေါင်း၍ `(-score, editor)` အစဉ်ဖြင့် စီပါ။
4. ရလဒ် တိုင်းကို `<rank>. <editor> <score>/<max> — <note>` လိုင်းဖြင့် ရိုက်ထုတ်ပါ။
5. `[OK] exercise_5 — editor ၄ ခုကို လိုအပ်ချက် ၅ မျိုးနှင့် အဆင့်သတ်ပြီးပါပြီ` လိုင်း ရိုက်ထုတ်ပါ။

**အောင်မြင်မှု စစ်နည်း** — အလေးချိန် စုစုပေါင်း ၁၀ ဖြစ်ရမည်။ Cursor နှင့် Windsurf အမှတ် တူညီရမည်။
Neovim ၏ အမှတ်သည် VS Code ထက် နည်းရမည်။ အလေးချိန် ကို ပြောင်းလျှင် အဆင့် ပြောင်းနိုင်သည်ကို
သတိပြုပါ — ထို အချက်သည် အလေးချိန် ရွေးချယ်မှု၏ အကျိုးသက်ရောက်မှု ဖြစ်သည်။

## Exercise 6 — Setup အစီရင်ခံစာ

**လိုအပ်ချက်** — Exercise ၁–၅ ၏ ရလဒ် များကို စုစည်း၍ setup အခြေအနေ နှင့် exit code ကို
ဆုံးဖြတ်သည့် အစီရင်ခံစာ ထုတ်ပါ။

**အဆင့်**

1. စစ်ဆေးချက် ၅ ခု သတ်မှတ်ပါ — `settings.json`၊ extensions၊ remote-ssh entry၊ format-on-save၊
   editor choice။
2. စစ်ဆေးချက် တိုင်းအတွက် `[PASS]` သို့မဟုတ် `[FAIL]` နှင့် အသေးစိတ် လိုင်း ရိုက်ထုတ်ပါ။
3. အောင်မြင်သည့် အရေအတွက် နှင့် စုစုပေါင်း ကို `passed/total` အဖြစ် ပြပါ။
4. အားလုံး အောင်မြင်လျှင် `READY` နှင့် exit code `0`၊ မဟုတ်လျှင် `INCOMPLETE` နှင့် exit code `1`
   ဆုံးဖြတ်ပါ။
5. လုပ်ရန် ကျန်သည့် command ကို လိုင်း တစ်လိုင်းဖြင့် ဖော်ပြပါ။
6. `[OK] exercise_6 — setup အစီရင်ခံစာ (5/5) ထုတ်ပြီးပါပြီ` လိုင်း ရိုက်ထုတ်ပါ။

**အောင်မြင်မှု စစ်နည်း** — `python3 modules/08_editor_setup/lab.py` သည် exit code 0 ဖြင့်
ဆုံးပြီး နောက်ဆုံး လိုင်းတွင် `[PASS] All 6/6 exercises passed successfully.` ထွက်ရမည်။
Exercise တိုင်း၏ `[OK] exercise_N — …` လိုင်း ၆ လိုင်း ထွက်ရမည်။
