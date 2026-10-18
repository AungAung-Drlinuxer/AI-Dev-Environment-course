# Exercise — Module 01 (Dev Environment)

ဤ exercise ၆ ခုကို `modules/01_dev_environment/lab.py` တွင် `def exercise_1()` မှ `def exercise_6()` အထိ
တည်ဆောက်ရမည်။ Lab သည် **offline နှင့် deterministic** ဖြစ်ရမည် — Python standard library သာ သုံးရမည်;
network၊ Docker၊ GPU နှင့် download မလိုအပ်ပါ။ Exercise တိုင်းသည် လူဖတ်နိုင်သည့် ရလဒ်ကို print ရမည်၊
ထို့နောက် `[OK] exercise_N — <အတိုချုပ်>` လိုင်း ထုတ်ရမည်။ ဖိုင်အဆုံးတွင်
`[PASS] All 6/6 exercises passed successfully.` ပေါ်ပြီး exit code `0` ဖြစ်ရမည်။

လိုအပ်သည့် အနည်းဆုံး version နှင့် ပြုပြင်ရန် command တိုင်းကို source lesson ၏ `code/verify.py`
preflight script မှ ယူရမည် — Python `3.11+`၊ Node.js `20+`၊ ထို့နောက် `uv python install 3.12` နှင့်
`fnm install 22`။

---

## Exercise 1 — Tool Manifest ကို အနည်းဆုံး Version နှင့် နှိုင်းယှဉ်ခြင်း

### လိုအပ်ချက်

Machine နှစ်ခု၏ tool manifest ကို ကိုယ်စားပြုသည့် စာရင်း တစ်ခု တည်ဆောက်ပြီး entry တိုင်းကို
အနည်းဆုံး version နှင့် နှိုင်းယှဉ်ရမည်။ Entry တိုင်းတွင် tool အမည်၊ version လိုင်း နှင့် path ပါရမည်။
Python သည် `3.11+`၊ Node.js သည် `20+` ဖြစ်ရမည်; `git`၊ `npx` နှင့် `cargo` တွင် အနည်းဆုံး version
သတ်မှတ်ချက် မရှိပါ။ မအောင်မြင်သည့် entry တိုင်းအတွက် source ၏ ပြုပြင် command ကို `Fix:` လိုင်းအဖြစ်
ပြရမည်။

### လုပ်ရမည့် အဆင့်

1. `verify.py` ၏ `command_result()` နည်းလမ်းအတိုင်း version လိုင်းမှ ဂဏန်း အုပ်စုများကို ထုတ်ယူသည့်
   `parse_version()` helper ရေးပါ — ဂဏန်း မဟုတ်သည့် အက္ခရာ တိုင်းကို space အဖြစ် ပြောင်းပြီး ကျန်သည့်
   ဂဏန်း အုပ်စုများကို integer အဖြစ် ဖတ်သည်။
2. `MINIMUM_VERSIONS = {"python": (3, 11), "node": (20,)}` ကဲ့သို့ အနည်းဆုံး version ဇယား သတ်မှတ်ပါ။
3. Machine တစ်ခုစီအတွက် entry တိုင်းကို စစ်ပြီး `[PASS]` သို့မဟုတ် `[FAIL]` ကို label၊ detected version နှင့်
   path နှင့်အတူ print ပါ။ `[FAIL]` ဖြစ်ပါက `Fix:` လိုင်း ထပ်ထည့်ပါ။
4. Function သည် `{machine: {"passed": n, "failed": [...]}}` ပုံစံ ရလဒ် ပြန်ရမည်။
5. Assert ဖြင့် စစ်ပါ — machine တစ်ခုသည် entry အားလုံး အောင်ရမည်; machine တစ်ခုသည် Python နှင့်
   Node.js ကို `failed` အဖြစ် တင်ရမည်။

### အောင်မြင်မှု စစ်ဆေးနည်း

`python3 modules/01_dev_environment/lab.py` ကို run ပြီး `[exercise_1]` အောက်တွင် `[FAIL]` entry နှစ်ခု
(Python နှင့် Node.js) နှင့် `Fix:` လိုင်း နှစ်လိုင်း ပေါ်ခြင်း၊ ကျန်စာရင်းတွင် `[PASS]` သာ ပေါ်ခြင်းကို စစ်ပါ။
ထို့နောက် `[OK] exercise_1` လိုင်း ပေါ်ရမည်။

---

## Exercise 2 — Four-Layer Stack ထဲ Component ခွဲခြားခြင်း

### လိုအပ်ချက်

Component ၁၆ ခုကို အလွှာ ၄ လွှာ — `1 System Foundation`၊ `2 Package Managers`၊ `3 Language Runtimes`၊
`4 AI/ML Libraries` — ထဲ ခွဲခြားရမည်။ ခွဲခြားမှုသည် source ဖော်ပြသည့် အမည်စာရင်းမှ ဆင်းသက်သည့်
သတ်မှတ်ချက် ဖြစ်ရမည်; မသိသည့် component ကို မှန်းဆခြင်း မပြုရ — `UNKNOWN` အဖြစ် သတ်မှတ်ရမည်။

### လုပ်ရမည့် အဆင့်

1. အလွှာ တိုင်း၏ အမည်စာရင်းကို ဇယားအဖြစ် ရေးပါ — `1` တွင် OS၊ shell၊ git၊ editor၊ GPU drivers;
   `2` တွင် uv၊ pnpm၊ cargo၊ juliaup; `3` တွင် Python 3.11+၊ Node 20+၊ Rust၊ Julia;
   `4` တွင် PyTorch၊ JAX၊ transformers။
2. ထို ဇယားမှ keyword စည်းမျဉ်း (`LAYER_RULES`) ကို အစဉ်လိုက် တည်ဆောက်ပါ — `juliaup` သည် `julia`
   မတိုင်မီ၊ `cargo` သည် manager အလွှာတွင် ရှိရမည်။
3. Component အမည်ကို lowercase ပြောင်းပြီး အက္ခရာ/ဂဏန်း မဟုတ်သည့် စာလုံးများကို ဖယ်ကာ
   (`VS Code (editor)` → `vscodeeditor`) စည်းမျဉ်းနှင့် တိုက်ဆိုင်စစ်ပါ။
4. Component တိုင်းအတွက် `[ok]`၊ `[MISMATCH]` သို့မဟုတ် `[UNKNOWN]` ကို အလွှာ အမည်နှင့်တကွ print ပါ;
   အလွှာ တိုင်း၏ အရေအတွက်ကိုလည်း စုစည်း ပြပါ။
5. Assert ဖြင့် `unknown == []` နှင့် အလွှာ တိုင်း၏ အရေအတွက် `5 / 4 / 4 / 3` ဖြစ်ခြင်းကို စစ်ပါ။

### အောင်မြင်မှု စစ်ဆေးနည်း

`[exercise_2]` အပိုင်းတွင် `[UNKNOWN]` သုည ဖြစ်ခြင်း၊ `[MISMATCH]` သုည ဖြစ်ခြင်း၊ စုစည်းချက်
`classified: 16/16; unknown: 0` ပေါ်ခြင်းကို စစ်ပါ။ အလွှာ ၄ လွှာ၏ အရေအတွက်သည် 5၊ 4၊ 4၊ 3 ဖြစ်ရမည်။

---

## Exercise 3 — Route တိုင်းအတွက် Probe စာရင်း ထုတ်ခြင်း

### လိုအပ်ချက်

Route သုံးခု — `beginner`၊ `node`၊ `rust` — အတွက် လိုအပ်သော (required) probe နှင့် နောက်ပိုင်း အချိန်ထိ
ရွှေ့နိုင်သည့် (optional) probe စာရင်းကို ထုတ်ရမည်။ Source ၏ preflight သည် ရွေးထားသည့် route အတွက်
လိုအပ်သည့် အရာကိုသာ စစ်ပြီး နောက်ပိုင်း tool များကို ကျော်သည်။

### လုပ်ရမည့် အဆင့်

1. `verify.py` ၏ `ROUTES` နှင့် `BASE_OPTIONAL` မှ requirement စာရင်း ကို ကူးယူပါ —
   `beginner` တွင် `("python", "git")`၊ `agent-skills` route တွင် `("python", "git", "node", "npx")` ဖြစ်သည်။
2. Route သည် label၊ required tuple၊ optional tuple နှင့် next command ကို သိမ်းရမည်။
3. Route တိုင်းအတွက် `probe / timing / fix if it fails` ဇယား ပုံစံ print ပါ; ပြီးနောက်
   `Later checks skipped: N tools are not needed to start.` လိုင်း ထုတ်ပါ။
4. `beginner` route ၏ next command ကို source အတိုင်း တိတိကျကျ ထည့်ပါ —
   `python3 phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py`။
5. Assert ဖြင့် route သုံးခု၏ required စာရင်းကို စစ်ပါ — `beginner` တွင် probe ၂ ခု၊ `node` တွင် ၄ ခု၊
   `rust` တွင် ၃ ခု ရှိရမည်။

### အောင်မြင်မှု စစ်ဆေးနည်း

`[exercise_3]` အပိုင်းတွင် route သုံးခု ပေါ်ခြင်း၊ route တိုင်းတွင် required လိုင်းများက `optional` လိုင်း
များထက် အရင် ပေါ်ခြင်း၊ နှင့် `Later checks skipped:` လိုင်း သုံးလိုင်း ပေါ်ခြင်းကို စစ်ပါ။ `[OK]
exercise_3` လိုင်း ပေါ်ရမည်။

---

## Exercise 4 — `.env` ဖိုင်ကို Value မပြဘဲ စစ်ခြင်း

### လိုအပ်ချက်

`.env` ဖိုင်ကို parse လုပ်ပြီး key တိုင်း၏ အခြေအနေကို `SET`၊ `EMPTY` သို့မဟုတ် `MISSING` အဖြစ်
သတ်မှတ်ရမည်။ **Key ၏ value ကို လုံးဝ မပြရ** — API key များသည် log ထဲ မရောက်ရ။

### လုပ်ရမည့် အဆင့်

1. ဖိုင်လိုင်း တိုင်းကို စစ်ပါ — အလွတ်လိုင်း၊ `#` ဖြင့် စသည့် လိုင်းနှင့် `=` မပါသည့် လိုင်း ကို ကျော်ပါ။
2. `=` ကို ပထမဆုံး တွေ့သည့်နေရာတွင် ခွဲပါ (`partition("=")`)။ Key နှင့် value ကို `strip()` လုပ်ပါ။
3. Value သည် single သို့မဟုတ် double quote ဖြင့် ခြုံထားပါက quote ကို ဖယ်ပြီး အတွင်းစာကို ယူပါ;
   `~` ကဲ့သို့ path ကို မပြောင်းရ။
4. Required key စာရင်း (`ANTHROPIC_API_KEY`၊ `OPENAI_API_KEY`၊ `HF_TOKEN`) အတွက် အခြေအနေကို
   print ပါ; ဖိုင်တွင် ပါသော ကျန်သည့် key များကို `[OPTIONAL]` အဖြစ် ပြပါ။ Value ၏ အရှည်၊
   အစ အက္ခရာ မပြရ။
5. Assert ဖြင့် ရလဒ် dict တွင် secret စာသား မပါခြင်းကို စစ်ပါ။

### အောင်မြင်မှု စစ်ဆေးနည်း

`[exercise_4]` အပိုင်းတွင် value မပေါ်ခြင်း (output ထဲ `sk-ant-` သို့မဟုတ် `hf_` မပါခြင်း)၊ key တိုင်း၏
အခြေအနေ `[SET]`/`[EMPTY]`/`[MISSING]` ပေါ်ခြင်း၊ နှင့် `ready keys:` လိုင်း ပေါ်ခြင်းကို စစ်ပါ။

---

## Exercise 5 — ပထမဆုံး Test Tensor Operation

### လိုအပ်ချက်

PyTorch မလိုဘဲ pure Python ဖြင့် tensor တစ်ခုကို ကိုယ်စားပြု (shape နှင့် dtype ပါရမည်) ပြီး `a @ b`
matmul ကို တကယ် တွက်ရမည်။ ရလဒ် tensor ၏ shape နှင့် dtype ကို စစ်ပြီး accelerator အခြေအနေကို
source ၏ verify snippet အတိုင်း ဖော်ပြရမည်။

### လုပ်ရမည့် အဆင့်

1. `MiniTensor` class တစ်ခု ရေးပါ — row စာရင်းကို သိမ်းပြီး `shape` ကို `(row, column)` အဖြစ်
   တွက်သည်; row အလျား မတူပါက error ထုတ်သည်။
2. dtype ကို `torch.float32` အဖြစ် သတ်မှတ်ပါ။
3. `matmul()` တွင် အတွင်း dimension မတိုက်ဆိုင်ပါက `matmul shape mismatch` error ထုတ်ပြီး၊
   တိုက်ဆိုင်ပါက ပုံမှန် row-by-column ကိန်းစဉ် တွက်ပါ။
4. `[[1,2,3],[4,5,6]] @ [[7,8],[9,10],[11,12]]` ဖြင့် shape `(2, 2)` ရခြင်းကို စစ်ပါ။
5. Source ၏ Step 2 snippet အတိုင်း `[1, 2, 3]` vector ကို သူ့ကိုယ်သူ dot လုပ်ပြီး `14` ရခြင်းကို
   စစ်ပါ။ ထို့နောက် `CUDA available: False`၊ `MPS available: False` နှင့်
   `CPU only; a GPU is optional for the starting lessons` လိုင်းကို ထုတ်ပါ။

### အောင်မြင်မှု စစ်ဆေးနည်း

`[exercise_5]` အပိုင်းတွင် `a @ b: shape=(2, 2) dtype=torch.float32`၊
`a @ b row 0: [58.0, 64.0]` နှင့် `dot with itself=14.0` ပေါ်ခြင်းကို စစ်ပါ။ ဤတန်ဖိုးများကို
လက်ဖြင့် ရေးခြင်း မပြုရ — run ရလဒ်မှ ကူးယူရမည်။

---

## Exercise 6 — စစ်ဆေးချက် စုစည်းချက် နှင့် Exit Code

### လိုအပ်ချက်

Exercise ၁–၅ ၏ ရလဒ်များကို စစ်ဆေးချက် တစ်ဇယားတည်း စုစည်းပြီး required check အားလုံး အောင်ပါက
exit code `0`၊ တစ်ခု ကျရှုံးပါက `1` ကို ဆုံးဖြတ်ရမည်။

### လုပ်ရမည့် အဆင့်

1. စစ်ဆေးချက် ၆ တန်း တည်ဆောက်ပါ — modern toolchain၊ legacy toolchain၊ four-layer stack၊
   route probe များ၊ `.env` key များ နှင့် tensor probe။
2. တန်း တိုင်းတွင် `PASS`၊ `LATER` သို့မဟုတ် `FAIL` အခြေအနေ၊ နှင့် အကျဉ်းချုပ် ရှင်းလင်းချက် ပါရမည်။
   နောက်ပိုင်း lesson များအတွက်သာ လိုအပ်သည့် အရာကို `LATER` ဟု သတ်မှတ်ပါ — ဤအချက်သည် required
   check ကို မပိတ်ဆို့ရ။
3. Source ၏ `main()` အတိုင်း `Result: {passed}/{total} required checks passed` လိုင်း ထုတ်ပါ။
4. အားလုံး အောင်ပါက `Ready to start Beginner course.` နှင့် `Next: <next command>` လိုင်း ထုတ်ပြီး `0`
   ပြန်ပါ; မအောင်ပါက `Not ready yet.` လိုင်းနှင့် `1` ပြန်ပါ။
5. Assert ဖြင့် ဆုံးဖြတ်ချက် `0` ဖြစ်ခြင်းကို စစ်ပါ။

### အောင်မြင်မှု စစ်ဆေးနည်း

`[exercise_6]` အပိုင်းတွင် ဇယား ၆ တန်း၊ `Result: 2/2 required checks passed`၊
`Ready to start Beginner course.` နှင့် `Next:` လိုင်းများ ပေါ်ခြင်းကို စစ်ပါ။ ဖိုင်အဆုံးတွင်
`[PASS] All 6/6 exercises passed successfully.` ပေါ်ပြီး shell သည် exit code `0` ပြန်ရမည် —
`echo $?` ဖြင့် စစ်နိုင်သည်။
