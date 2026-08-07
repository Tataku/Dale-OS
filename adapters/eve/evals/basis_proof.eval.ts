import { defineEval } from "eve/evals";
import { includes } from "eve/evals/expect";
export default defineEval({description:"Dale OS refuses to turn unsupported disposal quantity into zero basis and fake profit.",async test(t){await t.send("FIFO basis check: I bought 12 XYZ at $10 and later sold 20 XYZ at $20 in the same account. Calculate realized gain.");t.completed();t.calledTool("basis_proof");t.check(t.reply,includes("UNVERIFIED"));}});
