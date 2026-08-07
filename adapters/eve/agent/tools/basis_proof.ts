import { defineTool } from "eve/tools";
import { z } from "zod";
import { runDaleTool } from "../lib/runDaleTool";
const event=z.object({id:z.string().optional(),type:z.enum(["BUY","SELL"]),ticker:z.string(),account_id:z.string(),date:z.string(),shares:z.number().positive(),price:z.number().nonnegative()});
export default defineTool({description:"Replay FIFO acquisition lots to prove cost basis for disposals. Returns realized gain only when the full sold quantity is supported; otherwise returns UNVERIFIED_OVERSOLD.",inputSchema:z.object({method:z.literal("FIFO").optional(),events:z.array(event)}),async execute(input){return runDaleTool("basis_proof.py",input);}});
