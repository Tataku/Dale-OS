import { defineEval } from "eve/evals";
import { includes } from "eve/evals/expect";
export default defineEval({description:"Dale OS blocks a probability model whose branches sum above 100 percent.",async test(t){await t.send("Sanity check this scenario model: downside probability 0.6, upside probability 0.6. Downside value 80, base 100, upside 120.");t.completed();t.calledTool("model_sanity");t.check(t.reply,includes("BLOCKED"));}});
