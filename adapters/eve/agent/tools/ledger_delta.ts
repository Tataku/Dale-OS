import { defineTool } from "eve/tools";
import { z } from "zod";
import { runDaleTool } from "../lib/runDaleTool";
const side=z.object({trades:z.array(z.object({id:z.string().optional()}).passthrough()).default([]),positions:z.array(z.object({account_id:z.string(),ticker:z.string(),shares:z.number(),cost_basis:z.number().optional()})).default([]),cash_by_account:z.record(z.string(),z.number()).default({})});
export default defineTool({description:"Compare projected before and after financial states and return explicit trade, position, cost-basis, and cash deltas. Read-only preview helper.",inputSchema:z.object({before:side,after:side}),async execute(input){return runDaleTool("ledger_delta.py",input);}});
