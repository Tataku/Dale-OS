import { defineTool } from "eve/tools";
import { z } from "zod";
import { runDaleTool } from "../lib/runDaleTool";
export default defineTool({description:"Gate financial analytics on the readiness of their required upstream books, allowing clean analytics while withholding only contaminated outputs.",inputSchema:z.object({domains:z.record(z.string(),z.string()),analytics:z.record(z.string(),z.array(z.string()))}),async execute(input){return runDaleTool("close_books.py",input);}});
