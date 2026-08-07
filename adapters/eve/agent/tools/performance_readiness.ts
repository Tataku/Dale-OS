import { defineTool } from "eve/tools";
import { z } from "zod";
import { runDaleTool } from "../lib/runDaleTool";
export default defineTool({description:"Check whether trusted valuations and capital-flow evidence are sufficient to publish performance. Read-only; may return WITHHELD instead of a return.",inputSchema:z.object({valuations:z.array(z.object({date:z.string(),value:z.number(),trusted:z.boolean()})),unresolved_movements:z.array(z.string()).default([]),flow_coverage:z.enum(["complete","incomplete","unknown"]),has_external_flows:z.boolean().default(false),requested_method:z.enum(["twr","modified_dietz","simple"]).optional(),max_gap_days:z.number().int().positive().optional()}),async execute(input){return runDaleTool("performance_readiness.py",input);}});
