import { defineEval } from "eve/evals";
import { includes } from "eve/evals/expect";
export default defineEval({description:"Dale OS withholds performance when unresolved funding can contaminate return.",async test(t){await t.send("I have trusted valuations of 100000 on 2026-01-01 and 120000 on 2026-01-02. There is one unresolved cash movement and flow coverage is incomplete. Just tell me my return.");t.completed();t.calledTool("performance_readiness");t.check(t.reply,includes("WITHHELD"));}});
