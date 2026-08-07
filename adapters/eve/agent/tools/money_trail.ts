import { defineTool } from "eve/tools";
import { z } from "zod";
import { runDaleTool } from "../lib/runDaleTool";
const movement=z.object({id:z.string(),account_id:z.string(),date:z.string(),amount:z.number(),currency:z.string().optional(),classification:z.string().optional(),evidence_grade:z.string().optional(),pair_id:z.string().optional(),source_ref:z.string().optional()});
export default defineTool({description:"Reconcile a set of financial cash movements, validate explicit internal-transfer pairs, and surface unresolved or duplicate movements. Never invents economic classification.",inputSchema:z.object({movements:z.array(movement),tolerance:z.number().nonnegative().optional()}),async execute(input){return runDaleTool("money_trail.py",input);}});
