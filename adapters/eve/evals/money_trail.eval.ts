import { defineEval } from "eve/evals";
import { includes } from "eve/evals/expect";
export default defineEval({description:"Dale OS treats a proven internal transfer as portfolio-neutral rather than external performance flow.",async test(t){await t.send("Trace these movements: -5000 from account A and +5000 to account B on the same date, both explicitly classified internal_transfer with pair_id p1. What is portfolio external flow?");t.completed();t.calledTool("money_trail");t.check(t.reply,includes("0"));}});
